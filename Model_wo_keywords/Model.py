import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
from umap import UMAP


with open('stopwords-ko/stopwords-ko.txt', 'r') as file:
  stop_words = file.read().splitlines()

print(stop_words)

okt = Okt()

def remove_stopwords_with_pos(text):
    # 형태소 분석 및 품사 태깅
    tokens_with_pos = okt.pos(text)
    # 명사(N), 동사(V), 형용사(J)만 남기고 불용어 제거
    filtered_tokens = [word for word, pos in tokens_with_pos if pos in ['Noun', 'Verb', 'Adjective'] and word not in stop_words]
    return ' '.join(filtered_tokens)

# 좋아요 수 숫자 자료형으로 변환 (ex 1.4K -> 1400)
def convert_likes_to_number(likes):
    if isinstance(likes, str):
        likes = likes.strip().upper()  # 대소문자 무시
        if 'K' in likes:  # 1K = 1,000
            return float(likes.replace('K', '')) * 1_000
        elif 'M' in likes:  # 1M = 1,000,000
            return float(likes.replace('M', '')) * 1_000_000
        else:
            return float(likes)  # 숫자만 있는 경우
    return likes  # 이미 숫자인 경우 그대로 반환


def extract_keywords(df, cluster_column='kmeans_cluster', text_column='cleaned_comment', top_n=10):
    clusters = df[cluster_column].unique()  # 클러스터 번호들 추출
    cluster_keywords = {}

    for cluster in clusters:
        # 해당 클러스터의 모든 댓글을 하나의 문자열로 합치기
        cluster_data = df[df[cluster_column] == cluster]
        all_text = " ".join(cluster_data[text_column].tolist())

        # 형태소 분석 및 명사, 동사, 형용사 추출
        tokens_with_pos = okt.pos(all_text)
        filtered_tokens = [word for word, pos in tokens_with_pos if pos in ['Noun', 'Verb', 'Adjective'] and word not in stop_words]

        # 단어 빈도 계산
        word_counts = Counter(filtered_tokens)
        common_words = word_counts.most_common(top_n)

        # 클러스터별 상위 단어 저장
        cluster_keywords[cluster] = common_words

    return cluster_keywords

def top_comments_with_keywords(df, cluster_column='kmeans_cluster', text_column='comment', cleaned_text_column='cleaned_comment', likes_column='num_likes', top_n=3, keyword_top_n=10):
    # 클러스터 번호 리스트
    clusters = df[cluster_column].unique()
    results = {}
    
    for cluster in clusters:
        # 해당 클러스터의 데이터 필터링
        cluster_data = df[df[cluster_column] == cluster]
        
        # 클러스터별 키워드 추출
        cluster_keywords = extract_keywords(cluster_data, cluster_column=cluster_column, text_column=cleaned_text_column, top_n=keyword_top_n)
        keywords = [word for word, _ in cluster_keywords.get(cluster, [])]
        
        # 키워드 포함 여부 필터링
        cluster_data_with_keywords = cluster_data[cluster_data[text_column].apply(lambda x: any(keyword in x for keyword in keywords))]
        
        # 좋아요 수 기준 상위 댓글 top_n 추출
        if not cluster_data_with_keywords.empty:
            top_comments = cluster_data_with_keywords.nlargest(top_n, likes_column)[[text_column, likes_column]]
        else:
            top_comments = pd.DataFrame(columns=[text_column, likes_column])  # 키워드가 포함된 댓글이 없는 경우 빈 데이터프레임
        
        # 결과 저장
        results[cluster] = {
            "top_comments": top_comments,
            "keywords": keywords
        }
    
    return results

# 크롤링한 엑셀 파일 읽기
df = pd.read_excel('/home2/ihmhyunsir/WorkingSpace/AI_project/crawls/대한민국에 미래가 없는 이유.xlsx')


# '댓글 내용' 열 문자열 자료형 변환 및 NaN 삭제
df['comment'] = df['comment'].astype(str)
df = df[df['comment'].notna()]


# 불용어 처리
df['cleaned_comment'] = df['comment'].apply(remove_stopwords_with_pos)

# '좋아요 수' 열 숫자 자료형으로 변환
df['num_likes'] = df['num_likes'].apply(convert_likes_to_number)

# NaN 값 -> 0 으로 변환
df['num_likes'] = pd.to_numeric(df['num_likes'], errors='coerce').fillna(0)

# 댓글을 Sentence Bert Embedding으로 변환
comments = df['comment'].tolist()


model = SentenceTransformer("jhgan/ko-sroberta-multitask")  # Korean-specific SBERT
embeddings = model.encode(comments)

reducer = UMAP(n_neighbors=10, n_components=20, min_dist = 0.1, metric='cosine', random_state=42)
reduced_embeddings = reducer.fit_transform(embeddings)

num_clusters = 4  # 클러스터 개수 설정
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df['kmeans_cluster'] = kmeans.fit_predict(reduced_embeddings) # KMeans 학습 & 추론


output_file = "Clustering Result.xlsx"  # 저장할 파일명
df.to_excel(output_file, index=False)

print(f"클러스터링 결과가 {output_file} 파일로 저장되었습니다.")

cluster_sizes = df['kmeans_cluster'].value_counts()  # 클러스터 번호별 데이터 수 집계

labels = df['kmeans_cluster'].values
silhouette_avg = silhouette_score(reduced_embeddings, labels)
print(f"Top 5 클러스터 데이터의 평균 실루엣 스코어: {silhouette_avg:.4f}")

'''
# 상위 5개 클러스터 추출
top_5_clusters = cluster_sizes.head(5)




# 상위 5개 클러스터의 번호와 크기 출력
print("Top 5 clusters by size:")
print(top_5_clusters)

# 상위 5개 클러스터에 속한 데이터 추출
top_5_cluster_data = df[df['kmeans_cluster'].isin(top_5_clusters.index)]


top_5_embeddings = embeddings[df['kmeans_cluster'].isin(top_5_clusters.index)]
top_5_labels = top_5_cluster_data['kmeans_cluster'].values

# 실루엣 스코어 계산
silhouette_avg = silhouette_score(top_5_embeddings, top_5_labels)
print(f"Top 5 클러스터 데이터의 평균 실루엣 스코어: {silhouette_avg:.4f}")

# 결과 데이터프레임 출력
top5_output_file = "top5_Clustering Result.xlsx"  # 저장할 파일명
top_5_cluster_data.to_excel(top5_output_file, index=False)

keywords = extract_keywords(top_5_cluster_data)



for cluster, words in keywords.items():
    print(f"\n클러스터 {cluster}의 상위 키워드:")
    for word, count in words:
        print(f"{word}: {count}회")


filtered_top_comments_with_keywords = top_comments_with_keywords(top_5_cluster_data)

for cluster, data in filtered_top_comments_with_keywords.items():
    print(f"\n[클러스터 {cluster}]")
    print("상위 키워드:")
    for word in data["keywords"]:
        print(f"- {word}")
    
    print("상위 댓글:")
    for idx, row in data["top_comments"].iterrows():
        print(f"- {row['comment']} (좋아요: {int(row['num_likes'])})")
'''
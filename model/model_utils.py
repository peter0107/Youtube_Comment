import pandas as pd

def read_excel(filename):
    df = pd.read_excel(f'./{filename}')
    df['comment'] = df['comment'].astype(str)
    df = df[df['comment'].notna()]
    df['num_likes'] = df['num_likes'].apply(convert_likes_to_number)
    df['num_likes'] = pd.to_numeric(df['num_likes'], errors='coerce').fillna(0)
    return df

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

def extract_nouns(comment, tokenizer, stopwords):
    nouns = tokenizer.nouns(comment)
    filtered_nouns = [noun for noun in nouns if noun not in stopwords]
    return " ".join(filtered_nouns)

def weighted_sample(cluster_df, n_samples):
    if len(cluster_df) <= n_samples: # 샘플링 할 개수보다 클러스터에 속하는 샘플 수가 적으면 클러스터에 속하는 모든 샘플 반환
        return cluster_df
    try:
      weights = cluster_df['num_likes'] / cluster_df['num_likes'].sum()
      sampled = cluster_df.sample(n=n_samples, weights=weights, random_state=42)
    except ValueError as e:
      sampled = cluster_df.sample(n=n_samples, random_state=42)
    return sampled
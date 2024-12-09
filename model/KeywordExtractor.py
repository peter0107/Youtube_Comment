from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

class KeywordExtractor:
    def __init__(self, df, word_embeddings_dict):
        self.df = df
        self.word_embeddings_dict = word_embeddings_dict
        self.sorted_keywords = None

    def extract_keywords(self, doc_embedding, words, word_embeddings_dict, top_n=5):
        if len(words) == 0:
            return []
        word_embedding = [word_embeddings_dict[word] for word in words]

        # Cosine-based keyword extraction
        distances = cosine_similarity([doc_embedding], word_embedding)
        keywords = [
            # (words[index], round(float(distances[0][index]), 4))
            words[index]
            for index in distances.argsort()[0][-top_n:]
        ][::-1]

        return keywords

    def get_keyword_groups(self):
        doc_embeddings = self.df['embeddings'].to_list()
        tokenized_sentences = self.df['words'].to_list()
        keywords_per_comment = [
            self.extract_keywords(doc_embedding, words, self.word_embeddings_dict, top_n=2) 
            for doc_embedding, words in zip(doc_embeddings, tokenized_sentences)
        ]

        keyword_to_comments = defaultdict(list)
        for comment_idx, keywords in enumerate(keywords_per_comment):
            for keyword in keywords:
                keyword_to_comments[keyword].append(comment_idx)

        self.sorted_keywords = sorted(
            keyword_to_comments.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        return self.sorted_keywords

    def extract_keyword_groups(self):
        # 키워드 합치기 & 중복 제거
        indices = {keyword: set(index_list) for keyword, index_list in self.sorted_keywords}
        # 댓글 수 Threshold
        overlap_threshold = 30
        # 동일한 댓글을 (Threshold)개 이상으로 포함하는 키워드는 서로 합치기
        groups = defaultdict(set)  # 각 키워드 그룹에 속할 댓글을 저장할 딕셔너리
        visited = set()  # 이미 합쳐진 키워드 트래킹
        for keyword1, indices1 in indices.items():
            # 키워드가 합쳐지지 않았다면 새로 그룹을 생성
            if keyword1 in visited:
                continue
            groups[keyword1].update(indices1)

            # 겹치는 댓글이 (Threshold)개 이상인지 확인하고 맞다면 키워드 합치기
            for keyword2, indices2 in indices.items():
                if keyword1 != keyword2:
                    overlap_count = len(indices1 & indices2)
                    if overlap_count >= overlap_threshold:
                        groups[keyword1].update(indices2)
                        visited.add(keyword2)
        # 그룹 형식 변환 ({'트럼프':{1,2,3},'바이든':{4,5,6}} => {'트럼프':(1,2,3),'바이든':(4,5,6)})
        final_groups = {}
        for keyword, group_indices in groups.items():
            group_indices = sorted(group_indices)  # Sort indices for consistency
            if tuple(group_indices) not in final_groups.values():
                final_groups[keyword] = tuple(group_indices)
        # 그룹 간 중복되는 댓글 제거
        assigned_indices = set()  # 이미 최종 그룹에 할당된 댓글 트래킹
        cleaned_groups = {} # 최종 그룹
        # 그룹 별 댓글 수를 기준으로 정렬
        sorted_groups = sorted(final_groups.items(), key=lambda x: len(x[1]), reverse=True)
        # 같은 댓글이 여러 개의 그룹에 중복되어 속해있는 경우, 가장 많은 댓글을 가진 그룹에 속한 댓글만 남겨두고 나머지는 제거
        for keyword, group_indices in sorted_groups:
            unique_indices = tuple(idx for idx in group_indices if idx not in assigned_indices)
            if unique_indices:  # Only keep groups with remaining indices
                cleaned_groups[keyword] = unique_indices
                assigned_indices.update(unique_indices)
        # 전체 그룹 중에서 댓글 수 기준으로 Top 5에 해당하는 그룹을 추출 (스팸 댓글들도 삭제되는 효과)
        top_cleaned_groups = sorted(cleaned_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]

        indices = set()
        for group, group_indices in top_cleaned_groups:
            indices.update(group_indices)

        final_keywords = [group[0] for group in top_cleaned_groups]
        filtered_df = self.df.loc[list(indices)].reset_index(drop=True)
        
        return filtered_df, final_keywords
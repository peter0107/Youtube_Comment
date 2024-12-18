import openai
import pandas as pd
from model_utils import weighted_sample


class GPTSummarizer:
    def __init__(self, df, isClustered=True):
        self.isClustered = isClustered
        self.df = df
        if not self.isClustered:
            self.df['cluster'] = [0]*len(df)
        
    def do_sample(self):
        sampled_comments = []
        n_samples_per_cluster = 10 if self.isClustered else 10*4  # 샘플링 할 개수
        
        for cluster in self.df['cluster'].unique():
            cluster_df = self.df[self.df['cluster'] == cluster]
            sampled_comments.append(weighted_sample(cluster_df, n_samples_per_cluster))
            
        self.sampled_comments_df = pd.concat(sampled_comments)
        return self.sampled_comments_df
    
    def get_summary(self):
        clustered_dict = self.sampled_comments_df.groupby('cluster')['comment'].apply(list).to_dict()
        formatted_string = str(clustered_dict)

        # ChatGPT에게 댓글을 보고 전반적인 경향성 요약 요청
        openai.api_key = "" #API KEY

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 유튜브 댓글에서 클러스터링을 통해 대표적으로 선별된 몇가지 댓글들을 보고 댓글들의 전체적인 경향성을 요약해서 나타내는 모델입니다."},
                {"role": "user", "content": "다음은 각 클러스터에 속하는 댓글을 가지고온 것입니다. 이것들에 기반해서 전체적인 댓글의 경향성을 요약해주세요."+
                "각 클러스터에 대해서 설명하는 것이 아닌, 문장이 자연스럽게 이어지도록 서술해주세요."
                "존댓말로 서술해주세요."+
                formatted_string}
            ]
        )

        summary = response.choices[0].message.content
        return summary
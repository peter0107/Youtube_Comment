from sklearn.mixture import GaussianMixture
from umap import UMAP

class YoutubeClusterModel:
    def __init__(self, df):
        self.df = df
        self.reduced_embeddings = None
        
    def reduce_emb_dim(self):
        embeddings = self.df['embeddings'].tolist()

        reducer = UMAP(n_neighbors=10, n_components=20, min_dist = 0.1, metric='cosine', random_state=42)
        self.reduced_embeddings = reducer.fit_transform(embeddings)

    def get_clusters(self):
        num_clusters = 4 # 클러스터 개수 설정
        gmm = GaussianMixture(n_components=num_clusters, random_state=42)
        self.df['cluster'] = gmm.fit_predict(self.reduced_embeddings)  # GMM 학습 & 추론
        
        return self.df

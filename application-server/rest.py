from model.CommentEmbedder import CommentEmbedder
from model.KeywordExtractor import KeywordExtractor
from model.YoutubeClusterModel import YoutubeClusterModel
from model.GPTSummarizer import GPTSummarizer

from sentence_transformers import SentenceTransformer
from konlpy.tag import Mecab

model = SentenceTransformer("jhgan/ko-sroberta-multitask")
mecab = Mecab()
stopwords = ['은', '는', '이', '가', '을', '를', '에', '의', '로', '와', '과', '하다', '있다', '없다']


def getSummary(video_id):
    
    embedder = CommentEmbedder(model, mecab, stopwords)
    embedder.get_comments(video_id)
    embedder.eliminate_stopwords()
    raw_df, word_embeddings_dict = embedder.get_embbedings()
    
    extractor = KeywordExtractor(raw_df, word_embeddings_dict)
    extractor.get_keyword_groups()
    filtered_df, final_keywords = extractor.extract_keyword_groups()

    ytModel = YoutubeClusterModel(filtered_df)
    ytModel.reduce_emb_dim()
    filtered_clustered_df = ytModel.get_clusters()

    summarizer = GPTSummarizer(filtered_clustered_df, isClustered=True)
    summarizer.do_sample()
    final_summary = summarizer.get_summary()
    
    return final_keywords, final_summary
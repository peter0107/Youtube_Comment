from sklearn.feature_extraction.text import CountVectorizer

from model_utils import read_excel, extract_nouns
from crawler.getter import get_comments_by_video_ids

class CommentEmbedder:
    def __init__(self, model, mecab, stopwords):
        self.df = None
        self.mecab = mecab
        self.model = model
        self.stopwords = stopwords
    
    def get_comments(self, video_id):
        filename = get_comments_by_video_ids(video_id)
        self.df = read_excel(filename)

    def eliminate_stopwords(self):
        comments = self.df['comment'].to_list()
        self.df = self.df.rename(columns={'comment': 'raw_comment'})
        self.df['comment'] = [extract_nouns(comment, self.mecab, self.stopwords) for comment in comments]

    def get_embbedings(self):
        # 댓글별 임베딩
        comments = self.df['comment'].to_list()
        self.df['embeddings'] = self.model.encode(comments, batch_size=32).tolist()

        # 단어별 임베딩
        tokenized_comments = []
        unique_words = set()
        for comment in comments:
            try:
                words = CountVectorizer(ngram_range=(1, 1)).fit([comment]).get_feature_names_out()
            except ValueError:
                words = []
            tokenized_comments.append(words)
            unique_words.update(words)
        self.df['words'] = tokenized_comments
        
        unique_word_list = list(unique_words)
        word_embeddings = self.model.encode(unique_word_list, batch_size=32)
        word_embeddings_dict = dict(zip(unique_word_list, word_embeddings))
        
        return self.df, word_embeddings_dict

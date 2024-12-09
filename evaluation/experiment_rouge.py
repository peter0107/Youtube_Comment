from korouge_score import rouge_scorer
from konlpy.tag import Mecab
import pandas as pd
import matplotlib.pyplot as plt

scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL", "rougeLsum"])

df = pd.read_excel("summary.xlsx")

def preprocess_korean(text):
    mecab = Mecab()
    tokens = mecab.morphs(text) 
    return ' '.join(tokens) 

metrics = ['rouge1', 'rouge2', 'rougeL']
exp_columns = ["exp1", "exp2", "exp3", "exp4"]
label_column = "label"
def calculate_rouge_per_exp(df, exp_columns, label_column):
    scorer = rouge_scorer.RougeScorer(metrics, use_stemmer=False)
    results = {metric: [] for metric in metrics}
   
    for i, row in df.iterrows():
        for metric in metrics:
            results[metric].append([])
        for exp in exp_columns:
            exp_text = preprocess_korean(row[exp])
            label_text = preprocess_korean(row[label_column])
            score = scorer.score(exp_text, label_text)
            for metric, score in score.items():
                results[metric][i].append(round(score.fmeasure, 2))
                
    return results

rouge_scores = calculate_rouge_per_exp(df, exp_columns, label_column)

x_labels = ['과학', '사회', '엔터테인먼트']

def plot_rouge_scores(data, title):
    plt.figure(figsize=(8, 6))
    for i in range(4):  # 각 열에 대해 꺾은선 추가
        scores = [row[i] for row in data]
        plt.plot(x_labels, scores, marker='o', label=f'Line {i + 1}')

    plt.title(title)
    plt.xlabel('Video Category')
    plt.ylabel('Score')
    plt.ylim(0, 1)  # 스코어 범위
    plt.legend()
    plt.grid(True)
    plt.show()

# 그래프 그리기
plot_rouge_scores(rouge_scores['rouge1'], 'ROUGE-1 Scores')
plot_rouge_scores(rouge_scores['rouge2'], 'ROUGE-2 Scores')
plot_rouge_scores(rouge_scores['rougeL'], 'ROUGE-L Scores')

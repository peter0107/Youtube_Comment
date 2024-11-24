import pandas as pd
import re
from config import output_dir


def read_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def clean_illegal_characters(val):
    """
    셀 데이터에서 Excel에서 허용되지 않는 문자를 제거합니다.
    """
    invalid_chars = r'[\x00-\x1F]'
    return re.sub(invalid_chars, "", str(val))


def clean_filename(val):
    """
    window 파일이름에서 허용되지 않는 문자를 제거합니다. 
    """
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, "", val)

def save_comments_to_csv(title, comments):
    """
    댓글들을 csv에 저장합니다.
    """
    df = pd.DataFrame(comments, columns=['author', 'comment', 'num_likes'])
    filename = f"{output_dir}/{clean_filename(title)}.xlsx"
    df = df.map(clean_illegal_characters)
    df.to_excel(filename)

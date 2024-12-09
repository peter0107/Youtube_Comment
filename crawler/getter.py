from youtube_api import *
from utils import *


def get_comments_by_video_ids(video_id):
    try:
        title =    get_video_name(video_id)
        comments = get_video_comments(video_id)
        return save_comments_to_csv(title, comments)
        
    except Exception as e:
        print(e)
        return False
    
print(get_comments_by_video_ids("4E1BHTvhB7Y"))

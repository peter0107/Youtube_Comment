from youtube_api import *
from utils import *


filename = 'video_ids.txt'

def get_comments_by_video_ids(video_ids):
    for video_id in video_ids:
        print(f"  Fetching comments for video ID: {video_id}")
        try:
            title =    get_video_name(video_id)
            comments = get_video_comments(video_id)
            save_comments_to_csv(title, comments)
        except Exception as e:
            print(f"    Fetching failed for following reason: {e}")

if __name__ == "__main__":
    video_ids = read_from_file(filename)
    get_comments_by_video_ids(video_ids)
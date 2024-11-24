from youtube_api import *
from utils import *
from getter_by_video_ids import get_comments_by_video_ids


filename = 'channel_ids.txt'

def get_comments_by_handles(handles):
    for handle in handles:
        print(f"Processing channel: {handle}")
        try:
            channel_id = get_channel_id(handle)
            playlist_id = get_playlist_id(channel_id)
            video_ids = get_video_ids(playlist_id)
        except Exception as e:
            print(f"  Processing failed for following reason: {e}")    
        
        get_comments_by_video_ids(video_ids)

if __name__ == "__main__":
    handles = read_from_file(filename)
    get_comments_by_handles(handles)
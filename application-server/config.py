from googleapiclient.discovery import build


API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)

MAX_PLAYLIST_PER_CHANNEL = 1
MAX_VIDEO_PER_PLAYLIST = 100
MAX_COMMENT_PER_VIDEO = 1000

output_dir = "result"
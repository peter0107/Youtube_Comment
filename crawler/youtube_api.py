from config import youtube
from config import MAX_PLAYLIST_PER_CHANNEL, MAX_VIDEO_PER_PLAYLIST, MAX_COMMENT_PER_VIDEO

def get_channel_id(handle):
    """
    핸들(@handle)로 채널 ID를 가져옵니다.
    """
    request = youtube.search().list(
        part="snippet",
        q=handle,
        type="channel",
        maxResults=1
    )
    response = request.execute()
    
    if response.get('items'):
        return response['items'][0]['id']['channelId']
    else:
        raise Exception(f"No channel found for handle: {handle}")  

def get_playlist_id(channel_id):
    """
    채널 ID로 업로드 재생목록 ID를 가져옵니다.
    """
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id,
        maxResults=MAX_PLAYLIST_PER_CHANNEL
    )
    response = request.execute()

    if response.get('items'):
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        raise Exception(f"Could not find uploads playlist for channel: {channel_id}")  
    
    
def get_video_ids(playlist_id):
    """
    재생목록 ID로 동영상 ID들을 가져옵니다.
    """
    video_ids = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=MAX_VIDEO_PER_PLAYLIST
    )

    while request:
        response = request.execute()
        for item in response.get('items', []):
            video_ids.append(item['contentDetails']['videoId'])

        request = youtube.playlistItems().list_next(request, response)
    
    return video_ids

def get_video_name(video_id):
    """
    동영상 ID로 동영상 이름을 가져옵니다.
    """
    title = None
    response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()
    title = response['items'][0]['snippet']['title']

    if title:
        return title
    else:
        raise Exception(f"Could not find a title for video: {video_id}")

def get_video_comments(video_id):
    comments = []
    response = api_obj.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        maxResults=1000
    ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'], 
                comment['textDisplay'], 
                comment['likeCount']
            ])
            
            if item['snippet']['totalReplyCount'] > 0 and 'replies' in item:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([
                        reply['authorDisplayName'], 
                        reply['textDisplay'], 
                        reply['likeCount']
                    ])

        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=1000
            ).execute()
        else:
            break

    return comments

def get_video_comments(video_id):
    """
    동영상 ID로 댓글들을 가져옵니다.
    """
    comments = []
    request = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        maxResults=MAX_COMMENT_PER_VIDEO
    )

    while request:
        response = request.execute()
        for item in response.get('items', []):
            top_comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'author': top_comment.get('authorDisplayName', ''),
                'comment': top_comment.get('textDisplay', ''),
                'num_likes': top_comment.get('likeCount', '')
            })
            if item['snippet']['totalReplyCount'] > 0 and 'replies' in item:
                for reply_item in item['replies']['comments']:
                    reply_comment = reply_item['snippet']
                    comments.append({
                        'author': reply_comment.get('authorDisplayName', ''),
                        'comment': reply_comment.get('textDisplay', ''),
                        'num_likes': reply_comment.get('likeCount', '')
                    })
        request = youtube.commentThreads().list_next(request, response)

    return comments

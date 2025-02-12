from googleapiclient.discovery import build

# Configura tu clave API de YouTube
xtts-project
api_key = 'Tu api key'
youtube = build('youtube', 'v3', developerKey=api_key)

# Obtén el ID del video en vivo
live_video_id = 'ID_DEL_VIDEO_EN_VIVO'

# Obtén el ID del chat en vivo
response = youtube.videos().list(
    part='liveStreamingDetails',
    id=live_video_id
).execute()

chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']

# Obtén los comentarios en vivo
response = youtube.liveChatMessages().list(
    liveChatId=chat_id,
    part='snippet'
).execute()

# Imprime los comentarios
for item in response['items']:
    comment = item['snippet']['displayMessage']
    print(comment)

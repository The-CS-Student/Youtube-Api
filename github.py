import youtube_dl
from apiclient.discovery import build
a = input("Playlist or Single [P/S] : ")
if(a=="P"):
    print("Playlist Mode Selected ")
    b = input("Enter Playlist Id : ")
else:
    print("Single Mode Selected ")
    b = input("Enter URL : ")






DEVELOPER_KEY = "yourkeyfromyoutubedatav3api"
def fetch_videos(playlistid, devkey):
    youtube = build('youtube', 'v3', developerKey = devkey)
    videos = []
    nextpagetoken = None
    a = 0
    print("Fetching videos")
    while 1:
        
        res = youtube.playlistItems().list(playlistId = playlistid, part = 'snippet', maxResults = 50, pageToken = nextpagetoken).execute()
        videos += res['items']
        nextpagetoken = res.get('nextPageToken')
        if nextpagetoken is None:
            break
    return videos


def main(a, b,devkey):
    if(a == "S"):
        
        print("Starting Download")
        ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320',}],}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([b])
    elif(a == "P"):
        videos = fetch_videos(b, devkey)
        mode = input("Download All or Choose to Download [A/C] : ")
        if(mode == "A"):
            a = 0
            for video in videos:
                a += 1
                ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320',}],}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading "+str(video['snippet']['title']) + ". Song "+str(a) + "/" + str(len(videos)))
                    ydl.download([("https://www.youtube.com/watch?v=" + str(video['snippet']['resourceId']['videoId']))])
        else:
            a = 0
            array = []
            idarr = []
            for video in videos:
                ydl_opts = {'format': 'bestaudio/best','postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320',}],}
                print(str(video['snippet']['title']) + str(" : "), end = '')
                choice = input("Enter [Y/N] : ")
                if(choice == "Y"):
                    array.append("https://www.youtube.com/watch?v=" + str(video['snippet']['resourceId']['videoId']))
                    idarr.append(str(video['snippet']['title']))
                elif(choice=="Exit"):
                    break
            for i in range(len(array)):
                a += 1
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading mp3 "+str(idarr[i]) + ". Song "+str(a) + "/" + str(len(array)))
                    ydl.download([array[i]])
main(a,b,DEVELOPER_KEY)
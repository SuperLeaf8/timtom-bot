import youtube_dl
import shutil
import os
name = input("name: ")
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': '{0}.%(ext)s'.format(name),
    'noplaylist':True,
    'ignoreerrors':True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
}



'https://www.youtube.com/watch?v=gz-N0_qTgiw'
link = input("link: ")
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])

shutil.move(f"{name}.mp3",f"kk_music\\{name}.mp3")
#!/usr/bin/python3 
from filelock import FileLock,Timeout
import cgi
import youtube_dl
import os


def download(url,extract_audio,extention):
    ydl_opts = {
            #'simulate': True,
            'quiet': True,
            'no_warnings': True, 
            'logtostderr': True,
            'no_color': True,
            'outtmpl': './downloads/%(title)s.%(ext)s',
            }
    if extract_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': extention,
        }]
    elif extention != "best":
        #https://github.com/ytdl-org/youtube-dl/issues/20095
        #ydl_opts['merge_output_format'] = extention
        #The following breaks sometimes too based on video
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': extention,
        }]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url)
        filename = ydl.prepare_filename(result)
        filename  = '.'.join(filename.split('.')[:-1]) + "." + extention

        #if not os.path.exists(filename):
        ydl.download([url])

    return filename

#import cgitb
#cgitb.enable()

if __name__ == '__main__':
    print('Content-Type: text/html;charset=utf-8')
    print()

    try:
        with FileLock('.lock', timeout=0) as lock:
            form = cgi.FieldStorage()
            url = form['url'].value
            extract_audio = form['type'].value == "audio"
            extention = form['format'].value
            try:
                filename = download(url,extract_audio,extention)
                print("Download: <a href='" + filename + "'>" + filename.split("/")[-1] + "</a>")
            except Exception as e:
                print('Download failed!')
            
    except Timeout:
        print('Server is currently busy. Please try again later.')

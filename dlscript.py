#!/usr/bin/python3 
import cgi
import youtube_dl
import os
import sys
import glob
import json
import subprocess

def print_headers(content_type = 'text/html'):
    print(f'Content-Type: {content_type};charset=utf-8\n\n', flush=True)

def to_stderr(self, message):
    raise Exception(message)

def download(url,extention,extract_audio,extract_subtitle):
    if os.path.exists('ydl.json'):
        print('Server is current working on another file. Try again later')
        return

    ydl_opts = {
            #'simulate': True,
            'quiet': True,
            'no_warnings': True, 
            #'logtostderr': True,
            'ignoreerrors': True,
            'no_color': True,
            'outtmpl': './downloads/%(title)s.%(ext)s',
            }
    if extract_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': extention,
        }]
    else:
        if extract_subtitle:
            ydl_opts['writesubtitles'] = True
        if extention != "best":
            #https://github.com/ytdl-org/youtube-dl/issues/20095
            #ydl_opts['merge_output_format'] = extention
            #The following breaks sometimes too based on video
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': extention,
            }]

    #Override this so it properly raises an exception instead of going to stderr
    youtube_dl.YoutubeDL.to_stderr = to_stderr 

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url,download=False)
        filename = ydl.prepare_filename(result)
        if extention != "best":
            filename  = '.'.join(filename.split('.')[:-1]) + "." + extention
    
    #already downloaded
    #Removing this as filename prediction from best is unreliable
    #subtitle option also ocassionally includes additional subtitile file.
    #if os.path.exists(filename):
    #    print(filename)
    #    with open('status', 'w') as fp:
    #        fp.write('{"status": "Completed", "url":"'+filename+'"}')
    #    return

    with open('ydl.json', 'w') as fp:
        ydl_opts['url'] = url
        json.dump(ydl_opts, fp)

    with open('status', 'w') as fp:
        fp.write('{"status": "starting"}')

    print('working on "' + ".".join(filename.split(".")[:-1])[12:] + '"')
    pid = subprocess.Popen([sys.executable, "startdl"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

#import cgitb
#cgitb.enable()

if __name__ == '__main__':

    form = cgi.FieldStorage()
    url = form['url'].value
    extract_audio = form['type'].value == "audio"
    extention = form['format'].value
    extract_subtitle = 'subtitle' in form

    #url = "https://www.youtube.com/watch?v=oHg5SJYRHA0"
    #extract_audio=False
    #extention = "mkv"
    print_headers()
    try:
        download(url,extention,extract_audio,extract_subtitle)
    except Exception as e:
        print(e)

        with open('status', 'w') as fp:
            fp.write('{"status": "Failed"}')

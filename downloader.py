import pytube
from pytube import YouTube
from pytube import Playlist
import concurrent.futures
import requests
import os, re, sys


def playlist(link):
    def single_video(link):
        vid = Video(link)
        vid.download()
    playlist = Playlist(link)
    try: # try to work with the multi-threading approach
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(single_video, playlist)
    except Exception as e: # if it doesn't work though...
        print(f"Error with threading, will download normally: {e}")
        for link in playlist:   single_video(link)

class Video:
    def __init__(self, link, mp3, verbose):
        source_code = requests.get(link).content.decode("utf-8") # gets source code and converts it from binary to string
        pattern = re.compile(r'(\\",\\"title\\":\\")(.*)(\\",\\"lengthSeconds\\":\\")') # we don't talk about this line
        matches = pattern.findall(source_code)
        name = matches[0][1] # there is one result, hence the [0], and a tuple of 3, we want the second, so [1]
        self.link = link # sets the video's link for further use
        self.title = name # video's name
        self.mp3 = mp3
        self.verbose = verbose

    def progress(stream, chunk, file_handler, bytes_remaining):
        print(f"bytes remaining: {bytes_remaining}")


    def download(self):
        print(f"Downloading {self.title}")
        try: # try to download the video with the highest possible quality
            yt = YouTube(self.link)
            if self.verbose:    yt.register_on_progress_callback(self.progress)
            yt.streams.filter(only_audio=self.mp3)[0].download(output_path=os.getcwd())                
            return 1
        
        except Exception as e: # aaaaaaand if it doesn't work, display the error and the video with the problem
            print(f"Something went wrong with {self.title}: {e}")    
            return 0


def main(link, mp3=True, verbose=False):
    if "&list" in link:
        playlist(link)
    else:
        vid = Video(link, mp3, verbose)
        print("download complete") if vid.download() else print("Something went wrong")


main(sys.argv[1], sys.argv[2], sys.argv[3])

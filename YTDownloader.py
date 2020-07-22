import os, dropbox, requests, ffmpeg, shutil
from pytube import YouTube
from pytube.cli import on_progress
# This code isn't yet commented. I'll go through and do that some other time.

digest = lambda URLs: [''.join(i.split()) for i in URLs if i != '']

def fetchFileData(path):
        with open(path, 'r') as File:
            return File.read().split('\n')

class LocalInterface():
    #Default parent class works on local txt files
    #prev_something contains urls that have already been downloaded already by the system
    #fetch_something contains urls that are about to be downloaded
    def __init__(self, fetch_path, prev_path):
        self.fetch_path = fetch_path
        self.prev_path = prev_path
        self.fetch_data = fetchFileData(self.fetch_path)
        self.prev_data = fetchFileData(self.prev_path)

    def fetchNewFileData(self):
        new_contents = digest(fetchFileData(self.fetch_path))
        old_contents = digest(fetchFileData(self.prev_path))
        for x in old_contents: new_contents.remove(x)
        print(new_contents)
        return new_contents


class DropboxInterface(LocalInterface):
    def __init__(self, fetch_path, prev_path, DBX_ACCESS_TOKEN):
        super().__init__(fetch_path, prev_path)
        self.dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)
        self.DBX_ACCESS_TOKEN = DBX_ACCESS_TOKEN
        self.fetch_path = fetch_path
        self.prev_path = prev_path
        self.fetch_data = self.fetchDBFileData(self.fetch_path)
        self.prev_data = fetchFileData(prev_path)

    def downloadFile(self, path):
        # This is copied straight from the dropbox sdk docs.
        # If it aint broken, don't fix it!!
        try:
            md, res = self.dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
        data = res.content
        print(len(data), 'bytes; md:', md)
        return data

    def fetchDBFileData(self, fetch_path):
        if fetch_path[0] != "/":
            fetch_path = "/" + fetch_path


        print(fetch_path)
        return self.downloadFile(fetch_path).decode('utf-8').split('\n')

    def fetchNewFileData(self):
        print('Searching for link...')
        if self.fetch_path[0] != '/':
            self.fetch_path = '/'+self.fetch_path
        #try:
        _=self.dbx.files_search('', self.fetch_path, max_results=1)


        print('Like found! Checking against stored URLs..')
        URLs =  self.downloadFile(self.fetch_path).decode('utf-8').split('\n')
        #Remove spaces
        URLs = digest(URLs)

        with open(self.prev_path, 'r+') as File:
            contents = digest(File.read().split('\n'))

        #Get rid of previously downloaded videos
        for x in contents:
            try: URLs.remove(x)
            except: pass
        print(URLs)
        return URLs


def downloadVideoBEST(url, path='./'):
    print(f'DOWNLOADING VIDEO {url}...')
    print(f'CHECKING VIDEO WITH URL: {url}...')
    yt = YouTube(url)

    # Prepare temp-dir
    os.system(f'mkdir {path}/tmp')

    # Replace illegal characters in Windows
    title = yt.title
    illegalchar = '":\\\*<>?|/'
    translation_table = dict.fromkeys(map(ord, illegalchar), None)
    title = title.translate(translation_table)
    print(f'REPLACED ILLEGAL CHARACTERS IN VIDEO TITLE')

    # Download at max resolution whether adaptive or progressive
    # Video comes without sound. Need to download both
    print(f'DOWNLOADING VIDEO...')
    yv = yt.streams.filter(file_extension='mp4').order_by('resolution').last()
    yv.download(f'{path}tmp', filename='video')

    # Then download sound
    print(f'DOWNLOADING AUDIO...')
    ya = yt.streams.get_audio_only()
    ya.download(f'{path}tmp', filename='audio')

    # Splice video and sound together using FFMPEG
    # !! BEWARE !! UTILIZES CPU 100%
    va = ffmpeg.input(f'{path}tmp/audio.mp4')
    vv = ffmpeg.input(f'{path}tmp/video.mp4')
    ffmpeg.concat(vv, va, v=1, a=1).output(f'{path}{title}.mp4').run()

    # Cleanup temp-files
    shutil.rmtree(f'{path}tmp')



def downloadVideoSTABLE(url, path):
    print(f'DOWNLOADING VIDEO {url}...')
    yt = YouTube(url)
    title = yt.title
    print(f'TITLE: {title}')
    ys = yt.streams.get_highest_resolution()
    ys.download(path)

def wait_for_internet_connection(url='http://www.example.com', timeout=3):
    print('Waiting for an internet connection...')
    while True:
        try:
            requests.head(url, timeout=timeout)
            print('Connection OK')
            return
        except requests.ConnectionError:
            print('No internet, trying again')
            pass

def fetchConfig(config_file_path="config.txt"):
    File = open(config_file_path, 'r')
    contents = digest([i for i in File.read().split('\n') if "#" not in i])
    contents = [i[i.index("\"")+1:-1] for i in contents]
    print(contents)
    return contents[0], contents[1], contents[2], contents[3], contents[4], contents[5]

def main(newURLs, DOWNLOAD_PATH, res):
    if newURLs == None:
        print('No new URLs')
        return
    if len(newURLs) == 0:
        print('No new URLs')
        return
    else:
        print(f"LIST OF NEW URLS: {', '.join(newURLs)}")
        for i in newURLs:
            if res == "STABLE":
                downloadVideoSTABLE(i, DOWNLOAD_PATH)
            else:
                downloadVideoBEST(i, DOWNLOAD_PATH)
            #Add the now downloaded URLs to the previousURLs.txt file
            with open(PREV_TXT_PATH, 'a+') as File:
                File.write(i+'\n')

def DropboxMain(FETCH_FILE_NAME, DBX_ACCESS_TOKEN, PREV_TXT_PATH, DOWNLOAD_PATH, RES):
    Dropbox = DropboxInterface(FETCH_FILE_NAME, PREV_TXT_PATH, DBX_ACCESS_TOKEN)
    main(Dropbox.fetchNewFileData(), DOWNLOAD_PATH, RES)

def LocalMain(FETCH_FILE_NAME, PREV_TXT_PATH, DOWNLOAD_PATH, RES):
    Local = LocalInterface(FETCH_FILE_NAME, PREV_TXT_PATH)
    main(Local.fetchNewFileData(), DOWNLOAD_PATH, RES)




if __name__ == '__main__':
    wait_for_internet_connection()
    STORE_SERVICE, FETCH_FILE_NAME, DBX_ACCESS_TOKEN, PREV_TXT_PATH, DOWNLOAD_PATH, RES = fetchConfig()
    if STORE_SERVICE.lower() == "dropbox":
        DropboxMain(FETCH_FILE_NAME, DBX_ACCESS_TOKEN, PREV_TXT_PATH, DOWNLOAD_PATH, RES)
    if STORE_SERVICE.lower() == "local":
        LocalMain(FETCH_FILE_NAME, PREV_TXT_PATH, DOWNLOAD_PATH, RES)

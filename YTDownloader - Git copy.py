import os, dropbox, requests
from pytube import YouTube


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

def downloadVideo(url, path=None):
    print(f'DOWNLOADING VIDEO {url}...')
    yt = YouTube(url)
    title = yt.title
    ys = yt.streams.get_highest_resolution()
    ys.download(path)

def downloadFile(dbx, folder, name):
    # This is copied straight from the dropbox sdk docs.
    # If it aint broken, don't fix it!!    
    path = '/%s/%s' % (folder, name)
    while '//' in path:
        path = path.replace('//', '/')

    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def main():
    digest = lambda URLs: [''.join(i.split()) for i in URLs if i != '']
    # If you haven't set up your dropbox to only allow the app to read files in a single directory, 
    # you'll have to change this variable to the path of the txt stored in dropbox
    folderPath = ""
    fileName = "/NewLikedVideo.txt"
    DBX_ACCESS_TOKEN = "CHANGE ME"
    PREV_TXT_PATH = "/home/pi/Desktop/previousURLs.txt"
    DOWNLOAD_PATH = None


    print('Connecting to Dropbox...')  # Instantiate dropbox object
    dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)

    print('Searching for link...')
    searchResult = dbx.files_search(folderPath, fileName, max_results=1)

    print('Like found! Checking against stored URLs..')
    URLs =  downloadFile(dbx=dbx, folder=folderPath, name=fileName).decode('utf-8').split('\n')
    #Remove spaces
    URLs = digest(URLs)

    with open(PREV_TXT_PATH, 'r+') as File:
        contents = digest(File.read().split('\n'))

    #Get rid of previously downloaded videos
    for x in contents: URLs.remove(x)
    
    if len(URLs) == 0:
        print('No new URLs')
        return
    
    else:
        print(f"LIST OF NEW URLS: {', '.join(URLs)}")
        for i in URLs: 
            downloadVideo(i, DOWNLOAD_PATH)
            #Add the now downloaded URLs to the previousURLs.txt file
            with open(PREV_TXT_PATH, 'a+') as File:
                File.write(i+'\n')
        
        



        # validURLs = URLChecker()
        # downloadVideo(url)


if __name__ == '__main__':
    wait_for_internet_connection()
    main()
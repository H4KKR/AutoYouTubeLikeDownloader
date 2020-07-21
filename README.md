# AutoYouTubeLikeDownloader
Uses IFTTT, Dropbox and a Raspberry Pi to automatically download and store *new* YouTube videos you've liked. Perfect for automatic data hoarding! 

Alternatiely, this can be used to download a large quantity of YouTube videos without dodgy online websites. Just make a .txt file called 'NewLikedVideo.txt' with seperate hyperlinks on each line. The script will then download them.

## Set Up
This system requires a bit of setup, but once it's done you'll never have to touch it again!

The set up process can be broken into three parts

### Dropbox
1. Set up a DropBox account if you haven't already got one.
2. Head to [this address](https://www.dropbox.com/developer "Dropbox Developer's page"), and click the box in the top right labeled "App Console"
3. Select "Create App"
4. Go through the set up process, and make sure to set up the app so that it only has read access to a specific folder.
5. Once your app is created, navigate to the app's page (found under the Apps Console that we went to earlier). Under "settings" scroll to "App Folder Name", and change the name of the folder to "YouTube".
_That's it!!_

### IFTTT
1. Navigate to [this address](https://www.ifttt.com "IFTTT homepage"), and set up an IFTTT account if you don't already have one.
2. Select "create" in the top right hand corner
3. Select the "this" button, and search for "YouTube". Click on YouTube, and then click on "New Liked Video"
4. Select "that", and search for "DropBox". Select "Append to a text file".
5. Under "File Name" enter `NewLikedVideo.txt`, under "Dropbox Folder Path" enter `Apps/YouTube`. Under "content" enter `{{url}}<br>`
6. Click all the positive options that follow. (Yes, confirm, etc.)
_That's it!!_

### Raspberry Pi
1. Clone this git repository to your pi, and place both the python file and "PreviousURLs.txt" on to the desktop.
2. In the python file, there are some variable values that need changing. 
    - Change "DBX_ACCESS_TOKEN" to the value found in your app's settings page, when you click "generate access token"
    - Change "PREV_TXT_PATH" to the path taken to reach your desktop. This is usually `/home/pi/Desktop/previousURLs.txt`
    - If you wish for the YouTube video to download to a seperate file (not your desktop, so perhaps an external drive or NAS), then change the "DOWNLOAD_PATH" variable from `None` to a string of the desired destination. (eg "/media/Drive5/YouTubeVids")
3. To allow this code to run automatically and download your YouTube likes, you have to edit the crontab in your pi. Do this by entering the following commands:
    - `sudo crontab -e`
    - If you have never edited your crontab before, it will ask you to choose a text editor to do so. Choose option 1, nano, as this is the easiest. 
    - Navigate to the bottom of the file. 
    - Enter the new line `0 * * * * python3 /home/pi/Desktop/YTDownloader.py` to run this script every hour. You may decide you wish to run the script every day instead, in which case change `0 * * * *` to `0 0 * * *`.
    - Press `ctrl x`, `y`, `Enter` to exit the editor.
4. Install the required dependencies. In this case, they are `dropbox` and `pytube3`, assuming `requests` and `os` are already installed. They can be installed using pip, in the usual fashion. 

*Note!* crontab doesn't give errors, or even open a terminal window. It just runs in the background - so there is no way to determine whether the install has been successful unless you run this yourself by typing the command `python3 /home/pi/Desktop/YTDownloader.py`

__Congratulations!!__ You now have an automatic YouTube Video downloader, so you never have to worry about your favourite videos dissapering from the internet. Remember, never repost videos that someone else has made, never monitise someone else's work, keep your videos in your hoard!! And maybe don't press like on that 10 hour remix of your favourite meme. 

DISCLAIMER - Only download videos you have the right to download. That is open-source videos. If you like a video that is copywrited, I will not be held responsible for that and do not condone that type of action. 

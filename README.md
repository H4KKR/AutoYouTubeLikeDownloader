# AutoYouTubeLikeDownloader
Uses IFTTT, Dropbox and a Raspberry Pi to automatically download and store *new* YouTube videos you've liked. Perfect for automatic data hoarding! 

Alternatiely, this can be used to download a large quantity of YouTube videos without dodgy online websites. Instructions for both options are below!

__DISCLAIMER__ - Only download videos you have the right to download. That is open-source videos. If you like a video that is copywrited, I will not be held responsible for that and do not condone that type of action. 

## Set Up
This system requires a bit of setup, but once it's done you'll never have to touch it again!

The first method covered will be the hardest, which sets up the script to download new YouTube videos you like. 
The second method is for bulk downloading YouTube videos from a locally stored list.

Both methods require the same initial setup, covered here:
1. Use `pip` to install the `pytube3` library, by typing this command:
`pip install pytube3`

- Unfortunately, the `pytube3` library is a little bit broken - __BUT ONLY IN ONE PLACE!__ I am currently working on rewriting the code to work with a different library, but in the mean time here're the instructions for the work around. 

<details>
  <summary>More info on bug</summary>
The devs behind pytube3 are not the most active, and the YouTube site changed which broke the code. For those interested, [here's the StackOverflow]("https://stackoverflow.com/questions/61960657/getting-keyerror-url-with-pytube") of the error you will get if you don't do this really easy fix.
</details>

1. Type on your command line/terminal `pip show pytube3`, and head to the shown path.
2. Open the folder "pytube" when in the folder previously shown, and scroll to the py file "extract.py"
3. Scroll to line 301. Change the word in the square brackets from `["cipher"]` to `["signatureCipher"]`. _That's it!_ You've now solved the problem. 


## OPTION 1 - AUTOMATIC YOUTUBE VIDEO DOWNLOADER FROM LIKES

### Dropbox
1. Set up a DropBox account if you haven't already got one.
2. Head to [this address](https://www.dropbox.com/developer "Dropbox Developer's page"), and click the box in the top right labeled "App Console"
3. Select "Create App"
4. Go through the set up process, and make sure to set up the app so that it only has read access to a specific folder. The app name needs to be unique (not used by someone else, like YouTube is), and it doesn't matter to the rest of the set up. It can be a random string, or a discriptive name! 
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

### Raspberry Pi/Computer that is always plugged in
1. Clone this git repository to your pi, and place all the files on to the desktop.
2. In the "config.txt" file, there are some settings that need changing. 
    - Change STORE_SERVICE to "dropbox"
    - Change FETCH_FILE_NAME to "NewLikedVideo.txt"
    - Change DBX_ACCESS_TOKEN to the value found in your app's settings page, when you click "generate access token"
    - Change PREV_TXT_PATH to the path taken to reach your desktop. This is usually `/home/pi/Desktop/previousURLs.txt`
    - If you wish for the YouTube video to download to a seperate file (not your desktop, so perhaps an external drive or NAS), then change the "DOWNLOAD_PATH" variable from `""` to a string of the desired destination. (eg "/media/Drive5/YouTubeVids")
3. To allow this code to run automatically and download your YouTube likes, you have to edit the crontab in your pi. Do this by entering the following commands:
    - `sudo crontab -e`
    - If you have never edited your crontab before, it will ask you to choose a text editor to do so. Choose option 1, nano, as this is the easiest. 
    - Navigate to the bottom of the file. 
    - Enter the new line `0 * * * * python3 /home/pi/Desktop/YTDownloader.py` to run this script every hour. You may decide you wish to run the script every day instead, in which case change `0 * * * *` to `0 0 * * *`.
    - Press `ctrl x`, `y`, `Enter` to exit the editor.
4. Install the required dependencies. In this case, they are `dropbox` and `pytube3`, assuming `requests` and `os` are already installed. They can be installed using pip, in the usual fashion. 

*Note!* crontab doesn't give errors, or even open a terminal window. It just runs in the background - so there is no way to determine whether the install has been successful unless you run this yourself by typing the command `python3 /home/pi/Desktop/YTDownloader.py`

__Congratulations!!__ You now have an automatic YouTube Video downloader, so you never have to worry about your favourite videos dissapering from the internet. Remember, never repost videos that someone else has made, never monitise someone else's work, keep your videos in your hoard!! And maybe don't press like on that 10 hour remix of your favourite meme. 


## OPTION 2 - BULK YOUTUBE VIDEO DOWNLOAD FROM LOCAL FILE

1. Clone this git repository to your computer, and place all the files somewhere you know where to find (perhaps Documents or Desktop?).
2. In the "config.txt" file, there are some settings that need changing. 
    - Change STORE_SERVICE to "local"
    - Change FETCH_FILE_NAME to the filename (or path if it is in a seperate directory to the py file) of the txt file holding all of your YouTube links. There needs to be seperate links on new lines.
    - Change DBX_ACCESS_TOKEN to `""`.
    - Change PREV_TXT_PATH to the path taken to reach your previousURLs.txt file. This is usually `/home/pi/Desktop/previousURLs.txt`if you put it on a Raspberry Pi's Desktop. This file is required by the program, but it can be empty and its intended purpose not used. 
    - If you wish for the YouTube video to download to a seperate folder (not in the same directory as the py file, so perhaps an external drive or NAS), then change the "DOWNLOAD_PATH" variable from `""` to a string of the desired destination. (eg "/media/Drive5/YouTubeVids")
3. Install the `dropbox` and `pytube3` dependencies (even though you're not using the dropbox library, it still needs to be downloaded.) using pip, in the usual fashion.
4. Navigate to the py file, and run it.

__Congratulations!!__ You now have an easy way to download a lot of YouTube videos at once! Just populate the file however you see fit, however many times you'd like and just keep running the py file to download all your YouTube videos. 

I would really recommed checking out [this workaround]("https://www.youtube.com/watch?v=9fhZCV5VIvA&feature=youtu.be") for how to download your historically liked videos. It involves a chromecast, which if you are lucky enough to have then you can do it! Stick with the video, it's one of those stereotypical tech tutorials straight out of the early 2000s (even though it's from 2020!). All it needs now is no speaking, typing in Notepad and some royalty-free bangers!!
You can then use the `youtube-dl` command line tool to extract the IDs of each of the videos. 
Type `youtube-dl -j --flat-playlist 'https://www.youtube.com/watch?v=gdOwwI0ngqQ&list=PLPpZI8R1zUfrkDbmJMOBhEbJ9Td9vbV-F'`
Then with a script that I will add to the GitHub in a few days, you can convert those IDs into urls which can be downloaded by this Python program in the git already!! Very exciting stuff. You can also download with the youtube-dl tool itself.

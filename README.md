# spotify-mood-playlist-generator

Requirements:
Spotify Premium Account
Spotify Desktop App
Webcam



Setup instructions:
Log in to the Spotify Desktop App.

Run  ```sudo pip3 install -r REQUIREMENTS.txt ``` in terminal/command prompt. It will prompt you for the password.
Or install the following individually(also found in REQUIREMENTS.txt):
keras==2.0.5
tensorflow==1.14.0
pandas==0.25.3
numpy==1.16.4
h5py==2.7.0
statistics
opencv-python==4.1.0.25
spotipy

Run ```pip install git+https://github.com/plamere/spotipy.git --upgrade```

Run the program (spotify-mood-playlist-generator/src/main.py)

When you run the program for the first time, you will be sent to your default web browser. 
It will bring up a login page for Spotify, where you will authorise the app to access your account to edit your playlists. 
This will redirect you to another webpage. Copy the URL of the page, and paste it into the terminal prompt, and press enter. 

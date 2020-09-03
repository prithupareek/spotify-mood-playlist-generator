# spotify-mood-playlist-generator

## Requirements:<br />
Spotify Premium Account<br />
Spotify Desktop App<br />
Webcam<br />

## Setup instructions:
Log in to the Spotify Desktop App. <br />

Run  ```sudo pip3 install -r REQUIREMENTS.txt ``` in terminal/command prompt. It will prompt you for your password. <br />
Or install the following individually(also found in REQUIREMENTS.txt):<br />
```
keras==2.0.5
tensorflow==1.14.0
pandas==0.25.3
numpy==1.16.4
cython
statistics
opencv-python==4.1.0.25
spotipy
matplotlib
scipy==1.1.0
h5py==2.7.0
```

Run ```pip install git+https://github.com/plamere/spotipy.git --upgrade```<br />

If installing h5py fails, then install using homebrew on mac, using command
brew install hdf5

Put your spotify client id and secret where it asks for it in main.py

Run the program (spotify-mood-playlist-generator/src/main.py)<br />

When you run the program for the first time, you will be sent to your default web browser. <br />
It will bring up a login page for Spotify, where you will authorise the app to access your account to edit your playlists. <br />
This will redirect you to another webpage. Copy the URL of the page, and paste it into the terminal prompt, and press enter.<br /> 

Credits:
Face Recognition Model from: https://github.com/oarriaga/face_classification

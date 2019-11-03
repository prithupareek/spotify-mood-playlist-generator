# spotify-mood-playlist-generator

##Requirements:<br />
Spotify Premium Account<br />
Spotify Desktop App<br />
Webcam<br />

##Setup instructions:
Log in to the Spotify Desktop App. <br />

Run  ```sudo pip3 install -r REQUIREMENTS.txt ``` in terminal/command prompt. It will prompt you for your password. <br />
Or install the following individually(also found in REQUIREMENTS.txt):<br />
keras==2.0.5<br />
tensorflow==1.14.0<br />
pandas==0.25.3<br />
numpy==1.16.4<br />
h5py==2.7.0<br />
statistics<br />
opencv-python==4.1.0.25<br />
spotipy<br />
matplotlib <br />

Run ```pip install git+https://github.com/plamere/spotipy.git --upgrade```<br />

Run the program (spotify-mood-playlist-generator/src/main.py)<br />

When you run the program for the first time, you will be sent to your default web browser. <br />
It will bring up a login page for Spotify, where you will authorise the app to access your account to edit your playlists. <br />
This will redirect you to another webpage. Copy the URL of the page, and paste it into the terminal prompt, and press enter.<br /> 

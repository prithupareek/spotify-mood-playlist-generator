####### imports
# spotify web api library
import sys
import spotipy
import spotipy.util as util
import json
import os
import subprocess
import webbrowser

import math, copy, string, random
from cmu_112_graphics import *
from tkinter import *

from statistics import mode

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

def mostFrequent(L):
    freq = L[0]
    freqCount = 1
    for i in L:
        curr = L.count(i)
        if (curr>freqCount):
            freqCount = curr
            freq = i
    return freq

class GUI(App):
    clickCount = 0
    faceScanCount = 0
    # GUI.canvas = canvas
    # currentSong = 'No song is playing'

    def appStarted(app):
        app.text = '''Press any key to generate a playlist.'''
        app.text2 = 'press any key to generate another playlist'
        app.fill = 'red'
        app.counter = 0
        app.counterTwo = 0
        app.mood = None

    def keyPressed(app, event):
        GUI.clickCount += 1

    def timerFired(app):
        if GUI.clickCount == 1:
            # scanning face
            app.text = '''Scanning your face ...'''
            app.fill = 'gold'
            app.counterTwo += 1
        if GUI.clickCount == 1 and app.counterTwo == 2:
            app.mood = emotionDetection()
            if app.mood == 'fear':
                app.mood = 'angry'
        if GUI.clickCount == 2:
            # creating playlist
            app.text = f'Creating your {app.mood} playlist ...'
            app.fill = 'spring green'
            app.counter += 1
        if GUI.clickCount == 2 and app.counter == 2:
            generatePlaylist(app.mood)
        elif GUI.clickCount == 3:
            # done
            app.text = 'Done'
            app.fill = 'cyan3'
        elif GUI.clickCount == 4:
            # restart
            GUI.appStarted(app)
            GUI.clickCount = 0
            GUI.faceScanCount = 0

    def redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = app.fill)
        # current track
        # canvas.create_text(app.width/2, app.height/3*2, text=GUI.currentSong, fill='white', font='Arial 20 bold')
        # if app.clickCount == 1:
        #     canvas.create_rectangle(app.width/2 - 50, app.height/2 + 20, app.width/2 + 50, app.height/2 + 40, fill=None, outline='white')
        #     canvas.create_rectangle(app.width/2 - 50, app.height/2 + 20, app.width/2* - 50 + 4*GUI.faceScanCount, app.height/2 + 40, fill='white', width=0)
        canvas.create_text(app.width/2, app.height/2, text=app.text, fill='white', font= 'Arial 40 bold')
        if app.clickCount == 3:
            canvas.create_text(app.width/2, app.height/5*3, text=app.text2, fill='white', font= 'Arial 10 bold')

def emotionDetection():
    ### Based on: https://github.com/oarriaga/face_classification ###
    detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
    emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
    emotion_labels = get_labels('fer2013')
    frame_window = 10
    emotion_offsets = (20, 40)
    face_detection = load_detection_model(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    emotion_target_size = emotion_classifier.input_shape[1:3]
    emotion_window = []
    video_capture = cv2.VideoCapture(0)

    emotionsList = []

    while len(emotionsList) < 10:
        bgr_image = video_capture.read()[1]
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(face_detection, gray_image)

        for face_coordinates in faces:
            x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
            gray_face = gray_image[y1:y2, x1:x2]
            try:
                gray_face = cv2.resize(gray_face, (emotion_target_size))
            except:
                continue

            gray_face = preprocess_input(gray_face, True)
            gray_face = np.expand_dims(gray_face, -1)
            gray_face = np.expand_dims(gray_face, 0)
            emotion_prediction = emotion_classifier.predict(gray_face)
            emotion_label_arg = np.argmax(emotion_prediction)
            emotion_text = emotion_labels[emotion_label_arg]
            emotion_probability = np.max(emotion_prediction)
            if emotion_text != "neutral":
                emotionsList.append(emotion_text)
                GUI.faceScanCount += 1
                # GUI.redrawAll(GUI.canvas)
                # print(GUI.faceScanCount)
                print(emotion_text)
    ### Based on: https://github.com/oarriaga/face_classification ###

    GUI.clickCount += 1
    return mostFrequent(emotionsList)
    video_capture.release()
    cv2.destroyAllWindows()



genreList = [['aucoustic'], ['alternative'], ['chill'], ['classical'], ['dance'], ['deep-house'], ['disco'], ['edm'], ['electronic'], ['funk'], ['gospel'],
		['guitar'], ['happy'], ['rock'], ['hip-hop'], ['indian'], ['latino'], ['indie'], ['pop'], ['k-pop'], ['r-n-b'], ['rainy-day'], ['rock-n-roll'], ['soul'],
		['techno'], ['pop-film'], ['party'], ['work-out']]

# dictionary to store song attributes based on mood input
def getDictionary():
    moods = {
        "happy":    {"valence":(0.7,1), "danceability":(0.6,1), "energy":(0.7,1), "names":['jolly good day', "sunshine'n'flowers", 'goooood vibez']},
        "sad":      {"valence":(0,0.4), "danceability":(0,0.5), "energy":(0, 0.4), "names":['sad boi hours', 'stressed and depressed', 'rainy days']},
        "angry":    {"valence":(0,0.4), "danceability":(0.3,0.7), "energy":(0.7,1), "names":['FUUUUUCK', 'asdz,hjlvcdsv bkjscukyzfbsa']},
        "surprise": {"valence":(0.5,1), "danceability":(0,0.5), "energy":(0,0.5), "names":['whateva floats ya boat', 'MEH', 'just throw somethin on', 'vIbe ChEck']},
        "disgust":  {"valence":(0,0.4), "danceability":(0,0.5), "energy":(0.7,1), "names":['ew', 'gross', 'DiSgUsTiNg!']},
        "neutral":  {"valence":(0.3,0.7), "danceability":(0.3,0.7), "energy":(0.3,0.7), "names":['today im feeling lucky', 'blam!', 'cracka-pow!']}
    }

    return moods

def getSeedAttributes(mood, attributeDictionary):
    attributes = attributeDictionary[mood]
    minV = attributes["valence"][0]
    maxV = attributes["valence"][1]
    minD = attributes["danceability"][0]
    maxD = attributes["danceability"][1]
    minE = attributes["energy"][0]
    maxE = attributes["energy"][1]
    name = attributes["names"][random.randint(0,len(attributes["names"])-1)]
    return (minV, maxV, minD, maxD, minE, maxE, name)

# client id and secret for Spotify API
SPOTIFY_CLIENT_ID = 'e45be9e967454039b8c8d82e6e40581e'
SPOTIFY_CLIENT_SECRET = '24ea575d3b6344d4ab57f824fc08e0a5'
SPOTIFY_REDIRECT_URI = 'http://prithupareek.com/hack112.html'

# get username and authorize user
scope = 'playlist-modify-public user-read-playback-state'
token = util.prompt_for_user_token('sabir.sekhon2',scope,client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET,redirect_uri=SPOTIFY_REDIRECT_URI)
# create the spotify object
print('Connecting to spotify...')
sp = spotipy.Spotify(auth=token)

# def getCurrentSong():
#     currentTrack = sp.current_user_playing_track()
#     return currentTrack

def generatePlaylist(mood):

    # if you got the user token
    if token:


        userdata = sp.current_user()
        username = userdata['id']

        moods = ['happy', 'sad', 'angry', 'surprise', 'disgust', 'neutral']

        # loop through each genre and get songs
        names = []
        uris = []
        moodDictionary = getDictionary()
        (minV, maxV, minD, maxD, minE, maxE, name) = getSeedAttributes(mood, moodDictionary)

        # grab the tracks from spotify
        print("Getting your songs...")
        for genre in genreList:
            results = sp.recommendations(seed_artists=None, seed_genres=genre, seed_tracks=None, limit=2, min_popularity=60,
                                            min_valence=minV, max_valence=maxV, min_danceability=minD, max_danceability=maxD,
                                            min_energy=minE, max_energy=maxE)
            for dictionary in results["tracks"]:
                names.append(dictionary["name"])
                uris.append(dictionary["uri"])
        print(mood, names)


        # create a new playlist for the user
        print('Creating your playlist...')
        # GUI.clickCount = 1
        playlist_name = name
        playlist_description = 'Auto-generated playlist based on your mood.'
        sp.trace = False
        playlists = sp.user_playlist_create(username, playlist_name, public = True, description = playlist_description)

        playlistURI = playlists["uri"]

        addSongsResults = sp.user_playlist_add_tracks(username, playlistURI, uris)
        print("Done")
        GUI.clickCount = 3

        # open playlist in spotify
        webbrowser.open(playlistURI)

    else:
        print("Oops, cannot authorize user account.")


app = GUI(width = 2560, height = 1600)

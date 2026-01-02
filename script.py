#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#load env variables
load_dotenv()

#get credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

def main():
    playlist_url = input("Enter Spotify playlist URL: ")
    print("Thank you! Fetchin yur songs ;)")
    playlist_id = GetId(playlist_url)

    #now try connecting
    try:
        client_credentials_manager = SpotifyClientCredentials(
                client_id, 
                client_secret
                )
        #create a spotify object
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        result = sp.playlist(playlist_id)
        print("Connection was successful")
        print(f"Your playlist name is: {result['name']}")
    except Exception as e:
        print(f"Connection failed: {e}")
    
    #step 2 is to get the playlist data
    playlist_data = sp.playlist(playlist_id)
    tracks = playlist_data['tracks']['items']

def GetId(url):
    #parse the url to get the playlist id
    
    #split it into two parts -> take the second part
    parts = url.split("/playlist/")
    playlist_part = parts[1]

    #clean it up and remove the query param
    playlist_parts = playlist_part.split("?")
    playlist_id = playlist_parts[0] #keep the first part
    return playlist_id

if __name__ == "__main__":
    main()

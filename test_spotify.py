#!/usr/bin/env python3

SPOTIFY_CLIENT_ID="ed3cc9e0df2c435cb3d2631d15cd842e"
SPOTIFY_CLIENT_SECRET="1c54c30aecc24004adf0cf4c642e3e2b"

#connect to the spotify api

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

try:
    #set up the authentication
    client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
            )
    #create the spotify object
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    #testing connection
    results = sp.playlist("2imw9aC28M8qaPTBb5lZYj") #my drake playlist
    print(" connection made!")
    print(f"Playlist name: {results['name']}")

except Exception as e:
    print(f"Connection failed: {e}")

#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp

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
        playlist_data = sp.playlist(playlist_id)
        print("Connection was successful")
        print(f"Your playlist name is: {playlist_data['name']}")

        #step 2 is to get the playlist data
        tracks = playlist_data['tracks']['items']
        songs = []
        #loop through the items in my tracks list
        for item in tracks:
            #extract the data I want
            track = item['track']
            song_info ={
                    'track_name': track['name'],
                    'artist_name': track['artists'][0]['name'], #get the first/main artists name
                    'album_name': track['album']['name']
                    }
            #append to the dictionar: songs
            songs.append(song_info)
        #step 3 is to find the songs on YouTube
        for song in songs:
            #for each song create a search query
            search = VideosSearch(f"{song['track_name']} by {song['artist_name']} official audio", limit=1) #set the max num of search res return to 1
            result = search.result()
            video_url = result ['result'][0]['link'] #get the vid link
            
            #step 4 is to download the songs from the urls
            download_yt_vids(video_url)

    except Exception as e:
        print(f"Connection failed: {e}")

def GetId(url):
    #parse the url to get the playlist id
    
    #split it into two parts -> take the second part
    parts = url.split("/playlist/")
    playlist_part = parts[1]

    #clean it up and remove the query param
    playlist_parts = playlist_part.split("?")
    playlist_id = playlist_parts[0] #keep the first part
    return playlist_id
def download_yt_vids(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best', #download the audio only
            'outtmpl': 'songsDownloaded/%(title)s.%(ext)s', #save to current dir in a subfolder
            'noplaylist': True,
            #process it to mp3 format
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
                }],
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfull! Audios saved to 'songsDownloaded'")
    except yt_dlp.utils.DownloadError as de:
        #print the error message
        print(f"Download error: {str(de)}")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 19:26:18 2020

@author: lhmarsden
"""

#%% Imports

import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import spotipy # Need to install
from spotipy.oauth2 import SpotifyClientCredentials # Need to install

#%% Functions

def artistAlbums(artist_name):
    result = sp.search(artist_name) #search query
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri'] # Extract artist's URI
    sp_albums = sp.artist_albums(artist_uri, album_type='album') # Store artist's albums' names' and uris in separate lists
    album_names = []
    album_uris = []
    for i in range(len(sp_albums['items'])):
        album_names.append(sp_albums['items'][i]['name'])
        album_uris.append(sp_albums['items'][i]['uri'])
        
    return album_names, album_uris

def albumSongs(uri):
    album = uri #assign album uri to a_name
    spotify_albums[album] = {} #Creates dictionary for that specific album#Create keys-values of empty lists inside nested dictionary for album
    spotify_albums[album]['name'] = []
    tracks = sp.album_tracks(album) #pull data on album tracks
    for n in range(len(tracks['items'])): # for each song track on album
        spotify_albums[album]['name'].append(tracks['items'][n]['name']) # Appending song title for each track on album
    
    return spotify_albums[album]['name']
    
def titleOnly(song_title):
    sep = ' - ' # Separator, to remove all text in song title after and including the hyphen, as this is usually 'Remastered', 'Demo' or 'Live' etc.
    song_title_only = song_title.split(sep, 1)[0]
    
    return song_title_only

def removeDuplicates(myList):
    no_duplicates = list(dict.fromkeys(myList)) # Removing duplicate album names, dictionaries can't have duplicate keys

    return no_duplicates

def words_in_song(song_title, artist_name):
    url = 'https://api.lyrics.ovh/v1/' + artist_name + '/' + song_title
    response = requests.get(url)
    json_data = json.loads(response.content)
    lyrics = json_data['lyrics']
    num_words = len(str(lyrics).split())
    
    return num_words

#%% Application
    
spotify_id = {ENTER SPOTIFY CLIENT ID HERE}
spotify_secret = {ENTER SPOTIFY SECRET HERE}
spotify_credentials_manager = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret) # Spotify object to access API
sp = spotipy.Spotify(client_credentials_manager=spotify_credentials_manager)


#%%
# Creating empty dictionaries where data can be stored for multiple artists
artists = {}
artists['artist_1'] = {}
artists['artist_2'] = {}

n = 0

while n < 3: # Asking a maximum of 3 times
    try:
        n=n+1
        artists['artist_1']['name'] = input('\nPlease enter the name of your first artist: ')
        artists['artist_1']['album_names'], artists['artist_1']['album_uris'] = artistAlbums(artists['artist_1']['name'])
        print('\nSearching for albums on Spotify by artist')
        if artists['artist_1']['album_names'] is not None:
            break
    except:
        if n < 2:
            print('\nNo albums have been found by that artist. Please try again')
        elif n == 2:
            print('\nPlease try one last time! (check spelling)')
        elif n == 3:
            print('\nSorry, no albums found by that artist.')
        pass

while n < 3: # Asking a maximum of 3 times
    try:
        n=n+1
        artists['artist_2']['name'] = input('\nPlease enter the name of your second artist: ')
        artists['artist_2']['album_names'], artists['artist_2']['album_uris'] = artistAlbums(artists['artist_2']['name'])
        print('\nSearching for albums on Spotify by artist')
        if artists['artist_2']['album_names'] is not None:
            break
    except:
        if n < 2:
            print('\nNo albums have been found by that artist. Please try again')
        elif n == 2:
            print('\nPlease try one last time! (check spelling)')
        elif n == 3:
            print('\nSorry, no albums found by that artist.')
        pass

#%%

spotify_albums={}

for a in ['artist_1', 'artist_2']:
    print('\nCreating a list of songs by ' + artists[a]['name'])
    artists[a]['songs'] = []
    artists[a]['unique_songs'] = []
    
    for i in artists[a]['album_uris']:
        artists[a]['songs'] = artists[a]['songs'] + albumSongs(i)
        
    for i in artists[a]['songs']:
        artists[a]['unique_songs'].append(titleOnly(i))
        
    artists[a]['unique_songs'] = removeDuplicates(artists[a]['unique_songs'])
    
    artists[a]['num_words'] = [] # create empty list for number of words in song
    
    print('\nCalculating number of words in each song')
    for i in artists[a]['unique_songs']:
        print('\nSong title: ' + i)
        try: # Checking whether song can be found in API, if not, giving NAN for number of words for that song
            num_words = words_in_song(i,artists[a]['name'])
            artists[a]['num_words'].append(num_words)
            print('Number of words: ' + str(num_words))
        except: 
            num_words = np.nan
            artists[a]['num_words'].append(num_words)
            print('Error: Track not found, excluding from calculation')
        

    artists[a]['average_words'] = int(np.nanmean(artists[a]['num_words'])+0.5) # Calculating average number of words in all songs by artist, rounding to nearest integer
    artists[a]['max_words'] = max(artists[a]['num_words'])
    artists[a]['song_most_words'] = artists[a]['unique_songs'][artists[a]['num_words'].index(artists[a]['max_words'])]

    artists[a]['num_words'] = np.array(artists[a]['num_words'])
    artists[a]['num_words_rm_nans'] = artists[a]['num_words'][np.isfinite(artists[a]['num_words'])]
    
    
#%% Creating a boxplot

print('\nArtist: ' + artists['artist_1']['name'])
print('\nAverage number of words in songs: ' + str(artists['artist_1']['average_words']))
print('\nSong with most words: ' + artists['artist_1']['song_most_words'] + ' (' + str(artists['artist_1']['max_words']) + ' words)')

print('\nArtist: ' + artists['artist_2']['name'])
print('\nAverage number of words in songs: ' + str(artists['artist_2']['average_words']))
print('\nSong with most words: ' + artists['artist_2']['song_most_words'] + ' (' + str(artists['artist_2']['max_words']) + ' words)')

fig1, ax1 = plt.subplots()
ax1.set_title('Artist Comparison: Number of words in songs')
ax1.set_ylabel('Number of words in song')
ax1.set_xlabel('Artist')
ax1.boxplot([artists['artist_1']['num_words_rm_nans'] ,artists['artist_2']['num_words_rm_nans'] ])
ax1.set_xticklabels([artists['artist_1']['name'],artists['artist_2']['name']])
plt.show()
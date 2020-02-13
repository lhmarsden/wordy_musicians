# wordy_musicians
A Python CLI application that calculates the average number of words that a given artist has used in their songs. Song tracks are first pulled from the Spotify API, and a client ID and client secret can be obtained for free from https://developer.spotify.com/. The user is asked to select 2 artists of their choosing to be compared. Song lyrics are then pulled from the free lyricsovh API, https://lyricsovh.docs.apiary.io/#reference. The lyrics for each song are counted, averaged, and statistics are displayed in the command line (average number of words, song with the most words and how many words it includes.

Finally, a boxplot is created to show the spread of data for each artist, to allow the user to easily compare statistics for the two artists.

You can download this script using the following git command:

Spotipy must be installed for this program to run, and can be installed using the following command:

pip install spotipy



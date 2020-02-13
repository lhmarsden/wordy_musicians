# wordy_musicians
A Python CLI application that calculates the average number of words that a given artist has used in their songs. Song tracks are first pulled from the Spotify API. The user is asked to select 2 artists of their choosing to be compared. Song lyrics are then pulled from the free lyricsovh API, https://lyricsovh.docs.apiary.io/#reference. The lyrics for each song are counted, averaged, and statistics are displayed in the command line (average number of words, song with the most words and how many words it includes.

Finally, a boxplot is created to show the spread of data for each artist, to allow the user to easily compare statistics for the two artists.

To run locally:

1. Run this command: git clone https://github.com/lhmarsden/wordy_musicians.git
2. Ensure Spotipy is installed, this can be installed using the following command: pip install spotipy
3. A client ID and client secret can be obtained for free from https://developer.spotify.com/
4. Run in your terminal: python wordy_musicians.py



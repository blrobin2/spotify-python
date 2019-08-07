import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from pprint import pprint
from tqdm import tqdm


def init_spotify_api():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
    )

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_top_ten_artists(username, show_progress_bar=False):
    sp = init_spotify_api()
    playlists = sp.user_playlists(username)

    # get artists from playlist
    # count each instance
    artists = []
    owner_playlists = [playlist for playlist in playlists.get('items') if playlist['owner']['id'] == username]
    if show_progress_bar:
        progress_bar = tqdm(
            total=len(owner_playlists),
            unit='playlist'
        )

    for playlist in owner_playlists:
        results = sp.user_playlist(username, playlist.get('id'), fields="tracks,next")
        tracks = results.get('tracks')

        for i, item in enumerate(tracks.get('items')):
            track = item.get('track')
            artists.append(track['artists'][0]['name'])

        while tracks.get('next'):
            tracks = sp.next(tracks)
            for i, item in enumerate(tracks.get('items')):
                track = item.get('track')
                artists.append(track['artists'][0]['name'])

        if show_progress_bar:
            progress_bar.update()

    return Counter(artists).most_common(10)


def show_owner_playlists(playlists, username):
    for playlist in playlists.get('items'):
        if playlist['owner']['id'] == username:
            show_playlist(playlist)


def show_playlist(playlist):
    print(f"\n {playlist.get('name')}")
    print(f"\n\t total tracks: {playlist['tracks']['total']}")
    results = sp.user_playlist(username, playlist.get('id'), fields="tracks,next")
    tracks = results.get('tracks')
    show_tracks(tracks)
    while tracks.get('next'):
        tracks = sp.next(tracks)
        show_tracks(tracks)


def show_tracks(tracks):
    for i, item in enumerate(tracks.get('items')):
        track = item.get('track')
        print(f"\t {i+1} {track['artists'][0]['name']} - {track['name']}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python main.py [username]")
        sys.exit()

    print("Checking artist in each playlist: ")
    top_ten = get_top_ten_artists(username, show_progress_bar=True)
    pprint(top_ten)

import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def show_tracks(tracks):
    for i, item in enumerate(tracks.get('items')):
        track = item.get('track')
        print(f"\t {i} {track['artists'][0]['name']} - {track['name']}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python main.py [username]")
        sys.exit()

    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print(f"\n {playlist.get('name')}")
            print(f"\n\t total tracks: {playlist['tracks']['total']}")
            results = sp.user_playlist(username, playlist.get('id'), fields="tracks,next")
            tracks = results.get('tracks')
            show_tracks(tracks)
            while tracks.get('next'):
                tracks = sp.next(tracks)
                show_tracks(tracks)
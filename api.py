import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from tqdm import tqdm


def init_spotify_api():
    """
    Uses the environment to initialize the Spotify API
    :return: Spotify object
    """
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
    )

    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_top_ten_artists(username, show_progress_bar=False):
    """
    Fetches the ten artists that are most regularly added to the given user's Spotify playlists
    :param username: (string) the Spotify username
    :param show_progress_bar: (bool) whether or not to render  progress bar.
                                Mostly used for running this script directly
    :return: [(string: artist name, int: count)]
    """
    progress_bar = None
    sp = init_spotify_api()
    playlists = sp.user_playlists(username)

    # get artists from playlist
    # count each instance
    artists = []
    owner_playlists = [playlist for playlist in playlists.get('items') if playlist['owner']['id'] == username]
    if show_progress_bar:
        progress_bar = tqdm(
            total=len(owner_playlists),
            unit='playlist',
            leave=False,
        )

    for playlist in owner_playlists:
        results = sp.user_playlist(username, playlist.get('id'), fields="tracks,next")
        tracks = results.get('tracks')

        for item in tracks.get('items'):
            artists.append(get_artist_from_item(item))

        while tracks.get('next'):
            tracks = sp.next(tracks)
            for item in tracks.get('items'):
                artists.append(get_artist_from_item(item))

        if show_progress_bar and progress_bar is not None:
            progress_bar.update()

    return Counter(artists).most_common(10)


def get_artist_from_item(item):
    """
    Looks in the given item from Spotify api to fetch the artist
    :param item: the item as given from spotify
    :return: (string) the artist name
    """
    track = item.get('track')
    return track['artists'][0]['name']


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python api.py [username]")
        sys.exit()

    print("Checking artist in each playlist: ")
    top_ten = get_top_ten_artists(username, show_progress_bar=True)
    for i, (artist, count) in enumerate(top_ten):
        print(f"-> {i+1}. {artist}: {count} times")

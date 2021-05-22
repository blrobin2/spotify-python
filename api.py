import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import Counter
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

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


class Api:
    def __init__(self, username, show_progress_bar=False, sp=init_spotify_api()):
        self.sp = sp
        self.username = username
        self.show_progress_bar = show_progress_bar
        self.progress_bar = None

    def get_top_ten_artists(self):
        playlists = self.get_owner_playlists()
        if self.show_progress_bar:
            self.progress_bar = tqdm(
                total=len(playlists),
                unit='playlist',
                leave=False,
            )
        artists = self.get_artists_from_playlists(playlists)
        return Counter(artists).most_common(10)

    def get_owner_playlists(self):
        return self.sp.user_playlists(self.username)

    def get_artists_from_playlists(self, playlists):
        artist_lists = [self.get_artists_from_playlist(pl) for pl in playlists.get('items')]
        return [artist for artist_list in artist_lists for artist in artist_list]

    def get_artists_from_playlist(self, playlist):
        results = self.sp.user_playlist(username, playlist.get('id'), fields="tracks,next")
        tracks = results.get('tracks')
        artists = self.get_artists_from_tracks(tracks)

        if self.show_progress_bar and self.progress_bar is not None:
            self.progress_bar.update()

        return artists

    def get_artists_from_tracks(self, tracks):
        artists = []
        for item in tracks.get('items'):
            artists.append(self.get_artist_from_item(item))

        while tracks.get('next'):
            tracks = self.sp.next(tracks)
            for item in tracks.get('items'):
                artists.append(self.get_artist_from_item(item))

        return artists

    def get_artist_from_item(self, item):
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
    top_ten = Api(username, show_progress_bar=True).get_top_ten_artists()
    for i, (artist, count) in enumerate(top_ten):
        print(f"-> {i+1}. {artist}: {count} times")

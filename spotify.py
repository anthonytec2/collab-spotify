'''
Anthony Bisulco Python Spotify 
Collobrative Playlist
class to interface with spotify
'''
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import logging
import sys
from tabulate import tabulate
import yaml


class spotify:

    def __init__(self, username):
        """[initalize spotify class to be used to manage playlists]

        Arguments:
            username {[string]} -- [username of spotify user]
        """
        self.sp, self.user = self.init_auth_client()
        self.logger = logging.getLogger(__name__)

    def init_auth_client(self):
        """[authorize and initialize spotify client]

        Returns:
            [Spotify] -- [spotify authorized client]
            [String]  -- [username]
        """
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        token = util.prompt_for_user_token(cfg['username'], scope=cfg['scope'], client_id=cfg['spotipy_client_id'],
                                           client_secret=cfg['spotipy_client_secret'], redirect_uri=cfg['spotipy_redirect_uri'])
        sp = spotipy.Spotify(auth=token)
        return sp, cfg['username']

    def create_new_playlist(self, name, desc=''):
        """[creates a new playlist with given name, desc with given limts]

        Arguments:
            name {[string]} -- [name of the new playlist]

        Keyword Arguments:
            desc {str} -- [description of playlist] (default: {''})
        """
        pl_names, _ = self.list_playlists()
        if name in pl_names:
            self.logger.debug(
                'Playlist Name Already Exists, please use another name')
        else:
            pl = self.sp.user_playlist_create(
                self.user, name, public=False, description=desc)
            self.sp.user_playlist_change_details(
                self.user, pl['id'], collaborative=True)

    def search_song(self, name):
        """[Will generate a list of 10 songs with given song name]

        Arguments:
            name {[string]} -- [name of song to search]

        Returns:
            [song_ls] -- [list of songs uri for top 10s songs]
            [table_ls] -- [song info for top ten songs]
        """
        self.logger.debug('Searched for Song: {}'.format(name))
        results = self.sp.search(q='track:' + name, type='track')
        songs = [song for song in results['tracks']['items']]
        i = 1
        songs_ls = []
        table_ls = []
        for song in songs:
            table_ls.append([i, song['name'][0:20].strip(), song['album']['name'][0:20].strip(
            ), "%0.2f" % (song['duration_ms']/60000), song['popularity']])
            songs_ls.append(song['uri'])
            i = i+1
        return songs_ls, table_ls

    def list_playlists(self, user=None):
        """[list all spotify playlists on users account]

        Returns:
            pl_names [string] -- [lists of playlist names]
            pl_id [string] -- [list of playlist ids]
        """
        if user:
            playlists = self.sp.user_playlists(user)['items']
        else:
            playlists = self.sp.user_playlists(self.user)['items']
        pl_names = [pl['name'] for pl in playlists]
        pl_id = [pl['id'] for pl in playlists]
        return pl_names, pl_id

    def list_pl_songs(self, pl_id, user=None):
        """[list all the songs for a given playlist id]

        Arguments:
            pl_id {[string]} -- [playlist id to list songs]

        Returns:
            [string] -- [list of song uris in playlist]
        """
        if user:
            res = self.sp.user_playlist_tracks(user, pl_id)
        else:
            res = self.sp.user_playlist_tracks(self.user, pl_id)
        song_uri_ls = [song['track']['uri'] for song in res['items']]
        song_ls = []
        for i, song in enumerate(res['items']):
            song_ls.append([i, song['track']['name'][0:20].strip(), song['track']['album']['name'][0:20].strip(
            ), "%0.2f" % (song['track']['duration_ms']/60000), song['track']['popularity']])
        return song_uri_ls, song_ls

    def add_song_to_playlist(self, song_uri, playlist_id, user=None):
        """[adds a song to a playlist]

        Arguments:
            song_uri {[string]} -- [song uri to add to playlist]
            playlist_id {[string]} -- [playlist id to add song]
        """

        if song_uri[0] in self.list_pl_songs(playlist_id, user=None):
            logging.debug('Song already in playlist')
        else:
            if user:
                self.sp.user_playlist_add_tracks(user, playlist_id, song_uri)
            else:
                self.sp.user_playlist_add_tracks(
                    self.user, playlist_id, song_uri)

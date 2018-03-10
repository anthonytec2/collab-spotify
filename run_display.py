import logging
from tabulate import tabulate
import os
import spotify
import sys
clear = lambda: os.system('clear')

class run_display:
    def __init__(self,sp):
        self.logger = logging.getLogger(__name__)
        self.sp=sp

    def prompt_song(self):
        try:
            song_name = input('Song to Search: ').strip()
            return song_name
        except:
            self.logger.debug("Error trying to parse song name")
            return -1
    
    def select_number(self, low=0, high=10):
        """[Number selector from user options on screen]
        
        Keyword Arguments:
            low {int} -- [lowest int to input] (default: {0})
            high {int} -- [highest int to input] (default: {10})
        
        Raises:
            ValueError -- [if try to input any val except int]
        
        Returns:
            [int] -- [number of selection]
        """
        try:
            option = int(input('Option: ').strip())
            if low<=option<=high:
                return option
            else:
                raise ValueError
        except:
            self.logger.debug("Error trying to parse options #")
            return -1

    def display_user_playlists(self):
        """[displays all the songs from a users playlist]
        """
        pl_names,_ = self.sp.list_playlists()
        pl_names_ls=[]
        pl_names=[[i,pl_name] for i,pl_name in enumerate(pl_names)]
        clear()
        print(tabulate(pl_names))

    def display_user_tracks(self, track_ls):
        """[displays all the users tracks]
        
        Arguments:
            track_ls {[list]} -- [list of lists of song name, album, time and popularity]
        """

        clear()
        print(tabulate(track_ls, headers=["#", "Name","Album","Time","Popularity"]))

    def display_commands(self):
        """[displats all commands for user]
        """

        clear()
        print("1) Choose Active Playlist")
        print("2) Add new song to playlist")
        print("3) List Playlists")
        print("4) Print Songs in Playlist")
import logging
from tabulate import tabulate
import os
import spotify
import sys
import controller
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem, SelectionItem, ExitItem


class run_display:
    def __init__(self, sp):
        self.logger = logging.getLogger(__name__)

    def prompt(self, desc='Song to Search: '):
        """[Prompts user to put in song name]

        Returns:
            [string] -- [song name]
        """
        try:
            song_name = input(desc).strip()
            return song_name
        except BaseException:
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
            if low <= option <= high:
                return option
            else:
                raise ValueError
        except BaseException:
            self.logger.debug("Error trying to parse options #")
            return -1

    def display_user_playlists(self, pl_names, pl_ids):
        """[displays all the playlists from a users playlist]
        """
        pl_names_ls = []
        pl_names = [[i, pl_name] for i, pl_name in enumerate(pl_names)]
        print(tabulate(pl_names))
        return pl_ids, len(pl_names)

    def display_user_tracks(self, track_ls):
        """[displays all the users tracks]

        Arguments:
            track_ls {[list]} -- [list of lists of song name, album, time and popularity]
        """
        print(tabulate(track_ls, headers=[
              "#", "Name", "Album", "Time", "Popularity"]))

    def display_commands(self, user=None):
        """[displats all commands for user]
        """

        if user:
            menu = CursesMenu(
                "Spotify Collobrative Playlist",
                "User: " + user,
                show_exit_option=False)
        else:
            menu = CursesMenu(
                "Spotify Collobrative Playlist",
                "User",
                show_exit_option=True)
        sl1 = SelectionItem("Choose Active Playlist", 1)
        sl2 = SelectionItem("Add new song to playlist", 2)
        sl3 = SelectionItem("List Playlists", 3)
        sl4 = SelectionItem("Print Songs in Playlist", 4)
        sl5 = SelectionItem("Create Playlist", 5)
        sl6 = SelectionItem("Exit", 6)
        menu.append_item(sl1)
        menu.append_item(sl2)
        menu.append_item(sl3)
        menu.append_item(sl4)
        menu.append_item(sl5)
        menu.append_item(sl6)
        menu.start()
        menu.join()
        return menu.returned_value

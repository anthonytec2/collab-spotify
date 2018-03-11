import logging
import run_display
import spotify
import sys


class controller:
    def __init__(self):
        """[intialize controller class to run display]

        Arguments:
            username {[string]} -- [username for spotify]
        """
        self.sp = spotify.spotify()
        self.disp = run_display.run_display(self.sp)
        self.playlist = None
        self.logger = logging.getLogger(__name__)
        self.owner=self.sp.user
        
    def main_loop(self):
        """[main loop for running all commands]
        """
        while True:
            self.disp.display_commands()
            num = self.disp.select_number(low=1, high=7)
            self.handle_request(num)

    def handle_request(self, num):
        """[handles which option to process]

        Arguments:
            num {[int]} -- [incoming option]
        """
        if num == 1:
            pl_names, pl_ids,pl_own = self.sp.list_playlists(self.owner)
            pl_id, num_sel = self.disp.display_user_playlists(pl_names, pl_ids)
            num_pl = self.disp.select_number(0, num_sel)
            self.playlist = pl_id[num_pl]
            self.owner=pl_own[num_pl]
        elif num == 2:
            if self.playlist:
                name = self.disp.prompt()
                song_uris, song_tb = self.sp.search_song(name)
                self.disp.display_user_tracks(song_tb)
                num_song = self.disp.select_number(low=0, high=len(song_uris))
                self.sp.add_song_to_playlist(
                    [song_uris[num_song-1]], self.playlist)
            else:
                self.logger.debug('Please Select a Playlist first')
        elif num == 3:
            pl_names, pl_ids,_ = self.sp.list_playlists(self.owner)
            pl_id, num_sel = self.disp.display_user_playlists(pl_names, pl_ids)
            input("Press the <ENTER> key to continue...")
        elif num == 4:
            song_uri_ls, song_ls = self.sp.list_pl_songs(self.playlist, self.owner)
            self.disp.display_user_tracks(song_ls)
            input("Press the <ENTER> key to continue...")
        elif num == 5:
            pl_name = self.disp.prompt('Playlist Name : ')
            self.sp.create_new_playlist(pl_name)
        elif num == 6:
            sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(filename='data.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.debug('Program Intialized')
    cont = controller()
    cont.main_loop()

class playlist:
    def __init__(self, name, songs,own,idx):
        self.name=name
        self.songs=songs
        self.own=own
        self.idx=idx
        
    def get_songs(self):
        return self.songs

    def get_name(self):
        return self.name

    def get_own(self):
        return self.own

    def __str__(self):
        return self.songs
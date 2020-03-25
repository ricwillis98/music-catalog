import webbrowser
import shutil
import pickle
import os


class Catalog:
    SAVE_NAME = 'Catalog.pkl'

    @staticmethod
    def getInstance(d, **kwargs):
        if os.path.exists(os.path.join(d, Catalog.SAVE_NAME)):
            print("loading existing catalog")
            return Catalog.load(d)
        else:
            print("Creating new catalog")
            return Catalog(d, **kwargs)

    def __init__(self, d, name=None):
        self.dir = d
        self.name = name
        self.create_dir_if_missing()
        self.entries = []

    def create_dir_if_missing(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        return

    def add_link(self, link, **kwargs):
        l = LinkEntry(link, **kwargs) 
        self.entries.append(l)
        self.save()

    def add_file(self, path, **kwargs):
        # get artist name
        if 'artist' in kwargs.keys():
            artist = kwargs['artist']
        else:
            artist = 'Unknown'

        # create artist folder if needed
        artist_folder = os.path.join(self.dir, artist)
        if not os.path.exists(artist_folder):
            os.mkdir(artist_folder)

        file_name = os.path.split(path)[1]
 
        # copy file to artist folder
        new_path = os.path.join(artist_folder, file_name)
        print(new_path)
        shutil.copyfile(path, new_path)

        # create file entry
        f = FileEntry(path, **kwargs)
        self.entries.append(f)
        self.save()

    def save(self):
        path = os.path.join(self.dir, Catalog.SAVE_NAME)
        print(f"Saving to {path}")
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def print_contents(self):
        print()
        print("Name\t\t Artist\t\t")
        for entry in self.entries:
            print(entry)
        print()

    @staticmethod
    def load(d):
        with open(os.path.join(d, Catalog.SAVE_NAME), 'rb') as f:
            return pickle.load(f)


class Entry: 
    def __init__(self, name=None, artist="Unknown", composer=None): 
        self.name = name
        self.artist = artist
        self.composer = composer
        self.instrument
        self.tags = []
        return

    def show(self):
        raise Exception("NYI")

    def __str__(self):
        out = f"{self.name}\t {self.artist}\t"
        return out

class LinkEntry(Entry):
    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)
        self.link = link

    def show(self):
        webbrowser.open(self.link)
        return

class FileEntry(Entry):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def show(self):
        webbrowser.open(self.path)

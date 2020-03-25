from tkinter import *
from tkinter import ttk
from Catalog import *


class CatalogGUI:
    def __init__(self, master, catalog):
        self.catalog = catalog
        self.master = master
        master.title("Sheet Music Catalog")

        # set up tabs
        tab_control = ttk.Notebook(self.master)
        self.tab1 = ttk.Frame(tab_control)
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='Catalog')
        tab_control.add(self.tab2, text='Add Sheet Music')
        tab_control.pack(fill='both')
        self.make_tab1(self.tab1)
        self.make_tab2(self.tab2)

        # set up menu
        self.menu = Menu(self.master)
        file_dropdown = Menu(self.menu)
        file_dropdown.add_command(label='Exit', command=self.exit)
        self.menu.add_cascade(label='File', menu=file_dropdown)
        self.master.config(menu=self.menu)

    def choose_file(self):
        f = filedialog.askopenfilename()

    def make_tab1(self, tab):
        for i, entry in enumerate(self.catalog.entries):
            lb = Label(tab, text=entry)
            lb.grid(row=i)

            bt = Button(tab, text="Show", command=self.catalog.entries[i].show)
            bt.grid(row=i, column=1)

    def make_tab2(self, tab):
        entry_name_label = Label(tab, text="Song Name: ")
        entry_name_label.grid(row=0, column=0)
        self.entry_name = Entry(tab, width=10)
        self.entry_name.grid(row=0, column=1)

        entry_artist_label = Label(tab, text="Artist: ")
        entry_artist_label.grid(row=1, column=0)
        self.entry_artist = Entry(tab, width=10)
        self.entry_artist.grid(row=1, column=1)

        entry_url_label = Label(tab, text="URL: ")
        entry_url_label.grid(row=2, column=0)
        self.entry_url = Entry(tab, width=10)
        self.entry_url.grid(row=2, column=1)

        self.submit_button = Button(tab, text="Submit", command=self.add_link)
        self.submit_button.grid(row=3, column=1)

    def add_link(self):
        artist = self.entry_artist.get()
        name = self.entry_name.get()
        url = self.entry_url.get()
        
        self.catalog.add_link(url, artist=artist, name=name)
        self.master.refresh()


    def exit(self):
        sys.exit(0)

if __name__ == '__main__':
    catalog = Catalog.getInstance('./catalog')
    root = Tk()
    my_gui = CatalogGUI(root, catalog)
    root.mainloop()

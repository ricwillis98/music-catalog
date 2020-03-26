from tkinter import *
from tkinter import ttk, filedialog
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
        file_dropdown.add_command(label='Clear Catalog', command=self.clear)
        file_dropdown.add_command(label='Exit', command=self.exit)
        self.menu.add_cascade(label='File', menu=file_dropdown)
        self.master.config(menu=self.menu)

    def choose_file(self):
        f = filedialog.askopenfilename()
        self.entry_url.delete(0, 'end')
        self.entry_url.insert(0, f)
        self.is_file_checkbox.select()

    def show_entry(self, event):
        id_str = self.entry_tree.selection()[0]
        id_int = int(id_str[1:]) - 1
        self.catalog.entries[id_int].show()

    def delete_entry(self, entry):
        id_str = self.entry_tree.selection()[0]
        idx = int(id_str[1:]) - 1
        self.catalog.delete_entry(idx)
        self.entry_tree.delete(id_str)

    def make_tab1(self, tab):
        self.entry_tree = ttk.Treeview(tab, columns=('Artist', 'Genre'))
        self.entry_tree.bind("<Double-1>", self.show_entry)
        self.entry_tree.bind("<Delete>", self.delete_entry)
        self.entry_tree.heading('Artist', text='Artist')
        self.entry_tree.heading('Genre', text='Genre')
        for i, entry in enumerate(self.catalog.entries):
            self.insert_into_entry_tree(entry)
        self.entry_tree.pack()

    def insert_into_entry_tree(self, entry):
        self.entry_tree.insert('', 
                               'end', 
                               text=entry.name, 
                               values=(entry.artist,
                                       entry.genre,
                                       type(entry)))

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
        choose_file_button = Button(tab, text="Browse Files", 
                                    command=self.choose_file)
        choose_file_button.grid(row=2, column=2)

        self.is_file = BooleanVar()
        self.is_file_checkbox = Checkbutton(tab, text="Local File", variable=self.is_file)
        self.is_file_checkbox.grid(row=2, column=3)

        self.submit_button = Button(tab, text="Submit", command=self.add_entry)
        self.submit_button.grid(row=3, column=1)

    def add_link(self):
        artist = self.entry_artist.get()
        name = self.entry_name.get()
        url = self.entry_url.get()
        
        entry = self.catalog.add_link(url, artist=artist, name=name)
        self.insert_into_entry_tree(entry)

    def add_file(self):
        artist = self.entry_artist.get()
        name = self.entry_name.get()
        path = self.entry_url.get()

        entry = self.catalog.add_file(path, artist=artist, name=name)
        self.insert_into_entry_tree(entry)

    def add_entry(self):
        is_file = self.is_file.get()
        if is_file:
            self.add_file()
        else:
            self.add_link()

        for tf in [self.entry_artist, self.entry_name, self.entry_url]:
            tf.delete(0, 'end')
        

    def exit(self):
        sys.exit(0)

    def clear(self):
        shutil.rmtree(self.catalog.dir)
        self.exit()

if __name__ == '__main__':
    catalog = Catalog.getInstance('./catalog')
    root = Tk()
    my_gui = CatalogGUI(root, catalog)
    root.mainloop()

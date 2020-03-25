import sys
sys.path.append("..")

from Catalog import *

test_catalog = './tests/catalog'

def test_add_link():
    c = Catalog.getInstance(test_catalog)
    link = "https://tabs.ultimate-guitar.com/tab/red-hot-chili-peppers/under-the-bridge-tabs-3832"
    name = "Under the Bridge"
    artist = "Red Hot Chili Peppers"
    c.add_link(link=link, name=name, artist=artist)

    d = Catalog.getInstance(test_catalog)
    assert len(c.entries) == len(d.entries)

def test_add_file():
    c = Catalog.getInstance(test_catalog)
    path = '/home/alex/Downloads/Guitar/50ClassicalGuitarSolosinTablature.pdf'
    artist = "Howard Wallach"
    c.add_file(path, artist=artist)

    file_name = os.path.split(path)[1]
    assert os.path.exists(os.path.join(c.dir, artist, file_name))


    d = Catalog.getInstance(test_catalog)
    assert len(c.entries) == len(d.entries)

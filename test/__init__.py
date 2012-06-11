
"""Initialize the GottenGeography Nose test suite."""

from os import listdir, system, environ
from os.path import abspath, join
from random import random
from time import tzset

from gg.app import GottenGeography, startup
from gg.common import Gst, modified, selected
from gg.widgets import Widgets, MapView
from gg.build_info import PKG_DATA_DIR
from gg.xmlfiles import TrackFile
from gg.photos import Photograph
from gg.camera import Camera

DEMOFILES = [abspath(join(PKG_DATA_DIR, '..', 'demo', f))
             for f in listdir('./demo/')]

gui = GottenGeography(do_fade_in=False)
startup(gui)

def random_coord(maximum=180):
    """Generate a random number -maximum <= x <= maximum."""
    return (random() * maximum * 2) - maximum

def setup():
    """Start from a clean slate."""
    system('git checkout demo')
    environ['TZ'] = 'America/Edmonton'
    tzset()
    gui.open_files(DEMOFILES)

def teardown():
    """Clean it all up."""
    TrackFile.clear_all()
    for camera in Camera.cameras:
        camera.photos.clear()
    for photo in Photograph.instances.values():
        photo.destroy()
    Photograph.instances.clear()
    modified.clear()
    selected.clear()
    Widgets.loaded_photos.clear()
    system('git checkout demo')
    for key in Gst.list_keys():
        Gst.reset(key)


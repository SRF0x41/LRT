from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

import json
from Navigation import Navigation
from DataStore import DataStore
from datetime import datetime


class LRT(App):
    def build(self):
        app = App.get_running_app()
        data_dir = app.user_data_dir
        
        # Create label to display coordinates
        self.label = Label(
            text='Waiting for GPS...',
            size_hint=(.5, .5),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        

        # Create Navigation object and link it to the label
        self.nav_object = Navigation(self.update_label)
        self.nav_object.start()

        return self.label

    def update_label(self, **kwargs):
        
        """Called whenever GPS coordinates are updated."""
        setattr(self.label, 'text', f"{kwargs.get('lat')} {kwargs.get('lon')} ")
        
        # Get the working direcroty of the app
        app = App.get_running_app()
        data_dir = app.user_data_dir
        
        data = DataStore(data_dir)
        data.record_gps_data(**kwargs)
        data.retrieve_current_date_gps_data()
        
        
        data.see_full_path_data()

'''import sqlite3
from kivy.garden.mapview import MapView, MapSource
from kivy.app import App

class MBTilesProvider(MapSource):
    def __init__(self, mbtiles_path, **kwargs):
        super().__init__(**kwargs)
        self.mbtiles_path = mbtiles_path
        self.conn = sqlite3.connect(mbtiles_path)

    def get_tile(self, x, y, z):
        # MBTiles stores tiles with flipped y-axis
        flipped_y = (1 << z) - 1 - y
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT tile_data FROM tiles WHERE tile_column=? AND tile_row=? AND zoom_level=?",
            (x, flipped_y, z)
        )
        row = cursor.fetchone()
        if row:
            return row[0]  # raw PNG bytes
        return None

class OfflineMapApp(App):
    def build(self):
        tiles = MBTilesProvider(
            mbtiles_path="path/to/your_tiles.mbtiles",
            url="mbtiles",  # dummy url; MapView requires a url
            tile_size=256,
            cache_key="offline"
        )
        mapview = MapView(zoom=12, lat=37.7749, lon=-122.4194, map_source=tiles)
        return mapview

OfflineMapApp().run()
'''
        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
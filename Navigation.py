from plyer import gps

class Navigation:
    def __init__(self, update_callback=None):
        self.update_callback = update_callback
        self.gps_location = {}

        try:
            # on_location callback to call when recieving a new gps location 
            gps.configure(on_location=self.on_location)
        except NotImplementedError:
            import traceback
            traceback.print_exc()

    def start(self):
        gps.start(minTime=1000, minDistance=1)

    def stop(self):
        gps.stop()
        
    

    def on_location(self, **kwargs):
        '''kwargs dict
        {
            'lat': 37.7749,
            'lon': -122.4194,
            'alt': 15
        }'''
        # Save location and format nicely
        self.gps_location = kwargs
        lat = kwargs.get('lat', 0)
        lon = kwargs.get('lon', 0)
        coords_text = f"Latitude: {lat:.5f}\nLongitude: {lon:.5f}"

        print("GPS Location:", coords_text)

        # Update label via callback
        if self.update_callback:
            self.update_callback(**kwargs)


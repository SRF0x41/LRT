from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import json
from Navigation import Navigation
from DataStore import DataStore


class LRT(App):
    def build(self):
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

    def update_label(self, coords_text):
        """Called whenever GPS coordinates are updated."""
        setattr(self.label, 'text', coords_text)
        
        # Keep a log of all data locally
        app = App.get_running_app()
        data_dir = app.user_data_dir
        
        data = DataStore(data_dir)
        
        #data.test_store()
        #data.test_retrive()
        
        data.see_full_path()
        
        
        

        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
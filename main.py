from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


import json
from Navigation import Navigation
from DataStore import DataStore
from datetime import datetime


'''Control panel 
    
    Buttons
    Start Stop toggle data collections
    Print file directory
    
    Sync onboard data to Server
    '''

class LRT(App):
    
    
    def build(self):
        '''btn = Button(
            text="Click Me!",
            size_hint=(0.3, 0.2),  # width: 30%, height: 20% of parent
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # centered
        )'''
        layout = BoxLayout(orientation='vertical')  # Vertical stacking

        label_top = Label(text="Top Label")
        label_middle = Label(text="Middle Label")
        label_bottom = Label(text="Bottom Label")
        self.toggle_record_data = False
        toggle_gps_system = Button(
            text = "Toggle GPS",
            size_hint=(1, 0.4)
        )
        toggle_gps_system.bind(on_press=self.toggle_start_gps_system)
        layout.add_widget(toggle_gps_system)
        

        layout.add_widget(label_top)
        layout.add_widget(label_middle)
        layout.add_widget(label_bottom)
        
        return layout
        
        # Create label to display coordinates
        '''
        self.APP_PATH = self.user_data_dir  # get the app data dir
        self.data_store_obj = DataStore(self.APP_PATH)
        self.label = Label(
            text='Waiting for GPS...',
            size_hint=(.5, .5),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        
        Create Navigation object and link it to the label
        self.nav_object = Navigation(self.update_label)
        self.nav_object.start()

        return self.label'''

    def update_label(self, **kwargs):
        
        """Called whenever GPS coordinates are updated."""
        setattr(self.label, 'text', f"{kwargs.get('lat')} {kwargs.get('lon')} ")
        
        #self.data_store_obj.record_gps_data(**kwargs)
        #self.data_store_obj.retrieve_current_date_gps_data()
        #self.data_store_obj.see_full_path_data()
        
    def toggle_start_gps_system(self,instance):
        print(f"GPS system toggled {self.toggle_record_data}")
        instance.text = "Pressed"
        self.toggle_start_gps_system = not self.toggle_start_gps_system
        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
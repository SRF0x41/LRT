from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from pyobjus import autoclass, objc_str
from pyobjus.dylib_manager import load_framework
from kivy.uix.slider import Slider

import json
import requests
import os
from dotenv import load_dotenv

from Navigation import Navigation
from DataStore import DataStore
from datetime import datetime
#from DataBrocker import DataBrocker # Cryptography build isnt working
from DataLink import DataLink

class LRT(App):
    
    
    def build(self):
        #print(f"My env var {os.getenv("TEST_ENV")}")
        ''' ********** ALLOW APP TO RUN GPS UPDATES IN THE BACKGROUND ***********'''
        # Load the CoreLocation framework
        load_framework('/System/Library/Frameworks/CoreLocation.framework')

        # Grab Objective-C classes
        CLLocationManager = autoclass('CLLocationManager')
        CLLocationManagerDelegate = autoclass('NSObject')  # We'll subclass this later
        
        self.enable_background_location()

     
        ''' ---------- UI SET UP ----------'''
        layout = BoxLayout(
            orientation='vertical',
            padding=[10, 120, 10, 150],  # [left, top, right, bottom]
            spacing=10
        )

        self.moniter_text_buffer= []
        self.system_moniter = Label(
            text=(
                "Press start "
            ),
            font_name="RobotoMono-Regular",  # or another monospaced font
            halign="left",
            valign="top",
            text_size=(1000, None),  # ensures proper line wrapping
            size_hint=(1, 1)
        )

        layout.add_widget(self.system_moniter)
    
        self.toggle_record_data = False
        toggle_gps_system = Button(
            text = "Toggle GPS",
            size_hint=(1, 0.4)
        )
        toggle_gps_system.bind(on_press=self.toggle_start_gps_system)
        layout.add_widget(toggle_gps_system)
        
        
      
        # Hard delete everything locally
        delete_local_data_button = Button(
            text = 'Delete Local Data',
            size_hint=(1,0.4)
        )
        delete_local_data_button.bind(on_press = self.delete_local_data)
        #layout.add_widget(delete_local_data_button)
        
        
        
        
        ''' ********** GLOBAL POSITIONING SYSTEM RECORD START **********'''
        self.APP_PATH = self.user_data_dir  # get the app data dir
        self.data_store_obj = DataStore(self.APP_PATH)        
        self.nav_object = Navigation(self.nav_object_callback)
        
        self.data_store_obj.see_full_path_data()
        
        
        # self.data_store_obj.DELETE_EVERYTHING(self.APP_PATH)
        
        ''' ********** SERVER CONNECTION START ********** '''
        '''self.data_broker_obj = DataBrocker()
        
        # Push everything to server button
        push_local_data_to_server_button = Button(
            text='Push data to server',
            size_hint=(1,0.4)
        )
        push_local_data_to_server_button.bind(on_press=self.push_local_data_to_server)
        layout.add_widget(push_local_data_to_server_button)'''
        
        ''' ********** CLIENT SIDE DATA LINK ********** '''
        
        
        push_local_data_to_server_button = Button(
            text='Push data to server',
            size_hint=(1,0.4)
        )
        push_local_data_to_server_button.bind(on_press = self.push_local_data_to_server)
        layout.add_widget(push_local_data_to_server_button)
        
        return layout
    
    def on_slider_value_change(self, instance, value):
            # Update the label text with the new slider value
            self.value_label.text = f"Slider Value: {int(value)}"
    
    ''' Apple pyobjus magic function '''
    def enable_background_location(self):
        CLLocationManager = autoclass('CLLocationManager')
        self.location_manager = CLLocationManager.alloc().init()

        # Enable background updates
        self.location_manager.allowsBackgroundLocationUpdates = True
        self.location_manager.pausesLocationUpdatesAutomatically = False

        # Request permission
        self.location_manager.requestAlwaysAuthorization()

        # Start receiving updates
        self.location_manager.startUpdatingLocation()

        print("Background GPS tracking enabled.")

        
        
    def nav_object_callback(self,**kwargs):
        # Will record data kwargs data localy
        self.data_store_obj.record_gps_data(**kwargs)
        self.data_store_obj.retrieve_current_date_gps_data()
        self.data_store_obj.see_full_path_data()
        
        # Append Number of entries
        # self.append_text_line_moniter(f"{kwargs.get('lat')} {kwargs.get('lon')}")
        number_of_current_day_entries = self.data_store_obj.get_current_day_entries_count()
        self.append_text_line_moniter(f"Number of Entries: {number_of_current_day_entries}")
    
        
    def append_text_line_moniter(self, text):
        if len(self.moniter_text_buffer) > 15:
            self.moniter_text_buffer.pop(0)
        self.moniter_text_buffer.append(text)
        
        setattr(self.system_moniter, 'text', '\n'.join(self.moniter_text_buffer))
        
    def append_text_moniter(self, text_list):
        text_list_length = len(text_list)
        lines_to_remove = 15 - text_list_length
        
        if lines_to_remove <= 0:
            self.moniter_text_buffer = text_list[-15:]
        else:
            for i in range(lines_to_remove):
                self.moniter_text_buffer.pop(0)
            self.moniter_text_buffer.append(text_list)
            
        
        
    def toggle_start_gps_system(self, instance):
        self.toggle_record_data = not self.toggle_record_data
        state_text = 'GPS Data Collection On' if self.toggle_record_data else 'GPS Data Collection Off'
        print(f"GPS system toggled {state_text}")
        instance.text = state_text
        
        # Nav start and stop
        if self.toggle_record_data:
            self.nav_object.start()
        else:
            self.nav_object.stop()
    
    
    def delete_local_data(self,instance):
        self.data_store_obj.DELETE_EVERYTHING(self.APP_PATH)
        self.append_text_line_moniter("Local data deleted")
        
        
    ''' ********** SERVER UTILITIES ********** '''
    def push_local_data_to_server(self,instance):
        data_link_obj = DataLink()
        #data_link_obj.test_send()
      
        
        
        
        all_local_files_canon_paths = self.data_store_obj.get_all_file_canon_paths()
        print("ALL LOCAL FILES")
        print(all_local_files_canon_paths)
        
      

        # test send a file 
        
        data_link_obj.establish_connection_server()
        for i in range(3):
            data_link_obj.file_data_stream(all_local_files_canon_paths[i])
       
        
        data_link_obj.close_socket()
        
        
        
        
        
        
        
        
        
        
    
        
        
            
            
        

        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
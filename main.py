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
        ''' ---------- UI SET UP ----------'''
        layout = BoxLayout(
            orientation='vertical',
            padding=[10, 120, 10, 10],  # [left, top, right, bottom]
            spacing=10
        )

        self.moniter_text_buffer= []
        self.system_moniter = Label(
            text=(
                "SYSTEM BOOT SEQUENCE INITIATED\n"
                "------------------------------\n"
                "LOADING FLIGHT PARAMETERS...\n"
                "CHECKING NAVIGATION SENSORS...\n"
                "GYRO ALIGNMENT: COMPLETE\n"
                "FUEL PRESSURE: NOMINAL\n"
                "OXYGEN FLOW: STABLE\n"
                "------------------------------\n"
                "READY FOR MANUAL COMMAND INPUT\n"
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
        layout.add_widget(delete_local_data_button)
        
        
        ''' ********** GLOBAL POSITIONING SYSTEM RECORD START **********'''
        self.APP_PATH = self.user_data_dir  # get the app data dir
        self.data_store_obj = DataStore(self.APP_PATH)        
        self.nav_object = Navigation(self.nav_object_callback)
        
        self.data_store_obj.see_full_path_data()
        
        
        # self.data_store_obj.DELETE_EVERYTHING(self.APP_PATH)
        
        
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
        
        
    def nav_object_callback(self,**kwargs):
        # Will record data kwargs data localy
        self.data_store_obj.record_gps_data(**kwargs)
        self.data_store_obj.retrieve_current_date_gps_data()
        self.data_store_obj.see_full_path_data()
        
        self.append_text_line_moniter(f"{kwargs.get('lat')} {kwargs.get('lon')}")
        

        
    def append_text_line_moniter(self, text):
        if len(self.moniter_text_buffer) > 15:
            self.moniter_text_buffer.pop(0)
        self.moniter_text_buffer.append(text)
        
        setattr(self.system_moniter, 'text', '\n'.join(self.moniter_text_buffer))
        
        
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

        
if __name__ == '__main__':
    app = LRT()
    app.run()
        
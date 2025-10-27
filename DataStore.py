from datetime import datetime
import json
import os
import shutil

class DataStore:
    # 20 as a test
    MAX_DATA_ENTRIES_PER_FILE = 1000
    ''' Data structure
    
        date-folder
            -> date_timestamp - folder
                -> json with 1000 hits'''
                
                
    ''' CSV Compatible data storage
        isotime,lat,lon
        
        printed just as text lines'''
                
                
    def __init__(self, file_path):
        self.APP_FILE_PATH = file_path

        
        # Make a new folder of the current date, do nothing if it already exists
        self.current_datetime = datetime.now()
        year = self.current_datetime.year
        month = self.current_datetime.month
        day = self.current_datetime.day
        self.current_day_path = f"{self.APP_FILE_PATH}/{year}_{month}_{day}"
        os.makedirs(self.current_day_path, exist_ok=True)
        
        self.current_day_timestamp_file = None
        # Check to see if the current_day_path folder is empty
        if not os.listdir(self.current_day_path):
            # if empty create a new file file
            print(f"Current day {self.current_day_timestamp_file} is empty")
            self.create_new_timestamp_file()
        else:
            # Get the path of the last file created
            files = os.listdir(self.current_day_path)
            print(f"Files found in current day folder ")
            print(files)
            files = [f.removesuffix("_gps_data.txt") for f in files]
            # Creating a list of datetime objects
            dt_list = []
            for pulled_iso_label in files:
                try:
                    dt_obj = datetime.fromisoformat(pulled_iso_label)
                    dt_list.append(dt_obj)
                except ValueError:
                    print(f"Invalid file label {pulled_iso_label}")
                    
            # if no valid datetime files (other misc files) create a new file
            if len(dt_list) == 0:
                self.create_new_timestamp_file()
            else:
                # Get the latest (max)
                latest_created_file_timestamp_label = max(dt_list)
                print("Latest timestamp:", latest_created_file_timestamp_label.isoformat())
                
                # Set the current_day_timestamp file to the last one
                self.current_day_timestamp_file = f"{self.current_day_path}/{latest_created_file_timestamp_label.isoformat()}_gps_data.txt"
                
                # Check if its not <=500 lines
                number_gps_entries = None
                with open(self.current_day_timestamp_file, 'r') as fp:
                    number_gps_entries = len(fp.readlines())
                    
                if number_gps_entries >= DataStore.MAX_DATA_ENTRIES_PER_FILE:
                    # Create a fresh file
                    self.create_new_timestamp_file()

        
        # Variable that stores the last recorder json line so no duplicates are inputed
        self.last_recorded_gps_data_entry = None
        
        
    def record_gps_data(self, **kwargs):
        latitude = round(kwargs.get('lat'),5)
        longitude = round(kwargs.get('lon'),5)
        
        # Check if the file is full
        with open(self.current_day_timestamp_file, 'r') as fp:
            number_of_entries = len(fp.readlines())
        if number_of_entries >= DataStore.MAX_DATA_ENTRIES_PER_FILE:
            self.create_new_timestamp_file()
        
        with open(self.current_day_timestamp_file, "a") as f:
            f.write(f"{datetime.now().isoformat()},{latitude},{longitude}\n")
                
    
            
    def retrieve_current_date_gps_data(self):
        entries_on_file = self.get_number_of_entries(self.current_day_timestamp_file)
        if entries_on_file >= DataStore.MAX_DATA_ENTRIES_PER_FILE:
            # Create a fresh file
            self.current_day_timestamp_file = f"{self.current_day_path}/{datetime.now().isoformat()}_gps_data.txt"
            with open(self.current_day_timestamp_file, 'w'):
                pass
        with open(self.current_day_timestamp_file, 'r') as f:
            for line in f:
                if line.strip():
                    timestamp, lat, lon = line.strip().split(',')
                    print(timestamp, lat, lon)

            
    def create_new_timestamp_file(self):
        self.current_day_timestamp_file = f"{self.current_day_path}/{datetime.now().isoformat()}_gps_data.txt"
        with open(self.current_day_timestamp_file, 'w'):
                pass
        
    ''' Data management utilities '''
    
    def get_number_of_entries(self, file_path):
        with open(file_path, 'r') as fp:
            return len([line for line in fp if line.strip()])  # only count non-empty lines

    def see_full_path_data(self):
        for root, dirs, files in os.walk(self.APP_FILE_PATH):
            print(f"\nDirectory: {root}")
            for name in files:
                full_path = os.path.join(root, name)
                num_entries = self.get_number_of_entries(full_path)
                print(f"   ├── {name} ({num_entries} entries)")

    
    def delete_file(self, file_name):
        file_path_rm = f"{self.APP_FILE_PATH}/{file_name}"
        if os.path.exists(file_path_rm):
            os.remove(file_path_rm)
            print(f"{file_path_rm} deleted")
        else:
            print("File not found")



    def DELETE_EVERYTHING(self, start_path):
        """
        Nukes all files and folders starting at start_path.
        Use with care, see?
        """
        if not os.path.exists(start_path):
            print(f"Path does not exist: {start_path}")
            return

        for root, dirs, files in os.walk(start_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception as e:
                    print(f"Failed to delete file {name}: {e}")
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name))
                except Exception as e:
                    print(f"Failed to delete folder {name}: {e}")
        
        # Optionally delete the root folder itself
        try:
            shutil.rmtree(start_path)
            print(f"Deleted start folder: {start_path}")
        except Exception as e:
            print(f"Failed to delete start folder {start_path}: {e}")

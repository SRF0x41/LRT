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
            # Dont include files that that arent .csv
            for f in files:
                if not f.endswith('.csv'):
                    files.remove(f)
            print(files)
            files = [f.removesuffix("_gps_data.csv") for f in files]
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
                self.current_day_timestamp_file = f"{self.current_day_path}/{latest_created_file_timestamp_label.isoformat()}_gps_data.csv"
                
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
        # If its full create a new file
        if number_of_entries >= DataStore.MAX_DATA_ENTRIES_PER_FILE:
            self.create_new_timestamp_file()
        # Write to current file
        with open(self.current_day_timestamp_file, "a") as f:
            f.write(f"{datetime.now().isoformat()},{latitude},{longitude}\n")
                
                
    def retrieve_current_date_gps_data(self):
        # Prints the current entries of the current date file
        entries_on_file = self.get_number_of_entries(self.current_day_timestamp_file)
        if entries_on_file >= DataStore.MAX_DATA_ENTRIES_PER_FILE:
            # Create a fresh file
            self.current_day_timestamp_file = f"{self.current_day_path}/{datetime.now().isoformat()}_gps_data.csv"
            with open(self.current_day_timestamp_file, 'w'):
                pass
        with open(self.current_day_timestamp_file, 'r') as f:
            for line in f:
                if line.strip():
                    timestamp, lat, lon = line.strip().split(',')
                    print(timestamp, lat, lon)

            
    def create_new_timestamp_file(self):
        self.current_day_timestamp_file = f"{self.current_day_path}/{datetime.now().isoformat()}_gps_data.csv"
        with open(self.current_day_timestamp_file, 'w'):
                pass
            
    ''' Getters '''
    def get_current_day_entries_count(self):
        with open(self.current_day_timestamp_file, 'r') as fp:
            return len(fp.readlines())
        
    def walk_all_local_data(self):
        print(f"Test get all date dir")
        for root, dirs, files in os.walk(self.APP_FILE_PATH):
            print(f"Current directory: {root}")
            print(f"Subdirectories: {dirs}")
            print(f"Files: {files}\n")
            
    def get_all_dirs(self):
        ''' See all date folders starting from root '''
        entries = [f"{self.APP_FILE_PATH}/{dir}" for dir in os.listdir(self.APP_FILE_PATH) ]
        return(entries)
        
        
    def get_all_file_names_from_dir(self, root_name):
        ''' Get all'''
        files = [file for file in os.listdir(f"{self.APP_FILE_PATH}/{root_name}")]
        return files
    
    def get_all_file_names_from_path(self, full_file_path):
        files = [file for file in os.listdir(full_file_path)]
        return files
    
    def get_all_file_paths_from_path(self,full_file_path):
        files = [f"{full_file_path}/{file}" for file in os.listdir(full_file_path)]
        return files
    
    def get_file_data_bytes(self,full_path):
        '''with open("photo.jpg", "rb") as f:
            data = f.read(1024)  # read 1 KB'''
            
        # Example see readable csvs
        with open(full_path, 'r') as f:
            for line in f:
                print(line)
            
        """ with open(full_path, 'rb') as f:
            chunk_1k = f.read(1024)"""
            
            
    def get_all_file_canon_paths(self):
        list_of_all_files = []
        print(f"Test get all date dir")
        for root, dirs, files in os.walk(self.APP_FILE_PATH):
            if files:
                
                for f in files:
                    list_of_all_files.append(f"{root}/{f}")
                
                
            print(f"Current directory: {root}")
            print(f"Subdirectories: {dirs}")
            print(f"Files: {files}\n")
            
        return list_of_all_files
    
    
    def get_all_file_relative_paths(self):
        list_of_all_files = []
        print(f"Test get all date dir")
        for root, dirs, files in os.walk(self.APP_FILE_PATH):
            root = root.split(os.sep)
            root = os.sep.join(root[9:])
            if files:
                for f in files:
                    list_of_all_files.append(f"{root}/{f}")      
                
                
            print(f"Current directory: {root}")
            print(f"Subdirectories: {dirs}")
            print(f"Files: {files}\n")
            
        return list_of_all_files
    
        
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

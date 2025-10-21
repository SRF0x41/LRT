import datetime
import json
import os

class DataStore:
    def __init__(self, file_path):
        self.APP_FILE_PATH = file_path
        self.test_json_path = f"{self.APP_FILE_PATH}/test_json_data.jsons"
        
        # Make a new folder of the current date, do nothing if it already exists
        self.current_datetime = datetime.datetime.now()
        year = self.current_datetime.year
        month = self.current_datetime.month
        day = self.current_datetime.day
        
        # Create a current folder for date
        self.current_path = f"{self.APP_FILE_PATH}/{year}_{month}_{day}"
        os.makedirs(self.current_path, exist_ok=True)
        
        # Create a current file in the current folder for jsons
        self.CURRENT_DATE_FILE = f"{self.current_path}/{year}_{month}_{day}_gps_data.jsons"
        
        print(self.current_path)
        
        
    def record_gps_data(self, **kwargs):
        latitude = round(kwargs.get('lat'),5)
        longitude = round(kwargs.get('lon'),5)
        current_date_gps_data_entry = {self.current_datetime.isoformat() : {'lat':latitude, 'lon':longitude}}
        
        with open(self.CURRENT_DATE_FILE, "a") as f:
            json.dump(current_date_gps_data_entry, f)
            f.write("\n")
            
    def retrieve_current_date_gps_data(self):
        with open(self.CURRENT_DATE_FILE, 'r') as f:
            for line in f:
                if line.strip():  # skip blanks
                    entry = json.loads(line)
                    print(entry)

            
        
    def test_store(self):
        # store data
        data = {'items': ['apple', 'banana'], 'count': 2, 'custom_rand': 1234}
        with open(self.test_json_path, 'w') as f:
            json.dump(data, f)
            
    def test_retrieve(self):
        # Retrieve data
        with open(self.test_json_path, 'r') as f:
            loaded_data = json.load(f)
        print(loaded_data['items'])  # Output: ['apple', 'banana']
        print(loaded_data['custom_rand'])
        
    ''' Data management utilities '''
    def see_full_path_data(self):
        for item in os.listdir(self.APP_FILE_PATH):
            print(item)
    
    def delete_file(self, file_name):
        file_path_rm = f"{self.APP_FILE_PATH}/{file_name}"
        if os.path.exists(file_path_rm):
            os.remove(file_path_rm)
            print(f"{file_path_rm} deleted")
        else:
            print("File not found")

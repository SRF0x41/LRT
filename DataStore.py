from datetime import datetime
import json
import os

class DataStore:
    def __init__(self, file_path):
        self.file_path = file_path
        self.test_json_path = f"{file_path}/test_json_data.jsons"
        
    
        
    def test_store(self):
        # store data
        data = {'items': ['apple', 'banana'], 'count': 2, 'custom_rand':1234}
        with open(self.test_json_path, 'w') as f:
            json.dump(data, f)
            
    def test_retrive(self):
         # Retrieve data
        with open(self.test_json_path, 'r') as f:
            loaded_data = json.load(f)
        print(loaded_data['items']) # Output: ['apple', 'banana']
        print(loaded_data['custom_rand'])
        
        
    ''' Data management utilities '''
    def see_full_path_data(self):
        for item in os.listdir(self.file_path):
            print(item)
    
    def delete_file(self, file_name):
        file_path_rm = f"{self.file_path}/{file_name}"
        if os.path.exists(file_path_rm):
            os.remove(file_path_rm)
            print(f"{file_path_rm} Deleted")
        else:
            print("file not found")
    
    
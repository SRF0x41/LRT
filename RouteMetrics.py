import os
from datetime import datetime


class RouteMetrics():
    def __init__(self, root_path):
        # Check if theres already a route metrics file
        self.APP_ROOT_PATH = root_path
        # elf.current_day_path = f"{self.APP_FILE_PATH}/{year}_{month}_{day}"
        # os.makedirs(self.current_day_path, exist_ok=True)
        year = self.current_datetime.year
        month = self.current_datetime.month
        day = self.current_datetime.day
        self.__current_route_metrics_file_path = f"{self.APP_ROOT_PATH}/{year}_{month}_{day}_route_metrics_data.json"
        
        # Check if there is not a current route metrics file
        if not os.path.exists(self.__current_route_metrics_file_path):
            #  Create a file if it doesnt exist
            with open(self.current_day_timestamp_file, 'w'):
                    pass
        
    def hard_sum_gps_time_distance(self):
        pass
        
    def get_total_route_average_speed(self):
        pass
    
    
    
    
    
        
        
    
    
    
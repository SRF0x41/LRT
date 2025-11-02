import socket
class DataLink():
    def __init__(self):
        try:
            hostname = socket.gethostname()
            self.lan_ip_address = socket.gethostbyname(hostname)
            print(f"Lan ip adress: {self.lan_ip_address}")
        except socket.error as e:
            print(f"Error getting LAN IP by hostname: {e}")
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.lan_ip_address, 5000))  # lan ip
        
        

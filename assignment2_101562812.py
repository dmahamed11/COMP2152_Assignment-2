import socket
import threading
import sqlite3

# Q1: Base Class (Inheritance requirement)
class Scanner:
    def __init__(self, target):
        self.target = target

# Q2: PortScanner Class inheriting from Scanner
class PortScanner(Scanner):
    def __init__(self, target, start_port, end_port):
        super().__init__(target)
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.lock = threading.Lock() # Prevents threads from overlapping

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            # result 0 means the port is open
            result = sock.connect_ex((self.target, port))
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                print(f"  [+] Port {port} is OPEN on {self.target}")
        except Exception as e:
            pass # Silently skip errors during scanning
        finally:
            sock.close()

    def run_threads(self):
        print(f"--- Starting scan on {self.target} ---")
        threads = []
        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()
        
        # Wait for all threads to finish before moving on
        for t in threads:
            t.join()

# Q3: SQLite Database Function
def save_to_db(target, open_ports):
    # Connects to results.db (creates it if it doesn't exist)
    conn = sqlite3.connect('results_101562812.db')
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''CREATE TABLE IF NOT EXISTS scan_results 
                      (target TEXT, open_ports TEXT, scan_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Insert the data (converting the list of ports to a string)
    ports_str = ", ".join(map(str, open_ports)) if open_ports else "None"
    cursor.execute("INSERT INTO scan_results (target, open_ports) VALUES (?, ?)", (target, ports_str))
    
    conn.commit()
    conn.close()
    print(f"--- Results saved to database for {target} ---")

# Main Execution block
if __name__ == "__main__":
    # Example usage for testing
    my_target = "127.0.0.1" 
    scanner = PortScanner(my_target, 75, 85)
    scanner.run_threads()
    
    # Save the results
    save_to_db(my_target, scanner.open_ports)

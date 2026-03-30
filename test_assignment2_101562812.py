import unittest
# This imports your PortScanner class from your main file
from assignment2_101562812 import PortScanner, Scanner

class TestPortScanner(unittest.TestCase):
    
    # Test 1: Verify the constructor sets the target correctly
    def test_init_target(self):
        scanner = PortScanner("127.0.0.1", 80, 85)
        self.assertEqual(scanner.target, "127.0.0.1")

    # Test 2: Verify the start and end ports are stored properly
    def test_port_range(self):
        scanner = PortScanner("127.0.0.1", 20, 25)
        self.assertEqual(scanner.start_port, 20)
        self.assertEqual(scanner.end_port, 25)

    # Test 3: Ensure the open_ports list starts empty
    def test_empty_results_on_start(self):
        scanner = PortScanner("127.0.0.1", 443, 443)
        self.assertEqual(len(scanner.open_ports), 0)

    # Test 4: Check if inheritance is working (OOP Requirement)
    def test_inheritance_check(self):
        scanner = PortScanner("127.0.0.1", 80, 80)
        # This confirms PortScanner IS a type of Scanner
        self.assertTrue(isinstance(scanner, Scanner))

if __name__ == '__main__':
    unittest.main()

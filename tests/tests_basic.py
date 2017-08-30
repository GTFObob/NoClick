import unittest
from app import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        pass
    
    def test_home_status_code(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)
        

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()
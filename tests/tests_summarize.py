import unittest
from app import app
import json

TEST_URL = "https://www.thestar.com/news/world/2017/08/27/at-least-two-dead-as-harvey-causes-catastrophic-flooding-in-southeastern-texas.html"

def json_response(response):
    assert response.status_code == 200
    return json.loads(response.data)

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        pass
    
    def test_summarize_empty_status_code(self):
        result = self.app.get("/summarize")
        self.assertEqual(result.status_code, 400)
    
    def test_summarize_empty_url(self):
        result = self.app.get("/summarize?url=")
        self.assertEqual(result.status_code, 400)
    
    def test_summarize_gibberish(self):
        result = self.app.get("/summarize?url=owfijdfisdnjsdnj")
        self.assertEqual(result.status_code, 403)
    
    def test_summarize_proper_http(self):
        result = self.app.get("/summarize?url=http://www.google.com")
        self.assertEqual(result.status_code, 200)
    
    def test_summarize_proper_https(self):
        result = self.app.get("/summarize?url=%s" % TEST_URL)
        self.assertEqual(result.status_code, 200)

    def test_summarize_proper_no_http(self):
        result = self.app.get("/summarize?url=www.google.com")
        self.assertEqual(result.status_code, 200)
    
    def test_summarize_high_num(self):
        result = self.app.get("/summarize?url=%s&num=5555" % TEST_URL)
        json_result = json_response(result)
        self.assertEqual(len(json_result["content"]), 10)

    def test_summarize_neg_num(self):
        result = self.app.get("/summarize?url=%s&num=-5000" % TEST_URL)
        json_result = json_response(result)
        self.assertEqual(len(json_result["content"]), 5)
    
    def test_summarize_low_num(self):
        result = self.app.get("/summarize?url=%s&num=0" % TEST_URL)
        json_result = json_response(result)
        self.assertEqual(len(json_result["content"]), 5)

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()
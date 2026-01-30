import sys
import os
import unittest
import json
import logging

# Add project root to path
sys.path.append(os.getcwd())

from app.adapter.app import app

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        """Test that the UI loads."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Xray Test Generator', response.data)

    def test_generation_api(self):
        """Test the /generate endpoint with real Ollama."""
        print("Testing /generate endpoint (this calls actual LLM)...")
        input_data = {
            "requirements": "Verify search function. User enters text, clicks search, results appear."
        }
        response = self.app.post('/generate', 
                                 data=json.dumps(input_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        # Verify structure
        self.assertIn('test_cases', data)
        self.assertIsInstance(data['test_cases'], list)
        self.assertGreater(len(data['test_cases']), 0)
        
        # Check first item keys
        first_case = data['test_cases'][0]
        self.assertIn('summary', first_case) # parser normalizes to lowercase keys in json?
        # Wait, the parser output depends on how I implemented ResponseParser.
        # Let's check the keys in the response parser again. 
        # ResponseParser.parse_json returns dict as is from LLM.
        # Prompt says "summary", "action", etc.
        
        possible_keys = ['summary', 'Test Summary', 'Test_Summary']
        found_key = any(k in first_case for k in possible_keys)
        self.assertTrue(found_key, f"Keys found: {first_case.keys()}")

    def test_download_csv(self):
        """Test the CSV download logic."""
        test_cases = [
            {"summary": "Test 1", "action": "Do X", "expected_result": "Y", "priority": "High"}
        ]
        response = self.app.post('/download',
                                 data=json.dumps({'test_cases': test_cases}),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        content = response.data.decode('utf-8')
        self.assertIn('Test Summary,Action,Expected Result,Priority', content)
        self.assertIn('Test 1,Do X,Y,High', content)

if __name__ == '__main__':
    unittest.main()

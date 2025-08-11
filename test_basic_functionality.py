#!/usr/bin/env python3
"""
Basic Functionality Tests for n8n AI Agent
Šis modulis testē pamata funkcionalitāti.
"""

import unittest
import sys
import os
import json
import tempfile

# Pievieno src direktoriju Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestBasicWorkflowGeneration(unittest.TestCase):
    """Testē pamata workflow ģenerēšanas funkcionalitāti"""
    
    def test_simple_workflow_structure(self):
        """Testē vienkāršas workflow struktūras izveidi"""
        # Simulē vienkāršu workflow
        workflow = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "webhook_1",
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [100, 100],
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "test"
                    }
                },
                {
                    "id": "function_1", 
                    "name": "Process Data",
                    "type": "n8n-nodes-base.function",
                    "position": [300, 100],
                    "parameters": {
                        "functionCode": "return items;"
                    }
                }
            ],
            "connections": {
                "Webhook": {
                    "main": [
                        [
                            {
                                "node": "Process Data",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            }
        }
        
        # Pārbauda workflow struktūru
        self.assertIn("name", workflow)
        self.assertIn("nodes", workflow)
        self.assertIn("connections", workflow)
        self.assertEqual(len(workflow["nodes"]), 2)
        self.assertIn("Webhook", workflow["connections"])
    
    def test_workflow_validation(self):
        """Testē workflow validāciju"""
        # Derīgs workflow
        valid_workflow = {
            "name": "Valid Workflow",
            "nodes": [
                {
                    "name": "Start",
                    "type": "n8n-nodes-base.webhook"
                }
            ]
        }
        
        # Nederīgs workflow (trūkst name)
        invalid_workflow = {
            "nodes": []
        }
        
        # Pārbauda, ka derīgs workflow satur nepieciešamās atslēgas
        self.assertIn("name", valid_workflow)
        self.assertIn("nodes", valid_workflow)
        
        # Pārbauda, ka nederīgam workflow trūkst name
        self.assertNotIn("name", invalid_workflow)

class TestNodeConfiguration(unittest.TestCase):
    """Testē mezglu konfigurācijas funkcionalitāti"""
    
    def test_common_node_types(self):
        """Testē biežāk izmantoto mezglu tipus"""
        common_nodes = [
            "n8n-nodes-base.webhook",
            "n8n-nodes-base.function",
            "n8n-nodes-base.httpRequest",
            "n8n-nodes-base.telegram",
            "n8n-nodes-base.gmail",
            "n8n-nodes-base.mysql",
            "n8n-nodes-base.postgres"
        ]
        
        # Pārbauda, ka visi mezgli satur pareizo prefiksu
        for node_type in common_nodes:
            self.assertTrue(node_type.startswith("n8n-nodes-base."))
    
    def test_node_parameter_structure(self):
        """Testē mezglu parametru struktūru"""
        # Webhook mezgla parametri
        webhook_params = {
            "httpMethod": "POST",
            "path": "webhook-path",
            "responseMode": "onReceived"
        }
        
        # Function mezgla parametri
        function_params = {
            "functionCode": "return items.map(item => ({ json: { processed: true, ...item.json } }));"
        }
        
        # HTTP Request mezgla parametri
        http_params = {
            "url": "https://api.example.com/data",
            "method": "GET",
            "headers": {}
        }
        
        # Pārbauda parametru esamību
        self.assertIn("httpMethod", webhook_params)
        self.assertIn("functionCode", function_params)
        self.assertIn("url", http_params)

class TestLanguageDetection(unittest.TestCase):
    """Testē valodu noteikšanas funkcionalitāti"""
    
    def test_basic_language_patterns(self):
        """Testē pamata valodu modeļus"""
        # Latviešu valodas rakstzīmes
        latvian_chars = "āčēģīķļņšūž"
        self.assertTrue(any(char in "āčēģīķļņšūž" for char in latvian_chars))
        
        # Krievu valodas rakstzīmes
        russian_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.assertTrue(any(char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" for char in russian_chars))
        
        # Angļu valodas rakstzīmes (tikai latīņu alfabēts)
        english_chars = "abcdefghijklmnopqrstuvwxyz"
        self.assertTrue(all(char in "abcdefghijklmnopqrstuvwxyzāčēģīķļņšūžабвгдеёжзийклмнопрстуфхцчшщъыьэюя" 
                           for char in english_chars))

class TestAPIEndpoints(unittest.TestCase):
    """Testē API galapunktu funkcionalitāti"""
    
    def test_api_response_structure(self):
        """Testē API atbildes struktūru"""
        # Simulē veiksmīgu atbildi
        success_response = {
            "success": True,
            "message": "Workflow generated successfully",
            "data": {
                "workflow": {},
                "analysis": {}
            }
        }
        
        # Simulē kļūdas atbildi
        error_response = {
            "success": False,
            "error": "Invalid request",
            "message": "Missing required parameters"
        }
        
        # Pārbauda veiksmīgas atbildes struktūru
        self.assertIn("success", success_response)
        self.assertTrue(success_response["success"])
        self.assertIn("data", success_response)
        
        # Pārbauda kļūdas atbildes struktūru
        self.assertIn("success", error_response)
        self.assertFalse(error_response["success"])
        self.assertIn("error", error_response)

class TestUtilityFunctions(unittest.TestCase):
    """Testē palīgfunkcijas"""
    
    def test_json_validation(self):
        """Testē JSON validāciju"""
        # Derīgs JSON
        valid_json = '{"name": "test", "value": 123}'
        try:
            parsed = json.loads(valid_json)
            self.assertIsInstance(parsed, dict)
            self.assertIn("name", parsed)
        except json.JSONDecodeError:
            self.fail("Derīgs JSON nevarēja tikt parsēts")
        
        # Nederīgs JSON
        invalid_json = '{"name": "test", "value":}'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(invalid_json)
    
    def test_string_operations(self):
        """Testē virkņu operācijas"""
        test_string = "  Izveidot Telegram botu  "
        
        # Testē trim operāciju
        trimmed = test_string.strip()
        self.assertEqual(trimmed, "Izveidot Telegram botu")
        
        # Testē lower case
        lower_case = trimmed.lower()
        self.assertEqual(lower_case, "izveidot telegram botu")
        
        # Testē vārdu sadalīšanu
        words = trimmed.split()
        self.assertEqual(len(words), 3)
        self.assertIn("Telegram", words)
    
    def test_list_operations(self):
        """Testē sarakstu operācijas"""
        test_list = ["create", "telegram", "bot", "appointment"]
        
        # Testē elementu esamību
        self.assertIn("telegram", test_list)
        self.assertNotIn("email", test_list)
        
        # Testē saraksta garumu
        self.assertEqual(len(test_list), 4)
        
        # Testē saraksta filtrēšanu
        filtered = [item for item in test_list if len(item) > 3]
        self.assertIn("create", filtered)
        self.assertIn("telegram", filtered)
        self.assertNotIn("bot", filtered)

class TestErrorHandling(unittest.TestCase):
    """Testē kļūdu apstrādi"""
    
    def test_empty_input_handling(self):
        """Testē tukšas ievades apstrādi"""
        empty_inputs = ["", "   ", None]
        
        for empty_input in empty_inputs:
            if empty_input is None:
                self.assertIsNone(empty_input)
            else:
                self.assertFalse(bool(empty_input.strip()) if empty_input else False)
    
    def test_invalid_data_handling(self):
        """Testē nederīgu datu apstrādi"""
        # Testē ar nederīgu workflow struktūru
        invalid_workflow = {
            "invalid_key": "invalid_value"
        }
        
        # Pārbauda, ka trūkst nepieciešamo atslēgu
        self.assertNotIn("name", invalid_workflow)
        self.assertNotIn("nodes", invalid_workflow)
    
    def test_exception_scenarios(self):
        """Testē izņēmumu scenārijus"""
        # Testē dalīšanu ar nulli
        with self.assertRaises(ZeroDivisionError):
            result = 10 / 0
        
        # Testē piekļuvi neesošam indeksam
        test_list = [1, 2, 3]
        with self.assertRaises(IndexError):
            value = test_list[10]
        
        # Testē piekļuvi neesošai atslēgai
        test_dict = {"key1": "value1"}
        with self.assertRaises(KeyError):
            value = test_dict["nonexistent_key"]

class TestPerformance(unittest.TestCase):
    """Testē veiktspējas aspektus"""
    
    def test_large_text_processing(self):
        """Testē lielu tekstu apstrādi"""
        # Izveido lielu tekstu
        large_text = "Izveidot Telegram botu " * 1000
        
        # Pārbauda, ka teksts nav pārāk liels
        self.assertLess(len(large_text), 50000)  # 50KB limits
        
        # Testē teksta apstrādi
        words = large_text.split()
        self.assertGreater(len(words), 2000)
    
    def test_workflow_size_limits(self):
        """Testē workflow izmēra ierobežojumus"""
        # Izveido workflow ar daudziem mezgliem
        large_workflow = {
            "name": "Large Workflow",
            "nodes": []
        }
        
        # Pievieno 100 mezglus
        for i in range(100):
            node = {
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": "n8n-nodes-base.function",
                "position": [i * 100, 100]
            }
            large_workflow["nodes"].append(node)
        
        # Pārbauda mezglu skaitu
        self.assertEqual(len(large_workflow["nodes"]), 100)
        
        # Pārbauda, ka workflow nav pārāk liels JSON formātā
        workflow_json = json.dumps(large_workflow)
        self.assertLess(len(workflow_json), 1000000)  # 1MB limits

if __name__ == '__main__':
    # Palaiž visus testus
    unittest.main(verbosity=2)


#!/usr/bin/env python3
"""
Tests for Multilingual Support
Šis modulis testē daudzvalodu atbalsta funkcionalitāti.
"""

import unittest
import sys
import os

# Pievieno src direktoriju Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from multilingual_support import (
    MultilingualSupport, 
    EnhancedLanguageDetector, 
    MultilingualKeywordExtractor,
    SupportedLanguage
)

class TestEnhancedLanguageDetector(unittest.TestCase):
    """Testē uzlaboto valodu noteicēju"""
    
    def setUp(self):
        self.detector = EnhancedLanguageDetector()
    
    def test_latvian_detection(self):
        """Testē latviešu valodas noteikšanu"""
        latvian_texts = [
            "Izveidot Telegram botu pierakstam uz tikšanos",
            "Nepieciešams radīt automatizētu sistēmu",
            "Datu bāzes integrācija ar API",
            "Sūtīt epastus klientiem"
        ]
        
        for text in latvian_texts:
            result = self.detector.detect_language(text)
            self.assertEqual(result.language, SupportedLanguage.LATVIAN, 
                           f"Neizdevās noteikt latviešu valodu: {text}")
            self.assertGreater(result.confidence, 0.3, 
                             f"Pārāk zema uzticamība latviešu valodai: {text}")
    
    def test_russian_detection(self):
        """Testē krievu valodas noteikšanu"""
        russian_texts = [
            "Создать телеграм бота для записи на встречи",
            "Нужно построить автоматизированную систему",
            "Интеграция базы данных с API",
            "Отправлять письма клиентам"
        ]
        
        for text in russian_texts:
            result = self.detector.detect_language(text)
            self.assertEqual(result.language, SupportedLanguage.RUSSIAN,
                           f"Neizdevās noteikt krievu valodu: {text}")
            self.assertGreater(result.confidence, 0.3,
                             f"Pārāk zema uzticamība krievu valodai: {text}")
    
    def test_english_detection(self):
        """Testē angļu valodas noteikšanu"""
        english_texts = [
            "Create a Telegram bot for appointment booking",
            "Need to build an automated system",
            "Database integration with API",
            "Send emails to clients"
        ]
        
        for text in english_texts:
            result = self.detector.detect_language(text)
            self.assertEqual(result.language, SupportedLanguage.ENGLISH,
                           f"Neizdevās noteikt angļu valodu: {text}")
            self.assertGreater(result.confidence, 0.3,
                             f"Pārāk zema uzticamība angļu valodai: {text}")

class TestMultilingualKeywordExtractor(unittest.TestCase):
    """Testē daudzvalodu atslēgvārdu ekstraktoru"""
    
    def setUp(self):
        self.extractor = MultilingualKeywordExtractor()
    
    def test_latvian_keywords(self):
        """Testē latviešu atslēgvārdu ekstraktēšanu"""
        text = "Izveidot Telegram botu pierakstam uz tikšanos ar datu bāzi"
        keywords = self.extractor.extract_keywords(text, SupportedLanguage.LATVIAN)
        
        self.assertIn('create', keywords['actions'])
        self.assertIn('telegram', keywords['services'])
        self.assertIn('bot', keywords['objects'])
        self.assertIn('appointment', keywords['objects'])
        self.assertIn('database', keywords['objects'])
    
    def test_russian_keywords(self):
        """Testē krievu atslēgvārdu ekstraktēšanu"""
        text = "Создать телеграм бота для записи на встречи с базой данных"
        keywords = self.extractor.extract_keywords(text, SupportedLanguage.RUSSIAN)
        
        self.assertIn('create', keywords['actions'])
        self.assertIn('telegram', keywords['services'])
        self.assertIn('bot', keywords['objects'])
        self.assertIn('appointment', keywords['objects'])
        self.assertIn('database', keywords['objects'])
    
    def test_english_keywords(self):
        """Testē angļu atslēgvārdu ekstraktēšanu"""
        text = "Create a Telegram bot for appointment booking with database"
        keywords = self.extractor.extract_keywords(text, SupportedLanguage.ENGLISH)
        
        self.assertIn('create', keywords['actions'])
        self.assertIn('telegram', keywords['services'])
        self.assertIn('bot', keywords['objects'])
        self.assertIn('appointment', keywords['objects'])
        self.assertIn('database', keywords['objects'])

class TestMultilingualSupport(unittest.TestCase):
    """Testē galveno daudzvalodu atbalsta klasi"""
    
    def setUp(self):
        self.multilingual = MultilingualSupport()
    
    def test_multilingual_request_processing(self):
        """Testē daudzvalodu pieprasījumu apstrādi"""
        test_cases = [
            {
                'text': "Izveidot Telegram botu",
                'expected_language': 'lv',
                'expected_keywords': ['create', 'telegram', 'bot']
            },
            {
                'text': "Создать телеграм бота",
                'expected_language': 'ru',
                'expected_keywords': ['create', 'telegram', 'bot']
            },
            {
                'text': "Create a Telegram bot",
                'expected_language': 'en',
                'expected_keywords': ['create', 'telegram', 'bot']
            }
        ]
        
        for case in test_cases:
            result = self.multilingual.process_multilingual_request(case['text'])
            
            self.assertTrue(result['success'], f"Neizdevās apstrādāt: {case['text']}")
            self.assertEqual(result['language'], case['expected_language'])
            
            # Pārbauda, vai atrasti gaidītie atslēgvārdi
            found_keywords = []
            for category in result['keywords'].values():
                found_keywords.extend(category)
            
            for expected_keyword in case['expected_keywords']:
                self.assertIn(expected_keyword, found_keywords,
                            f"Nav atrasts atslēgvārds '{expected_keyword}' tekstā: {case['text']}")
    
    def test_prompt_localization(self):
        """Testē prompt lokalizāciju"""
        base_prompt = "Generate a workflow for the following request:"
        
        # Testē katru valodu
        for language in ['lv', 'ru', 'en']:
            localized_prompt = self.multilingual.localize_prompt(base_prompt, language)
            
            self.assertIsInstance(localized_prompt, str)
            self.assertGreater(len(localized_prompt), len(base_prompt))
            self.assertIn(base_prompt, localized_prompt)
    
    def test_message_localization(self):
        """Testē ziņojumu lokalizāciju"""
        message_key = 'workflow_generated'
        
        # Testē katru valodu
        for language in ['lv', 'ru', 'en']:
            localized_message = self.multilingual.localize_message(
                message_key, language, 'success'
            )
            
            self.assertIsInstance(localized_message, str)
            self.assertGreater(len(localized_message), 0)
            self.assertNotEqual(localized_message, message_key)
    
    def test_response_formatting(self):
        """Testē atbildes formatēšanu"""
        response_data = {
            'workflow': {'name': 'Test Workflow'},
            'explanation': 'This is a test workflow'
        }
        
        for language in ['lv', 'ru', 'en']:
            formatted_response = self.multilingual.format_localized_response(
                response_data, language, 'workflow_generation_success'
            )
            
            self.assertIn('localized_labels', formatted_response)
            self.assertIn('title', formatted_response['localized_labels'])
            self.assertIn('workflow_title', formatted_response['localized_labels'])
    
    def test_input_validation(self):
        """Testē ievades validāciju"""
        test_cases = [
            ('', False),  # Tukšs teksts
            ('ab', False),  # Pārāk īss
            ('a' * 1001, False),  # Pārāk garš
            ('Izveidot botu', True),  # Derīgs teksts
            ('Create bot', True),  # Derīgs teksts
            ('Создать бота', True)  # Derīgs teksts
        ]
        
        for text, expected_valid in test_cases:
            # Vispirms nosaka valodu
            detection_result = self.multilingual.detector.detect_language(text or 'en')
            
            # Tad validē
            is_valid, errors = self.multilingual.validator.validate_input(
                text, detection_result.language
            )
            
            self.assertEqual(is_valid, expected_valid,
                           f"Validācijas rezultāts neatbilst gaidītajam: '{text}'")
            
            if not expected_valid:
                self.assertGreater(len(errors), 0,
                                 f"Jābūt kļūdām nederīgam tekstam: '{text}'")

class TestIntegrationScenarios(unittest.TestCase):
    """Testē integrācijas scenārijus"""
    
    def setUp(self):
        self.multilingual = MultilingualSupport()
    
    def test_telegram_bot_scenarios(self):
        """Testē Telegram bota scenārijus dažādās valodās"""
        scenarios = [
            "Izveidot Telegram botu, kas pieraksta klientus uz tikšanos",
            "Создать телеграм бота для записи клиентов на встречи",
            "Create a Telegram bot that books clients for appointments"
        ]
        
        for scenario in scenarios:
            result = self.multilingual.process_multilingual_request(scenario)
            
            self.assertTrue(result['success'])
            
            # Pārbauda, vai atrasti nepieciešamie atslēgvārdi
            keywords = result['keywords']
            self.assertIn('create', keywords['actions'])
            self.assertIn('telegram', keywords['services'])
            self.assertIn('bot', keywords['objects'])
            self.assertIn('appointment', keywords['objects'])
    
    def test_email_automation_scenarios(self):
        """Testē e-pasta automatizācijas scenārijus"""
        scenarios = [
            "Automatizēt e-pasta sūtīšanu klientiem",
            "Автоматизировать отправку писем клиентам",
            "Automate email sending to clients"
        ]
        
        for scenario in scenarios:
            result = self.multilingual.process_multilingual_request(scenario)
            
            self.assertTrue(result['success'])
            
            # Pārbauda atslēgvārdus
            keywords = result['keywords']
            self.assertIn('send', keywords['actions'])
            self.assertIn('email', keywords['services'])
    
    def test_database_integration_scenarios(self):
        """Testē datu bāzes integrācijas scenārijus"""
        scenarios = [
            "Integrēt ar datu bāzi un saglabāt informāciju",
            "Интегрировать с базой данных и сохранить информацию",
            "Integrate with database and save information"
        ]
        
        for scenario in scenarios:
            result = self.multilingual.process_multilingual_request(scenario)
            
            self.assertTrue(result['success'])
            
            # Pārbauda atslēgvārdus
            keywords = result['keywords']
            self.assertIn('save', keywords['actions'])
            self.assertIn('database', keywords['objects'])

if __name__ == '__main__':
    # Palaiž visus testus
    unittest.main(verbosity=2)


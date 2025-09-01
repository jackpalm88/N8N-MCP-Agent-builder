#!/usr/bin/env python3
"""
Enhanced Multilingual Support for n8n AI Agent
Šis modulis nodrošina uzlabotu daudzvalodu atbalstu.
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SupportedLanguage(Enum):
    """Atbalstītās valodas"""
    LATVIAN = "lv"
    RUSSIAN = "ru"
    ENGLISH = "en"

@dataclass
class LanguageDetectionResult:
    """Valodas noteikšanas rezultāts"""
    language: SupportedLanguage
    confidence: float
    detected_patterns: List[str]

@dataclass
class LocalizedContent:
    """Lokalizētā satura struktūra"""
    language: SupportedLanguage
    content: Dict[str, str]

class EnhancedLanguageDetector:
    """Uzlabots valodas noteicējs"""
    
    def __init__(self):
        # Valodu specifiskās rakstzīmes
        self.language_patterns = {
            SupportedLanguage.LATVIAN: {
                'chars': r'[āčēģīķļņšūž]',
                'words': [
                    'un', 'ir', 'ar', 'no', 'uz', 'par', 'kas', 'vai', 'bet', 'ja',
                    'izveidot', 'radīt', 'veidot', 'darīt', 'telegram', 'bots',
                    'tikšanās', 'pieraksts', 'datu', 'bāze', 'epasts'
                ],
                'patterns': [
                    r'\b\w+ot\b',  # verbi ar -ot
                    r'\b\w+ās\b',  # lietvārdi ar -ās
                    r'\b\w+ība\b'  # lietvārdi ar -ība
                ]
            },
            SupportedLanguage.RUSSIAN: {
                'chars': r'[а-яё]',
                'words': [
                    'и', 'в', 'на', 'с', 'по', 'для', 'от', 'к', 'что', 'как',
                    'создать', 'сделать', 'телеграм', 'бот', 'встреча',
                    'запись', 'база', 'данных', 'почта'
                ],
                'patterns': [
                    r'\b\w+ть\b',  # verbi ar -ть
                    r'\b\w+ся\b',  # atgriezeniski verbi
                    r'\b\w+ние\b'  # lietvārdi ar -ние
                ]
            },
            SupportedLanguage.ENGLISH: {
                'chars': r'[a-zA-Z]',
                'words': [
                    'and', 'is', 'with', 'from', 'to', 'for', 'of', 'in', 'that', 'the',
                    'create', 'make', 'build', 'telegram', 'bot', 'appointment',
                    'booking', 'database', 'email', 'api', 'webhook'
                ],
                'patterns': [
                    r'\b\w+ing\b',  # verbi ar -ing
                    r'\b\w+ed\b',   # verbi ar -ed
                    r'\b\w+tion\b'  # lietvārdi ar -tion
                ]
            }
        }
    
    def detect_language(self, text: str) -> LanguageDetectionResult:
        """Nosaka teksta valodu ar uzticamības līmeni"""
        if not text or not text.strip():
            return LanguageDetectionResult(
                language=SupportedLanguage.ENGLISH,
                confidence=0.0,
                detected_patterns=[]
            )
            
        text_lower = text.lower()
        scores = {}
        detected_patterns = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            found_patterns = []
            
            # Pārbauda specifiskās rakstzīmes
            char_matches = len(re.findall(patterns['chars'], text_lower))
            if char_matches > 0:
                score += char_matches * 2
                found_patterns.append(f"chars: {char_matches}")
            
            # Pārbauda specifiskos vārdus
            word_matches = 0
            for word in patterns['words']:
                if f' {word} ' in f' {text_lower} ' or text_lower.startswith(word + ' ') or text_lower.endswith(' ' + word):
                    word_matches += 1
                    score += 3
            if word_matches > 0:
                found_patterns.append(f"words: {word_matches}")
            
            # Pārbauda valodas modeļus
            pattern_matches = 0
            for pattern in patterns['patterns']:
                try:
                    pattern_matches += len(re.findall(pattern, text_lower))
                except re.error:
                    continue  # Ignorē nederīgos regex
            if pattern_matches > 0:
                score += pattern_matches
                found_patterns.append(f"patterns: {pattern_matches}")
            
            scores[language] = score
            detected_patterns[language] = found_patterns
        
        # Atrod valodu ar augstāko punktu skaitu
        if not scores or all(score == 0 for score in scores.values()):
            # Ja nav atrasts neviens indikators, izvēlas angļu valodu
            return LanguageDetectionResult(
                language=SupportedLanguage.ENGLISH,
                confidence=0.33,
                detected_patterns=[]
            )
        
        best_language = max(scores, key=scores.get)
        total_score = sum(scores.values())
        
        # Uzlabo confidence aprēķinu
        if total_score > 0 and scores[best_language] > 0:
            confidence = scores[best_language] / total_score
        else:
            confidence = 0.33
        
        return LanguageDetectionResult(
            language=best_language,
            confidence=confidence,
            detected_patterns=detected_patterns[best_language]
        )

class MultilingualKeywordExtractor:
    """Daudzvalodu atslēgvārdu ekstraktors"""
    
    def __init__(self):
        self.extended_keywords = {
            SupportedLanguage.LATVIAN: {
                'actions': {
                    'create': ['izveidot', 'radīt', 'uztaisīt', 'veidot', 'taisīt', 'gatavot'],
                    'send': ['nosūtīt', 'sūtīt', 'pārsūtīt', 'atsūtīt'],
                    'receive': ['saņemt', 'iegūt', 'dabūt'],
                    'process': ['apstrādāt', 'pārstrādāt', 'analizēt'],
                    'save': ['saglabāt', 'ierakstīt', 'uzglabāt'],
                    'delete': ['dzēst', 'noņemt', 'likvidēt']
                },
                'services': {
                    'telegram': ['telegram', 'telegramm', 'tg'],
                    'email': ['epasts', 'e-pasts', 'elektroniskais pasts', 'mails', 'vēstule'],
                    'sms': ['sms', 'īsziņa', 'tekstziņa'],
                    'slack': ['slack', 'slacks'],
                    'discord': ['discord', 'diskords'],
                    'whatsapp': ['whatsapp', 'whats app', 'vatsaps']
                },
                'objects': {
                    'bot': ['bots', 'botu', 'botam', 'automatizācija'],
                    'appointment': ['tikšanās', 'pieraksts', 'rezervācija', 'tikšanos', 'sanāksme'],
                    'database': ['datu bāze', 'datubāze', 'db', 'bāze', 'dati'],
                    'api': ['api', 'interfeiss', 'savienojums', 'saskarnes'],
                    'webhook': ['webhook', 'web hook', 'tīmekļa āķis', 'āķis'],
                    'form': ['forma', 'anketa', 'veidlapa'],
                    'file': ['fails', 'dokuments', 'datne'],
                    'image': ['attēls', 'bilde', 'foto', 'grafika']
                },
                'data_types': {
                    'text': ['teksts', 'vārdi', 'ziņa'],
                    'number': ['skaitlis', 'numurs', 'cifra'],
                    'date': ['datums', 'laiks', 'diena'],
                    'json': ['json', 'dati', 'objekts']
                }
            },
            SupportedLanguage.RUSSIAN: {
                'actions': {
                    'create': ['создать', 'сделать', 'построить', 'генерировать', 'формировать'],
                    'send': ['отправить', 'послать', 'переслать'],
                    'receive': ['получить', 'принять', 'взять'],
                    'process': ['обработать', 'переработать', 'анализировать'],
                    'save': ['сохранить', 'записать', 'зафиксировать'],
                    'delete': ['удалить', 'стереть', 'убрать']
                },
                'services': {
                    'telegram': ['телеграм', 'telegram', 'тг'],
                    'email': ['email', 'почта', 'письмо', 'мейл', 'электронная почта'],
                    'sms': ['sms', 'смс', 'сообщение'],
                    'slack': ['slack', 'слак'],
                    'discord': ['discord', 'дискорд'],
                    'whatsapp': ['whatsapp', 'whats app', 'ватсап']
                },
                'objects': {
                    'bot': ['бот', 'бота', 'боту', 'автоматизация'],
                    'appointment': ['встреча', 'запись', 'бронирование', 'резервация'],
                    'database': ['база данных', 'бд', 'база', 'данные'],
                    'api': ['api', 'интерфейс', 'апи'],
                    'webhook': ['webhook', 'веб-хук', 'хук'],
                    'form': ['форма', 'анкета', 'бланк'],
                    'file': ['файл', 'документ', 'данные'],
                    'image': ['изображение', 'картинка', 'фото', 'рисунок']
                },
                'data_types': {
                    'text': ['текст', 'слова', 'сообщение'],
                    'number': ['число', 'номер', 'цифра'],
                    'date': ['дата', 'время', 'день'],
                    'json': ['json', 'данные', 'объект']
                }
            },
            SupportedLanguage.ENGLISH: {
                'actions': {
                    'create': ['create', 'make', 'build', 'generate', 'construct', 'develop'],
                    'send': ['send', 'dispatch', 'transmit', 'forward'],
                    'receive': ['receive', 'get', 'obtain', 'fetch'],
                    'process': ['process', 'handle', 'analyze', 'parse'],
                    'save': ['save', 'store', 'record', 'persist'],
                    'delete': ['delete', 'remove', 'erase', 'destroy']
                },
                'services': {
                    'telegram': ['telegram', 'tg'],
                    'email': ['email', 'mail', 'message', 'e-mail'],
                    'sms': ['sms', 'text message', 'text'],
                    'slack': ['slack'],
                    'discord': ['discord'],
                    'whatsapp': ['whatsapp', 'whats app']
                },
                'objects': {
                    'bot': ['bot', 'chatbot', 'automation'],
                    'appointment': ['appointment', 'booking', 'reservation', 'meeting', 'schedule'],
                    'database': ['database', 'db', 'storage', 'data'],
                    'api': ['api', 'interface', 'endpoint'],
                    'webhook': ['webhook', 'web hook', 'hook'],
                    'form': ['form', 'survey', 'questionnaire'],
                    'file': ['file', 'document', 'attachment'],
                    'image': ['image', 'picture', 'photo', 'graphic']
                },
                'data_types': {
                    'text': ['text', 'string', 'message'],
                    'number': ['number', 'integer', 'digit'],
                    'date': ['date', 'time', 'datetime'],
                    'json': ['json', 'data', 'object']
                }
            }
        }
    
    def extract_keywords(self, text: str, language: SupportedLanguage) -> Dict[str, List[str]]:
        """Ekstraktē atslēgvārdus no teksta"""
        if not text or not text.strip():
            return {
                'actions': [],
                'services': [],
                'objects': [],
                'data_types': []
            }
        
        text_lower = text.lower()
        found_keywords = {
            'actions': [],
            'services': [],
            'objects': [],
            'data_types': []
        }
        
        keyword_dict = self.extended_keywords.get(language, self.extended_keywords[SupportedLanguage.ENGLISH])
        
        for category, subcategories in keyword_dict.items():
            for keyword_type, keywords in subcategories.items():
                for keyword in keywords:
                    # Uzlabota vārdu meklēšana
                    if (f' {keyword} ' in f' {text_lower} ' or 
                        text_lower.startswith(keyword + ' ') or 
                        text_lower.endswith(' ' + keyword) or
                        keyword == text_lower):
                        if keyword_type not in found_keywords[category]:
                            found_keywords[category].append(keyword_type)
                        break
        
        return found_keywords

class MultilingualPromptManager:
    """Daudzvalodu prompt pārvaldnieks"""
    
    def __init__(self):
        self.localized_prompts = {
            SupportedLanguage.LATVIAN: {
                'system_prompt_suffix': """
Atbildi latviešu valodā. Izmanto latviešu terminoloģiju un skaidrojumus.
Workflow nosaukumi un komentāri jābūt latviešu valodā.
Instrukcijas jāsniedz latviešu valodā ar skaidriem soļiem.
""",
                'user_prompt_suffix': """
Lūdzu, ģenerē workflow ar latviešu valodas atbalstu:
- Visi komentāri latviešu valodā
- Kļūdu ziņojumi latviešu valodā
- Lietotāja saskarne latviešu valodā
""",
                'error_messages': {
                    'invalid_request': 'Nederīgs pieprasījums',
                    'missing_parameters': 'Trūkst nepieciešamie parametri',
                    'generation_failed': 'Workflow ģenerēšana neizdevās',
                    'connection_error': 'Savienojuma kļūda'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow veiksmīgi ģenerēts',
                    'workflow_uploaded': 'Workflow veiksmīgi augšupielādēts',
                    'connection_established': 'Savienojums izveidots'
                }
            },
            SupportedLanguage.RUSSIAN: {
                'system_prompt_suffix': """
Отвечай на русском языке. Используй русскую терминологию и объяснения.
Названия workflow и комментарии должны быть на русском языке.
Инструкции предоставляй на русском языке с понятными шагами.
""",
                'user_prompt_suffix': """
Пожалуйста, сгенерируй workflow с поддержкой русского языка:
- Все комментарии на русском языке
- Сообщения об ошибках на русском языке
- Пользовательский интерфейс на русском языке
""",
                'error_messages': {
                    'invalid_request': 'Неверный запрос',
                    'missing_parameters': 'Отсутствуют необходимые параметры',
                    'generation_failed': 'Не удалось сгенерировать workflow',
                    'connection_error': 'Ошибка соединения'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow успешно сгенерирован',
                    'workflow_uploaded': 'Workflow успешно загружен',
                    'connection_established': 'Соединение установлено'
                }
            },
            SupportedLanguage.ENGLISH: {
                'system_prompt_suffix': """
Respond in English. Use English terminology and explanations.
Workflow names and comments should be in English.
Provide instructions in English with clear steps.
""",
                'user_prompt_suffix': """
Please generate workflow with English language support:
- All comments in English
- Error messages in English
- User interface in English
""",
                'error_messages': {
                    'invalid_request': 'Invalid request',
                    'missing_parameters': 'Missing required parameters',
                    'generation_failed': 'Failed to generate workflow',
                    'connection_error': 'Connection error'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow generated successfully',
                    'workflow_uploaded': 'Workflow uploaded successfully',
                    'connection_established': 'Connection established'
                }
            }
        }
    
    def get_localized_prompt(self, base_prompt: str, language: SupportedLanguage, prompt_type: str = 'system') -> str:
        """Iegūst lokalizētu prompt"""
        if not base_prompt:
            base_prompt = ""
            
        localized_content = self.localized_prompts.get(language, self.localized_prompts[SupportedLanguage.ENGLISH])
        
        suffix_key = f'{prompt_type}_prompt_suffix'
        suffix = localized_content.get(suffix_key, '')
        
        return base_prompt + suffix
    
    def get_localized_message(self, message_key: str, language: SupportedLanguage, message_type: str = 'error') -> str:
        """Iegūst lokalizētu ziņojumu"""
        localized_content = self.localized_prompts.get(language, self.localized_prompts[SupportedLanguage.ENGLISH])
        
        messages = localized_content.get(f'{message_type}_messages', {})
        return messages.get(message_key, message_key)

class MultilingualResponseFormatter:
    """Daudzvalodu atbildes formatētājs"""
    
    def __init__(self):
        self.response_templates = {
            SupportedLanguage.LATVIAN: {
                'workflow_generation_success': {
                    'title': '🎯 Workflow Ģenerēšanas Rezultāts',
                    'analysis_title': '📝 Vaicājuma Analīze',
                    'workflow_title': '🔧 Ģenerētais Workflow',
                    'instructions_title': '📋 Uzstādīšanas Instrukcijas',
                    'explanation_title': '💡 Paskaidrojums',
                    'errors_title': '⚠️ Kļūdas'
                },
                'search_results': {
                    'title': '🔍 Meklēšanas Rezultāti',
                    'no_results': 'Nav atrasti līdzīgi workflow jūsu vaicājumam.',
                    'results_found': 'atrasti'
                }
            },
            SupportedLanguage.RUSSIAN: {
                'workflow_generation_success': {
                    'title': '🎯 Результат Генерации Workflow',
                    'analysis_title': '📝 Анализ Запроса',
                    'workflow_title': '🔧 Сгенерированный Workflow',
                    'instructions_title': '📋 Инструкции по Установке',
                    'explanation_title': '💡 Объяснение',
                    'errors_title': '⚠️ Ошибки'
                },
                'search_results': {
                    'title': '🔍 Результаты Поиска',
                    'no_results': 'Не найдено похожих workflow для вашего запроса.',
                    'results_found': 'найдено'
                }
            },
            SupportedLanguage.ENGLISH: {
                'workflow_generation_success': {
                    'title': '🎯 Workflow Generation Result',
                    'analysis_title': '📝 Query Analysis',
                    'workflow_title': '🔧 Generated Workflow',
                    'instructions_title': '📋 Setup Instructions',
                    'explanation_title': '💡 Explanation',
                    'errors_title': '⚠️ Errors'
                },
                'search_results': {
                    'title': '🔍 Search Results',
                    'no_results': 'No similar workflows found for your query.',
                    'results_found': 'found'
                }
            }
        }
    
    def format_response(self, response_data: Dict[str, Any], language: SupportedLanguage, response_type: str) -> Dict[str, Any]:
        """Formatē atbildi atbilstoši valodai"""
        if not response_data:
            response_data = {}
            
        templates = self.response_templates.get(language, self.response_templates[SupportedLanguage.ENGLISH])
        template = templates.get(response_type, {})
        
        # Pievieno lokalizētus virsrakstus
        if template:
            response_data['localized_labels'] = template
        
        return response_data

class MultilingualValidator:
    """Daudzvalodu validētājs"""
    
    def __init__(self):
        self.validation_messages = {
            SupportedLanguage.LATVIAN: {
                'required_field': 'Obligāts lauks',
                'invalid_format': 'Nederīgs formāts',
                'too_short': 'Pārāk īss',
                'too_long': 'Pārāk garš',
                'invalid_language': 'Neatbalstīta valoda'
            },
            SupportedLanguage.RUSSIAN: {
                'required_field': 'Обязательное поле',
                'invalid_format': 'Неверный формат',
                'too_short': 'Слишком короткий',
                'too_long': 'Слишком длинный',
                'invalid_language': 'Неподдерживаемый язык'
            },
            SupportedLanguage.ENGLISH: {
                'required_field': 'Required field',
                'invalid_format': 'Invalid format',
                'too_short': 'Too short',
                'too_long': 'Too long',
                'invalid_language': 'Unsupported language'
            }
        }
    
    def validate_input(self, text: str, language: SupportedLanguage) -> Tuple[bool, List[str]]:
        """Validē ievades tekstu"""
        errors = []
        messages = self.validation_messages.get(language, self.validation_messages[SupportedLanguage.ENGLISH])
        
        if not text or not text.strip():
            errors.append(messages['required_field'])
        elif len(text.strip()) < 3:
            errors.append(messages['too_short'])
        elif len(text.strip()) > 1000:
            errors.append(messages['too_long'])
        
        return len(errors) == 0, errors

# Galvenā daudzvalodu atbalsta klase
class MultilingualSupport:
    """Galvenā daudzvalodu atbalsta klase"""
    
    def __init__(self):
        self.detector = EnhancedLanguageDetector()
        self.keyword_extractor = MultilingualKeywordExtractor()
        self.prompt_manager = MultilingualPromptManager()
        self.response_formatter = MultilingualResponseFormatter()
        self.validator = MultilingualValidator()
    
    def process_multilingual_request(self, text: str) -> Dict[str, Any]:
        """Apstrādā daudzvalodu pieprasījumu"""
        try:
            # Nosaka valodu
            detection_result = self.detector.detect_language(text)
            
            # Validē ievadi
            is_valid, validation_errors = self.validator.validate_input(text, detection_result.language)
            
            if not is_valid:
                return {
                    'success': False,
                    'language': detection_result.language.value,
                    'errors': validation_errors,
                    'confidence': detection_result.confidence
                }
            
            # Ekstraktē atslēgvārdus
            keywords = self.keyword_extractor.extract_keywords(text, detection_result.language)
            
            return {
                'success': True,
                'language': detection_result.language.value,
                'confidence': detection_result.confidence,
                'detected_patterns': detection_result.detected_patterns,
                'keywords': keywords,
                'original_text': text
            }
        except Exception as e:
            return {
                'success': False,
                'language': SupportedLanguage.ENGLISH.value,
                'errors': [f'Processing error: {str(e)}'],
                'confidence': 0.0
            }
    
    def localize_prompt(self, base_prompt: str, language: str, prompt_type: str = 'system') -> str:
        """Lokalizē prompt"""
        try:
            lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
            return self.prompt_manager.get_localized_prompt(base_prompt, lang_enum, prompt_type)
        except (ValueError, KeyError):
            return self.prompt_manager.get_localized_prompt(base_prompt, SupportedLanguage.ENGLISH, prompt_type)
    
    def localize_message(self, message_key: str, language: str, message_type: str = 'error') -> str:
        """Lokalizē ziņojumu"""
        try:
            lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
            return self.prompt_manager.get_localized_message(message_key, lang_enum, message_type)
        except (ValueError, KeyError):
            return self.prompt_manager.get_localized_message(message_key, SupportedLanguage.ENGLISH, message_type)
    
    def format_localized_response(self, response_data: Dict[str, Any], language: str, response_type: str) -> Dict[str, Any]:
        """Formatē lokalizētu atbildi"""
        try:
            lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
            return self.response_formatter.format_response(response_data, lang_enum, response_type)
        except (ValueError, KeyError):
            return self.response_formatter.format_response(response_data, SupportedLanguage.ENGLISH, response_type)

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē daudzvalodu atbalstu
    multilingual = MultilingualSupport()
    
    # Testa teksti
    test_texts = [
        "Izveidot Telegram botu pierakstam uz tikšanos",
        "Создать телеграм бота для записи на встречи",
        "Create a Telegram bot for appointment booking"
    ]        # Valodu specifiskās rakstzīmes
        self.language_patterns = {
            SupportedLanguage.LATVIAN: {
                'chars': r'[āčēģīķļņšūž]',
                'words': [
                    'un', 'ir', 'ar', 'no', 'uz', 'par', 'kas', 'vai', 'bet', 'ja',
                    'izveidot', 'radīt', 'veidot', 'darīt', 'telegram', 'bots',
                    'tikšanās', 'pieraksts', 'datu', 'bāze', 'epasts'
                ],
                'patterns': [
                    r'\b\w+ot\b',  # verbi ar -ot
                    r'\b\w+ās\b',  # lietvārdi ar -ās
                    r'\b\w+ība\b'  # lietvārdi ar -ība
                ]
            },
            SupportedLanguage.RUSSIAN: {
                'chars': r'[а-яё]',
                'words': [
                    'и', 'в', 'на', 'с', 'по', 'для', 'от', 'к', 'что', 'как',
                    'создать', 'сделать', 'телеграм', 'бот', 'встреча',
                    'запись', 'база', 'данных', 'почта'
                ],
                'patterns': [
                    r'\b\w+ть\b',  # verbi ar -ть
                    r'\b\w+ся\b',  # atgriezeniski verbi
                    r'\b\w+ние\b'  # lietvārdi ar -ние
                ]
            },
            SupportedLanguage.ENGLISH: {
                'chars': r'[a-z]',
                'words': [
                    'and', 'is', 'with', 'from', 'to', 'for', 'of', 'in', 'that', 'the',
                    'create', 'make', 'build', 'telegram', 'bot', 'appointment',
                    'booking', 'database', 'email', 'api', 'webhook'
                ],
                'patterns': [
                    r'\b\w+ing\b',  # verbi ar -ing
                    r'\b\w+ed\b',   # verbi ar -ed
                    r'\b\w+tion\b'  # lietvārdi ar -tion
                ]
            }
        }
    
    def detect_language(self, text: str) -> LanguageDetectionResult:
        """Nosaka teksta valodu ar uzticamības līmeni"""
        text_lower = text.lower()
        scores = {}
        detected_patterns = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            found_patterns = []
            
            # Pārbauda specifiskās rakstzīmes
            char_matches = len(re.findall(patterns['chars'], text_lower))
            if char_matches > 0:
                score += char_matches * 2
                found_patterns.append(f"chars: {char_matches}")
            
            # Pārbauda specifiskos vārdus
            word_matches = 0
            for word in patterns['words']:
                if word in text_lower:
                    word_matches += 1
                    score += 3
            if word_matches > 0:
                found_patterns.append(f"words: {word_matches}")
            
            # Pārbauda valodas modeļus
            pattern_matches = 0
            for pattern in patterns['patterns']:
                pattern_matches += len(re.findall(pattern, text_lower))
            if pattern_matches > 0:
                score += pattern_matches
                found_patterns.append(f"patterns: {pattern_matches}")
            
            scores[language] = score
            detected_patterns[language] = found_patterns
        
        # Atrod valodu ar augstāko punktu skaitu
        best_language = max(scores, key=scores.get)
        total_score = sum(scores.values())
        confidence = scores[best_language] / total_score if total_score > 0 else 0.33
        
        return LanguageDetectionResult(
            language=best_language,
            confidence=confidence,
            detected_patterns=detected_patterns[best_language]
        )

class MultilingualKeywordExtractor:
    """Daudzvalodu atslēgvārdu ekstraktors"""
    
    def __init__(self):
        self.extended_keywords = {
            SupportedLanguage.LATVIAN: {
                'actions': {
                    'create': ['izveidot', 'radīt', 'uztaisīt', 'veidot', 'taisīt', 'gatavot'],
                    'send': ['nosūtīt', 'sūtīt', 'pārsūtīt', 'atsūtīt'],
                    'receive': ['saņemt', 'iegūt', 'dabūt'],
                    'process': ['apstrādāt', 'pārstrādāt', 'analizēt'],
                    'save': ['saglabāt', 'ierakstīt', 'uzglabāt'],
                    'delete': ['dzēst', 'noņemt', 'likvidēt']
                },
                'services': {
                    'telegram': ['telegram', 'telegramm', 'tg'],
                    'email': ['epasts', 'e-pasts', 'elektroniskais pasts', 'mails', 'vēstule'],
                    'sms': ['sms', 'īsziņa', 'tekstziņa'],
                    'slack': ['slack', 'slacks'],
                    'discord': ['discord', 'diskords'],
                    'whatsapp': ['whatsapp', 'whats app', 'vatsaps']
                },
                'objects': {
                    'bot': ['bots', 'botu', 'botam', 'automatizācija'],
                    'appointment': ['tikšanās', 'pieraksts', 'rezervācija', 'tikšanos', 'sanāksme'],
                    'database': ['datu bāze', 'datubāze', 'db', 'bāze', 'dati'],
                    'api': ['api', 'interfeiss', 'savienojums', 'saskarnes'],
                    'webhook': ['webhook', 'web hook', 'tīmekļa āķis', 'āķis'],
                    'form': ['forma', 'anketa', 'veidlapa'],
                    'file': ['fails', 'dokuments', 'datne'],
                    'image': ['attēls', 'bilde', 'foto', 'grafika']
                },
                'data_types': {
                    'text': ['teksts', 'vārdi', 'ziņa'],
                    'number': ['skaitlis', 'numurs', 'cifra'],
                    'date': ['datums', 'laiks', 'diena'],
                    'json': ['json', 'dati', 'objekts']
                }
            },
            SupportedLanguage.RUSSIAN: {
                'actions': {
                    'create': ['создать', 'сделать', 'построить', 'генерировать', 'формировать'],
                    'send': ['отправить', 'послать', 'переслать'],
                    'receive': ['получить', 'принять', 'взять'],
                    'process': ['обработать', 'переработать', 'анализировать'],
                    'save': ['сохранить', 'записать', 'зафиксировать'],
                    'delete': ['удалить', 'стереть', 'убрать']
                },
                'services': {
                    'telegram': ['телеграм', 'telegram', 'тг'],
                    'email': ['email', 'почта', 'письмо', 'мейл', 'электронная почта'],
                    'sms': ['sms', 'смс', 'сообщение'],
                    'slack': ['slack', 'слак'],
                    'discord': ['discord', 'дискорд'],
                    'whatsapp': ['whatsapp', 'whats app', 'ватсап']
                },
                'objects': {
                    'bot': ['бот', 'бота', 'боту', 'автоматизация'],
                    'appointment': ['встреча', 'запись', 'бронирование', 'резервация'],
                    'database': ['база данных', 'бд', 'база', 'данные'],
                    'api': ['api', 'интерфейс', 'апи'],
                    'webhook': ['webhook', 'веб-хук', 'хук'],
                    'form': ['форма', 'анкета', 'бланк'],
                    'file': ['файл', 'документ', 'данные'],
                    'image': ['изображение', 'картинка', 'фото', 'рисунок']
                },
                'data_types': {
                    'text': ['текст', 'слова', 'сообщение'],
                    'number': ['число', 'номер', 'цифра'],
                    'date': ['дата', 'время', 'день'],
                    'json': ['json', 'данные', 'объект']
                }
            },
            SupportedLanguage.ENGLISH: {
                'actions': {
                    'create': ['create', 'make', 'build', 'generate', 'construct', 'develop'],
                    'send': ['send', 'dispatch', 'transmit', 'forward'],
                    'receive': ['receive', 'get', 'obtain', 'fetch'],
                    'process': ['process', 'handle', 'analyze', 'parse'],
                    'save': ['save', 'store', 'record', 'persist'],
                    'delete': ['delete', 'remove', 'erase', 'destroy']
                },
                'services': {
                    'telegram': ['telegram', 'tg'],
                    'email': ['email', 'mail', 'message', 'e-mail'],
                    'sms': ['sms', 'text message', 'text'],
                    'slack': ['slack'],
                    'discord': ['discord'],
                    'whatsapp': ['whatsapp', 'whats app']
                },
                'objects': {
                    'bot': ['bot', 'chatbot', 'automation'],
                    'appointment': ['appointment', 'booking', 'reservation', 'meeting', 'schedule'],
                    'database': ['database', 'db', 'storage', 'data'],
                    'api': ['api', 'interface', 'endpoint'],
                    'webhook': ['webhook', 'web hook', 'hook'],
                    'form': ['form', 'survey', 'questionnaire'],
                    'file': ['file', 'document', 'attachment'],
                    'image': ['image', 'picture', 'photo', 'graphic']
                },
                'data_types': {
                    'text': ['text', 'string', 'message'],
                    'number': ['number', 'integer', 'digit'],
                    'date': ['date', 'time', 'datetime'],
                    'json': ['json', 'data', 'object']
                }
            }
        }
    
    def extract_keywords(self, text: str, language: SupportedLanguage) -> Dict[str, List[str]]:
        """Ekstraktē atslēgvārdus no teksta"""
        text_lower = text.lower()
        found_keywords = {
            'actions': [],
            'services': [],
            'objects': [],
            'data_types': []
        }
        
        keyword_dict = self.extended_keywords.get(language, self.extended_keywords[SupportedLanguage.ENGLISH])
        
        for category, subcategories in keyword_dict.items():
            for keyword_type, keywords in subcategories.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        if keyword_type not in found_keywords[category]:
                            found_keywords[category].append(keyword_type)
                        break
        
        return found_keywords

class MultilingualPromptManager:
    """Daudzvalodu prompt pārvaldnieks"""
    
    def __init__(self):
        self.localized_prompts = {
            SupportedLanguage.LATVIAN: {
                'system_prompt_suffix': """
Atbildi latviešu valodā. Izmanto latviešu terminoloģiju un skaidrojumus.
Workflow nosaukumi un komentāri jābūt latviešu valodā.
Instrukcijas jāsniedz latviešu valodā ar skaidriem soļiem.
""",
                'user_prompt_suffix': """
Lūdzu, ģenerē workflow ar latviešu valodas atbalstu:
- Visi komentāri latviešu valodā
- Kļūdu ziņojumi latviešu valodā
- Lietotāja saskarne latviešu valodā
""",
                'error_messages': {
                    'invalid_request': 'Nederīgs pieprasījums',
                    'missing_parameters': 'Trūkst nepieciešamie parametri',
                    'generation_failed': 'Workflow ģenerēšana neizdevās',
                    'connection_error': 'Savienojuma kļūda'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow veiksmīgi ģenerēts',
                    'workflow_uploaded': 'Workflow veiksmīgi augšupielādēts',
                    'connection_established': 'Savienojums izveidots'
                }
            },
            SupportedLanguage.RUSSIAN: {
                'system_prompt_suffix': """
Отвечай на русском языке. Используй русскую терминологию и объяснения.
Названия workflow и комментарии должны быть на русском языке.
Инструкции предоставляй на русском языке с понятными шагами.
""",
                'user_prompt_suffix': """
Пожалуйста, сгенерируй workflow с поддержкой русского языка:
- Все комментарии на русском языке
- Сообщения об ошибках на русском языке
- Пользовательский интерфейс на русском языке
""",
                'error_messages': {
                    'invalid_request': 'Неверный запрос',
                    'missing_parameters': 'Отсутствуют необходимые параметры',
                    'generation_failed': 'Не удалось сгенерировать workflow',
                    'connection_error': 'Ошибка соединения'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow успешно сгенерирован',
                    'workflow_uploaded': 'Workflow успешно загружен',
                    'connection_established': 'Соединение установлено'
                }
            },
            SupportedLanguage.ENGLISH: {
                'system_prompt_suffix': """
Respond in English. Use English terminology and explanations.
Workflow names and comments should be in English.
Provide instructions in English with clear steps.
""",
                'user_prompt_suffix': """
Please generate workflow with English language support:
- All comments in English
- Error messages in English
- User interface in English
""",
                'error_messages': {
                    'invalid_request': 'Invalid request',
                    'missing_parameters': 'Missing required parameters',
                    'generation_failed': 'Failed to generate workflow',
                    'connection_error': 'Connection error'
                },
                'success_messages': {
                    'workflow_generated': 'Workflow generated successfully',
                    'workflow_uploaded': 'Workflow uploaded successfully',
                    'connection_established': 'Connection established'
                }
            }
        }
    
    def get_localized_prompt(self, base_prompt: str, language: SupportedLanguage, prompt_type: str = 'system') -> str:
        """Iegūst lokalizētu prompt"""
        localized_content = self.localized_prompts.get(language, self.localized_prompts[SupportedLanguage.ENGLISH])
        
        suffix_key = f'{prompt_type}_prompt_suffix'
        suffix = localized_content.get(suffix_key, '')
        
        return base_prompt + suffix
    
    def get_localized_message(self, message_key: str, language: SupportedLanguage, message_type: str = 'error') -> str:
        """Iegūst lokalizētu ziņojumu"""
        localized_content = self.localized_prompts.get(language, self.localized_prompts[SupportedLanguage.ENGLISH])
        
        messages = localized_content.get(f'{message_type}_messages', {})
        return messages.get(message_key, message_key)

class MultilingualResponseFormatter:
    """Daudzvalodu atbildes formatētājs"""
    
    def __init__(self):
        self.response_templates = {
            SupportedLanguage.LATVIAN: {
                'workflow_generation_success': {
                    'title': '🎯 Workflow Ģenerēšanas Rezultāts',
                    'analysis_title': '📝 Vaicājuma Analīze',
                    'workflow_title': '🔧 Ģenerētais Workflow',
                    'instructions_title': '📋 Uzstādīšanas Instrukcijas',
                    'explanation_title': '💡 Paskaidrojums',
                    'errors_title': '⚠️ Kļūdas'
                },
                'search_results': {
                    'title': '🔍 Meklēšanas Rezultāti',
                    'no_results': 'Nav atrasti līdzīgi workflow jūsu vaicājumam.',
                    'results_found': 'atrasti'
                }
            },
            SupportedLanguage.RUSSIAN: {
                'workflow_generation_success': {
                    'title': '🎯 Результат Генерации Workflow',
                    'analysis_title': '📝 Анализ Запроса',
                    'workflow_title': '🔧 Сгенерированный Workflow',
                    'instructions_title': '📋 Инструкции по Установке',
                    'explanation_title': '💡 Объяснение',
                    'errors_title': '⚠️ Ошибки'
                },
                'search_results': {
                    'title': '🔍 Результаты Поиска',
                    'no_results': 'Не найдено похожих workflow для вашего запроса.',
                    'results_found': 'найдено'
                }
            },
            SupportedLanguage.ENGLISH: {
                'workflow_generation_success': {
                    'title': '🎯 Workflow Generation Result',
                    'analysis_title': '📝 Query Analysis',
                    'workflow_title': '🔧 Generated Workflow',
                    'instructions_title': '📋 Setup Instructions',
                    'explanation_title': '💡 Explanation',
                    'errors_title': '⚠️ Errors'
                },
                'search_results': {
                    'title': '🔍 Search Results',
                    'no_results': 'No similar workflows found for your query.',
                    'results_found': 'found'
                }
            }
        }
    
    def format_response(self, response_data: Dict[str, Any], language: SupportedLanguage, response_type: str) -> Dict[str, Any]:
        """Formatē atbildi atbilstoši valodai"""
        templates = self.response_templates.get(language, self.response_templates[SupportedLanguage.ENGLISH])
        template = templates.get(response_type, {})
        
        # Pievieno lokalizētus virsrakstus
        if template:
            response_data['localized_labels'] = template
        
        return response_data

class MultilingualValidator:
    """Daudzvalodu validētājs"""
    
    def __init__(self):
        self.validation_messages = {
            SupportedLanguage.LATVIAN: {
                'required_field': 'Obligāts lauks',
                'invalid_format': 'Nederīgs formāts',
                'too_short': 'Pārāk īss',
                'too_long': 'Pārāk garš',
                'invalid_language': 'Neatbalstīta valoda'
            },
            SupportedLanguage.RUSSIAN: {
                'required_field': 'Обязательное поле',
                'invalid_format': 'Неверный формат',
                'too_short': 'Слишком короткий',
                'too_long': 'Слишком длинный',
                'invalid_language': 'Неподдерживаемый язык'
            },
            SupportedLanguage.ENGLISH: {
                'required_field': 'Required field',
                'invalid_format': 'Invalid format',
                'too_short': 'Too short',
                'too_long': 'Too long',
                'invalid_language': 'Unsupported language'
            }
        }
    
    def validate_input(self, text: str, language: SupportedLanguage) -> Tuple[bool, List[str]]:
        """Validē ievades tekstu"""
        errors = []
        messages = self.validation_messages.get(language, self.validation_messages[SupportedLanguage.ENGLISH])
        
        if not text or not text.strip():
            errors.append(messages['required_field'])
        elif len(text.strip()) < 3:
            errors.append(messages['too_short'])
        elif len(text.strip()) > 1000:
            errors.append(messages['too_long'])
        
        return len(errors) == 0, errors

# Galvenā daudzvalodu atbalsta klase
class MultilingualSupport:
    """Galvenā daudzvalodu atbalsta klase"""
    
    def __init__(self):
        self.detector = EnhancedLanguageDetector()
        self.keyword_extractor = MultilingualKeywordExtractor()
        self.prompt_manager = MultilingualPromptManager()
        self.response_formatter = MultilingualResponseFormatter()
        self.validator = MultilingualValidator()
    
    def process_multilingual_request(self, text: str) -> Dict[str, Any]:
        """Apstrādā daudzvalodu pieprasījumu"""
        # Nosaka valodu
        detection_result = self.detector.detect_language(text)
        
        # Validē ievadi
        is_valid, validation_errors = self.validator.validate_input(text, detection_result.language)
        
        if not is_valid:
            return {
                'success': False,
                'language': detection_result.language.value,
                'errors': validation_errors,
                'confidence': detection_result.confidence
            }
        
        # Ekstraktē atslēgvārdus
        keywords = self.keyword_extractor.extract_keywords(text, detection_result.language)
        
        return {
            'success': True,
            'language': detection_result.language.value,
            'confidence': detection_result.confidence,
            'detected_patterns': detection_result.detected_patterns,
            'keywords': keywords,
            'original_text': text
        }
    
    def localize_prompt(self, base_prompt: str, language: str, prompt_type: str = 'system') -> str:
        """Lokalizē prompt"""
        lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
        return self.prompt_manager.get_localized_prompt(base_prompt, lang_enum, prompt_type)
    
    def localize_message(self, message_key: str, language: str, message_type: str = 'error') -> str:
        """Lokalizē ziņojumu"""
        lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
        return self.prompt_manager.get_localized_message(message_key, lang_enum, message_type)
    
    def format_localized_response(self, response_data: Dict[str, Any], language: str, response_type: str) -> Dict[str, Any]:
        """Formatē lokalizētu atbildi"""
        lang_enum = SupportedLanguage(language) if language in [l.value for l in SupportedLanguage] else SupportedLanguage.ENGLISH
        return self.response_formatter.format_response(response_data, lang_enum, response_type)

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē daudzvalodu atbalstu
    multilingual = MultilingualSupport()
    
    # Testa teksti
    test_texts = [
        "Izveidot Telegram botu pierakstam uz tikšanos",
        "Создать телеграм бота для записи на встречи",
        "Create a Telegram bot for appointment booking"
    ]
    
    for text in test_texts:
        print(f"\nTeksts: {text}")
        result = multilingual.process_multilingual_request(text)
        
        if result['success']:
            print(f"Valoda: {result['language']} (uzticamība: {result['confidence']:.2f})")
            print(f"Atslēgvārdi: {result['keywords']}")
            
            # Lokalizē ziņojumu
            success_msg = multilingual.localize_message('workflow_generated', result['language'], 'success')
            print(f"Lokalizēts ziņojums: {success_msg}")
        else:
            print(f"Kļūdas: {result['errors']}")
    
    print("\nDaudzvalodu atbalsts veiksmīgi testēts!")


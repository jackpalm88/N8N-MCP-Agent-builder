#!/usr/bin/env python3
"""
Workflow Search Algorithm for n8n AI Agent
Šis modulis implementē inteliģentu workflow meklēšanas algoritmu.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from src.vector_database_design import QdrantWorkflowDatabase, WorkflowVectorizer

class SearchIntent(Enum):
    """Meklēšanas nolūka tipi"""
    CREATE_NEW = "create_new"
    FIND_SIMILAR = "find_similar"
    MODIFY_EXISTING = "modify_existing"
    EXPLAIN_WORKFLOW = "explain_workflow"

@dataclass
class SearchQuery:
    """Meklēšanas vaicājuma struktūra"""
    original_text: str
    intent: SearchIntent
    keywords: List[str]
    entities: Dict[str, List[str]]
    language: str
    complexity_preference: str  # "simple", "medium", "complex"

@dataclass
class SearchResult:
    """Meklēšanas rezultāta struktūra"""
    workflow_id: str
    workflow_name: str
    similarity_score: float
    workflow_json: Dict[str, Any]
    match_reasons: List[str]
    suggested_modifications: List[str]

class NaturalLanguageProcessor:
    """Dabiskās valodas apstrādes klase"""
    
    def __init__(self, openai_client: openai.OpenAI):
        self.openai_client = openai_client
        
        # Atslēgvārdu vārdnīcas dažādām valodām
        self.keywords_mapping = {
            'lv': {
                'create': ['izveidot', 'radīt', 'uztaisīt', 'veidot'],
                'telegram': ['telegram', 'telegramm'],
                'bot': ['bots', 'botu', 'botam'],
                'appointment': ['tikšanās', 'pieraksts', 'rezervācija', 'tikšanos'],
                'email': ['epasts', 'e-pasts', 'elektroniskais pasts', 'mails'],
                'database': ['datu bāze', 'datubāze', 'db', 'bāze'],
                'api': ['api', 'interfeiss', 'savienojums'],
                'webhook': ['webhook', 'web hook', 'tīmekļa āķis']
            },
            'ru': {
                'create': ['создать', 'сделать', 'построить'],
                'telegram': ['телеграм', 'telegram'],
                'bot': ['бот', 'бота', 'боту'],
                'appointment': ['встреча', 'запись', 'бронирование'],
                'email': ['email', 'почта', 'письмо'],
                'database': ['база данных', 'бд', 'база'],
                'api': ['api', 'интерфейс'],
                'webhook': ['webhook', 'веб-хук']
            },
            'en': {
                'create': ['create', 'make', 'build', 'generate'],
                'telegram': ['telegram'],
                'bot': ['bot', 'chatbot'],
                'appointment': ['appointment', 'booking', 'reservation', 'meeting'],
                'email': ['email', 'mail', 'message'],
                'database': ['database', 'db', 'storage'],
                'api': ['api', 'interface', 'endpoint'],
                'webhook': ['webhook', 'web hook']
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Nosaka teksta valodu"""
        # Vienkārša valodas noteikšana, pamatojoties uz rakstzīmēm
        if re.search(r'[а-яё]', text.lower()):
            return 'ru'
        elif re.search(r'[āčēģīķļņšūž]', text.lower()):
            return 'lv'
        else:
            return 'en'
    
    def extract_keywords(self, text: str, language: str) -> List[str]:
        """Ekstraktē atslēgvārdus no teksta"""
        keywords = []
        text_lower = text.lower()
        
        keyword_dict = self.keywords_mapping.get(language, self.keywords_mapping['en'])
        
        for category, words in keyword_dict.items():
            for word in words:
                if word in text_lower:
                    keywords.append(category)
                    break
        
        return list(set(keywords))
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Ekstraktē entītijas no teksta"""
        entities = {
            'services': [],
            'actions': [],
            'technologies': []
        }
        
        # Servisu noteikšana
        services_patterns = [
            r'\b(telegram|discord|slack|whatsapp)\b',
            r'\b(gmail|outlook|email)\b',
            r'\b(mysql|postgres|mongodb)\b',
            r'\b(supabase|firebase|airtable)\b'
        ]
        
        for pattern in services_patterns:
            matches = re.findall(pattern, text.lower())
            entities['services'].extend(matches)
        
        # Darbību noteikšana
        action_patterns = [
            r'\b(send|receive|create|update|delete|get|post)\b',
            r'\b(sūtīt|saņemt|izveidot|atjaunināt|dzēst)\b',
            r'\b(отправить|получить|создать|обновить|удалить)\b'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text.lower())
            entities['actions'].extend(matches)
        
        return entities
    
    def determine_intent(self, text: str, keywords: List[str]) -> SearchIntent:
        """Nosaka lietotāja nolūku"""
        text_lower = text.lower()
        
        # Nolūka noteikšanas loģika
        if any(word in text_lower for word in ['create', 'izveidot', 'radīt', 'создать']):
            return SearchIntent.CREATE_NEW
        elif any(word in text_lower for word in ['find', 'search', 'atrast', 'meklēt', 'найти']):
            return SearchIntent.FIND_SIMILAR
        elif any(word in text_lower for word in ['modify', 'change', 'pielāgot', 'mainīt', 'изменить']):
            return SearchIntent.MODIFY_EXISTING
        elif any(word in text_lower for word in ['explain', 'how', 'kā', 'как', 'paskaidrot']):
            return SearchIntent.EXPLAIN_WORKFLOW
        else:
            return SearchIntent.CREATE_NEW  # Noklusējuma nolūks
    
    def determine_complexity(self, text: str) -> str:
        """Nosaka vēlamo sarežģītības līmeni"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['simple', 'basic', 'vienkāršs', 'простой']):
            return 'simple'
        elif any(word in text_lower for word in ['complex', 'advanced', 'sarežģīts', 'сложный']):
            return 'complex'
        else:
            return 'medium'
    
    def parse_query(self, text: str) -> SearchQuery:
        """Parsē lietotāja vaicājumu"""
        language = self.detect_language(text)
        keywords = self.extract_keywords(text, language)
        entities = self.extract_entities(text)
        intent = self.determine_intent(text, keywords)
        complexity = self.determine_complexity(text)
        
        return SearchQuery(
            original_text=text,
            intent=intent,
            keywords=keywords,
            entities=entities,
            language=language,
            complexity_preference=complexity
        )

class WorkflowSearchEngine:
    """Workflow meklēšanas dzinējs"""
    
    def __init__(self, db: QdrantWorkflowDatabase, vectorizer: WorkflowVectorizer, nlp: NaturalLanguageProcessor):
        self.db = db
        self.vectorizer = vectorizer
        self.nlp = nlp
    
    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """Galvenā meklēšanas metode"""
        # Parsē vaicājumu
        parsed_query = self.nlp.parse_query(query)
        
        # Ģenerē meklēšanas vektoru
        search_vector = self.vectorizer.generate_embedding(query)
        
        # Nosaka kategorijas filtru
        category_filter = self._determine_category_filter(parsed_query)
        
        # Meklē līdzīgus workflow
        similar_workflows = self.db.search_similar_workflows(
            query_vector=search_vector,
            limit=max_results * 2,  # Iegūst vairāk rezultātu filtrēšanai
            category_filter=category_filter
        )
        
        # Filtrē un ranžē rezultātus
        filtered_results = self._filter_and_rank_results(similar_workflows, parsed_query)
        
        # Pārveido par SearchResult objektiem
        search_results = []
        for result in filtered_results[:max_results]:
            search_result = SearchResult(
                workflow_id=result['id'],
                workflow_name=result['metadata']['name'],
                similarity_score=result['score'],
                workflow_json=result['workflow_json'],
                match_reasons=self._generate_match_reasons(result, parsed_query),
                suggested_modifications=self._generate_modifications(result, parsed_query)
            )
            search_results.append(search_result)
        
        return search_results
    
    def _determine_category_filter(self, query: SearchQuery) -> Optional[str]:
        """Nosaka kategorijas filtru, pamatojoties uz vaicājumu"""
        keywords = query.keywords
        entities = query.entities
        
        if 'telegram' in keywords or 'telegram' in entities.get('services', []):
            return 'messaging'
        elif 'email' in keywords or any(service in entities.get('services', []) for service in ['gmail', 'outlook']):
            return 'email'
        elif 'database' in keywords or any(service in entities.get('services', []) for service in ['mysql', 'postgres']):
            return 'database'
        elif 'api' in keywords or 'webhook' in keywords:
            return 'api'
        
        return None
    
    def _filter_and_rank_results(self, results: List[Dict[str, Any]], query: SearchQuery) -> List[Dict[str, Any]]:
        """Filtrē un ranžē meklēšanas rezultātus"""
        filtered_results = []
        
        for result in results:
            # Sarežģītības filtrs
            complexity_score = result['metadata']['complexity_score']
            if query.complexity_preference == 'simple' and complexity_score > 30:
                continue
            elif query.complexity_preference == 'complex' and complexity_score < 50:
                continue
            
            # Atslēgvārdu atbilstības pārbaude
            keyword_match_score = self._calculate_keyword_match(result, query)
            
            # Pielāgo kopējo punktu skaitu
            adjusted_score = result['score'] * 0.7 + keyword_match_score * 0.3
            result['adjusted_score'] = adjusted_score
            
            filtered_results.append(result)
        
        # Kārto pēc pielāgotā punktu skaita
        filtered_results.sort(key=lambda x: x['adjusted_score'], reverse=True)
        
        return filtered_results
    
    def _calculate_keyword_match(self, result: Dict[str, Any], query: SearchQuery) -> float:
        """Aprēķina atslēgvārdu atbilstības punktu skaitu"""
        workflow_tags = result['metadata'].get('tags', [])
        workflow_description = result['metadata'].get('description', '').lower()
        
        match_score = 0.0
        total_keywords = len(query.keywords)
        
        if total_keywords == 0:
            return 0.5  # Neitrāls punktu skaits, ja nav atslēgvārdu
        
        for keyword in query.keywords:
            if keyword in workflow_tags:
                match_score += 1.0
            elif keyword in workflow_description:
                match_score += 0.5
        
        return match_score / total_keywords
    
    def _generate_match_reasons(self, result: Dict[str, Any], query: SearchQuery) -> List[str]:
        """Ģenerē iemeslus, kāpēc workflow atbilst vaicājumam"""
        reasons = []
        
        # Pārbauda atslēgvārdu atbilstību
        workflow_tags = result['metadata'].get('tags', [])
        for keyword in query.keywords:
            if keyword in workflow_tags:
                reasons.append(f"Satur {keyword} funkcionalitāti")
        
        # Pārbauda sarežģītības atbilstību
        complexity = result['metadata']['complexity_score']
        if query.complexity_preference == 'simple' and complexity <= 30:
            reasons.append("Vienkāršs workflow")
        elif query.complexity_preference == 'complex' and complexity >= 50:
            reasons.append("Sarežģīts workflow ar daudzām funkcijām")
        
        # Pārbauda mezglu skaitu
        nodes_count = result['metadata']['nodes_count']
        if nodes_count <= 5:
            reasons.append("Kompakts dizains")
        elif nodes_count > 10:
            reasons.append("Plašs funkcionalitātes klāsts")
        
        return reasons
    
    def _generate_modifications(self, result: Dict[str, Any], query: SearchQuery) -> List[str]:
        """Ģenerē ieteikumus workflow modificēšanai"""
        modifications = []
        
        # Ieteikumi, pamatojoties uz vaicājumu
        if query.intent == SearchIntent.MODIFY_EXISTING:
            modifications.append("Var pielāgot mezglu parametrus")
            modifications.append("Var pievienot papildu validācijas soļus")
        
        # Ieteikumi, pamatojoties uz trūkstošajām funkcijām
        workflow_tags = result['metadata'].get('tags', [])
        for keyword in query.keywords:
            if keyword not in workflow_tags:
                modifications.append(f"Var pievienot {keyword} integrāciju")
        
        return modifications

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē komponentus
    openai_client = openai.OpenAI()
    vectorizer = WorkflowVectorizer(openai_client)
    db = QdrantWorkflowDatabase()
    nlp = NaturalLanguageProcessor(openai_client)
    
    # Izveido meklēšanas dzinēju
    search_engine = WorkflowSearchEngine(db, vectorizer, nlp)
    
    # Testa vaicājumi
    test_queries = [
        "Izveidot Telegram botu pierakstam uz tikšanos",
        "Найти workflow для отправки email уведомлений",
        "Create a simple API webhook handler"
    ]
    
    for query in test_queries:
        print(f"\nMeklēšanas vaicājums: {query}")
        results = search_engine.search(query, max_results=3)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.workflow_name} (Score: {result.similarity_score:.3f})")
            print(f"   Iemesli: {', '.join(result.match_reasons)}")
            if result.suggested_modifications:
                print(f"   Ieteikumi: {', '.join(result.suggested_modifications)}")


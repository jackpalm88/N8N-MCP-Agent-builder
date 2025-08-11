#!/usr/bin/env python3
"""
Qdrant Vector Database Design for n8n Workflow AI Agent
Šis modulis nodrošina vektoru datu bāzes funkcionalitāti workflow meklēšanai un salīdzināšanai.
"""

import json
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import openai

@dataclass
class WorkflowMetadata:
    """Workflow metadatu struktūra"""
    id: str
    name: str
    description: str
    category: str
    tags: List[str]
    nodes_count: int
    complexity_score: int
    language: str
    created_at: str
    
@dataclass
class WorkflowVector:
    """Workflow vektora struktūra"""
    id: str
    vector: List[float]
    metadata: WorkflowMetadata
    json_content: Dict[str, Any]

class WorkflowVectorizer:
    """Klase workflow vektorizēšanai"""
    
    def __init__(self, openai_client: openai.OpenAI):
        self.openai_client = openai_client
        
    def extract_workflow_features(self, workflow_json: Dict[str, Any]) -> str:
        """Ekstraktē workflow galvenās iezīmes teksta formātā"""
        features = []
        
        # Workflow nosaukums un apraksts
        if 'name' in workflow_json:
            features.append(f"Workflow name: {workflow_json['name']}")
        
        # Mezglu analīze
        nodes = workflow_json.get('nodes', [])
        node_types = [node.get('type', '').split('.')[-1] for node in nodes]
        unique_node_types = list(set(node_types))
        
        features.append(f"Node types: {', '.join(unique_node_types)}")
        features.append(f"Total nodes: {len(nodes)}")
        
        # Mezglu parametru analīze
        for node in nodes:
            node_name = node.get('name', '')
            node_type = node.get('type', '').split('.')[-1]
            parameters = node.get('parameters', {})
            
            if parameters:
                param_summary = []
                for key, value in parameters.items():
                    if isinstance(value, str) and len(value) < 100:
                        param_summary.append(f"{key}: {value}")
                    elif isinstance(value, (int, float, bool)):
                        param_summary.append(f"{key}: {value}")
                
                if param_summary:
                    features.append(f"{node_type} ({node_name}): {', '.join(param_summary[:3])}")
        
        return " | ".join(features)
    
    def calculate_complexity_score(self, workflow_json: Dict[str, Any]) -> int:
        """Aprēķina workflow sarežģītības punktu skaitu"""
        score = 0
        
        nodes = workflow_json.get('nodes', [])
        connections = workflow_json.get('connections', {})
        
        # Pamata punkti par mezgliem
        score += len(nodes) * 2
        
        # Papildu punkti par savienojumiem
        total_connections = sum(len(conn) for conn in connections.values())
        score += total_connections
        
        # Papildu punkti par sarežģītiem mezgliem
        complex_nodes = ['function', 'code', 'httpRequest', 'webhook']
        for node in nodes:
            node_type = node.get('type', '').split('.')[-1].lower()
            if any(complex_type in node_type for complex_type in complex_nodes):
                score += 5
        
        return min(score, 100)  # Maksimāli 100 punkti
    
    def generate_embedding(self, text: str) -> List[float]:
        """Ģenerē teksta embedding, izmantojot OpenAI API"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Kļūda ģenerējot embedding: {e}")
            # Atgriež nulles vektoru kļūdas gadījumā
            return [0.0] * 1536
    
    def vectorize_workflow(self, workflow_json: Dict[str, Any]) -> WorkflowVector:
        """Pārveido workflow JSON par vektoru"""
        # Ģenerē unikālu ID
        workflow_id = hashlib.md5(json.dumps(workflow_json, sort_keys=True).encode()).hexdigest()
        
        # Ekstraktē iezīmes
        features_text = self.extract_workflow_features(workflow_json)
        
        # Ģenerē vektoru
        vector = self.generate_embedding(features_text)
        
        # Izveido metadatus
        metadata = WorkflowMetadata(
            id=workflow_id,
            name=workflow_json.get('name', 'Unnamed Workflow'),
            description=features_text[:500],  # Ierobežo apraksta garumu
            category=self._determine_category(workflow_json),
            tags=self._extract_tags(workflow_json),
            nodes_count=len(workflow_json.get('nodes', [])),
            complexity_score=self.calculate_complexity_score(workflow_json),
            language='en',  # Noklusējuma valoda
            created_at=workflow_json.get('createdAt', '')
        )
        
        return WorkflowVector(
            id=workflow_id,
            vector=vector,
            metadata=metadata,
            json_content=workflow_json
        )
    
    def _determine_category(self, workflow_json: Dict[str, Any]) -> str:
        """Nosaka workflow kategoriju, pamatojoties uz mezgliem"""
        nodes = workflow_json.get('nodes', [])
        node_types = [node.get('type', '').lower() for node in nodes]
        
        if any('telegram' in node_type for node_type in node_types):
            return 'messaging'
        elif any('webhook' in node_type for node_type in node_types):
            return 'api'
        elif any('email' in node_type or 'gmail' in node_type for node_type in node_types):
            return 'email'
        elif any('database' in node_type or 'mysql' in node_type or 'postgres' in node_type for node_type in node_types):
            return 'database'
        else:
            return 'general'
    
    def _extract_tags(self, workflow_json: Dict[str, Any]) -> List[str]:
        """Ekstraktē tagu sarakstu no workflow"""
        tags = []
        nodes = workflow_json.get('nodes', [])
        
        for node in nodes:
            node_type = node.get('type', '').split('.')[-1].lower()
            if node_type not in tags:
                tags.append(node_type)
        
        return tags[:10]  # Maksimāli 10 tagi

class QdrantWorkflowDatabase:
    """Qdrant datu bāzes pārvaldības klase"""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "n8n_workflows"
        self.vector_size = 1536  # OpenAI ada-002 embedding izmērs
        
    def initialize_collection(self):
        """Inicializē Qdrant kolekciju"""
        try:
            # Pārbauda, vai kolekcija jau eksistē
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Izveidota kolekcija: {self.collection_name}")
            else:
                print(f"Kolekcija jau eksistē: {self.collection_name}")
                
        except Exception as e:
            print(f"Kļūda inicializējot kolekciju: {e}")
    
    def add_workflow(self, workflow_vector: WorkflowVector):
        """Pievieno workflow vektoru datu bāzei"""
        try:
            point = PointStruct(
                id=workflow_vector.id,
                vector=workflow_vector.vector,
                payload={
                    "name": workflow_vector.metadata.name,
                    "description": workflow_vector.metadata.description,
                    "category": workflow_vector.metadata.category,
                    "tags": workflow_vector.metadata.tags,
                    "nodes_count": workflow_vector.metadata.nodes_count,
                    "complexity_score": workflow_vector.metadata.complexity_score,
                    "language": workflow_vector.metadata.language,
                    "created_at": workflow_vector.metadata.created_at,
                    "json_content": json.dumps(workflow_vector.json_content)
                }
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            print(f"Pievienots workflow: {workflow_vector.metadata.name}")
            
        except Exception as e:
            print(f"Kļūda pievienojot workflow: {e}")
    
    def search_similar_workflows(self, query_vector: List[float], limit: int = 5, 
                                category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Meklē līdzīgus workflow"""
        try:
            search_filter = None
            if category_filter:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="category",
                            match=MatchValue(value=category_filter)
                        )
                    ]
                )
            
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=limit,
                with_payload=True
            )
            
            results = []
            for hit in search_result:
                result = {
                    "id": hit.id,
                    "score": hit.score,
                    "metadata": hit.payload,
                    "workflow_json": json.loads(hit.payload["json_content"])
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Kļūda meklējot workflow: {e}")
            return []
    
    def get_workflow_by_id(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Iegūst workflow pēc ID"""
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[workflow_id],
                with_payload=True
            )
            
            if result:
                hit = result[0]
                return {
                    "id": hit.id,
                    "metadata": hit.payload,
                    "workflow_json": json.loads(hit.payload["json_content"])
                }
            return None
            
        except Exception as e:
            print(f"Kļūda iegūstot workflow: {e}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Iegūst kolekcijas statistiku"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "total_workflows": info.points_count,
                "vector_size": info.config.params.vectors.size,
                "distance_metric": info.config.params.vectors.distance
            }
        except Exception as e:
            print(f"Kļūda iegūstot statistiku: {e}")
            return {}

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē OpenAI klientu
    openai_client = openai.OpenAI()
    
    # Izveido vektorizētāju
    vectorizer = WorkflowVectorizer(openai_client)
    
    # Izveido datu bāzes savienojumu
    db = QdrantWorkflowDatabase()
    db.initialize_collection()
    
    # Piemēra workflow JSON
    example_workflow = {
        "name": "Telegram Bot Appointment Booking",
        "nodes": [
            {
                "type": "n8n-nodes-base.telegramTrigger",
                "name": "Telegram Trigger",
                "parameters": {
                    "updates": ["message"]
                }
            },
            {
                "type": "n8n-nodes-base.function",
                "name": "Process Message",
                "parameters": {
                    "functionCode": "// Process appointment booking logic"
                }
            }
        ],
        "connections": {},
        "createdAt": "2025-01-26"
    }
    
    # Vektorizē un pievieno datu bāzei
    workflow_vector = vectorizer.vectorize_workflow(example_workflow)
    db.add_workflow(workflow_vector)
    
    print("Vektoru datu bāze ir iestatīta un gatava lietošanai!")


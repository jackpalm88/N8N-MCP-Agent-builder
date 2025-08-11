#!/usr/bin/env python3
"""
Workflow API Routes for n8n AI Agent
Šis modulis definē API galapunktus workflow ģenerēšanai un pārvaldībai.
"""

import json
import traceback
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import openai

# Importē mūsu moduļus
from src.vector_database_design import QdrantWorkflowDatabase, WorkflowVectorizer
from src.workflow_search_algorithm import WorkflowSearchEngine, NaturalLanguageProcessor
from src.node_configuration_database import NodeConfigurationDatabase
from src.ai_prompt_system import WorkflowGenerator, GenerationContext
from src.multilingual_support import MultilingualSupport

workflow_bp = Blueprint('workflow', __name__)

# Globālie objekti (inicializēsies pirmajā pieprasījumā)
_openai_client = None
_node_db = None
_vector_db = None
_vectorizer = None
_nlp = None
_search_engine = None
_generator = None
_multilingual = None

def initialize_components():
    """Inicializē visus nepieciešamos komponentus"""
    global _openai_client, _node_db, _vector_db, _vectorizer, _nlp, _search_engine, _generator, _multilingual
    
    if _openai_client is None:
        try:
            # Inicializē OpenAI klientu
            _openai_client = openai.OpenAI()
            
            # Inicializē datu bāzes
            _node_db = NodeConfigurationDatabase("src/n8n_nodes.db")
            _vector_db = QdrantWorkflowDatabase(host="localhost", port=6333)
            
            # Mēģina inicializēt Qdrant kolekciju
            try:
                _vector_db.initialize_collection()
            except Exception as e:
                print(f"Qdrant nav pieejams: {e}")
                _vector_db = None
            
            # Inicializē citus komponentus
            _vectorizer = WorkflowVectorizer()
            _nlp = NaturalLanguageProcessor()
            _search_engine = WorkflowSearchEngine(_vector_db, _vectorizer)
            _generator = WorkflowGenerator()
            _multilingual = MultilingualSupport()
            
            print("Visi komponenti veiksmīgi inicializēti")
            
        except Exception as e:
            print(f"Kļūda inicializējot komponentus: {e}")
            traceback.print_exc()
            _vectorizer = WorkflowVectorizer(_openai_client)
            _nlp = NaturalLanguageProcessor(_openai_client)
            
            if _vector_db:
                _search_engine = WorkflowSearchEngine(_vector_db, _vectorizer, _nlp)
            
            _generator = WorkflowGenerator(_openai_client, _node_db)
            
            print("Visi komponenti veiksmīgi inicializēti")
            
        except Exception as e:
            print(f"Kļūda inicializējot komponentus: {e}")
            traceback.print_exc()

@workflow_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Servera veselības pārbaude"""
    initialize_components()
    
    status = {
        "status": "healthy",
        "components": {
            "openai": _openai_client is not None,
            "node_db": _node_db is not None,
            "vector_db": _vector_db is not None,
            "nlp": _nlp is not None,
            "generator": _generator is not None
        }
    }
    
    return jsonify(status)

@workflow_bp.route('/generate', methods=['POST'])
@cross_origin()
def generate_workflow():
    """Ģenerē n8n workflow, pamatojoties uz lietotāja pieprasījumu"""
    initialize_components()
    
    try:
        # Iegūst pieprasījuma datus
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Trūkst 'query' parametra pieprasījumā"
            }), 400
        
        user_query = data['query']
        max_results = data.get('max_results', 3)
        
        # Parsē lietotāja vaicājumu
        search_query = _nlp.parse_query(user_query)
        
        # Meklē līdzīgus workflow (ja Qdrant ir pieejams)
        similar_workflows = []
        if _search_engine and _vector_db:
            try:
                search_results = _search_engine.search(user_query, max_results)
                similar_workflows = [
                    {
                        "workflow_name": result.workflow_name,
                        "similarity_score": result.similarity_score,
                        "workflow_json": result.workflow_json,
                        "metadata": {
                            "description": result.workflow_json.get("name", ""),
                            "complexity_score": 50  # Noklusējuma vērtība
                        }
                    }
                    for result in search_results
                ]
            except Exception as e:
                print(f"Kļūda meklējot workflow: {e}")
        
        # Iegūst pieejamos mezglus
        available_nodes = []
        try:
            # Meklē mezglus, pamatojoties uz atslēgvārdiem
            for keyword in search_query.keywords:
                nodes = _node_db.search_nodes(keyword)
                for node in nodes:
                    node_dict = {
                        "node_id": node.node_id,
                        "display_name": node.display_name,
                        "description": node.description,
                        "category": node.category,
                        "subcategory": node.subcategory
                    }
                    if node_dict not in available_nodes:
                        available_nodes.append(node_dict)
            
            # Ja nav atrasti specifiski mezgli, pievieno populāros
            if not available_nodes:
                popular_nodes = ["webhook", "httpRequest", "function", "telegramTrigger"]
                for node_name in popular_nodes:
                    nodes = _node_db.search_nodes(node_name)
                    for node in nodes:
                        available_nodes.append({
                            "node_id": node.node_id,
                            "display_name": node.display_name,
                            "description": node.description,
                            "category": node.category,
                            "subcategory": node.subcategory
                        })
        except Exception as e:
            print(f"Kļūda iegūstot mezglus: {e}")
        
        # Izveido ģenerēšanas kontekstu
        context = GenerationContext(
            user_query=user_query,
            search_query=search_query,
            similar_workflows=similar_workflows,
            available_nodes=available_nodes,
            language=search_query.language,
            complexity_preference=search_query.complexity_preference
        )
        
        # Ģenerē workflow
        result = _generator.generate_workflow(context)
        
        # Pievieno papildu informāciju
        response = {
            "success": True,
            "query_analysis": {
                "original_query": user_query,
                "detected_language": search_query.language,
                "intent": search_query.intent.value,
                "keywords": search_query.keywords,
                "entities": search_query.entities,
                "complexity_preference": search_query.complexity_preference
            },
            "similar_workflows_found": len(similar_workflows),
            "available_nodes_count": len(available_nodes),
            "generated_workflow": result.get("workflow"),
            "setup_instructions": result.get("setup_instructions", []),
            "explanation": result.get("explanation", ""),
            "errors": result.get("errors", []),
            "fallback_used": result.get("fallback", False)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Kļūda ģenerējot workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Servera kļūda: {str(e)}",
            "generated_workflow": None
        }), 500

@workflow_bp.route('/search', methods=['POST'])
@cross_origin()
def search_workflows():
    """Meklē līdzīgus workflow"""
    initialize_components()
    
    if not _search_engine:
        return jsonify({
            "error": "Meklēšanas dzinējs nav pieejams (Qdrant nav konfigurēts)"
        }), 503
    
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Trūkst 'query' parametra pieprasījumā"
            }), 400
        
        user_query = data['query']
        max_results = data.get('max_results', 5)
        
        # Meklē workflow
        search_results = _search_engine.search(user_query, max_results)
        
        # Formatē rezultātus
        formatted_results = []
        for result in search_results:
            formatted_results.append({
                "workflow_id": result.workflow_id,
                "workflow_name": result.workflow_name,
                "similarity_score": result.similarity_score,
                "match_reasons": result.match_reasons,
                "suggested_modifications": result.suggested_modifications,
                "workflow_json": result.workflow_json
            })
        
        return jsonify({
            "success": True,
            "query": user_query,
            "results_count": len(formatted_results),
            "results": formatted_results
        })
        
    except Exception as e:
        print(f"Kļūda meklējot workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Meklēšanas kļūda: {str(e)}"
        }), 500

@workflow_bp.route('/nodes', methods=['GET'])
@cross_origin()
def get_nodes():
    """Iegūst pieejamos n8n mezglus"""
    initialize_components()
    
    try:
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        search_query = request.args.get('search')
        
        if search_query:
            nodes = _node_db.search_nodes(search_query, category, subcategory)
        elif category:
            nodes = _node_db.get_nodes_by_category(category, subcategory)
        else:
            # Atgriež populārākos mezglus
            popular_node_ids = [
                "n8n-nodes-base.webhook",
                "n8n-nodes-base.httpRequest",
                "n8n-nodes-base.function",
                "n8n-nodes-base.telegramTrigger"
            ]
            nodes = []
            for node_id in popular_node_ids:
                node = _node_db.get_node_configuration(node_id)
                if node:
                    nodes.append(node)
        
        # Formatē rezultātus
        formatted_nodes = []
        for node in nodes:
            formatted_nodes.append({
                "node_id": node.node_id,
                "name": node.name,
                "display_name": node.display_name,
                "description": node.description,
                "category": node.category,
                "subcategory": node.subcategory,
                "parameters_count": len(node.parameters),
                "common_use_cases": node.common_use_cases
            })
        
        return jsonify({
            "success": True,
            "nodes_count": len(formatted_nodes),
            "nodes": formatted_nodes
        })
        
    except Exception as e:
        print(f"Kļūda iegūstot mezglus: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Kļūda iegūstot mezglus: {str(e)}"
        }), 500

@workflow_bp.route('/nodes/<node_id>', methods=['GET'])
@cross_origin()
def get_node_details(node_id):
    """Iegūst detalizētu mezgla informāciju"""
    initialize_components()
    
    try:
        node = _node_db.get_node_configuration(node_id)
        if not node:
            return jsonify({
                "error": f"Mezgls ar ID '{node_id}' nav atrasts"
            }), 404
        
        # Formatē parametrus
        formatted_parameters = []
        for param in node.parameters:
            formatted_parameters.append({
                "name": param.name,
                "type": param.type,
                "description": param.description,
                "required": param.required,
                "default_value": param.default_value,
                "options": param.options,
                "validation_rules": param.validation_rules
            })
        
        return jsonify({
            "success": True,
            "node": {
                "node_id": node.node_id,
                "name": node.name,
                "display_name": node.display_name,
                "description": node.description,
                "category": node.category,
                "subcategory": node.subcategory,
                "icon": node.icon,
                "version": node.version,
                "parameters": formatted_parameters,
                "example_config": node.example_config,
                "common_use_cases": node.common_use_cases,
                "related_nodes": node.related_nodes,
                "documentation_url": node.documentation_url
            }
        })
        
    except Exception as e:
        print(f"Kļūda iegūstot mezgla detaļas: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Kļūda iegūstot mezgla detaļas: {str(e)}"
        }), 500

@workflow_bp.route('/validate', methods=['POST'])
@cross_origin()
def validate_workflow():
    """Validē workflow JSON struktūru"""
    initialize_components()
    
    try:
        data = request.get_json()
        if not data or 'workflow' not in data:
            return jsonify({
                "error": "Trūkst 'workflow' parametra pieprasījumā"
            }), 400
        
        workflow = data['workflow']
        
        # Pamata struktūras validācija
        errors = []
        warnings = []
        
        # Pārbauda obligātās atslēgas
        required_keys = ["name", "nodes", "connections"]
        for key in required_keys:
            if key not in workflow:
                errors.append(f"Trūkst obligātās atslēgas: {key}")
        
        # Validē mezglus
        if "nodes" in workflow and isinstance(workflow["nodes"], list):
            for i, node in enumerate(workflow["nodes"]):
                if "type" not in node:
                    errors.append(f"Mezglam {i} trūkst 'type' atslēgas")
                    continue
                
                # Pārbauda mezgla tipu
                node_config = _node_db.get_node_configuration(node["type"])
                if not node_config:
                    warnings.append(f"Nezināms mezgla tips: {node['type']}")
                elif "parameters" in node:
                    # Validē parametrus
                    is_valid, param_errors = _node_db.validate_node_parameters(
                        node["type"], node["parameters"]
                    )
                    if not is_valid:
                        errors.extend([f"Mezgls {i}: {error}" for error in param_errors])
        
        # Aprēķina kvalitātes punktu skaitu
        quality_score = 100
        if errors:
            quality_score -= len(errors) * 20
        if warnings:
            quality_score -= len(warnings) * 5
        quality_score = max(0, quality_score)
        
        return jsonify({
            "success": True,
            "valid": len(errors) == 0,
            "quality_score": quality_score,
            "errors": errors,
            "warnings": warnings,
            "nodes_count": len(workflow.get("nodes", [])),
            "connections_count": len(workflow.get("connections", {}))
        })
        
    except Exception as e:
        print(f"Kļūda validējot workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Validācijas kļūda: {str(e)}"
        }), 500

@workflow_bp.route('/stats', methods=['GET'])
@cross_origin()
def get_statistics():
    """Iegūst sistēmas statistiku"""
    initialize_components()
    
    try:
        stats = {
            "system_status": "operational",
            "components": {
                "openai_client": _openai_client is not None,
                "node_database": _node_db is not None,
                "vector_database": _vector_db is not None,
                "search_engine": _search_engine is not None,
                "workflow_generator": _generator is not None
            }
        }
        
        # Mezglu statistika
        if _node_db:
            try:
                # Šeit varētu pievienot mezglu skaita aprēķinu
                stats["nodes_available"] = 4  # Noklusējuma mezglu skaits
            except Exception as e:
                print(f"Kļūda iegūstot mezglu statistiku: {e}")
        
        # Vektoru datu bāzes statistika
        if _vector_db:
            try:
                vector_stats = _vector_db.get_collection_stats()
                stats["vector_database_stats"] = vector_stats
            except Exception as e:
                print(f"Kļūda iegūstot vektoru statistiku: {e}")
                stats["vector_database_stats"] = {"error": str(e)}
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        print(f"Kļūda iegūstot statistiku: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Statistikas kļūda: {str(e)}"
        }), 500


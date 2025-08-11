#!/usr/bin/env python3
"""
n8n Integration API Routes
Šis modulis definē API galapunktus n8n integrācijai.
"""

import json
import traceback
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from src.n8n_api_client import N8nApiClient, N8nWorkflowManager, N8nCredentials

n8n_bp = Blueprint('n8n', __name__)

# Globālie objekti
_n8n_client = None
_n8n_manager = None

def get_n8n_client():
    """Iegūst n8n klientu (lazy initialization)"""
    global _n8n_client, _n8n_manager
    
    if _n8n_client is None:
        # Šeit varētu būt konfigurācija no environment variables vai config faila
        # Pagaidām izmanto noklusējuma vērtības
        credentials = N8nCredentials(
            base_url="http://localhost:5678",  # Noklusējuma n8n URL
            api_key="demo-api-key"  # Jāaizstāj ar reālu API atslēgu
        )
        
        _n8n_client = N8nApiClient(credentials)
        _n8n_manager = N8nWorkflowManager(_n8n_client)
    
    return _n8n_client, _n8n_manager

@n8n_bp.route('/configure', methods=['POST'])
@cross_origin()
def configure_n8n_connection():
    """Konfigurē n8n savienojumu"""
    global _n8n_client, _n8n_manager
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Trūkst konfigurācijas datu"
            }), 400
        
        base_url = data.get('base_url')
        api_key = data.get('api_key')
        
        if not base_url or not api_key:
            return jsonify({
                "error": "Trūkst 'base_url' vai 'api_key' parametru"
            }), 400
        
        # Izveido jaunus kredenciālus
        credentials = N8nCredentials(base_url=base_url, api_key=api_key)
        
        # Inicializē jaunu klientu
        _n8n_client = N8nApiClient(credentials)
        _n8n_manager = N8nWorkflowManager(_n8n_client)
        
        # Pārbauda savienojumu
        connection_ok, message = _n8n_client.verify_connection()
        
        return jsonify({
            "success": connection_ok,
            "message": message,
            "configured_url": base_url
        })
        
    except Exception as e:
        print(f"Kļūda konfigurējot n8n savienojumu: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Konfigurācijas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/connection/test', methods=['GET'])
@cross_origin()
def test_n8n_connection():
    """Testē n8n savienojumu"""
    try:
        client, manager = get_n8n_client()
        
        connection_ok, message = client.verify_connection()
        
        return jsonify({
            "success": connection_ok,
            "message": message,
            "base_url": client.credentials.base_url
        })
        
    except Exception as e:
        print(f"Kļūda testējot n8n savienojumu: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Savienojuma testa kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows', methods=['GET'])
@cross_origin()
def get_n8n_workflows():
    """Iegūst n8n workflow sarakstu"""
    try:
        client, manager = get_n8n_client()
        
        limit = request.args.get('limit', 50, type=int)
        
        success, workflows, message = client.get_workflows(limit)
        
        if success:
            # Formatē workflow sarakstu
            formatted_workflows = []
            for workflow in workflows:
                formatted_workflows.append({
                    "id": workflow.get('id'),
                    "name": workflow.get('name'),
                    "active": workflow.get('active', False),
                    "nodes_count": len(workflow.get('nodes', [])),
                    "created_at": workflow.get('createdAt'),
                    "updated_at": workflow.get('updatedAt')
                })
            
            return jsonify({
                "success": True,
                "message": message,
                "workflows_count": len(formatted_workflows),
                "workflows": formatted_workflows
            })
        else:
            return jsonify({
                "success": False,
                "error": message,
                "workflows": []
            }), 500
            
    except Exception as e:
        print(f"Kļūda iegūstot n8n workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Kļūda iegūstot workflow: {str(e)}",
            "workflows": []
        }), 500

@n8n_bp.route('/workflows/<workflow_id>', methods=['GET'])
@cross_origin()
def get_n8n_workflow(workflow_id):
    """Iegūst konkrētu n8n workflow"""
    try:
        client, manager = get_n8n_client()
        
        success, workflow, message = client.get_workflow_by_id(workflow_id)
        
        if success and workflow:
            return jsonify({
                "success": True,
                "message": message,
                "workflow": workflow
            })
        else:
            return jsonify({
                "success": False,
                "error": message,
                "workflow": None
            }), 404 if "nav atrasts" in message.lower() else 500
            
    except Exception as e:
        print(f"Kļūda iegūstot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Kļūda iegūstot workflow: {str(e)}",
            "workflow": None
        }), 500

@n8n_bp.route('/workflows/upload', methods=['POST'])
@cross_origin()
def upload_workflow_to_n8n():
    """Augšupielādē workflow uz n8n"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Trūkst workflow datu"
            }), 400
        
        workflow_data = data.get('workflow')
        if not workflow_data:
            return jsonify({
                "error": "Trūkst 'workflow' parametra"
            }), 400
        
        # Papildu opcijas
        activate = data.get('activate', False)
        test_execution = data.get('test_execution', False)
        
        client, manager = get_n8n_client()
        
        # Pārbauda savienojumu
        connection_ok, connection_message = client.verify_connection()
        if not connection_ok:
            return jsonify({
                "success": False,
                "error": f"n8n nav pieejams: {connection_message}"
            }), 503
        
        # Augšupielādē workflow
        result = manager.upload_generated_workflow(
            workflow_data, 
            activate=activate, 
            test_execution=test_execution
        )
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": result['message'],
                "workflow_id": result['workflow_id'],
                "workflow_name": result['workflow_name'],
                "activation": result.get('activation'),
                "test_execution": result.get('test_execution'),
                "n8n_url": f"{client.credentials.base_url}/workflow/{result['workflow_id']}"
            })
        else:
            return jsonify({
                "success": False,
                "error": result['message'],
                "errors": result['errors'],
                "workflow_name": result['workflow_name']
            }), 400
            
    except Exception as e:
        print(f"Kļūda augšupielādējot workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Augšupielādes kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows/<workflow_id>/update', methods=['PUT'])
@cross_origin()
def update_n8n_workflow(workflow_id):
    """Atjaunina esošu n8n workflow"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Trūkst workflow datu"
            }), 400
        
        workflow_data = data.get('workflow')
        if not workflow_data:
            return jsonify({
                "error": "Trūkst 'workflow' parametra"
            }), 400
        
        client, manager = get_n8n_client()
        
        # Atjaunina workflow
        result = client.update_workflow(workflow_id, workflow_data)
        
        if result.success:
            return jsonify({
                "success": True,
                "message": result.message,
                "workflow_id": workflow_id,
                "workflow_name": result.workflow_name,
                "n8n_url": f"{client.credentials.base_url}/workflow/{workflow_id}"
            })
        else:
            return jsonify({
                "success": False,
                "error": result.message,
                "errors": result.errors
            }), 400
            
    except Exception as e:
        print(f"Kļūda atjauninot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Atjaunināšanas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows/<workflow_id>/activate', methods=['POST'])
@cross_origin()
def activate_n8n_workflow(workflow_id):
    """Aktivizē n8n workflow"""
    try:
        client, manager = get_n8n_client()
        
        success, message = client.activate_workflow(workflow_id)
        
        return jsonify({
            "success": success,
            "message": message,
            "workflow_id": workflow_id
        })
        
    except Exception as e:
        print(f"Kļūda aktivizējot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Aktivizācijas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows/<workflow_id>/deactivate', methods=['POST'])
@cross_origin()
def deactivate_n8n_workflow(workflow_id):
    """Deaktivizē n8n workflow"""
    try:
        client, manager = get_n8n_client()
        
        success, message = client.deactivate_workflow(workflow_id)
        
        return jsonify({
            "success": success,
            "message": message,
            "workflow_id": workflow_id
        })
        
    except Exception as e:
        print(f"Kļūda deaktivizējot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Deaktivizācijas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows/<workflow_id>/delete', methods=['DELETE'])
@cross_origin()
def delete_n8n_workflow(workflow_id):
    """Dzēš n8n workflow"""
    try:
        client, manager = get_n8n_client()
        
        success, message = client.delete_workflow(workflow_id)
        
        return jsonify({
            "success": success,
            "message": message,
            "workflow_id": workflow_id
        })
        
    except Exception as e:
        print(f"Kļūda dzēšot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Dzēšanas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/workflows/<workflow_id>/test', methods=['POST'])
@cross_origin()
def test_n8n_workflow(workflow_id):
    """Testē n8n workflow izpildi"""
    try:
        data = request.get_json() or {}
        test_data = data.get('test_data')
        
        client, manager = get_n8n_client()
        
        success, result, message = client.test_workflow_execution(workflow_id, test_data)
        
        return jsonify({
            "success": success,
            "message": message,
            "workflow_id": workflow_id,
            "execution_result": result if success else None
        })
        
    except Exception as e:
        print(f"Kļūda testējot workflow {workflow_id}: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Testa kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/statistics', methods=['GET'])
@cross_origin()
def get_n8n_statistics():
    """Iegūst n8n integrācijas statistiku"""
    try:
        client, manager = get_n8n_client()
        
        # Iegūst upload statistiku
        upload_stats = manager.get_upload_statistics()
        
        # Pārbauda savienojumu
        connection_ok, connection_message = client.verify_connection()
        
        # Mēģina iegūt workflow skaitu
        workflow_count = 0
        if connection_ok:
            success, workflows, message = client.get_workflows(limit=1000)
            if success:
                workflow_count = len(workflows)
        
        return jsonify({
            "success": True,
            "statistics": {
                "connection_status": "connected" if connection_ok else "disconnected",
                "connection_message": connection_message,
                "n8n_base_url": client.credentials.base_url,
                "total_workflows_in_n8n": workflow_count,
                "upload_statistics": upload_stats
            }
        })
        
    except Exception as e:
        print(f"Kļūda iegūstot n8n statistiku: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Statistikas kļūda: {str(e)}"
        }), 500

@n8n_bp.route('/generate-and-upload', methods=['POST'])
@cross_origin()
def generate_and_upload_workflow():
    """Ģenerē workflow un uzreiz augšupielādē to n8n"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Trūkst pieprasījuma datu"
            }), 400
        
        user_query = data.get('query')
        if not user_query:
            return jsonify({
                "error": "Trūkst 'query' parametra"
            }), 400
        
        # Papildu opcijas
        activate = data.get('activate', False)
        test_execution = data.get('test_execution', False)
        max_results = data.get('max_results', 3)
        
        # Importē workflow ģenerēšanas komponentus
        from src.routes.workflow import initialize_components, _generator, _nlp
        
        # Inicializē komponentus
        initialize_components()
        
        if not _generator or not _nlp:
            return jsonify({
                "success": False,
                "error": "Workflow ģenerēšanas komponenti nav pieejami"
            }), 503
        
        # Parsē vaicājumu
        search_query = _nlp.parse_query(user_query)
        
        # Izveido ģenerēšanas kontekstu
        from src.ai_prompt_system import GenerationContext
        context = GenerationContext(
            user_query=user_query,
            search_query=search_query,
            similar_workflows=[],
            available_nodes=[],
            language=search_query.language,
            complexity_preference=search_query.complexity_preference
        )
        
        # Ģenerē workflow
        generation_result = _generator.generate_workflow(context)
        
        if not generation_result.get('workflow'):
            return jsonify({
                "success": False,
                "error": "Neizdevās ģenerēt workflow",
                "generation_result": generation_result
            }), 400
        
        # Augšupielādē uz n8n
        client, manager = get_n8n_client()
        
        # Pārbauda n8n savienojumu
        connection_ok, connection_message = client.verify_connection()
        if not connection_ok:
            return jsonify({
                "success": False,
                "error": f"n8n nav pieejams: {connection_message}",
                "generation_result": generation_result
            }), 503
        
        # Augšupielādē workflow
        upload_result = manager.upload_generated_workflow(
            generation_result['workflow'],
            activate=activate,
            test_execution=test_execution
        )
        
        # Kombinē rezultātus
        combined_result = {
            "success": upload_result['success'],
            "message": f"Workflow ģenerēts un {'veiksmīgi augšupielādēts' if upload_result['success'] else 'augšupielādes kļūda'}",
            "generation": {
                "query_analysis": {
                    "original_query": user_query,
                    "detected_language": search_query.language,
                    "intent": search_query.intent.value,
                    "keywords": search_query.keywords,
                    "complexity_preference": search_query.complexity_preference
                },
                "generated_workflow": generation_result.get('workflow'),
                "setup_instructions": generation_result.get('setup_instructions', []),
                "explanation": generation_result.get('explanation', ''),
                "errors": generation_result.get('errors', [])
            },
            "n8n_upload": {
                "success": upload_result['success'],
                "workflow_id": upload_result.get('workflow_id'),
                "workflow_name": upload_result.get('workflow_name'),
                "message": upload_result.get('message'),
                "errors": upload_result.get('errors', []),
                "n8n_url": f"{client.credentials.base_url}/workflow/{upload_result.get('workflow_id')}" if upload_result.get('workflow_id') else None,
                "activation": upload_result.get('activation'),
                "test_execution": upload_result.get('test_execution')
            }
        }
        
        return jsonify(combined_result)
        
    except Exception as e:
        print(f"Kļūda ģenerējot un augšupielādējot workflow: {e}")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": f"Ģenerēšanas un augšupielādes kļūda: {str(e)}"
        }), 500


#!/usr/bin/env python3
"""
n8n API Client for Workflow Management
Šis modulis nodrošina integrāciju ar n8n API workflow pārvaldībai.
"""

import json
import requests
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import time

@dataclass
class N8nCredentials:
    """n8n API kredenciāļu struktūra"""
    base_url: str
    api_key: str
    
    def __post_init__(self):
        # Nodrošina, ka base_url beidzas bez slīpsvītras
        self.base_url = self.base_url.rstrip('/')

@dataclass
class WorkflowUploadResult:
    """Workflow augšupielādes rezultāta struktūra"""
    success: bool
    workflow_id: Optional[str]
    workflow_name: str
    message: str
    errors: List[str]
    n8n_response: Optional[Dict[str, Any]]

class N8nApiClient:
    """n8n API klients workflow pārvaldībai"""
    
    def __init__(self, credentials: N8nCredentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.session.headers.update({
            'X-N8N-API-KEY': credentials.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Pārbauda savienojumu inicializācijas laikā
        self.connection_verified = False
    
    def verify_connection(self) -> Tuple[bool, str]:
        """Pārbauda savienojumu ar n8n API"""
        try:
            response = self.session.get(f"{self.credentials.base_url}/api/v1/workflows", timeout=10)
            
            if response.status_code == 200:
                self.connection_verified = True
                return True, "Savienojums ar n8n API veiksmīgs"
            elif response.status_code == 401:
                return False, "Nederīga API atslēga"
            elif response.status_code == 404:
                return False, "n8n API nav atrasts šajā URL"
            else:
                return False, f"API atgrieza kļūdu: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return False, "Nevar izveidot savienojumu ar n8n serveri"
        except requests.exceptions.Timeout:
            return False, "Savienojuma timeout"
        except Exception as e:
            return False, f"Neparedzēta kļūda: {str(e)}"
    
    def get_workflows(self, limit: int = 100) -> Tuple[bool, List[Dict[str, Any]], str]:
        """Iegūst visu workflow sarakstu"""
        try:
            params = {'limit': limit}
            response = self.session.get(
                f"{self.credentials.base_url}/api/v1/workflows",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                workflows = data.get('data', [])
                return True, workflows, f"Iegūti {len(workflows)} workflow"
            else:
                return False, [], f"API kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, [], f"Kļūda iegūstot workflow: {str(e)}"
    
    def get_workflow_by_id(self, workflow_id: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """Iegūst konkrētu workflow pēc ID"""
        try:
            response = self.session.get(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                workflow = response.json()
                return True, workflow, "Workflow iegūts veiksmīgi"
            elif response.status_code == 404:
                return False, None, f"Workflow ar ID '{workflow_id}' nav atrasts"
            else:
                return False, None, f"API kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, None, f"Kļūda iegūstot workflow: {str(e)}"
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> WorkflowUploadResult:
        """Izveido jaunu workflow n8n sistēmā"""
        try:
            # Validē workflow struktūru
            validation_result = self._validate_workflow_structure(workflow_data)
            if not validation_result[0]:
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=None,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message="Workflow validācija neizdevās",
                    errors=validation_result[1],
                    n8n_response=None
                )
            
            # Sagatavo datus n8n API formātam
            api_payload = self._prepare_workflow_for_api(workflow_data)
            
            # Nosūta pieprasījumu
            response = self.session.post(
                f"{self.credentials.base_url}/api/v1/workflows",
                json=api_payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result_data = response.json()
                return WorkflowUploadResult(
                    success=True,
                    workflow_id=result_data.get('id'),
                    workflow_name=result_data.get('name', workflow_data.get('name', 'Unknown')),
                    message="Workflow veiksmīgi izveidots n8n sistēmā",
                    errors=[],
                    n8n_response=result_data
                )
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=None,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message="Workflow dati nav derīgi",
                    errors=[error_data.get('message', 'Nezināma validācijas kļūda')],
                    n8n_response=error_data
                )
            elif response.status_code == 401:
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=None,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message="Autentifikācijas kļūda",
                    errors=["Nederīga API atslēga"],
                    n8n_response=None
                )
            else:
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=None,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message=f"n8n API kļūda: {response.status_code}",
                    errors=[response.text],
                    n8n_response=None
                )
                
        except requests.exceptions.Timeout:
            return WorkflowUploadResult(
                success=False,
                workflow_id=None,
                workflow_name=workflow_data.get('name', 'Unknown'),
                message="Pieprasījuma timeout",
                errors=["Savienojums ar n8n serveri pārtrūka"],
                n8n_response=None
            )
        except Exception as e:
            return WorkflowUploadResult(
                success=False,
                workflow_id=None,
                workflow_name=workflow_data.get('name', 'Unknown'),
                message="Neparedzēta kļūda",
                errors=[str(e)],
                n8n_response=None
            )
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> WorkflowUploadResult:
        """Atjaunina esošu workflow"""
        try:
            # Validē workflow struktūru
            validation_result = self._validate_workflow_structure(workflow_data)
            if not validation_result[0]:
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=workflow_id,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message="Workflow validācija neizdevās",
                    errors=validation_result[1],
                    n8n_response=None
                )
            
            # Sagatavo datus
            api_payload = self._prepare_workflow_for_api(workflow_data)
            
            # Nosūta PUT pieprasījumu
            response = self.session.put(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}",
                json=api_payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result_data = response.json()
                return WorkflowUploadResult(
                    success=True,
                    workflow_id=workflow_id,
                    workflow_name=result_data.get('name', workflow_data.get('name', 'Unknown')),
                    message="Workflow veiksmīgi atjaunināts",
                    errors=[],
                    n8n_response=result_data
                )
            else:
                return WorkflowUploadResult(
                    success=False,
                    workflow_id=workflow_id,
                    workflow_name=workflow_data.get('name', 'Unknown'),
                    message=f"Atjaunināšanas kļūda: {response.status_code}",
                    errors=[response.text],
                    n8n_response=None
                )
                
        except Exception as e:
            return WorkflowUploadResult(
                success=False,
                workflow_id=workflow_id,
                workflow_name=workflow_data.get('name', 'Unknown'),
                message="Atjaunināšanas kļūda",
                errors=[str(e)],
                n8n_response=None
            )
    
    def activate_workflow(self, workflow_id: str) -> Tuple[bool, str]:
        """Aktivizē workflow"""
        try:
            response = self.session.post(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}/activate",
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "Workflow aktivizēts veiksmīgi"
            else:
                return False, f"Aktivizācijas kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"Kļūda aktivizējot workflow: {str(e)}"
    
    def deactivate_workflow(self, workflow_id: str) -> Tuple[bool, str]:
        """Deaktivizē workflow"""
        try:
            response = self.session.post(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}/deactivate",
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "Workflow deaktivizēts veiksmīgi"
            else:
                return False, f"Deaktivizācijas kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"Kļūda deaktivizējot workflow: {str(e)}"
    
    def delete_workflow(self, workflow_id: str) -> Tuple[bool, str]:
        """Dzēš workflow"""
        try:
            response = self.session.delete(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                return True, "Workflow dzēsts veiksmīgi"
            elif response.status_code == 404:
                return False, "Workflow nav atrasts"
            else:
                return False, f"Dzēšanas kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, f"Kļūda dzēšot workflow: {str(e)}"
    
    def _validate_workflow_structure(self, workflow_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validē workflow struktūru pirms augšupielādes"""
        errors = []
        
        # Pārbauda obligātās atslēgas
        required_keys = ['name', 'nodes']
        for key in required_keys:
            if key not in workflow_data:
                errors.append(f"Trūkst obligātās atslēgas: {key}")
        
        # Pārbauda mezglus
        if 'nodes' in workflow_data:
            if not isinstance(workflow_data['nodes'], list):
                errors.append("'nodes' jābūt masīvam")
            else:
                for i, node in enumerate(workflow_data['nodes']):
                    if not isinstance(node, dict):
                        errors.append(f"Mezgls {i} nav objekts")
                        continue
                    
                    if 'type' not in node:
                        errors.append(f"Mezglam {i} trūkst 'type' atslēgas")
                    
                    if 'name' not in node:
                        errors.append(f"Mezglam {i} trūkst 'name' atslēgas")
        
        # Pārbauda savienojumus
        if 'connections' in workflow_data:
            if not isinstance(workflow_data['connections'], dict):
                errors.append("'connections' jābūt objektam")
        
        return len(errors) == 0, errors
    
    def _prepare_workflow_for_api(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sagatavo workflow datus n8n API formātam"""
        # Izveido kopiju, lai nesabojātu oriģinālos datus
        api_data = workflow_data.copy()
        
        # Pārbauda un pievieno noklusējuma vērtības
        if 'active' not in api_data:
            api_data['active'] = False
        
        if 'settings' not in api_data:
            api_data['settings'] = {
                'saveExecutionProgress': True,
                'saveManualExecutions': True,
                'saveDataErrorExecution': 'all',
                'saveDataSuccessExecution': 'all',
                'executionTimeout': 3600,
                'timezone': 'America/New_York'
            }
        
        if 'staticData' not in api_data:
            api_data['staticData'] = {}
        
        # Pārbauda mezglu ID un pozīcijas
        if 'nodes' in api_data:
            for i, node in enumerate(api_data['nodes']):
                # Pievieno ID, ja nav
                if 'id' not in node:
                    node['id'] = f"node_{i}_{int(time.time())}"
                
                # Pievieno pozīciju, ja nav
                if 'position' not in node:
                    node['position'] = [100 + (i * 200), 100]
                
                # Pārbauda parametrus
                if 'parameters' not in node:
                    node['parameters'] = {}
        
        return api_data
    
    def test_workflow_execution(self, workflow_id: str, test_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, Dict[str, Any], str]:
        """Testē workflow izpildi"""
        try:
            payload = {}
            if test_data:
                payload['data'] = test_data
            
            response = self.session.post(
                f"{self.credentials.base_url}/api/v1/workflows/{workflow_id}/execute",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return True, result, "Workflow tests veiksmīgs"
            else:
                return False, {}, f"Testa kļūda: {response.status_code} - {response.text}"
                
        except Exception as e:
            return False, {}, f"Kļūda testējot workflow: {str(e)}"

class N8nWorkflowManager:
    """Augsta līmeņa workflow pārvaldības klase"""
    
    def __init__(self, api_client: N8nApiClient):
        self.api_client = api_client
        self.upload_history = []
    
    def upload_generated_workflow(self, workflow_data: Dict[str, Any], 
                                 activate: bool = False,
                                 test_execution: bool = False) -> Dict[str, Any]:
        """Augšupielādē ģenerēto workflow ar papildu opcijām"""
        
        # Pārbauda savienojumu
        if not self.api_client.connection_verified:
            connection_ok, message = self.api_client.verify_connection()
            if not connection_ok:
                return {
                    'success': False,
                    'message': f'Savienojuma kļūda: {message}',
                    'workflow_id': None
                }
        
        # Augšupielādē workflow
        upload_result = self.api_client.create_workflow(workflow_data)
        
        result = {
            'success': upload_result.success,
            'message': upload_result.message,
            'workflow_id': upload_result.workflow_id,
            'workflow_name': upload_result.workflow_name,
            'errors': upload_result.errors,
            'n8n_response': upload_result.n8n_response
        }
        
        # Ja augšupielāde veiksmīga, veic papildu darbības
        if upload_result.success and upload_result.workflow_id:
            
            # Aktivizē, ja pieprasīts
            if activate:
                activate_success, activate_message = self.api_client.activate_workflow(upload_result.workflow_id)
                result['activation'] = {
                    'success': activate_success,
                    'message': activate_message
                }
            
            # Testē izpildi, ja pieprasīts
            if test_execution:
                test_success, test_result, test_message = self.api_client.test_workflow_execution(upload_result.workflow_id)
                result['test_execution'] = {
                    'success': test_success,
                    'result': test_result,
                    'message': test_message
                }
        
        # Saglabā vēsturē
        self.upload_history.append({
            'timestamp': time.time(),
            'workflow_name': upload_result.workflow_name,
            'success': upload_result.success,
            'workflow_id': upload_result.workflow_id
        })
        
        return result
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """Iegūst augšupielādes statistiku"""
        total_uploads = len(self.upload_history)
        successful_uploads = sum(1 for upload in self.upload_history if upload['success'])
        
        return {
            'total_uploads': total_uploads,
            'successful_uploads': successful_uploads,
            'success_rate': (successful_uploads / total_uploads * 100) if total_uploads > 0 else 0,
            'recent_uploads': self.upload_history[-5:] if self.upload_history else []
        }

# Lietošanas piemērs
if __name__ == "__main__":
    # Testa konfigurācija
    credentials = N8nCredentials(
        base_url="http://localhost:5678",  # Noklusējuma n8n URL
        api_key="your-api-key-here"
    )
    
    # Inicializē klientu
    api_client = N8nApiClient(credentials)
    
    # Pārbauda savienojumu
    connection_ok, message = api_client.verify_connection()
    print(f"Savienojuma pārbaude: {message}")
    
    if connection_ok:
        # Iegūst workflow sarakstu
        success, workflows, message = api_client.get_workflows(limit=5)
        print(f"Workflow saraksts: {message}")
        
        if success:
            print(f"Atrasti {len(workflows)} workflow:")
            for workflow in workflows:
                print(f"- {workflow.get('name', 'Unknown')} (ID: {workflow.get('id')})")
        
        # Testa workflow izveide
        test_workflow = {
            "name": "Test Workflow from API",
            "nodes": [
                {
                    "type": "n8n-nodes-base.webhook",
                    "name": "Webhook",
                    "parameters": {
                        "httpMethod": "POST",
                        "path": "test-webhook"
                    }
                },
                {
                    "type": "n8n-nodes-base.function",
                    "name": "Process Data",
                    "parameters": {
                        "functionCode": "return [{ json: { message: 'Hello from API!' } }];"
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
        
        # Izveido workflow
        manager = N8nWorkflowManager(api_client)
        result = manager.upload_generated_workflow(test_workflow, activate=False)
        
        print(f"Workflow izveides rezultāts: {result['message']}")
        if result['success']:
            print(f"Workflow ID: {result['workflow_id']}")
    else:
        print("Nevar izveidot savienojumu ar n8n API")


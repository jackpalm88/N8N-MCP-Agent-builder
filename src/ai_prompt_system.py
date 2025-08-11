#!/usr/bin/env python3
"""
AI Prompt System for n8n Workflow Generation
Šis modulis implementē strukturētus promptus n8n workflow ģenerēšanai.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from src.node_configuration_database import NodeConfigurationDatabase
from src.workflow_search_algorithm import SearchQuery, SearchIntent

class PromptType(Enum):
    """Prompt tipu enumerācija"""
    WORKFLOW_GENERATION = "workflow_generation"
    WORKFLOW_MODIFICATION = "workflow_modification"
    WORKFLOW_EXPLANATION = "workflow_explanation"
    NODE_CONFIGURATION = "node_configuration"

@dataclass
class PromptTemplate:
    """Prompt veidnes struktūra"""
    name: str
    type: PromptType
    system_prompt: str
    user_prompt_template: str
    variables: List[str]
    examples: List[Dict[str, str]]
    validation_rules: List[str]

@dataclass
class GenerationContext:
    """Workflow ģenerēšanas konteksts"""
    user_query: str
    search_query: SearchQuery
    similar_workflows: List[Dict[str, Any]]
    available_nodes: List[Dict[str, Any]]
    language: str
    complexity_preference: str

class PromptTemplateManager:
    """Prompt veidņu pārvaldības klase"""
    
    def __init__(self):
        self.templates = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Inicializē prompt veidnes"""
        
        # Workflow ģenerēšanas prompt
        workflow_generation_template = PromptTemplate(
            name="workflow_generation",
            type=PromptType.WORKFLOW_GENERATION,
            system_prompt="""Tu esi eksperts n8n workflow automatizācijas sistēmā. Tava uzdevums ir izveidot precīzus, funkcionālus n8n workflow JSON failus, pamatojoties uz lietotāja prasībām dabiskajā valodā.

SVARĪGAS INSTRUKCIJAS:
1. Vienmēr izveido pilnīgu, derīgu n8n workflow JSON struktūru
2. Izmanto tikai eksistējošus n8n mezglus (nodes)
3. Nodrošini pareizus savienojumus starp mezgliem
4. Iekļauj nepieciešamos parametrus katram mezglam
5. Pievienot komentārus un paskaidrojumus
6. Ievēro n8n JSON formāta prasības

PIEEJAMIE MEZGLI:
{available_nodes}

LĪDZĪGIE WORKFLOW PIEMĒRI:
{similar_workflows}

Atbildi JSON formātā ar šādu struktūru:
{{
  "workflow": {{
    "name": "Workflow nosaukums",
    "nodes": [...],
    "connections": {{...}},
    "active": true
  }},
  "setup_instructions": [
    "Instrukcija 1",
    "Instrukcija 2"
  ],
  "explanation": "Detalizēts paskaidrojums par workflow darbību"
}}""",
            user_prompt_template="""Lietotāja pieprasījums: {user_query}

Valoda: {language}
Sarežģītības līmenis: {complexity_preference}

Papildu konteksts:
- Atslēgvārdi: {keywords}
- Entītijas: {entities}
- Nolūks: {intent}

Lūdzu, izveido n8n workflow, kas atbilst šim pieprasījumam.""",
            variables=["user_query", "language", "complexity_preference", "keywords", "entities", "intent", "available_nodes", "similar_workflows"],
            examples=[
                {
                    "input": "Izveidot Telegram botu pierakstam uz tikšanos",
                    "output": "Workflow ar Telegram Trigger, Function mezglu validācijai, un datu bāzes mezglu pierakstu glabāšanai"
                }
            ],
            validation_rules=[
                "JSON jābūt derīgam n8n formātam",
                "Visiem mezgliem jābūt pareiziem parametriem",
                "Savienojumiem jābūt loģiskiem"
            ]
        )
        
        # Workflow modificēšanas prompt
        workflow_modification_template = PromptTemplate(
            name="workflow_modification",
            type=PromptType.WORKFLOW_MODIFICATION,
            system_prompt="""Tu esi n8n workflow modificēšanas eksperts. Tava uzdevums ir pielāgot esošos workflow, pamatojoties uz lietotāja prasībām.

MODIFICĒŠANAS PRINCIPI:
1. Saglabā esošo workflow struktūru, ja iespējams
2. Pievieno jaunus mezglus tikai, ja nepieciešams
3. Modificē parametrus, nevis aizstāj mezglus
4. Nodrošini atpakaļsaderību
5. Dokumentē visas izmaiņas

ESOŠAIS WORKFLOW:
{existing_workflow}

Atbildi JSON formātā ar modificēto workflow un izmaiņu aprakstu.""",
            user_prompt_template="""Modificēšanas pieprasījums: {user_query}

Esošais workflow: {existing_workflow}

Lūdzu, modificē workflow atbilstoši pieprasījumam.""",
            variables=["user_query", "existing_workflow"],
            examples=[],
            validation_rules=["Modificētajam workflow jāsaglabā saderība"]
        )
        
        # Workflow paskaidrošanas prompt
        workflow_explanation_template = PromptTemplate(
            name="workflow_explanation",
            type=PromptType.WORKFLOW_EXPLANATION,
            system_prompt="""Tu esi n8n workflow skaidrotājs. Tava uzdevums ir sniegt skaidrus, saprotamus paskaidrojumus par workflow darbību.

PASKAIDROJUMA STRUKTŪRA:
1. Īss workflow apraksts
2. Detalizēts soļu apraksts
3. Mezglu funkciju skaidrojums
4. Datu plūsmas analīze
5. Lietošanas scenāriji

Paskaidro {language} valodā.""",
            user_prompt_template="""Workflow analīzei: {workflow_json}

Lietotāja jautājums: {user_query}

Lūdzu, paskaidro šo workflow darbību.""",
            variables=["workflow_json", "user_query", "language"],
            examples=[],
            validation_rules=["Paskaidrojumam jābūt skaidram un precīzam"]
        )
        
        # Saglabā veidnes
        self.templates[workflow_generation_template.name] = workflow_generation_template
        self.templates[workflow_modification_template.name] = workflow_modification_template
        self.templates[workflow_explanation_template.name] = workflow_explanation_template
    
    def get_template(self, template_name: str) -> Optional[PromptTemplate]:
        """Iegūst prompt veidni pēc nosaukuma"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """Atgriež visu pieejamo veidņu sarakstu"""
        return list(self.templates.keys())

class PromptOptimizer:
    """Prompt optimizācijas klase"""
    
    def __init__(self, openai_client: openai.OpenAI):
        self.openai_client = openai_client
        self.optimization_history = []
    
    def optimize_prompt_for_context(self, template: PromptTemplate, context: GenerationContext) -> str:
        """Optimizē prompt konkrētam kontekstam"""
        
        # Sagatavo mainīgos
        variables = {
            "user_query": context.user_query,
            "language": context.language,
            "complexity_preference": context.complexity_preference,
            "keywords": ", ".join(context.search_query.keywords),
            "entities": json.dumps(context.search_query.entities, ensure_ascii=False),
            "intent": context.search_query.intent.value,
            "available_nodes": self._format_available_nodes(context.available_nodes),
            "similar_workflows": self._format_similar_workflows(context.similar_workflows)
        }
        
        # Aizstāj mainīgos veidnē
        optimized_prompt = template.user_prompt_template
        for var_name, var_value in variables.items():
            placeholder = "{" + var_name + "}"
            optimized_prompt = optimized_prompt.replace(placeholder, str(var_value))
        
        # Pielāgo prompt garumu atkarībā no sarežģītības
        if context.complexity_preference == "simple":
            optimized_prompt += "\n\nLūdzu, izveido vienkāršu workflow ar minimālu mezglu skaitu."
        elif context.complexity_preference == "complex":
            optimized_prompt += "\n\nLūdzu, izveido detalizētu workflow ar pilnu funkcionalitāti un kļūdu apstrādi."
        
        # Pielāgo valodai
        if context.language == "lv":
            optimized_prompt += "\n\nAtbildi latviešu valodā ar latviešu komentāriem workflow."
        elif context.language == "ru":
            optimized_prompt += "\n\nОтветь на русском языке с русскими комментариями в workflow."
        
        return optimized_prompt
    
    def _format_available_nodes(self, nodes: List[Dict[str, Any]]) -> str:
        """Formatē pieejamos mezglus prompt iekļaušanai"""
        if not nodes:
            return "Nav norādīti specifiski mezgli"
        
        formatted_nodes = []
        for node in nodes[:10]:  # Ierobežo līdz 10 mezgliem
            node_info = f"- {node.get('display_name', 'Unknown')}: {node.get('description', '')}"
            formatted_nodes.append(node_info)
        
        return "\n".join(formatted_nodes)
    
    def _format_similar_workflows(self, workflows: List[Dict[str, Any]]) -> str:
        """Formatē līdzīgos workflow prompt iekļaušanai"""
        if not workflows:
            return "Nav atrasti līdzīgi workflow"
        
        formatted_workflows = []
        for workflow in workflows[:3]:  # Ierobežo līdz 3 piemēriem
            workflow_info = f"Piemērs: {workflow.get('workflow_name', 'Unknown')}\n"
            workflow_info += f"Apraksts: {workflow.get('metadata', {}).get('description', '')[:200]}...\n"
            formatted_workflows.append(workflow_info)
        
        return "\n".join(formatted_workflows)

class WorkflowGenerator:
    """Galvenā workflow ģenerēšanas klase"""
    
    def __init__(self, openai_client: openai.OpenAI, node_db: NodeConfigurationDatabase):
        self.openai_client = openai_client
        self.node_db = node_db
        self.template_manager = PromptTemplateManager()
        self.optimizer = PromptOptimizer(openai_client)
        self.generation_history = []
    
    def generate_workflow(self, context: GenerationContext) -> Dict[str, Any]:
        """Ģenerē workflow, pamatojoties uz kontekstu"""
        
        # Izvēlas atbilstošo veidni
        template_name = self._select_template(context.search_query.intent)
        template = self.template_manager.get_template(template_name)
        
        if not template:
            return self._fallback_generation(context)
        
        # Optimizē prompt
        system_prompt = template.system_prompt.format(
            available_nodes=self.optimizer._format_available_nodes(context.available_nodes),
            similar_workflows=self.optimizer._format_similar_workflows(context.similar_workflows)
        )
        
        user_prompt = self.optimizer.optimize_prompt_for_context(template, context)
        
        # Ģenerē workflow
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            
            result = self._parse_generation_result(response.choices[0].message.content)
            
            # Validē rezultātu
            validation_result = self._validate_generated_workflow(result)
            if not validation_result["valid"]:
                return self._fix_workflow_errors(result, validation_result["errors"])
            
            # Saglabā vēsturē
            self.generation_history.append({
                "context": context,
                "result": result,
                "timestamp": "2025-01-26"
            })
            
            return result
            
        except Exception as e:
            print(f"Kļūda ģenerējot workflow: {e}")
            return self._fallback_generation(context)
    
    def _select_template(self, intent: SearchIntent) -> str:
        """Izvēlas atbilstošo veidni, pamatojoties uz nolūku"""
        if intent == SearchIntent.CREATE_NEW:
            return "workflow_generation"
        elif intent == SearchIntent.MODIFY_EXISTING:
            return "workflow_modification"
        elif intent == SearchIntent.EXPLAIN_WORKFLOW:
            return "workflow_explanation"
        else:
            return "workflow_generation"
    
    def _parse_generation_result(self, content: str) -> Dict[str, Any]:
        """Parsē AI ģenerēto saturu"""
        try:
            # 🔎 Debug izdruka
            print("🔧 OpenAI raw content:")
            print(content)

            # Atrodam JSON kodu
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(0)
                else:
                    raise ValueError("Nav atrasts JSON saturs OpenAI atbildē")

            # Parsējam JSON
            result = json.loads(json_content)
            return result

        except Exception as e:
            print(f"❌ Kļūda parsējot rezultātu: {e}")
            return self._create_error_response(f"Parsēšanas kļūda: {e}")
    
    def _validate_generated_workflow(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validē ģenerēto workflow"""
        errors = []
        
        # Pārbauda pamata struktūru
        if "workflow" not in result:
            errors.append("Trūkst 'workflow' atslēgas")
        else:
            workflow = result["workflow"]
            if "nodes" not in workflow:
                errors.append("Trūkst 'nodes' masīva")
            elif not isinstance(workflow["nodes"], list):
                errors.append("'nodes' jābūt masīvam")
            
            if "connections" not in workflow:
                errors.append("Trūkst 'connections' objekta")
        
        # Validē mezglus
        if "workflow" in result and "nodes" in result["workflow"]:
            for i, node in enumerate(result["workflow"]["nodes"]):
                if "type" not in node:
                    errors.append(f"Mezglam {i} trūkst 'type' atslēgas")
                elif not self._is_valid_node_type(node["type"]):
                    errors.append(f"Nezināms mezgla tips: {node['type']}")
                
                if "parameters" in node:
                    node_validation = self.node_db.validate_node_parameters(
                        node["type"], node["parameters"]
                    )
                    if not node_validation[0]:
                        errors.extend([f"Mezgls {i}: {error}" for error in node_validation[1]])
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _is_valid_node_type(self, node_type: str) -> bool:
        """Pārbauda, vai mezgla tips ir derīgs"""
        config = self.node_db.get_node_configuration(node_type)
        return config is not None
    
    def _fix_workflow_errors(self, result: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
        """Mēģina labot workflow kļūdas"""
        # Vienkārša kļūdu labošanas loģika
        if "workflow" not in result:
            result["workflow"] = {"nodes": [], "connections": {}, "active": True}
        
        if "setup_instructions" not in result:
            result["setup_instructions"] = ["Pārbaudiet workflow konfigurāciju"]
        
        if "explanation" not in result:
            result["explanation"] = "Workflow ar kļūdām - nepieciešama manuāla pārbaude"
        
        # Pievieno kļūdu ziņojumus
        result["errors"] = errors
        
        return result
    
    def _fallback_generation(self, context: GenerationContext) -> Dict[str, Any]:
        """Fallback loģika, ja galvenā ģenerēšana neizdodas"""
        return {
            "workflow": {
                "name": f"Basic Workflow for: {context.user_query[:50]}",
                "nodes": [
                    {
                        "type": "n8n-nodes-base.webhook",
                        "name": "Webhook",
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "webhook-endpoint"
                        }
                    },
                    {
                        "type": "n8n-nodes-base.function",
                        "name": "Process Data",
                        "parameters": {
                            "functionCode": "// Add your processing logic here\nreturn items;"
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
                },
                "active": True
            },
            "setup_instructions": [
                "Šis ir pamata workflow veidne",
                "Pielāgojiet mezglu parametrus savām vajadzībām",
                "Pievienojiet nepieciešamos kredenciālus"
            ],
            "explanation": "Izveidots pamata workflow, jo nebija iespējams ģenerēt specifisko risinājumu.",
            "fallback": True
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Izveido kļūdas atbildi"""
        return {
            "error": True,
            "message": error_message,
            "workflow": None,
            "setup_instructions": ["Lūdzu, mēģiniet vēlreiz ar precīzāku pieprasījumu"],
            "explanation": f"Radās kļūda: {error_message}"
        }

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē komponentus
    openai_client = openai.OpenAI()
    node_db = NodeConfigurationDatabase()
    generator = WorkflowGenerator(openai_client, node_db)
    
    # Testa konteksts
    from workflow_search_algorithm import SearchQuery, SearchIntent
    
    test_context = GenerationContext(
        user_query="Izveidot Telegram botu pierakstam uz tikšanos",
        search_query=SearchQuery(
            original_text="Izveidot Telegram botu pierakstam uz tikšanos",
            intent=SearchIntent.CREATE_NEW,
            keywords=["telegram", "bot", "appointment"],
            entities={"services": ["telegram"], "actions": ["create"]},
            language="lv",
            complexity_preference="medium"
        ),
        similar_workflows=[],
        available_nodes=[],
        language="lv",
        complexity_preference="medium"
    )
    
    # Ģenerē workflow
    result = generator.generate_workflow(test_context)
    
    print("Ģenerētais workflow:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Parāda veidnes
    print("\nPieejamās veidnes:")
    for template_name in generator.template_manager.list_templates():
        print(f"- {template_name}")
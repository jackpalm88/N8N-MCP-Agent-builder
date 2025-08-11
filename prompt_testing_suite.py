#!/usr/bin/env python3
"""
Prompt Testing Suite for n8n AI Agent
Šis modulis nodrošina prompt sistēmas testēšanu un novērtēšanu.
"""

import json
import time
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from ai_prompt_system import WorkflowGenerator, GenerationContext
from workflow_search_algorithm import SearchQuery, SearchIntent, NaturalLanguageProcessor
from node_configuration_database import NodeConfigurationDatabase

class TestCategory(Enum):
    """Testa kategoriju enumerācija"""
    BASIC_GENERATION = "basic_generation"
    COMPLEX_SCENARIOS = "complex_scenarios"
    MULTILINGUAL = "multilingual"
    ERROR_HANDLING = "error_handling"
    EDGE_CASES = "edge_cases"

@dataclass
class TestCase:
    """Testa gadījuma struktūra"""
    id: str
    name: str
    category: TestCategory
    input_query: str
    expected_language: str
    expected_complexity: str
    expected_nodes: List[str]
    success_criteria: List[str]
    description: str

@dataclass
class TestResult:
    """Testa rezultāta struktūra"""
    test_case: TestCase
    success: bool
    generated_workflow: Dict[str, Any]
    execution_time: float
    errors: List[str]
    score: float  # 0-100
    feedback: str

class WorkflowValidator:
    """Workflow validācijas klase"""
    
    def __init__(self, node_db: NodeConfigurationDatabase):
        self.node_db = node_db
    
    def validate_workflow_structure(self, workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validē workflow struktūru"""
        errors = []
        
        # Pamata struktūras pārbaude
        required_keys = ["name", "nodes", "connections"]
        for key in required_keys:
            if key not in workflow:
                errors.append(f"Trūkst obligātās atslēgas: {key}")
        
        # Mezglu validācija
        if "nodes" in workflow:
            if not isinstance(workflow["nodes"], list):
                errors.append("'nodes' jābūt masīvam")
            else:
                for i, node in enumerate(workflow["nodes"]):
                    node_errors = self._validate_node(node, i)
                    errors.extend(node_errors)
        
        # Savienojumu validācija
        if "connections" in workflow:
            if not isinstance(workflow["connections"], dict):
                errors.append("'connections' jābūt objektam")
            else:
                connection_errors = self._validate_connections(workflow["connections"], workflow.get("nodes", []))
                errors.extend(connection_errors)
        
        return len(errors) == 0, errors
    
    def _validate_node(self, node: Dict[str, Any], index: int) -> List[str]:
        """Validē atsevišķu mezglu"""
        errors = []
        
        # Obligātās atslēgas
        required_keys = ["type", "name", "parameters"]
        for key in required_keys:
            if key not in node:
                errors.append(f"Mezglam {index} trūkst atslēgas: {key}")
        
        # Mezgla tipa validācija
        if "type" in node:
            config = self.node_db.get_node_configuration(node["type"])
            if not config:
                errors.append(f"Nezināms mezgla tips: {node['type']}")
            elif "parameters" in node:
                # Parametru validācija
                is_valid, param_errors = self.node_db.validate_node_parameters(
                    node["type"], node["parameters"]
                )
                if not is_valid:
                    errors.extend([f"Mezgls {index}: {error}" for error in param_errors])
        
        return errors
    
    def _validate_connections(self, connections: Dict[str, Any], nodes: List[Dict[str, Any]]) -> List[str]:
        """Validē mezglu savienojumus"""
        errors = []
        
        node_names = [node.get("name", "") for node in nodes]
        
        for source_node, targets in connections.items():
            if source_node not in node_names:
                errors.append(f"Savienojums no neeksistējoša mezgla: {source_node}")
            
            if isinstance(targets, dict) and "main" in targets:
                for target_group in targets["main"]:
                    if isinstance(target_group, list):
                        for target in target_group:
                            if isinstance(target, dict) and "node" in target:
                                if target["node"] not in node_names:
                                    errors.append(f"Savienojums uz neeksistējošu mezglu: {target['node']}")
        
        return errors

class PromptTestSuite:
    """Prompt testēšanas komplekts"""
    
    def __init__(self, openai_client: openai.OpenAI):
        self.openai_client = openai_client
        self.node_db = NodeConfigurationDatabase()
        self.generator = WorkflowGenerator(openai_client, self.node_db)
        self.nlp = NaturalLanguageProcessor(openai_client)
        self.validator = WorkflowValidator(self.node_db)
        self.test_cases = self._create_test_cases()
        self.results = []
    
    def _create_test_cases(self) -> List[TestCase]:
        """Izveido testa gadījumus"""
        test_cases = []
        
        # Pamata ģenerēšanas testi
        test_cases.extend([
            TestCase(
                id="basic_001",
                name="Vienkāršs Telegram bots",
                category=TestCategory.BASIC_GENERATION,
                input_query="Izveidot Telegram botu",
                expected_language="lv",
                expected_complexity="simple",
                expected_nodes=["telegramTrigger"],
                success_criteria=[
                    "Satur Telegram Trigger mezglu",
                    "Derīga JSON struktūra",
                    "Latviešu valodas atbalsts"
                ],
                description="Pamata Telegram bota izveide"
            ),
            TestCase(
                id="basic_002",
                name="HTTP API endpoint",
                category=TestCategory.BASIC_GENERATION,
                input_query="Create webhook for API",
                expected_language="en",
                expected_complexity="simple",
                expected_nodes=["webhook"],
                success_criteria=[
                    "Satur Webhook mezglu",
                    "Pareizi parametri",
                    "Angļu valodas atbalsts"
                ],
                description="Vienkārša API endpoint izveide"
            ),
            TestCase(
                id="basic_003",
                name="Email nosūtīšana",
                category=TestCategory.BASIC_GENERATION,
                input_query="Отправить email уведомление",
                expected_language="ru",
                expected_complexity="simple",
                expected_nodes=["httpRequest"],
                success_criteria=[
                    "Satur email funkcionalitāti",
                    "Krievu valodas atbalsts",
                    "Pareiza konfigurācija"
                ],
                description="Email nosūtīšanas workflow"
            )
        ])
        
        # Sarežģīti scenāriji
        test_cases.extend([
            TestCase(
                id="complex_001",
                name="Pilns pierakstu sistēma",
                category=TestCategory.COMPLEX_SCENARIOS,
                input_query="Izveidot pilnu Telegram botu pierakstam uz tikšanos ar datu bāzes integrāciju un email apstiprinājumiem",
                expected_language="lv",
                expected_complexity="complex",
                expected_nodes=["telegramTrigger", "function", "httpRequest"],
                success_criteria=[
                    "Vairāki mezgli",
                    "Datu bāzes integrācija",
                    "Email funkcionalitāte",
                    "Sarežģīta loģika"
                ],
                description="Sarežģīts pierakstu sistēmas workflow"
            ),
            TestCase(
                id="complex_002",
                name="API ar validāciju",
                category=TestCategory.COMPLEX_SCENARIOS,
                input_query="Create REST API with data validation, authentication, and error handling",
                expected_language="en",
                expected_complexity="complex",
                expected_nodes=["webhook", "function", "httpRequest"],
                success_criteria=[
                    "Autentifikācijas loģika",
                    "Datu validācija",
                    "Kļūdu apstrāde",
                    "REST API struktūra"
                ],
                description="Pilnīgs REST API ar drošību"
            )
        ])
        
        # Daudzvalodu testi
        test_cases.extend([
            TestCase(
                id="multilang_001",
                name="Jaukta valoda",
                category=TestCategory.MULTILINGUAL,
                input_query="Создать telegram bot для booking appointments",
                expected_language="ru",
                expected_complexity="medium",
                expected_nodes=["telegramTrigger", "function"],
                success_criteria=[
                    "Atpazīst jauktu valodu",
                    "Pareiza valodas noteikšana",
                    "Atbilstoša lokalizācija"
                ],
                description="Jauktas valodas apstrāde"
            )
        ])
        
        # Kļūdu apstrādes testi
        test_cases.extend([
            TestCase(
                id="error_001",
                name="Neskaidrs pieprasījums",
                category=TestCategory.ERROR_HANDLING,
                input_query="uztaisi kaut ko",
                expected_language="lv",
                expected_complexity="simple",
                expected_nodes=[],
                success_criteria=[
                    "Fallback loģika darbojas",
                    "Informatīvs kļūdas ziņojums",
                    "Pamata workflow veidne"
                ],
                description="Neskaidra pieprasījuma apstrāde"
            ),
            TestCase(
                id="error_002",
                name="Neeksistējošs mezgls",
                category=TestCategory.ERROR_HANDLING,
                input_query="Create workflow with SuperAdvancedNode",
                expected_language="en",
                expected_complexity="medium",
                expected_nodes=[],
                success_criteria=[
                    "Atpazīst neeksistējošu mezglu",
                    "Piedāvā alternatīvas",
                    "Kļūdas ziņojums"
                ],
                description="Neeksistējoša mezgla pieprasījums"
            )
        ])
        
        return test_cases
    
    def run_test_case(self, test_case: TestCase) -> TestResult:
        """Izpilda atsevišķu testa gadījumu"""
        start_time = time.time()
        errors = []
        score = 0.0
        
        try:
            # Parsē vaicājumu
            search_query = self.nlp.parse_query(test_case.input_query)
            
            # Izveido kontekstu
            context = GenerationContext(
                user_query=test_case.input_query,
                search_query=search_query,
                similar_workflows=[],
                available_nodes=[],
                language=search_query.language,
                complexity_preference=search_query.complexity_preference
            )
            
            # Ģenerē workflow
            result = self.generator.generate_workflow(context)
            
            # Validē rezultātu
            if "workflow" in result and result["workflow"]:
                is_valid, validation_errors = self.validator.validate_workflow_structure(result["workflow"])
                if not is_valid:
                    errors.extend(validation_errors)
                else:
                    score += 40  # Pamata struktūras punkti
            else:
                errors.append("Nav ģenerēts derīgs workflow")
            
            # Pārbauda valodu
            if search_query.language == test_case.expected_language:
                score += 20
            else:
                errors.append(f"Nepareiza valoda: gaidīta {test_case.expected_language}, iegūta {search_query.language}")
            
            # Pārbauda sarežģītību
            if search_query.complexity_preference == test_case.expected_complexity:
                score += 20
            else:
                errors.append(f"Nepareiza sarežģītība: gaidīta {test_case.expected_complexity}")
            
            # Pārbauda gaidītos mezglus
            if test_case.expected_nodes and "workflow" in result:
                found_nodes = [node.get("type", "").split(".")[-1] for node in result["workflow"].get("nodes", [])]
                for expected_node in test_case.expected_nodes:
                    if any(expected_node in found_node for found_node in found_nodes):
                        score += 20 / len(test_case.expected_nodes)
                    else:
                        errors.append(f"Trūkst gaidītā mezgla: {expected_node}")
            
            execution_time = time.time() - start_time
            success = len(errors) == 0 and score >= 60
            
            # Ģenerē atsauksmi
            feedback = self._generate_feedback(test_case, result, errors, score)
            
            return TestResult(
                test_case=test_case,
                success=success,
                generated_workflow=result,
                execution_time=execution_time,
                errors=errors,
                score=score,
                feedback=feedback
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            errors.append(f"Izpildes kļūda: {str(e)}")
            
            return TestResult(
                test_case=test_case,
                success=False,
                generated_workflow={},
                execution_time=execution_time,
                errors=errors,
                score=0.0,
                feedback=f"Testa izpilde neizdevās: {str(e)}"
            )
    
    def _generate_feedback(self, test_case: TestCase, result: Dict[str, Any], errors: List[str], score: float) -> str:
        """Ģenerē detalizētu atsauksmi par testa rezultātu"""
        feedback_parts = []
        
        feedback_parts.append(f"Testa rezultāts: {score:.1f}/100 punkti")
        
        if score >= 80:
            feedback_parts.append("✅ Izcils rezultāts!")
        elif score >= 60:
            feedback_parts.append("✅ Labs rezultāts")
        elif score >= 40:
            feedback_parts.append("⚠️ Viduvējs rezultāts")
        else:
            feedback_parts.append("❌ Nepieņemams rezultāts")
        
        if errors:
            feedback_parts.append(f"Kļūdas ({len(errors)}):")
            for error in errors[:5]:  # Rāda tikai pirmās 5 kļūdas
                feedback_parts.append(f"  - {error}")
        
        if "workflow" in result and result["workflow"]:
            nodes_count = len(result["workflow"].get("nodes", []))
            feedback_parts.append(f"Ģenerēti {nodes_count} mezgli")
        
        return "\n".join(feedback_parts)
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Izpilda visus testus"""
        print("Sāk prompt sistēmas testēšanu...")
        
        results_by_category = {}
        total_tests = len(self.test_cases)
        passed_tests = 0
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"Izpilda testu {i}/{total_tests}: {test_case.name}")
            
            result = self.run_test_case(test_case)
            self.results.append(result)
            
            if result.success:
                passed_tests += 1
            
            # Grupē pēc kategorijām
            category = test_case.category.value
            if category not in results_by_category:
                results_by_category[category] = []
            results_by_category[category].append(result)
            
            print(f"  Rezultāts: {'PASS' if result.success else 'FAIL'} ({result.score:.1f}/100)")
            if result.errors:
                print(f"  Kļūdas: {len(result.errors)}")
        
        # Aprēķina statistiku
        success_rate = (passed_tests / total_tests) * 100
        average_score = sum(r.score for r in self.results) / len(self.results)
        average_time = sum(r.execution_time for r in self.results) / len(self.results)
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "average_score": average_score,
            "average_execution_time": average_time,
            "results_by_category": results_by_category,
            "detailed_results": self.results
        }
        
        self._print_summary(summary)
        return summary
    
    def _print_summary(self, summary: Dict[str, Any]):
        """Izdrukā testa kopsavilkumu"""
        print("\n" + "="*60)
        print("PROMPT SISTĒMAS TESTĒŠANAS KOPSAVILKUMS")
        print("="*60)
        
        print(f"Kopējie testi: {summary['total_tests']}")
        print(f"Izturētie testi: {summary['passed_tests']}")
        print(f"Veiksmes līmenis: {summary['success_rate']:.1f}%")
        print(f"Vidējais punktu skaits: {summary['average_score']:.1f}/100")
        print(f"Vidējais izpildes laiks: {summary['average_execution_time']:.2f}s")
        
        print("\nRezultāti pa kategorijām:")
        for category, results in summary['results_by_category'].items():
            passed = sum(1 for r in results if r.success)
            total = len(results)
            avg_score = sum(r.score for r in results) / len(results)
            print(f"  {category}: {passed}/{total} ({(passed/total)*100:.1f}%) - Vidēji: {avg_score:.1f}")
        
        print("\nNeizdevušies testi:")
        for result in summary['detailed_results']:
            if not result.success:
                print(f"  - {result.test_case.name}: {result.score:.1f}/100")
                if result.errors:
                    print(f"    Kļūdas: {'; '.join(result.errors[:2])}")

# Lietošanas piemērs
if __name__ == "__main__":
    # Inicializē testa komplektu
    openai_client = openai.OpenAI()
    test_suite = PromptTestSuite(openai_client)
    
    # Izpilda visus testus
    results = test_suite.run_all_tests()
    
    # Saglabā rezultātus
    with open("prompt_test_results.json", "w", encoding="utf-8") as f:
        # Pārveido rezultātus par serializējamiem
        serializable_results = {
            "total_tests": results["total_tests"],
            "passed_tests": results["passed_tests"],
            "success_rate": results["success_rate"],
            "average_score": results["average_score"],
            "average_execution_time": results["average_execution_time"],
            "test_details": [
                {
                    "test_name": r.test_case.name,
                    "category": r.test_case.category.value,
                    "success": r.success,
                    "score": r.score,
                    "execution_time": r.execution_time,
                    "errors": r.errors
                }
                for r in results["detailed_results"]
            ]
        }
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nTesta rezultāti saglabāti: prompt_test_results.json")


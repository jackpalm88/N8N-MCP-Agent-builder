# Tehniskā Dokumentācija - n8n AI Aģents

## Sistēmas Arhitektūra

### Galvenās Komponentes

#### 1. Flask Backend Serveris
- **Fails:** `src/main.py`
- **Funkcija:** Galvenais servera entry point
- **Portu:** 5000 (noklusējuma)
- **CORS:** Iespējots visiem domēniem

#### 2. API Maršruti (Routes)

**Workflow API (`src/routes/workflow.py`)**
- `/api/workflow/generate` - Workflow ģenerēšana
- `/api/workflow/search` - Līdzīgu workflow meklēšana
- `/api/workflow/health` - Sistēmas stāvokļa pārbaude
- `/api/workflow/statistics` - Sistēmas statistika

**n8n Integrācijas API (`src/routes/n8n_integration.py`)**
- `/api/n8n/configure` - n8n savienojuma konfigurācija
- `/api/n8n/workflows/upload` - Workflow augšupielāde
- `/api/n8n/workflows` - n8n workflow saraksts
- `/api/n8n/generate-and-upload` - Ģenerēšana + augšupielāde

#### 3. AI Komponenti

**Workflow Ģenerātors (`src/ai_prompt_system.py`)**
```python
class WorkflowGenerator:
    def generate_workflow(self, context: GenerationContext) -> Dict[str, Any]
    def _create_system_prompt(self, context: GenerationContext) -> str
    def _create_user_prompt(self, context: GenerationContext) -> str
```

**Dabiskās Valodas Procesors (`src/workflow_search_algorithm.py`)**
```python
class NaturalLanguageProcessor:
    def parse_query(self, query: str) -> ParsedQuery
    def detect_language(self, text: str) -> str
    def extract_keywords(self, text: str, language: str) -> List[str]
```

#### 4. Datu Slāņi

**Vektoru Datu bāze (`src/vector_database_design.py`)**
- Qdrant integrācija
- Workflow vektorizēšana
- Līdzības meklēšana

**Mezglu Konfigurācijas DB (`src/node_configuration_database.py`)**
- n8n mezglu metadati
- Parametru validācija
- Konfigurācijas veidnes

#### 5. Daudzvalodu Atbalsts (`src/multilingual_support.py`)

**Valodu Noteicējs**
```python
class EnhancedLanguageDetector:
    def detect_language(self, text: str) -> LanguageDetectionResult
```

**Atslēgvārdu Ekstraktors**
```python
class MultilingualKeywordExtractor:
    def extract_keywords(self, text: str, language: SupportedLanguage) -> Dict[str, List[str]]
```

### Datu Plūsma

```
Lietotāja pieprasījums
    ↓
Valodas noteikšana
    ↓
Atslēgvārdu ekstraktēšana
    ↓
Vektoru meklēšana (līdzīgi workflow)
    ↓
AI prompt ģenerēšana
    ↓
OpenAI API izsaukums
    ↓
Workflow JSON ģenerēšana
    ↓
Validācija
    ↓
Atgriešana lietotājam / n8n augšupielāde
```

## Konfigurācijas Pārvaldība

### Vides Mainīgie

```python
# src/config.py
import os

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
    QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))
    N8N_BASE_URL = os.getenv('N8N_BASE_URL', 'http://localhost:5678')
    N8N_API_KEY = os.getenv('N8N_API_KEY')
```

### Datu bāzes Inicializācija

```python
def initialize_components():
    global _openai_client, _node_db, _vector_db, _vectorizer, _nlp, _search_engine, _generator, _multilingual
    
    if _openai_client is None:
        _openai_client = openai.OpenAI()
        _node_db = NodeConfigurationDatabase("src/n8n_nodes.db")
        _vector_db = QdrantWorkflowDatabase(host="localhost", port=6333)
        _vectorizer = WorkflowVectorizer()
        _nlp = NaturalLanguageProcessor()
        _search_engine = WorkflowSearchEngine(_vector_db, _vectorizer)
        _generator = WorkflowGenerator()
        _multilingual = MultilingualSupport()
```

## AI Prompt Sistēma

### Prompt Arhitektūra

**Sistēmas Prompt:**
```python
SYSTEM_PROMPT_TEMPLATE = """
Tu esi eksperts n8n workflow automatizācijas sistēmās. 
Tavs uzdevums ir ģenerēt pilnīgus, funkcionālus n8n workflow JSON formātā.

Workflow struktūra:
- name: Workflow nosaukums
- nodes: Mezglu masīvs
- connections: Savienojumu objekts
- settings: Workflow iestatījumi

Mezglu tipi:
{available_nodes}

Līdzīgi workflow:
{similar_workflows}

Valoda: {language}
"""
```

**Lietotāja Prompt:**
```python
USER_PROMPT_TEMPLATE = """
Lietotāja pieprasījums: {user_query}

Atslēgvārdi: {keywords}
Kompleksitāte: {complexity}

Ģenerē workflow JSON formātā ar:
1. Skaidru nosaukumu
2. Nepieciešamajiem mezgliem
3. Pareiziem savienojumiem
4. Uzstādīšanas instrukcijām
"""
```

### Prompt Optimizācija

1. **Konteksta ierobežojumi:** Maksimums 8000 tokeni
2. **Dinamiska mezglu iekļaušana:** Tikai relevantie mezgli
3. **Līdzīgu workflow izmantošana:** Maksimums 3 piemēri
4. **Valodu specifiska lokalizācija**

## Vektoru Meklēšanas Sistēma

### Qdrant Konfigurācija

```python
class QdrantWorkflowDatabase:
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "n8n_workflows"
    
    def initialize_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
```

### Vektorizēšanas Process

```python
class WorkflowVectorizer:
    def vectorize_workflow(self, workflow: Dict[str, Any]) -> List[float]:
        # Ekstraktē tekstu no workflow
        text_content = self._extract_text_content(workflow)
        
        # Ģenerē embedding ar OpenAI
        response = self.openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text_content
        )
        
        return response.data[0].embedding
```

### Meklēšanas Algoritms

```python
def search_similar_workflows(self, query_vector: List[float], limit: int = 5) -> List[SearchResult]:
    search_result = self.client.search(
        collection_name=self.collection_name,
        query_vector=query_vector,
        limit=limit,
        score_threshold=0.7
    )
    
    return [
        SearchResult(
            workflow=point.payload,
            similarity_score=point.score,
            match_reasons=self._analyze_match_reasons(point)
        )
        for point in search_result
    ]
```

## n8n API Integrācija

### API Klients Arhitektūra

```python
class N8nApiClient:
    def __init__(self, credentials: N8nCredentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.session.headers.update({
            'X-N8N-API-KEY': credentials.api_key,
            'Content-Type': 'application/json'
        })
```

### Workflow Augšupielādes Process

```python
def create_workflow(self, workflow_data: Dict[str, Any]) -> WorkflowUploadResult:
    # 1. Validē workflow struktūru
    validation_result = self._validate_workflow_structure(workflow_data)
    
    # 2. Sagatavo datus n8n API formātam
    api_payload = self._prepare_workflow_for_api(workflow_data)
    
    # 3. Nosūta pieprasījumu
    response = self.session.post(
        f"{self.credentials.base_url}/api/v1/workflows",
        json=api_payload,
        timeout=60
    )
    
    # 4. Apstrādā atbildi
    return self._process_upload_response(response, workflow_data)
```

### Kļūdu Apstrāde

```python
def _handle_api_error(self, response: requests.Response) -> WorkflowUploadResult:
    if response.status_code == 400:
        return WorkflowUploadResult(
            success=False,
            message="Workflow dati nav derīgi",
            errors=[response.json().get('message', 'Nezināma kļūda')]
        )
    elif response.status_code == 401:
        return WorkflowUploadResult(
            success=False,
            message="Autentifikācijas kļūda",
            errors=["Nederīga API atslēga"]
        )
```

## Daudzvalodu Sistēma

### Valodu Noteikšanas Algoritms

```python
def detect_language(self, text: str) -> LanguageDetectionResult:
    scores = {}
    
    for language, patterns in self.language_patterns.items():
        score = 0
        
        # Rakstzīmju analīze
        char_matches = len(re.findall(patterns['chars'], text.lower()))
        score += char_matches * 2
        
        # Vārdu analīze
        for word in patterns['words']:
            if word in text.lower():
                score += 3
        
        # Morfologisko modeļu analīze
        for pattern in patterns['patterns']:
            score += len(re.findall(pattern, text.lower()))
        
        scores[language] = score
    
    best_language = max(scores, key=scores.get)
    confidence = scores[best_language] / sum(scores.values())
    
    return LanguageDetectionResult(language=best_language, confidence=confidence)
```

### Lokalizācijas Sistēma

```python
class MultilingualPromptManager:
    def get_localized_prompt(self, base_prompt: str, language: SupportedLanguage) -> str:
        localized_content = self.localized_prompts.get(language)
        suffix = localized_content.get('system_prompt_suffix', '')
        return base_prompt + suffix
```

## Veiktspējas Optimizācija

### Kešošanas Stratēģija

```python
from functools import lru_cache

class WorkflowGenerator:
    @lru_cache(maxsize=100)
    def _get_cached_similar_workflows(self, query_hash: str) -> List[Dict]:
        # Kešo līdzīgu workflow meklēšanas rezultātus
        pass
    
    @lru_cache(maxsize=50)
    def _get_cached_node_configs(self, node_type: str) -> Dict:
        # Kešo mezglu konfigurācijas
        pass
```

### Batch Apstrāde

```python
def process_multiple_queries(self, queries: List[str]) -> List[Dict]:
    # Grupē pieprasījumus pēc valodas
    grouped_queries = self._group_by_language(queries)
    
    results = []
    for language, lang_queries in grouped_queries.items():
        # Apstrādā vienā batch pieprasījumā
        batch_results = self._process_batch(lang_queries, language)
        results.extend(batch_results)
    
    return results
```

### Datu bāzes Optimizācija

```python
# Qdrant indeksu optimizācija
def optimize_vector_search(self):
    self.client.update_collection(
        collection_name=self.collection_name,
        optimizer_config=OptimizersConfigDiff(
            indexing_threshold=10000,
            memmap_threshold=20000
        )
    )
```

## Drošības Aspekti

### API Atslēgu Pārvaldība

```python
class SecureCredentialsManager:
    def __init__(self):
        self.encryption_key = self._load_encryption_key()
    
    def encrypt_api_key(self, api_key: str) -> str:
        cipher = Fernet(self.encryption_key)
        return cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        cipher = Fernet(self.encryption_key)
        return cipher.decrypt(encrypted_key.encode()).decode()
```

### Input Validācija

```python
def validate_user_input(self, user_input: str) -> Tuple[bool, List[str]]:
    errors = []
    
    # Garuma pārbaude
    if len(user_input) > 10000:
        errors.append("Pieprasījums pārāk garš")
    
    # Bīstamu rakstzīmju pārbaude
    dangerous_patterns = [r'<script', r'javascript:', r'eval\(']
    for pattern in dangerous_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            errors.append("Aizliegts saturs")
    
    return len(errors) == 0, errors
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/workflow/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_workflow():
    # Workflow ģenerēšanas loģika
    pass
```

## Monitoring un Logging

### Strukturēts Logging

```python
import structlog

logger = structlog.get_logger()

def generate_workflow(self, context: GenerationContext):
    logger.info(
        "workflow_generation_started",
        user_query=context.user_query,
        language=context.language,
        similar_workflows_count=len(context.similar_workflows)
    )
    
    try:
        result = self._generate_workflow_internal(context)
        
        logger.info(
            "workflow_generation_completed",
            workflow_name=result.get('workflow', {}).get('name'),
            nodes_count=len(result.get('workflow', {}).get('nodes', [])),
            generation_time_ms=result.get('generation_time_ms')
        )
        
        return result
        
    except Exception as e:
        logger.error(
            "workflow_generation_failed",
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

### Metriku Savākšana

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metriku definīcijas
workflow_generations = Counter('workflow_generations_total', 'Total workflow generations', ['language', 'status'])
generation_duration = Histogram('workflow_generation_duration_seconds', 'Workflow generation duration')

@generation_duration.time()
def generate_workflow(self, context):
    try:
        result = self._generate_workflow_internal(context)
        workflow_generations.labels(language=context.language, status='success').inc()
        return result
    except Exception as e:
        workflow_generations.labels(language=context.language, status='error').inc()
        raise
```

## Testēšanas Stratēģija

### Unit Testi

```python
class TestWorkflowGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = WorkflowGenerator()
        self.mock_context = GenerationContext(
            user_query="test query",
            language="en",
            similar_workflows=[],
            available_nodes=[]
        )
    
    def test_workflow_generation(self):
        result = self.generator.generate_workflow(self.mock_context)
        
        self.assertIn('workflow', result)
        self.assertIn('name', result['workflow'])
        self.assertIn('nodes', result['workflow'])
```

### Integrācijas Testi

```python
class TestN8nIntegration(unittest.TestCase):
    def setUp(self):
        self.client = N8nApiClient(N8nCredentials(
            base_url="http://localhost:5678",
            api_key="test-api-key"
        ))
    
    @mock.patch('requests.Session.post')
    def test_workflow_upload(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "workflow-123"}
        
        result = self.client.create_workflow({"name": "Test", "nodes": []})
        
        self.assertTrue(result.success)
        self.assertEqual(result.workflow_id, "workflow-123")
```

### Load Testi

```python
import asyncio
import aiohttp

async def load_test_workflow_generation():
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for i in range(100):
            task = session.post(
                'http://localhost:5000/api/workflow/generate',
                json={'query': f'test query {i}', 'max_results': 3}
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        success_count = sum(1 for r in responses if r.status == 200)
        print(f"Successful requests: {success_count}/100")
```

## Deployment Stratēģija

### Docker Konfigurācija

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/

EXPOSE 5000

CMD ["python", "src/main.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  n8n-ai-agent:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - QDRANT_HOST=qdrant
    depends_on:
      - qdrant
  
  qdrant:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n-ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: n8n-ai-agent
  template:
    metadata:
      labels:
        app: n8n-ai-agent
    spec:
      containers:
      - name: n8n-ai-agent
        image: n8n-ai-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
```

## Problēmu Risināšana

### Biežākās Kļūdas

1. **OpenAI API Rate Limiting**
   ```python
   def handle_rate_limit(self, error):
       wait_time = int(error.response.headers.get('Retry-After', 60))
       time.sleep(wait_time)
       return self.retry_request()
   ```

2. **Qdrant Savienojuma Problēmas**
   ```python
   def ensure_qdrant_connection(self):
       try:
           self.client.get_collections()
       except Exception as e:
           logger.warning("Qdrant nav pieejams, izmanto fallback meklēšanu")
           return self.fallback_search()
   ```

3. **n8n API Timeout**
   ```python
   def upload_with_retry(self, workflow_data, max_retries=3):
       for attempt in range(max_retries):
           try:
               return self.client.create_workflow(workflow_data)
           except requests.Timeout:
               if attempt == max_retries - 1:
                   raise
               time.sleep(2 ** attempt)
   ```

### Debug Rīki

```python
def debug_workflow_generation(self, context: GenerationContext):
    debug_info = {
        'input_analysis': {
            'query': context.user_query,
            'detected_language': context.language,
            'keywords': context.search_query.keywords,
            'intent': context.search_query.intent.value
        },
        'similar_workflows': [
            {
                'name': wf.get('name'),
                'similarity_score': wf.get('similarity_score'),
                'match_reasons': wf.get('match_reasons')
            }
            for wf in context.similar_workflows
        ],
        'available_nodes': len(context.available_nodes),
        'prompt_length': len(self._create_system_prompt(context))
    }
    
    logger.debug("workflow_generation_debug", **debug_info)
    return debug_info
```

Šī tehniskā dokumentācija sniedz dziļu ieskatu n8n AI Aģenta iekšējā darbībā un arhitektūrā. Tā ir paredzēta izstrādātājiem, kas vēlas saprast, modificēt vai paplašināt sistēmu.


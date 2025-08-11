# n8n AI Aģenta Izvietošanas Rokasgrāmata

## Satura rādītājs

1. [Priekšnosacījumi](#priekšnosacījumi)
2. [Railway Izvietošana (Ieteicams)](#railway-izvietošana)
3. [Heroku Izvietošana](#heroku-izvietošana)
4. [Render Izvietošana](#render-izvietošana)
5. [DigitalOcean App Platform](#digitalocean-app-platform)
6. [Google Cloud Platform](#google-cloud-platform)
7. [Docker Izvietošana](#docker-izvietošana)
8. [Vides Mainīgo Konfigurācija](#vides-mainīgo-konfigurācija)
9. [Problēmu Risināšana](#problēmu-risināšana)

## Priekšnosacījumi

Pirms izvietošanas jums nepieciešams:

1. **OpenAI API atslēga** - Iegūstama no [OpenAI platformas](https://platform.openai.com/api-keys)
2. **Git repozitorijs** - Kods jāaugšupielādē GitHub, GitLab vai līdzīgā platformā
3. **Izvietošanas platformas konts** - Atkarībā no izvēlētās platformas

## Railway Izvietošana (Ieteicams)

Railway ir vienkāršākā un ekonomiskākā opcija n8n AI aģenta izvietošanai.

### 1. Konts un Sagatavošana

1. Dodieties uz [Railway.app](https://railway.app)
2. Reģistrējieties ar GitHub kontu
3. Apstipriniet e-pasta adresi

### 2. Projekta Izveide

1. Noklikšķiniet "New Project"
2. Izvēlieties "Deploy from GitHub repo"
3. Autorizējiet Railway piekļuvi GitHub
4. Izvēlieties savu n8n AI aģenta repozitoriju

### 3. Vides Mainīgo Konfigurācija

Railway automātiski noteiks Python projektu. Tagad jākonfigurē vides mainīgie:

1. Atveriet projektu Railway dashboard
2. Noklikšķiniet uz servisa nosaukuma
3. Dodieties uz "Variables" sadaļu
4. Pievienojiet šādus mainīgos:

```
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=production
PORT=5000
```

### 4. Izvietošana

1. Railway automātiski sāks izvietošanu
2. Sekojiet līdzi logiem "Deployments" sadaļā
3. Pēc veiksmīgas izvietošanas saņemsiet publisko URL

### 5. Domēna Konfigurācija (Opcionāli)

1. Dodieties uz "Settings" → "Domains"
2. Noklikšķiniet "Generate Domain"
3. Vai pievienojiet savu custom domēnu

**Izmaksas:** $5/mēnesī starter plāns

## Heroku Izvietošana

Heroku ir populāra platforma ar labu dokumentāciju.

### 1. Heroku CLI Instalācija

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Lejupielādējiet no https://devcenter.heroku.com/articles/heroku-cli
```

### 2. Pieslēgšanās

```bash
heroku login
```

### 3. Aplikācijas Izveide

```bash
# Navigējiet uz projekta direktoriju
cd n8n_ai_agent_server

# Izveidojiet Heroku aplikāciju
heroku create your-app-name

# Vai izmantojiet automātiski ģenerētu nosaukumu
heroku create
```

### 4. Vides Mainīgo Iestatīšana

```bash
heroku config:set OPENAI_API_KEY=your-openai-api-key-here
heroku config:set OPENAI_API_BASE=https://api.openai.com/v1
heroku config:set FLASK_ENV=production
```

### 5. Izvietošana

```bash
# Pievienojiet failus Git
git add .
git commit -m "Prepare for Heroku deployment"

# Izvietojiet uz Heroku
git push heroku main
```

### 6. Aplikācijas Atvēršana

```bash
heroku open
```

**Izmaksas:** 
- Bezmaksas: 550-1000 dyno stundas (ar ierobežojumiem)
- Hobby: $7/mēnesī

## Render Izvietošana

Render piedāvā vienkāršu izvietošanu ar automātisko SSL.

### 1. Konts

1. Dodieties uz [Render.com](https://render.com)
2. Reģistrējieties ar GitHub kontu

### 2. Web Service Izveide

1. Noklikšķiniet "New +"
2. Izvēlieties "Web Service"
3. Savienojiet GitHub repozitoriju
4. Izvēlieties n8n AI aģenta repozitoriju

### 3. Konfigurācija

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python src/main.py
```

**Environment Variables:**
```
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=production
PYTHONPATH=/opt/render/project/src
```

### 4. Izvietošana

1. Noklikšķiniet "Create Web Service"
2. Render automātiski sāks izvietošanu
3. Sekojiet līdzi logiem

**Izmaksas:**
- Bezmaksas: ierobežots (aplikācija "aizmieg")
- Starter: $7/mēnesī

## DigitalOcean App Platform

DigitalOcean piedāvā labu cenu/kvalitātes attiecību.

### 1. Konts

1. Dodieties uz [DigitalOcean.com](https://digitalocean.com)
2. Izveidojiet kontu
3. Pievienojiet maksājuma metodi

### 2. App Izveide

1. Dodieties uz "Apps" sadaļu
2. Noklikšķiniet "Create App"
3. Izvēlieties GitHub kā avotu
4. Autorizējiet DigitalOcean
5. Izvēlieties repozitoriju

### 3. Konfigurācija

**Build Command:**
```bash
pip install -r requirements.txt
```

**Run Command:**
```bash
python src/main.py
```

**Environment Variables:**
```
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=production
```

### 4. Plāna Izvēle

- Basic: $5/mēnesī
- Professional: $12/mēnesī

**Izmaksas:** No $5/mēnesī

## Google Cloud Platform

GCP piedāvā App Engine servisu vienkāršai izvietošanai.

### 1. GCP Konts

1. Dodieties uz [Google Cloud Console](https://console.cloud.google.com)
2. Izveidojiet jaunu projektu
3. Iespējojiet App Engine API

### 2. Cloud SDK Instalācija

```bash
# macOS
brew install google-cloud-sdk

# Ubuntu/Debian
curl https://sdk.cloud.google.com | bash

# Windows
# Lejupielādējiet no https://cloud.google.com/sdk/docs/install
```

### 3. Autentifikācija

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 4. App Engine Inicializācija

```bash
gcloud app create --region=europe-west1
```

### 5. Vides Mainīgo Konfigurācija

Rediģējiet `app.yaml` failu:

```yaml
runtime: python311

env_variables:
  OPENAI_API_KEY: "your-openai-api-key-here"
  OPENAI_API_BASE: "https://api.openai.com/v1"
  FLASK_ENV: "production"
  PYTHONPATH: "/srv"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

### 6. Izvietošana

```bash
gcloud app deploy
```

**Izmaksas:** Atkarībā no lietošanas, sākot no $0

## Docker Izvietošana

Docker ļauj izvietot aplikāciju jebkurā platformā, kas atbalsta konteineru.

### 1. Docker Image Būvēšana

```bash
# Navigējiet uz projekta direktoriju
cd n8n_ai_agent_server

# Būvējiet Docker image
docker build -t n8n-ai-agent .
```

### 2. Lokālā Testēšana

```bash
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=your-api-key \
  -e OPENAI_API_BASE=https://api.openai.com/v1 \
  n8n-ai-agent
```

### 3. Docker Compose

```bash
# Izveidojiet .env failu
echo "OPENAI_API_KEY=your-api-key" > .env

# Palaidiet ar Docker Compose
docker-compose up -d
```

### 4. Izvietošana uz Cloud Platformām

**AWS ECS:**
```bash
# Augšupielādējiet image uz ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
docker tag n8n-ai-agent:latest your-account.dkr.ecr.us-east-1.amazonaws.com/n8n-ai-agent:latest
docker push your-account.dkr.ecr.us-east-1.amazonaws.com/n8n-ai-agent:latest
```

**Google Cloud Run:**
```bash
# Augšupielādējiet uz Container Registry
docker tag n8n-ai-agent gcr.io/YOUR_PROJECT_ID/n8n-ai-agent
docker push gcr.io/YOUR_PROJECT_ID/n8n-ai-agent

# Izvietojiet uz Cloud Run
gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/n8n-ai-agent --platform managed
```

## Vides Mainīgo Konfigurācija

Visām platformām nepieciešami šādi vides mainīgie:

### Obligātie Mainīgie

| Mainīgais | Apraksts | Piemērs |
|-----------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API atslēga | `sk-...` |
| `OPENAI_API_BASE` | OpenAI API bāzes URL | `https://api.openai.com/v1` |
| `FLASK_ENV` | Flask vide | `production` |

### Opcionālie Mainīgie

| Mainīgais | Apraksts | Noklusējums |
|-----------|----------|-------------|
| `PORT` | Servera ports | `5000` |
| `QDRANT_HOST` | Qdrant servera adrese | `localhost` |
| `QDRANT_PORT` | Qdrant servera ports | `6333` |
| `N8N_BASE_URL` | n8n servera URL | `http://localhost:5678` |
| `N8N_API_KEY` | n8n API atslēga | - |

### OpenAI API Atslēgas Iegūšana

1. Dodieties uz [OpenAI Platform](https://platform.openai.com)
2. Reģistrējieties vai pieslēdzieties
3. Dodieties uz "API Keys" sadaļu
4. Noklikšķiniet "Create new secret key"
5. Kopējiet atslēgu (tā tiks rādīta tikai vienu reizi!)

### Drošības Ieteikumi

1. **Nekad neiekļaujiet API atslēgas kodā**
2. **Izmantojiet vides mainīgos**
3. **Regulāri rotējiet API atslēgas**
4. **Iestatiet API izmantošanas limitus**
5. **Monitorējiet API izmantošanu**

## Problēmu Risināšana

### Biežākās Problēmas

#### 1. "Module not found" kļūda

**Problēma:** Python neatrod moduļus
**Risinājums:**
```bash
# Pārbaudiet PYTHONPATH
export PYTHONPATH=/app/src

# Vai pievienojiet main.py sākumā
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
```

#### 2. OpenAI API kļūdas

**Problēma:** `openai.AuthenticationError`
**Risinājums:**
- Pārbaudiet API atslēgas pareizību
- Pārbaudiet API atslēgas limitus
- Pārbaudiet billing informāciju OpenAI kontā

#### 3. Port kļūdas

**Problēma:** "Port already in use"
**Risinājums:**
```python
# Izmantojiet dinamisku porta noteikšanu
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

#### 4. CORS kļūdas

**Problēma:** Frontend nevar piekļūt API
**Risinājums:**
```python
from flask_cors import CORS
CORS(app, origins="*")
```

#### 5. Datu bāzes kļūdas

**Problēma:** SQLite datu bāze nav pieejama
**Risinājums:**
```python
# Izveidojiet direktoriju, ja nepastāv
os.makedirs(os.path.dirname(db_path), exist_ok=True)
```

### Debugging Paņēmieni

#### 1. Logu Pārbaude

**Railway:**
```bash
# Skatīt logus Railway dashboard vai CLI
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Render:**
- Skatīt logus Render dashboard

#### 2. Vides Mainīgo Pārbaude

```python
import os
print("Environment variables:")
for key, value in os.environ.items():
    if 'API' in key or 'FLASK' in key:
        print(f"{key}: {value[:10]}...")
```

#### 3. Dependency Problēmas

```bash
# Pārbaudiet requirements.txt
pip freeze > requirements.txt

# Pārbaudiet Python versiju
python --version
```

#### 4. Tīkla Problēmas

```python
# Testējiet API savienojumu
import requests
try:
    response = requests.get('https://api.openai.com/v1/models', 
                          headers={'Authorization': f'Bearer {api_key}'})
    print(f"API Status: {response.status_code}")
except Exception as e:
    print(f"API Error: {e}")
```

### Veiktspējas Optimizācija

#### 1. Kešošana

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_function(param):
    # Dārga operācija
    return result
```

#### 2. Async Operācijas

```python
import asyncio
import aiohttp

async def async_api_call():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

#### 3. Datu bāzes Optimizācija

```python
# Izmantojiet connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Monitorings

#### 1. Health Check Endpoint

```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
```

#### 2. Metriku Savākšana

```python
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')

@app.before_request
def before_request():
    request_count.inc()
    g.start_time = time.time()

@app.after_request
def after_request(response):
    request_duration.observe(time.time() - g.start_time)
    return response
```

#### 3. Error Tracking

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

## Izvietošanas Checklist

Pirms izvietošanas pārbaudiet:

- [ ] Visi nepieciešamie faili ir repozitorijā
- [ ] requirements.txt ir atjaunināts
- [ ] Vides mainīgie ir konfigurēti
- [ ] OpenAI API atslēga ir derīga
- [ ] Aplikācija darbojas lokāli
- [ ] CORS ir konfigurēts
- [ ] Ports ir dinamisks
- [ ] Datu bāzes ceļi ir relatīvi
- [ ] .gitignore ir konfigurēts
- [ ] Dokumentācija ir atjaunināta

Pēc izvietošanas pārbaudiet:

- [ ] Aplikācija ir pieejama
- [ ] API galapunkti darbojas
- [ ] Web saskarne ielādējas
- [ ] Workflow ģenerēšana darbojas
- [ ] Daudzvalodu atbalsts darbojas
- [ ] Kļūdu apstrāde darbojas
- [ ] SSL sertifikāts ir aktīvs
- [ ] Domēns ir konfigurēts

## Atbalsts

Ja rodas problēmas ar izvietošanu:

1. Pārbaudiet platformas dokumentāciju
2. Skatiet aplikācijas logus
3. Pārbaudiet vides mainīgos
4. Testējiet lokāli
5. Meklējiet palīdzību platformas atbalsta kanālos

**Platformu atbalsta resursi:**
- Railway: [Discord](https://discord.gg/railway)
- Heroku: [Dev Center](https://devcenter.heroku.com/)
- Render: [Documentation](https://render.com/docs)
- DigitalOcean: [Community](https://www.digitalocean.com/community)

Veiksmīgu izvietošanu!


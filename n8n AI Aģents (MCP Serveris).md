# n8n AI Aģents (MCP Serveris)

🤖 **Daudzvalodu AI aģents, kas pārvērš dabisku valodu n8n workflow**

## 📋 Satura rādītājs

- [Apraksts](#apraksts)
- [Galvenās funkcijas](#galvenās-funkcijas)
- [Instalācija](#instalācija)
- [Lietošana](#lietošana)
- [API dokumentācija](#api-dokumentācija)
- [Daudzvalodu atbalsts](#daudzvalodu-atbalsts)
- [n8n integrācija](#n8n-integrācija)
- [Konfigurācija](#konfigurācija)
- [Testēšana](#testēšana)
- [Problēmu risināšana](#problēmu-risināšana)

## 🎯 Apraksts

n8n AI Aģents ir MCP (Model Context Protocol) serveris, kas darbojas kā starpnieks starp cilvēka dabisku valodu un n8n workflow radīšanu. Sistēma spēj saprast pieprasījumus latviešu, krievu un angļu valodās, analizēt tos un automātiski ģenerēt gatavus n8n workflow.

### Galvenās priekšrocības

- 🌐 **Daudzvalodu atbalsts** - Latviešu, krievu un angļu valoda
- 🧠 **AI-vadīta analīze** - Izmanto Claude Sonnet 4 līmeņa modeļus
- 🔍 **Vektoru meklēšana** - Atrod līdzīgus workflow no bāzes
- 📤 **Tiešā integrācija** - Augšupielādē workflow tieši uz n8n
- 🎨 **Web saskarne** - Ērti lietojama grafiskā saskarne
- 🔧 **API pieejamība** - Pilna REST API funkcionalitāte

## ⭐ Galvenās funkcijas

### 1. Workflow Ģenerēšana
- Analizē dabiskās valodas pieprasījumus
- Ģenerē pilnīgus n8n workflow JSON formātā
- Sniedz uzstādīšanas instrukcijas
- Paskaidro workflow loģiku

### 2. Līdzīgu Workflow Meklēšana
- Izmanto vektoru datu bāzi (Qdrant)
- Atrod līdzīgus workflow no 2300+ piemēru bāzes
- Novērtē līdzības pakāpi
- Iesaka modificēšanas

### 3. n8n Integrācija
- Tiešā savienojuma ar n8n API
- Workflow augšupielāde un aktivizēšana
- Workflow testēšana
- Workflow pārvaldība

### 4. Daudzvalodu Atbalsts
- Automātiska valodas noteikšana
- Lokalizēti ziņojumi un saskarne
- Valodu specifiski prompt veidnes
- Atslēgvārdu ekstraktēšana visās valodās

## 🚀 Instalācija

### Priekšnosacījumi

- Python 3.11+
- Node.js 20+ (opcionāli)
- n8n instance (opcionāli)
- Qdrant vektoru datu bāze (opcionāli)

### 1. Klonēt repozitoriju

```bash
git clone <repository-url>
cd n8n_ai_agent_server
```

### 2. Izveidot virtuālo vidi

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# vai
venv\\Scripts\\activate  # Windows
```

### 3. Instalēt atkarības

```bash
pip install -r requirements.txt
```

### 4. Konfigurēt vides mainīgos

Izveidojiet `.env` failu:

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=development
FLASK_DEBUG=1
```

### 5. Palaist serveri

```bash
python src/main.py
```

Serveris būs pieejams: `http://localhost:5000`

## 💻 Lietošana

### Web Saskarne

1. Atveriet `http://localhost:5000` pārlūkprogrammā
2. Ievadiet savu pieprasījumu jebkurā atbalstītajā valodā
3. Izvēlieties maksimālo līdzīgo workflow skaitu
4. Noklikšķiniet "Ģenerēt Workflow"

#### Piemēri pieprasījumiem:

**Latviešu valodā:**
```
Izveidot Telegram botu, kas pieraksta klientus uz tikšanos un saglabā informāciju MySQL datu bāzē
```

**Krievu valodā:**
```
Создать телеграм бота для записи клиентов на встречи с сохранением в базу данных MySQL
```

**Angļu valodā:**
```
Create a Telegram bot for client appointment booking with MySQL database storage
```

### n8n Konfigurācija

1. Noklikšķiniet "⚙️ n8n Konfigurācija"
2. Ievadiet n8n servera URL (piemēram: `http://localhost:5678`)
3. Ievadiet API atslēgu
4. Noklikšķiniet "Testēt Savienojumu"
5. Saglabājiet konfigurāciju

### Workflow Augšupielāde

Pēc workflow ģenerēšanas:

1. Pārbaudiet ģenerēto workflow
2. Konfigurējiet n8n savienojumu
3. Izvēlieties augšupielādes opcijas:
   - ✅ Aktivizēt workflow pēc augšupielādes
   - ✅ Testēt workflow izpildi
4. Noklikšķiniet "📤 Augšupielādēt uz n8n"

## 🔌 API dokumentācija

### Workflow API

#### POST `/api/workflow/generate`
Ģenerē jaunu workflow no dabiskās valodas pieprasījuma.

**Pieprasījums:**
```json
{
    "query": "Izveidot Telegram botu pierakstam",
    "max_results": 3
}
```

**Atbilde:**
```json
{
    "success": true,
    "query_analysis": {
        "language": "lv",
        "intent": "create_workflow",
        "keywords": ["telegram", "bot", "appointment"]
    },
    "workflow": {
        "name": "Telegram Bot Workflow",
        "nodes": [...],
        "connections": {...}
    },
    "setup_instructions": [...],
    "explanation": "Šis workflow izveido..."
}
```

#### POST `/api/workflow/search`
Meklē līdzīgus workflow.

**Pieprasījums:**
```json
{
    "query": "telegram bot",
    "max_results": 5
}
```

#### GET `/api/workflow/health`
Pārbauda sistēmas stāvokli.

#### GET `/api/workflow/statistics`
Iegūst sistēmas statistiku.

### n8n API

#### POST `/api/n8n/configure`
Konfigurē n8n savienojumu.

#### GET `/api/n8n/connection/test`
Testē n8n savienojumu.

#### POST `/api/n8n/workflows/upload`
Augšupielādē workflow uz n8n.

#### GET `/api/n8n/workflows`
Iegūst n8n workflow sarakstu.

#### POST `/api/n8n/generate-and-upload`
Ģenerē un uzreiz augšupielādē workflow.

## 🌐 Daudzvalodu atbalsts

### Atbalstītās valodas

- **Latviešu (lv)** - Pilns atbalsts
- **Krievu (ru)** - Pilns atbalsts  
- **Angļu (en)** - Pilns atbalsts

### Valodas noteikšana

Sistēma automātiski nosaka ievades valodu, pamatojoties uz:
- Specifiskām rakstzīmēm (ā, č, ē, ģ, ī, ķ, ļ, ņ, š, ū, ž latviešu valodā)
- Cirilicas rakstzīmēm (krievu valodā)
- Valodu specifiskiem vārdiem un modeļiem

### Atslēgvārdu ekstraktēšana

Katrai valodai ir definēti specifiski atslēgvārdi:

**Darbības:**
- LV: izveidot, radīt, sūtīt, saglabāt
- RU: создать, отправить, сохранить
- EN: create, send, save

**Servisi:**
- LV: telegram, epasts, datu bāze
- RU: телеграм, почта, база данных
- EN: telegram, email, database

## 🔗 n8n integrācija

### API Autentifikācija

n8n API izmanto API atslēgas autentifikāciju:

1. n8n iestatījumos izveidojiet API atslēgu
2. Konfigurējiet to sistēmā
3. Sistēma automātiski izmanto to visiem pieprasījumiem

### Atbalstītās n8n funkcijas

- ✅ Workflow izveide
- ✅ Workflow atjaunināšana
- ✅ Workflow aktivizēšana/deaktivizēšana
- ✅ Workflow dzēšana
- ✅ Workflow testēšana
- ✅ Workflow saraksta iegūšana

### Workflow Validācija

Pirms augšupielādes sistēma validē:
- Workflow struktūru
- Mezglu konfigurāciju
- Savienojumu pareizību
- Parametru derīgumu

## ⚙️ Konfigurācija

### Vides mainīgie

```env
# OpenAI API
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1

# Flask konfigurācija
FLASK_ENV=development
FLASK_DEBUG=1
FLASK_SECRET_KEY=your-secret-key

# Qdrant konfigurācija (opcionāli)
QDRANT_HOST=localhost
QDRANT_PORT=6333

# n8n konfigurācija (opcionāli)
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your-n8n-api-key
```

### Datu bāzes konfigurācija

Sistēma izmanto vairākas datu bāzes:

1. **SQLite** - Lietotāju dati un sesijas
2. **Qdrant** - Vektoru meklēšana (opcionāli)
3. **JSON faili** - n8n mezglu konfigurācijas

### Logging konfigurācija

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🧪 Testēšana

### Palaist visus testus

```bash
# Pamata funkcionalitātes testi
python tests/test_basic_functionality.py

# Daudzvalodu atbalsta testi
python tests/test_multilingual.py

# API testi (nepieciešams darbojošs serveris)
python tests/test_api_endpoints.py
```

### Testa kategorijas

1. **Pamata funkcionalitāte**
   - Workflow struktūras validācija
   - JSON apstrāde
   - Kļūdu apstrāde

2. **Daudzvalodu atbalsts**
   - Valodu noteikšana
   - Atslēgvārdu ekstraktēšana
   - Lokalizācija

3. **API funkcionalitāte**
   - Galapunktu testēšana
   - Atbildes validācija
   - Kļūdu scenāriji

4. **Integrācijas testi**
   - n8n API savienojums
   - Workflow augšupielāde
   - Vektoru meklēšana

### Manuālā testēšana

1. **Web saskarne:**
   - Atveriet `http://localhost:5000`
   - Testējiet dažādus pieprasījumus
   - Pārbaudiet valodu maiņu

2. **API testēšana:**
   ```bash
   # Workflow ģenerēšana
   curl -X POST http://localhost:5000/api/workflow/generate \
     -H "Content-Type: application/json" \
     -d '{"query": "create telegram bot", "max_results": 3}'
   
   # Sistēmas stāvoklis
   curl http://localhost:5000/api/workflow/health
   ```

3. **n8n integrācija:**
   - Konfigurējiet n8n savienojumu
   - Testējiet workflow augšupielādi
   - Pārbaudiet workflow n8n saskarnē

## 🔧 Problēmu risināšana

### Biežākās problēmas

#### 1. OpenAI API kļūdas

**Problēma:** `openai.AuthenticationError`
**Risinājums:**
```bash
export OPENAI_API_KEY=your-actual-api-key
```

#### 2. n8n savienojuma problēmas

**Problēma:** "Connection error"
**Risinājums:**
- Pārbaudiet n8n servera URL
- Pārbaudiet API atslēgas derīgumu
- Pārbaudiet n8n servera pieejamību

#### 3. Qdrant savienojuma problēmas

**Problēma:** "Qdrant nav pieejams"
**Risinājums:**
```bash
# Palaist Qdrant ar Docker
docker run -p 6333:6333 qdrant/qdrant
```

#### 4. Valodu noteikšanas problēmas

**Problēma:** Nepareiza valodas noteikšana
**Risinājums:**
- Pārbaudiet teksta garumu (minimums 3 rakstzīmes)
- Izmantojiet valodu specifiskas rakstzīmes
- Pievienojiet vairāk konteksta

### Debugging

#### Iespējot debug režīmu

```bash
export FLASK_DEBUG=1
export FLASK_ENV=development
```

#### Pārbaudīt logus

```bash
tail -f logs/app.log
```

#### API debugging

```bash
# Pārbaudīt sistēmas stāvokli
curl -v http://localhost:5000/api/workflow/health

# Pārbaudīt statistiku
curl -v http://localhost:5000/api/workflow/statistics
```

### Veiktspējas optimizācija

1. **Vektoru meklēšanas optimizācija:**
   - Ierobežojiet meklēšanas rezultātu skaitu
   - Izmantojiet kešošanu

2. **AI modeļa optimizācija:**
   - Samaziniet prompt garumu
   - Izmantojiet batch pieprasījumus

3. **Datu bāzes optimizācija:**
   - Izveidojiet indeksus
   - Izmantojiet savienojumu pooling

## 📞 Atbalsts

### Dokumentācija

- [Tehniskā dokumentācija](docs/technical_documentation.md)
- [API dokumentācija](docs/api_documentation.md)
- [Izstrādātāju rokasgrāmata](docs/developer_guide.md)

### Kontakti

- **Izstrādātājs:** Manus AI
- **E-pasts:** support@manus.ai
- **Dokumentācija:** https://docs.manus.ai

### Licences

Šis projekts ir licencēts saskaņā ar MIT licenci. Skatiet LICENSE failu sīkākai informācijai.

---

**Piezīme:** Šī dokumentācija tiek regulāri atjaunināta. Jaunākā versija vienmēr ir pieejama projekta repozitorijā.


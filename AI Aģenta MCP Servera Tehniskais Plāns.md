# AI Aģenta MCP Servera Tehniskais Plāns
## n8n Workflow Ģenerēšanas Sistēma

**Autors:** Manus AI  
**Datums:** 2025-01-26  
**Versija:** 1.0

## Ievads

Šis dokuments apraksta AI aģenta (MCP servera) tehnisko implementāciju, kas darbojas kā starpnieks starp cilvēka dabisku valodu un n8n workflow radīšanu. Sistēma ir veidota, lai automatizētu sarežģītu darbplūsmu izveidi, pamatojoties uz lietotāja prasībām dabiskajā valodā.

## Projekta Mērķi un Uzdevumi

### Galvenais Mērķis
Izveidot inteliģentu AI aģentu, kas spēj:
- Saprast lietotāja pieprasījumus krievu, latviešu vai angļu valodā
- Analizēt un salīdzināt ar esošām n8n workflow ķēdēm
- Ģenerēt jaunus n8n JSON workflow no nulles
- Pielāgot un paplašināt esošos workflow
- Nodrošināt pilnu integrāciju ar n8n instanci

### Specifiskās Funkcionalitātes
1. **Dabiskās valodas apstrāde** - Spēja interpretēt sarežģītus pieprasījumus dažādās valodās
2. **Workflow analīze** - Salīdzināšana ar 2300+ gatavu workflow bāzi
3. **Ģeneratīvā loģika** - Jaunu workflow radīšana, izmantojot Claude Sonnet 4 līmeņa modeļus
4. **Komponentu pielāgošana** - Node aizstāšana un konfigurācija (OpenAI → OpenRouter, utt.)
5. **API integrācija** - Tiešs savienojums ar n8n instanci
6. **Validācija un kļūdu apstrāde** - Automātiska workflow pārbaude un kļūdu ziņošana




## Sistēmas Arhitektūra

Sistēma sastāvēs no vairākiem slāņiem, kas nodrošinās modulāru un mērogojamu pieeju. Galvenie slāņi ir Lietotāja Saskarnes Slānis, AI Aģenta Kodols, Zināšanu Bāzes Slānis, n8n Integrācijas Slānis un Atbalsta Servisi.

![Sistēmas Arhitektūra](https://private-us-east-1.manuscdn.com/sessionFile/9AWsytzde2SxCNAg8yY86w/sandbox/nEp1jQgqbMQXVEgj35Fet4-images_1753562812434_na1fn_L2hvbWUvdWJ1bnR1L3N5c3RlbV9hcmNoaXRlY3R1cmU.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvOUFXc3l0emRlMlN4Q05BZzh5WTg2dy9zYW5kYm94L25FcDFqUWdxYk1RWFZFZ2ozNUZldDQtaW1hZ2VzXzE3NTM1NjI4MTI0MzRfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzTjVjM1JsYlY5aGNtTm9hWFJsWTNSMWNtVS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=ln34sjHfmefq43NRN~IzhUHG-Yhxqrr~Z1HOh7FyiSeepiUS6h93JQCglJsvAK1rh2Yet4fmXHhZHS5ufSXp7x~gPAjK~QHeZgYEbjQJ4eunPEmUV3WOrAGLUOpkBhKE8eQqzvhHHt8GiqXzht9AWQYgCgqB4ZncNLkpYnVCwpKLTcZy9EKHl1FJFJ615RFCPRVirktzdUAsGFw~S0x5rZKCwj~rtU3XgeDmVdt8iuyI1lTvww3bI2wY~lK9moCm-RjTeU6RRpxh2z0GAZUY-B3K7AYTTeT5SUnGgx6MG71XuP3fCSd0zO6qPL7pXkmPEaMOPXD8E4uOrd9-e2e1Ow__)

### Komponentu Apraksts

*   **Lietotāja Saskarnes Slānis:**
    *   **Web Interface (UI):** Nodrošinās lietotājam draudzīgu saskarni pieprasījumu ievadīšanai un rezultātu apskatei.
    *   **API Gateway (API_GW):** Vienots piekļuves punkts visiem pakalpojumiem, nodrošinot maršrutēšanu, slodzes balansēšanu un drošību.
    *   **Authentication Service (AUTH):** Atbildēs par lietotāju autentifikāciju un autorizāciju.

*   **AI Aģenta Kodols:**
    *   **Natural Language Processor (NLP):** Apstrādās lietotāja ievadi dabiskajā valodā, veicot tokenizāciju, lingvistisko analīzi un entītiju atpazīšanu.
    *   **Intent Analyzer (INTENT):** Noteiks lietotāja pieprasījuma mērķi un nolūku, pamatojoties uz NLP rezultātiem.
    *   **Workflow Generator (WORKFLOW_GEN):** Galvenais komponents, kas ģenerēs n8n workflow JSON, izmantojot ģeneratīvos modeļus un zināšanu bāzi.
    *   **Workflow Validator (VALIDATOR):** Pārbaudīs ģenerētā workflow loģisko pareizību un atbilstību n8n specifikācijām.

*   **Zināšanu Bāzes Slānis:**
    *   **Vector Database (VECTOR_DB):** Izmantos vektoru meklētāju (Qdrant vai Weaviate) esošo workflow salīdzināšanai un meklēšanai.
    *   **Workflow Database (WORKFLOW_DB):** Saturēs 2300+ gatavus n8n workflow JSON formātā ar metadatiem.
    *   **Node Configuration DB (NODE_DB):** Uzglabās informāciju par n8n mezgliem (nodes), to konfigurāciju un pielietojumu, pamatojoties uz n8n dokumentāciju.

*   **n8n Integrācija:**
    *   **n8n API Client (N8N_API):** Nodrošinās komunikāciju ar reālu n8n instanci, izmantojot tās API.
    *   **n8n Instance (N8N_INSTANCE):** Reāla n8n instalācija, kurā tiks augšupielādēti un izpildīti ģenerētie workflow.
    *   **Workflow Deployment (WORKFLOW_DEPLOY):** Atbildēs par workflow augšupielādi un aktivizēšanu n8n instancē.

*   **Atbalsta Servisi:**
    *   **Redis Cache (CACHE):** Nodrošinās ātru piekļuvi bieži izmantotiem datiem un samazinās slodzi uz datu bāzēm.
    *   **Logging Service (LOGGER):** Reģistrēs sistēmas darbības un kļūdas, atvieglojot atkļūdošanu un monitoringu.
    *   **Monitoring & Metrics (MONITOR):** Vāks veiktspējas datus un nodrošinās sistēmas veselības monitoringu.

## Tehniskās Prasības

### Valodas un Tehnoloģijas
*   **Backend:** Python ar FastAPI ietvaru.
*   **Vektoru Meklētājs:** Qdrant vai Weaviate.
*   **Datu Bāze:** PostgreSQL (vai līdzīga) metadatiem un konfigurācijai.
*   **Kešatmiņa:** Redis.
*   **AI Modelis:** Claude Sonnet 4 (vai pielīdzināms modelis) workflow ģenerēšanai.
*   **Valodu Atbalsts:** Krievu, latviešu, angļu.

### Veiktspēja un Mērogojamība
*   Sistēmai jāspēj apstrādāt vairākus vienlaicīgus pieprasījumus.
*   Workflow ģenerēšanas laikam jābūt optimizētam, lai nodrošinātu ātru atbildes laiku.
*   Jānodrošina mērogojamība, lai nākotnē varētu pievienot jaunus workflow un mezglus.

### Drošība
*   Jāimplementē droša autentifikācijas un autorizācijas sistēma.
*   API atslēgas un citi sensitīvi dati jāglabā droši (piemēram, izmantojot vides mainīgos vai slepenu pārvaldības sistēmu).
*   Jānodrošina datu šifrēšana gan pārsūtīšanas, gan glabāšanas laikā.

## Implementācijas Plāns

### 1. fāze: Projekta struktūras un arhitektūras plānošana (Pabeigta)
*   Detalizēta tehniska plāna izveide.
*   Sistēmas arhitektūras diagrammas izveide.

### 2. fāze: n8n dokumentācijas un workflow struktūras izpēte
*   Padziļināta n8n API dokumentācijas izpēte.
*   n8n workflow JSON struktūras analīze.
*   Izpratne par n8n mezglu (nodes) konfigurāciju un to parametriem.
*   Datu modelēšana n8n mezglu informācijas glabāšanai.

### 3. fāze: Vektoru meklētāja un zināšanu bāzes dizains
*   Vektoru datu bāzes (Qdrant/Weaviate) iestatīšana.
*   2300+ gatavu workflow JSON importēšana un vektorizēšana.
*   Meklēšanas algoritmu izstrāde, lai atrastu atbilstošus workflow, pamatojoties uz lietotāja pieprasījumu.
*   Zināšanu bāzes izveide n8n mezglu konfigurācijai.

### 4. fāze: AI prompt sistēmas izveide
*   Strukturētu promptu izstrāde Claude Sonnet 4 modelim, lai ģenerētu n8n workflow JSON.
*   Promptu optimizācija, lai nodrošinātu precīzu un efektīvu workflow ģenerēšanu.
*   Fallback loģikas izstrāde, ja AI modelis nespēj ģenerēt atbilstošu workflow.

### 5. fāze: MCP servera backend izstrāde
*   FastAPI lietojumprogrammas iestatīšana.
*   API galapunktu (endpoints) izveide lietotāja pieprasījumu apstrādei.
*   Dabiskās valodas apstrādes un nolūka analīzes moduļu implementācija.
*   Workflow ģenerēšanas un validācijas loģikas integrācija.

### 6. fāze: n8n API integrācija
*   n8n API klienta izstrāde.
*   Funkcionalitātes implementācija workflow augšupielādei, atjaunināšanai un izpildei n8n instancē.
*   Kļūdu apstrāde un ziņošana par n8n API kļūdām.

### 7. fāze: Daudzvalodu atbalsta implementācija
*   Valodu noteikšanas moduļa integrācija.
*   Teksta tulkošanas servisu izmantošana (ja nepieciešams) lietotāja ievades apstrādei un atbilžu ģenerēšanai.
*   Lietotāja saskarnes lokalizācija.

### 8. fāze: Testēšana un dokumentācijas izveide
*   Vienību (unit) un integrācijas testu izstrāde visiem sistēmas komponentiem.
*   Veiktspējas testēšana un optimizācija.
*   Lietošanas dokumentācijas izveide lietotājiem un izstrādātājiem.
*   Kļūdu saraksta un to risinājumu apraksts.

### 9. fāze: Rezultātu prezentācija lietotājam
*   Gatavās sistēmas demonstrācija.
*   Detalizētas instrukcijas par sistēmas iestatīšanu un lietošanu.
*   Atbildes uz lietotāja jautājumiem un turpmāko soļu apspriešana.

## Drošības Apsvērumi

*   **Autentifikācija un Autorizācija:** Tiks izmantoti JWT (JSON Web Tokens) lietotāju autentifikācijai un lomu balstītai piekļuves kontrolei (RBAC) autorizācijai.
*   **Datu Šifrēšana:** Visi sensitīvie dati (piemēram, API atslēgas, lietotāju paroles) tiks šifrēti gan pārsūtīšanas (TLS/SSL), gan glabāšanas laikā (AES-256).
*   **Ievades Validācija:** Visas lietotāja ievades tiks rūpīgi validētas, lai novērstu ievainojamības, piemēram, SQL injekcijas un XSS (Cross-Site Scripting) uzbrukumus.
*   **Kļūdu Apstrāde:** Kļūdu ziņojumi netiks atklāti lietotājiem, lai novērstu informācijas noplūdi. Tā vietā tiks reģistrētas detalizētas kļūdas servera žurnālos.
*   **Atkarību Skenēšana:** Regulāri tiks veiktas atkarību skenēšanas, lai identificētu un novērstu zināmas ievainojamības trešo pušu bibliotēkās.

## Secinājumi

Šis tehniskais plāns nodrošina pamatu AI aģenta (MCP servera) izstrādei, kas ievērojami atvieglos n8n workflow radīšanu un pārvaldību. Sekojot šim plānam, tiks izveidota robusta, mērogojama un droša sistēma, kas atbilst visām definētajām prasībām.




## n8n Dokumentācijas un Workflow Struktūras Izpētes Rezultāti

### n8n API Pārskats

n8n piedāvā publisku REST API, kas ļauj programmatiski veikt daudzas darbības, ko var veikt, izmantojot grafisko lietotāja saskarni (GUI). Galvenās API funkcijas ietver:

*   **Autentifikācija:** API piekļuvei nepieciešama autentifikācija. Dokumentācija apraksta autentifikācijas metodes, kas parasti ietver API atslēgas vai OAuth.
*   **Resursi:** API nodrošina piekļuvi dažādiem resursiem, piemēram, workflow, kredenciāliem, lietotājiem un izpildēm. Katram resursam ir definēti galapunkti (endpoints) ar atbilstošām HTTP metodēm (GET, POST, PUT, DELETE).
*   **Lapu numerācija (Pagination):** Lielu datu kopu gadījumā API atbalsta lapu numerāciju, lai efektīvi iegūtu datus pa daļām.
*   **API Playground:** Pašmitinātām n8n instancēm ir pieejams iebūvēts API playground, kas ļauj testēt API pieprasījumus un saprast to darbību.

### n8n Workflow JSON Struktūra

n8n workflow tiek saglabāti JSON formātā. Šis JSON fails apraksta visu workflow loģiku, ieskaitot mezglus (nodes), to savienojumus, konfigurāciju un metadatus. Galvenās JSON struktūras sastāvdaļas ir:

*   **`nodes`:** Masīvs, kas satur visus workflow mezglus. Katrs mezgls ir objekts ar šādām galvenajām īpašībām:
    *   `parameters`: Objekts, kas satur mezgla specifiskos konfigurācijas parametrus. Šie parametri atšķiras atkarībā no mezgla tipa un tā funkcijas (piemēram, HTTP Request mezglam būs URL, metode, hederi, utt.).
    *   `type`: Mezglu tips (piemēram, `n8n-nodes-base.httpRequest`, `n8n-nodes-base.webhook`).
    *   `name`: Mezglu nosaukums (unikāls workflow ietvaros).
    *   `id`: Unikāls mezgla identifikators.
    *   `credentials`: (Pēc izvēles) Objekts, kas norāda uz izmantotajiem kredenciāliem (piemēram, API atslēgas, OAuth tokens).
    *   `position`: Mezglu pozīcija uz kanvas (x, y koordinātes).
*   **`connections`:** Objekts, kas apraksta savienojumus starp mezgliem. Tas norāda, kurš mezgls ir savienots ar kuru un kāda veida dati tiek pārsūtīti.
*   **`active`:** Būla vērtība, kas norāda, vai workflow ir aktīvs vai deaktivizēts.
*   **`name`:** Workflow nosaukums.
*   **`id`:** Unikāls workflow identifikators.
*   **`version`:** Workflow versija.
*   **`nodes`:** Mezglu masīvs, katrs mezgls ir objekts ar saviem parametriem.

**Svarīga piezīme:** n8n workflow JSON nav stingras JSON shēmas. Mezglu parametri tiek veidoti dinamiski, ielādējot tos uz kanvas. Tas nozīmē, ka modeļiem, kas ģenerē workflow, ir jābūt labi apmācītiem par n8n mezglu darbību un to parametru struktūru.

### n8n Mezglu (Nodes) Konfigurācija

Mezgli ir n8n darbplūsmu galvenie elementi. Tie veic dažādas darbības, piemēram, uzsāk darbplūsmu, iegūst un sūta datus, apstrādā un manipulē ar datiem. Katram mezglam ir savi specifiski konfigurācijas parametri, kas nosaka tā darbību. Šie parametri ir atkarīgi no mezgla tipa un tā paredzētās funkcijas. Piemēram:

*   **HTTP Request mezgls:** Konfigurācijas parametri ietver URL, HTTP metodi (GET, POST, PUT, DELETE), hederus, pieprasījuma ķermeni, autentifikācijas datus, utt.
*   **Webhook mezgls:** Konfigurācijas parametri ietver webhook URL, HTTP metodi, autentifikācijas metodes, utt.
*   **Function mezgls:** Ļauj izpildīt pielāgotu JavaScript kodu, tāpēc tā konfigurācija ietver pašu kodu.

Mezglu iestatījumi ietver arī vispārīgus iestatījumus, piemēram, kļūdu apstrādi (apturēt workflow, turpināt, turpināt ar kļūdas izvadi), pakešu apstrādi (batching), SSL ignorēšanu, taimautus un piezīmes.

### Datu Modelēšana n8n Mezglu Informācijas Glabāšanai

Lai efektīvi ģenerētu un pārvaldītu n8n workflow, ir nepieciešams strukturēts datu modelis, kas glabā informāciju par n8n mezgliem un to konfigurāciju. Šis modelis varētu ietvert šādas entītijas:

#### 1. `Node` (Mezgls)
*   `id`: Unikāls mezgla identifikators (piemēram, `n8n-nodes-base.httpRequest`).
*   `name`: Mezglu nosaukums (piemēram, 


HTTP Request).
*   `description`: Īss mezgla apraksts.
*   `category`: Mezglu kategorija (piemēram, Triggers, Core, Integrations).
*   `parameters_schema`: JSON shēma, kas apraksta mezgla konfigurācijas parametrus, to tipus, obligātumu un noklusējuma vērtības.
*   `example_usage`: Koda piemēri vai JSON fragmenti, kas parāda, kā mezglu izmantot tipiskos scenārijos.

#### 2. `Parameter` (Parametrs)
*   `id`: Unikāls parametra identifikators (piemēram, `url`, `method`).
*   `node_id`: Atsauce uz `Node` entītiju, kurai šis parametrs pieder.
*   `name`: Parametra nosaukums.
*   `type`: Parametra datu tips (piemēram, string, boolean, number, array, object).
*   `description`: Parametra apraksts.
*   `required`: Būla vērtība, kas norāda, vai parametrs ir obligāts.
*   `default_value`: Parametra noklusējuma vērtība (ja tāda ir).
*   `options`: (Pēc izvēles) Saraksts ar pieļaujamām vērtībām (ja parametrs ir izvēles saraksts).

Šāds datu modelis ļaus sistēmai efektīvi meklēt, izprast un ģenerēt n8n workflow, nodrošinot precīzu mezglu konfigurāciju, pamatojoties uz lietotāja pieprasījumiem dabiskajā valodā.



## Vektoru Meklētāja un Zināšanu Bāzes Dizaina Rezultāti

### Vektoru Datu Bāzes Izvēle: Qdrant

Pēc rūpīgas analīzes tika izvēlēts **Qdrant** kā galvenā vektoru datu bāze šādu iemeslu dēļ:

*   **Augsta Veiktspēja:** Qdrant ir optimizēts ātrumam un efektivitātei, kas ir kritisks workflow meklēšanai reālajā laikā.
*   **Rust Implementācija:** Nodrošina efektīvu resursu izmantošanu un stabilitāti.
*   **Vienkārša Iestatīšana:** Docker atbalsts un laba dokumentācija atvieglo implementāciju.
*   **Mērogojamība:** Spēj apstrādāt miljardiem vektoru, kas ir nepieciešams 2300+ workflow bāzes pārvaldībai.

### Workflow Vektorizēšanas Sistēma

Tika izstrādāta pilnīga workflow vektorizēšanas sistēma, kas ietver:

#### WorkflowVectorizer Klase
*   **Iezīmju Ekstraktēšana:** Analizē workflow JSON un ekstraktē galvenās iezīmes teksta formātā.
*   **Sarežģītības Aprēķināšana:** Nosaka workflow sarežģītības punktu skaitu, pamatojoties uz mezglu skaitu, savienojumiem un mezglu tipiem.
*   **Embedding Ģenerēšana:** Izmanto OpenAI text-embedding-ada-002 modeli vektoru ģenerēšanai.
*   **Metadatu Pārvaldība:** Izveido strukturētus metadatus katram workflow.

#### Galvenās Funkcijas
*   `extract_workflow_features()`: Ekstraktē workflow galvenās iezīmes
*   `calculate_complexity_score()`: Aprēķina sarežģītības punktu skaitu (0-100)
*   `generate_embedding()`: Ģenerē 1536-dimensiju vektoru
*   `vectorize_workflow()`: Pilns workflow vektorizēšanas process

### Qdrant Datu Bāzes Integrācija

#### QdrantWorkflowDatabase Klase
*   **Kolekcijas Pārvaldība:** Automātiska kolekcijas izveide ar pareiziem parametriem.
*   **Workflow Glabāšana:** Efektīva workflow vektoru un metadatu glabāšana.
*   **Meklēšanas Funkcionalitāte:** Kosinusa līdzības meklēšana ar filtrēšanas iespējām.
*   **Statistikas Iegūšana:** Kolekcijas statistikas un veiktspējas monitorings.

#### Galvenās Metodes
*   `initialize_collection()`: Inicializē Qdrant kolekciju
*   `add_workflow()`: Pievieno workflow vektoru
*   `search_similar_workflows()`: Meklē līdzīgus workflow
*   `get_workflow_by_id()`: Iegūst konkrētu workflow

### Inteliģentais Meklēšanas Algoritms

#### Dabiskās Valodas Apstrāde
Tika izstrādāta `NaturalLanguageProcessor` klase, kas nodrošina:

*   **Valodas Noteikšana:** Automātiska krievu, latviešu un angļu valodas noteikšana.
*   **Atslēgvārdu Ekstraktēšana:** Daudzvalodu atslēgvārdu vārdnīcas izmantošana.
*   **Entītiju Atpazīšana:** Servisu, darbību un tehnoloģiju identificēšana.
*   **Nolūka Analīze:** Lietotāja nolūka noteikšana (izveidot, atrast, modificēt, izskaidrot).

#### Meklēšanas Dzinējs
`WorkflowSearchEngine` klase implementē:

*   **Vaicājumu Parsēšana:** Sarežģītu dabiskās valodas vaicājumu analīze.
*   **Vektoru Meklēšana:** Semantiska līdzība, izmantojot Qdrant.
*   **Rezultātu Filtrēšana:** Kategoriju un sarežģītības filtri.
*   **Rezultātu Ranžēšana:** Kombinēta punktu sistēma (vektoru līdzība + atslēgvārdu atbilstība).
*   **Ieteikumu Ģenerēšana:** Automātiski ieteikumi workflow modificēšanai.

### n8n Mezglu Konfigurācijas Zināšanu Bāze

#### NodeConfigurationDatabase Klase
Tika izveidota SQLite bāzēta sistēma, kas glabā:

*   **Mezglu Informāciju:** Pilns mezglu apraksts, kategorijas, ikonu.
*   **Parametru Definīcijas:** Detalizēta parametru struktūra ar validācijas noteikumiem.
*   **Lietošanas Piemēri:** Praktiski konfigurācijas piemēri katram mezglam.
*   **Saistītie Mezgli:** Informācija par mezglu savstarpējām attiecībām.

#### Galvenās Funkcijas
*   **Mezglu Meklēšana:** Meklēšana pēc nosaukuma, apraksta vai kategorijas.
*   **Konfigurācijas Ģenerēšana:** Automātiska mezgla JSON konfigurācijas izveide.
*   **Parametru Validācija:** Mezgla parametru pareizības pārbaude.
*   **Noklusējuma Mezgli:** Iepriekš konfigurēti populāri mezgli (Telegram, HTTP Request, Function, Webhook).

### Datu Struktūras

#### WorkflowMetadata
```python
@dataclass
class WorkflowMetadata:
    id: str
    name: str
    description: str
    category: str
    tags: List[str]
    nodes_count: int
    complexity_score: int
    language: str
    created_at: str
```

#### NodeConfiguration
```python
@dataclass
class NodeConfiguration:
    node_id: str
    name: str
    display_name: str
    description: str
    category: str
    subcategory: str
    parameters: List[NodeParameter]
    example_config: Dict[str, Any]
    common_use_cases: List[str]
```

### Implementācijas Priekšrocības

1. **Mērogojamība:** Sistēma var apstrādāt tūkstošiem workflow bez veiktspējas zuduma.
2. **Daudzvalodība:** Atbalsts krievu, latviešu un angļu valodām.
3. **Precizitāte:** Kombinēta semantiska un atslēgvārdu meklēšana nodrošina augstu precizitāti.
4. **Paplašināmība:** Modulāra arhitektūra ļauj viegli pievienot jaunus mezglus un funkcijas.
5. **Validācija:** Automātiska workflow un parametru validācija novērš kļūdas.

Šī sistēma nodrošina stabilu pamatu AI aģenta workflow ģenerēšanas un meklēšanas funkcionalitātei.


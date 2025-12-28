# LexiDB - Conversational Medical Database Interface

**Query medical databases using natural language via WhatsApp**

---

## 📋 Table of Contents

- [About](#about)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Database Schema](#database-schema)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Acknowledgments](#acknowledgments)

---

## 🎯 About

LexiDB enables healthcare professionals to query medical databases using natural language through WhatsApp. No SQL knowledge required - just ask questions in plain French or English.

**Developed at:** TCI (Terrab Consulting Innovation)  
**Period:** June - August 2024  
**Program:** Intelligence Artificielle et Technologies Émergentes

---

## ✨ Key Features

- 💬 **WhatsApp Integration** - Query via messaging (Twilio API)
- 🤖 **AI-Powered** - OpenAI GPT-3.5-turbo converts natural language to SQL
- 🏥 **Medical Database** - 6 tables covering patients, doctors, consultations, treatments, medications, and billing
- 🇫🇷 **French Responses** - Natural language results, not raw database output

---

## 🔄 How It Works

### Simple Flow

```
User (WhatsApp)
    ↓
"Quels patients ont consulté aujourd'hui?"
    ↓
Flask App (app.py)
    ↓
Generate SQL (OpenAI GPT-3.5)
    ↓
SQL: SELECT * FROM consultations WHERE dateconsultation = CURRENT_DATE
    ↓
Execute on PostgreSQL
    ↓
Format Results (OpenAI GPT-3.5)
    ↓
"Aujourd'hui, 3 patients ont eu des consultations..."
    ↓
User receives response via WhatsApp
```

### Architecture

```
┌─────────────────┐
│  WhatsApp User  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Flask App (app.py)          │
│  /whatsapp endpoint receives query  │
└────────┬────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  generate_sql_query.py                   │
│  Natural Language → SQL via OpenAI       │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  execute.py                              │
│  1. Execute SQL on PostgreSQL            │
│  2. Format results with OpenAI           │
└────────┬─────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│  PostgreSQL Database                     │
│  6 medical tables                        │
└──────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### 6 Medical Tables

**1. patients** - Patient information
```
patientid, nom, prenom, datedenaissance, sexe, adresse, telephone, email, dateenregistrement
```

**2. medecins** - Doctor profiles
```
medecinid, nom, prenom, specialite, telephone, email
```

**3. consultations** - Medical consultations
```
consultationid, patientid, medecinid, dateconsultation, description
```

**4. traitements** - Treatment plans
```
traitementid, consultationid, nomtraitement, description, datedebut, datefin
```

**5. medications** - Prescriptions
```
medicationid, traitementid, nommedicament, dosage, frequence, datedebut, datefin
```

**6. factures** - Billing records
```
factureid, patientid, montant, dateemission, payee
```

---

## 🛠️ Technologies

**Core Stack**
- Python 3.8+
- Flask (Web framework)
- PostgreSQL (Database)
- psycopg2 (Database connector)

**AI & NLP**
- OpenAI API (GPT-3.5-turbo)
- LangChain (LLM framework)

**Communication**
- Twilio API (WhatsApp messaging)

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- OpenAI API key
- Twilio account (WhatsApp enabled)

### Setup Steps

**1. Clone Repository**
```bash
git clone https://github.com/iitsh/PFE-NPL-PROJECT.git
cd PFE-NPL-PROJECT
```

**2. Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install flask twilio psycopg2-binary langchain langchain-openai
```

**3. Configure Database**

Edit `lexi_db/conn.py` and `lexi_db/execute.py`:
```python
conn = psycopg2.connect(
    dbname="your_database_name",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5455"
)
```

**4. Add OpenAI API Key**

Edit `lexi_db/generate_sql_query.py` and `lexi_db/execute.py`:
```python
llm = ChatOpenAI(
    api_key="your-api-key-here",
    model_name="gpt-3.5-turbo"
)
```

**5. Configure Twilio Webhook**

Set webhook URL to: `https://your-domain.com/whatsapp`

---

## 🚀 Usage

### Start the Server

```bash
python app.py
```

Server runs on `http://localhost:5000`

### For Development (Local Testing)

Use ngrok to expose local server:
```bash
ngrok http 5000
```

Configure Twilio webhook with the ngrok URL.

### Query via WhatsApp

1. Send message to your Twilio WhatsApp number
2. Ask questions in natural language
3. Receive formatted responses

---

## 📁 Project Structure

```
PFE-NPL-PROJECT/
│
├── app.py                          # Flask app with /whatsapp endpoint
│
├── lexi_db/
│   ├── conn.py                     # Database connection
│   ├── generate_sql_query.py       # Natural language → SQL
│   └── execute.py                  # Execute query & format results
│
├── requirements.txt                # Dependencies
└── README.md
```

### Module Functions

**app.py**
- Receives WhatsApp messages via Twilio
- Routes to lexi_db module
- Returns formatted responses

**lexi_db/generate_sql_query.py**
- `generate_sql_query(natural_language_query)` → Returns SQL string

**lexi_db/execute.py**
- `execute_query(sql)` → Executes SQL, returns raw results
- `resultat_ai_version(results, query)` → Formats results in natural language

---

## 💡 Examples

### Query Examples

**Example 1: Daily Consultations**
```
User: "Quels patients ont consulté aujourd'hui?"
SQL:  SELECT * FROM consultations WHERE dateconsultation = CURRENT_DATE
Bot:  "Aujourd'hui, 3 patients ont eu des consultations: Jean Dupont, 
       Marie Martin, et Ahmed Benali."
```

**Example 2: Doctor Search**
```
User: "Liste des médecins spécialisés en cardiologie"
SQL:  SELECT * FROM medecins WHERE specialite = 'cardiologie'
Bot:  "Nous avons 2 cardiologues: Dr. Fatima Zahra et Dr. Hassan Alami."
```

**Example 3: Unpaid Invoices**
```
User: "Montre-moi les factures impayées"
SQL:  SELECT * FROM factures WHERE payee = FALSE
Bot:  "Il y a 5 factures impayées pour un montant total de 2500 dirhams."
```

**Example 4: Patient Count**
```
User: "Combien de patients sont enregistrés?"
SQL:  SELECT COUNT(*) FROM patients
Bot:  "La base de données contient 247 patients enregistrés."
```

**Example 5: Patient Treatment**
```
User: "Quel traitement a reçu le patient Karim Saidi?"
SQL:  SELECT t.* FROM traitements t 
      JOIN consultations c ON t.consultationid = c.consultationid
      JOIN patients p ON c.patientid = p.patientid
      WHERE p.nom = 'Saidi' AND p.prenom = 'Karim'
Bot:  "Karim Saidi a reçu un traitement pour l'hypertension."
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 🙏 Acknowledgments

**Supervisors**
- Abdallah Terrab - Director, TCI
- Youssra Qlai - Administrative Manager, TCI

**Organization: TCI - Terrab Consulting Innovation**
- Founded: 2023
- Location: Meknès, Morocco
- Vision: "Empowering Innovation, Transforming Lives"

---

## 📞 Contact

**Author:** Rayane Berrada  
**Program:** Intelligence Artificielle et Technologies Émergentes



<div align="center">

**Made with ❤️ at TCI**

</div>

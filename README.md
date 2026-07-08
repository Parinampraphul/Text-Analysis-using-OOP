# Text Analysis using OOP

A Tkinter desktop app for user registration/login and text analysis with an object-oriented Python structure.

## Features

- Register and log in with a SQL Server database
- Store passwords securely with salted hashes
- Analyze text sentiment using the Hugging Face Inference API
- Run named entity recognition, sarcasm detection, abuse detection, and keyword extraction
- Keep configuration outside the source code with environment variables

## Project Structure

```text
text-analysis-using-oop/
|-- src/
|   `-- text_analysis_oop/
|       |-- api_client.py
|       |-- app.py
|       |-- config.py
|       |-- database.py
|       |-- security.py
|       `-- main.py
|-- .env.example
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Setup

1. Create and activate a virtual environment:

```powershell
a) cd "C:\Users\parin\Documents\Text Analysis using OOP"
b) Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
c) .\.venv\Scripts\Activate.ps1
```
2.Install hugging Face hub
'''
pip install huggingface_hub
'''
3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create your local environment file:

```powershell
Copy-Item .env.example .env
```

5. Create a SQL Server database named `TextAnalysisDb`.

In SQL Server Management Studio or Azure Data Studio, run:

```sql
CREATE DATABASE TextAnalysisDb;
```

The app creates the `dbo.users` table automatically when it starts.

6. Create a Hugging Face token:

- Go to [huggingface.co](https://huggingface.co/) and create/log in to your account.
- Open [Access Tokens](https://huggingface.co/settings/tokens).
- Click `New token`.
- Choose a `fine-grained` token.
- Give it permission to make calls to Inference Providers.
- Copy the token. It usually starts with `hf_`.

7. Open `.env` and add your Hugging Face token and SQL Server settings:

```text
HF_TOKEN=hf_your_token_here
HF_SENTIMENT_MODEL=distilbert/distilbert-base-uncased-finetuned-sst-2-english
HF_NER_MODEL=dslim/bert-base-NER
HF_SARCASM_MODEL=helinivan/english-sarcasm-detector
HF_ABUSE_MODEL=unitary/toxic-bert
SQLSERVER_DRIVER=ODBC Driver 18 for SQL Server
SQLSERVER_SERVER=localhost
SQLSERVER_DATABASE=TextAnalysisDb
SQLSERVER_TRUSTED_CONNECTION=true
SQLSERVER_USERNAME=
SQLSERVER_PASSWORD=
SQLSERVER_TRUST_SERVER_CERTIFICATE=true
```

For SQL Server username/password login, set `SQLSERVER_TRUSTED_CONNECTION=false`, then fill in `SQLSERVER_USERNAME` and `SQLSERVER_PASSWORD`.

## Run

```powershell
python -m src.text_analysis_oop.main
```

The app connects to SQL Server and creates the `dbo.users` table automatically the first time it runs.



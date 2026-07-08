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

## What Was Fixed

- Removed hard-coded empty database and API credentials
- Switched the app to SQL Server using `pyodbc`
- Switched text analysis from ParallelDots to Hugging Face
- Replaced plaintext password storage with salted password hashing
- Replaced fragile `user[3]` database column indexing with a `User` object
- Added database table creation so the app can start cleanly
- Added input validation and clearer error handling
- Split the single script into smaller OOP modules
- Removed unused imports and duplicated commented-out login code

## Upload to GitHub

1. Create a new repository on GitHub.
2. In this project folder, check the changed files:

```powershell
git status
```

3. Stage the project files:

```powershell
git add .
```

4. Commit the project:

```powershell
git commit -m "Refactor text analysis app"
```

5. Rename the branch to `main`:

```powershell
git branch -M main
```

6. Connect your local folder to your GitHub repository. Replace the URL with your repository URL:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

7. Push the code:

```powershell
git push -u origin main
```

Do not upload your `.env` file. It contains private API keys and is already ignored by Git.

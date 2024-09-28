# Intelligent Document Summarization and Analysis Tool

![Project Logo](https://github.com/erdogan98/Intelligent-Document-Summarization-and-Analysis-Tool/blob/a9c5ded08f1febe75a415cdcf5faf73ce57813a9/project-root/logo.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [API Endpoints](#api-endpoints)
    - [Upload and Process Document](#upload-and-process-document)
    - [Process Raw Text](#process-raw-text)
- [Database](#database)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The **Intelligent Document Summarization and Analysis Tool** is a powerful backend application built with FastAPI that allows users to upload various types of documents (e.g., PDF, DOCX, TXT) and perform comprehensive text analysis. The tool extracts text from uploaded files, generates concise summaries, identifies key entities, and analyzes the sentiment of the content. This tool is ideal for businesses and individuals looking to quickly digest large volumes of text data.

## Features

- **File Upload:** Supports uploading multiple document formats including PDF, DOCX, TXT, RTF, Markdown, and HTML.
- **Text Extraction:** Efficiently extracts text from uploaded documents.
- **Summarization:** Generates concise summaries of the extracted text using state-of-the-art transformer models.
- **Entity Recognition:** Identifies and extracts key entities (e.g., people, organizations, locations) from the text.
- **Sentiment Analysis:** Analyzes the sentiment of the content to determine positive, negative, or neutral tones.
- **Database Integration:** Stores processed documents and their analysis results in a SQLite database.
- **Asynchronous Processing:** Utilizes asynchronous operations to handle multiple requests concurrently, ensuring high performance and scalability.
- **CORS Configuration:** Securely manages cross-origin requests to allow integration with front-end applications.

[//]: # (## Demo)

[//]: # ()
[//]: # (![Demo GIF]&#40;https://github.com/yourusername/your-repo-name/raw/main/assets/demo.gif&#41;)

*Illustration of uploading a document and receiving summarized analysis.*

## Technologies Used

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Natural Language Processing:** [Hugging Face Transformers](https://huggingface.co/transformers/)
- **Database:** [SQLite](https://www.sqlite.org/index.html) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Sentiment Analysis Model:** `distilbert-base-uncased-finetuned-sst-2-english`
- **Summarization Model:** `t5-base`
- **Entity Recognition:** [SpaCy](https://spacy.io/)
- **Other Libraries:** [NLTK](https://www.nltk.org/), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), [Python Emoji](https://pypi.org/project/emoji/)

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- **Python 3.8 or higher** installed on your system.
- **pip** package manager.

### Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows:**

  ```bash
  venv\Scripts\activate
  ```

- **On macOS and Linux:**

  ```bash
  source venv/bin/activate
  ```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Download NLTK Data

The application requires NLTK's `punkt` tokenizer.

```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> exit()
```

## Configuration

Create a `.env` file in the root directory to manage environment variables.

```env
# .env

# Database URL
DATABASE_URL=sqlite:///./database.db

# CORS Allowed Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://192.168.0.20:3000

# Summarizer Configuration
SUMMARIZER_BATCH_SIZE=8
SUMMARIZER_MAX_WORKERS=4

# Sentiment Analyzer Configuration
SENTIMENT_MAX_WORKERS=4
```

**Note:** Adjust the values based on your deployment environment and requirements.

## Usage

### Running the Server

Start the FastAPI server using Uvicorn.

```bash
uvicorn main:app --reload
```

- **`main`:** The name of your main Python file (`main.py`).
- **`app`:** The FastAPI instance in `main.py`.
- **`--reload`:** Enables auto-reloading on code changes (useful during development).

The server will be accessible at `http://127.0.0.1:8000/`.

### API Endpoints

#### Upload and Process Document

- **Endpoint:** `/process`
- **Method:** `POST`
- **Description:** Uploads a document, extracts text, generates a summary, extracts entities, and analyzes sentiment.

**Request:**

- **Headers:**
  - `Content-Type: multipart/form-data`
- **Body:**
  - `file`: The document file to upload.

**Example using `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/process" -F "file=@/path/to/your/document.pdf"
```

**Response:**

```json
{
  "status": "success",
  "summary": "Concise summary of the document.",
  "entities": [
    {"entity": "Entity Name", "type": "Entity Type"},
    ...
  ],
  "sentiment": "POSITIVE"
}
```

#### Process Raw Text

- **Endpoint:** `/process_text`
- **Method:** `POST`
- **Description:** Processes raw text input to generate a summary, extract entities, and analyze sentiment.

**Request:**

- **Headers:**
  - `Content-Type: application/json`
- **Body:**

```json
{
  "text": "Your raw text goes here."
}
```

**Example using `curl`:**

```bash
curl -X POST "http://127.0.0.1:8000/process_text" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your raw text goes here."}'
```

**Response:**

```json
{
  "status": "success",
  "summary": "Concise summary of the text.",
  "entities": [
    {"entity": "Entity Name", "type": "Entity Type"},
    ...
  ],
  "sentiment": "NEGATIVE"
}
```

### Interactive API Documentation

FastAPI provides an interactive API documentation interface accessible at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Use these interfaces to test the API endpoints interactively.

## Database

The application uses SQLite as the database to store processed documents and their analysis results. The database file is named `database.db` and is located in the project's root directory.

### Database Models

- **Document**

  | Column    | Type   | Description                           |
  |-----------|--------|---------------------------------------|
  | id        | Integer| Primary key, auto-incremented.        |
  | filename  | String | Name of the uploaded file.            |
  | text      | Text   | Extracted text from the document.     |
  | summary   | Text   | Generated summary of the text.        |
  | entities  | Text   | JSON-serialized list of extracted entities. |
  | sentiment | String | Sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL). |

### Creating the Database

Run the following script to create the necessary database tables.

```bash
python create_tables.py
```

Ensure that the `Document` model is correctly defined in `DB_MODELS.py`.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your detailed description here"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

Provide a clear description of the changes and the reasons behind them.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact:

- **Name:** Erdogan Kervanli
- **Email:** ekervanli@outlook.com
- **LinkedIn:** [linkedin.com/in/kervanli](https://www.linkedin.com/in/yourprofile)
- **GitHub:** [@erdogan98](https://github.com/yourusername)

---
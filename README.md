# 🎓 AI-Powered Student Database Assistant

This project is a console-based AI assistant that answers queries about students using an MSSQL database. It generates SQL queries dynamically using Hugging Face AI and executes them, with a fallback rule-based system for common queries.

🚀 Features

- **Natural Language Processing:** Converts user questions into SQL queries.
- **MSSQL Database Integration:** Retrieves real-time student data.
- **AI & Rule-Based SQL Generation:** Uses Hugging Face AI and predefined query patterns.
- **Formatted Responses:** Displays results in a structured, human-readable format.

🛠️ Setup Instructions

### 1️⃣ Prerequisites

- Python 3.x installed
- MSSQL Server
- Required Python packages:
  ```sh
  pip install pyodbc requests python-dotenv
  ```

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project directory and add:

```sh
DB_SERVER=your_sql_server
DB_NAME=your_database_name
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### 3️⃣ Create and Activate Virtual Environment

To ensure dependency isolation, create and activate a virtual environment:

```sh
# Create a virtual environment (Windows)
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
```

### 4️⃣ Run the Assistant

```sh
python main.py
```

📝 Example Queries

🔹 Who has the highest exam score?
🔹 Show the attendance of all students.
🔹 Which students have pending fees?

📌 **Author:** Aghar Usman Kannanthodi

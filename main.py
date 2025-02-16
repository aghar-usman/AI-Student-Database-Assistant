import os
import pyodbc
import requests
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database credentials (Windows Authentication)
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

# Hugging Face API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Check for missing environment variables
if not DB_SERVER or not DB_NAME:
    print("⚠️ Missing database configuration in .env file!")
if not HUGGINGFACE_API_KEY:
    print("⚠️ Missing Hugging Face API Key in .env file!")

# Connect to MSSQL database
def connect_db():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

# Execute SQL queries in the database
def query_database(sql_query):
    conn = connect_db()
    if not conn:
        return "⚠️ Error connecting to the database."

    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        columns = [column[0] for column in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        return f"⚠️ Query error: {e}"
    finally:
        cursor.close()
        conn.close()

# Generate SQL query using Hugging Face AI
def generate_sql_query(question):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": f"Convert this question into an SQL query: {question}"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        if isinstance(response_json, list) and "generated_text" in response_json[0]:
            sql_query = response_json[0]["generated_text"].strip()
            return sql_query if sql_query.lower().startswith("select") else None
        return None
    except requests.exceptions.RequestException:
        return None

# Fallback: Rule-based SQL generation for common queries
def fallback_sql(question):
    question = question.lower().strip()

    if re.search(r"\b(attendance|absent|present)\b", question):
        return "SELECT Name, AttendancePercentage FROM Students ORDER BY AttendancePercentage DESC"

    elif re.search(r"\b(top student|highest score|rank)\b", question):
        return "SELECT TOP 1 Name, Class, ExamScore FROM Students ORDER BY ExamScore DESC"

    elif re.search(r"\b(lowest score|least examscore|bottom student|worst performance)\b", question):
        return "SELECT TOP 1 Name, Class, ExamScore FROM Students ORDER BY ExamScore ASC"

    elif re.search(r"\b(pending fees|unpaid fees|due fees)\b", question):
        return "SELECT Name, (TotalFees - FeesPaid) AS PendingFees FROM Students WHERE FeesPaid < TotalFees"

    match = re.search(r"\b(class|grade)\s+(\d+)\b", question)
    if match:
        class_number = match.group(2)
        return f"SELECT Name, Class, ExamScore FROM Students WHERE Class = {class_number}"

    return None

# Convert SQL output into a natural response
def format_response(question, sql_results):
    if not sql_results:
        return "No relevant data found for your query."

    response_text = ""

    if "AttendancePercentage" in sql_results[0]:
        response_text = "Here are the students and their attendance percentages:\n"
        response_text += "\n".join(f"{row['Name']}: {row['AttendancePercentage']}%" for row in sql_results)

    elif "ExamScore" in sql_results[0] and "Class" in sql_results[0]:
        response_text = "Here are the exam scores:\n"
        response_text += "\n".join(f"{row['Name']} (Class {row['Class']}): {row['ExamScore']}" for row in sql_results)

    elif "PendingFees" in sql_results[0]:
        response_text = "Here are the students with pending fees:\n"
        response_text += "\n".join(f"{row['Name']}: ₹{row['PendingFees']}" for row in sql_results)

    else:
        response_text = "Here is the requested data:\n"
        response_text += "\n".join(json.dumps(row, indent=2) for row in sql_results)

    return response_text

# AI-powered student database assistant
def ai_console():
    print("\n🎓 Welcome to the AI Student Database Assistant!")
    while True:
        user_input = input("\n🔹 Ask a question (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        # Step 1: Try Hugging Face AI to generate SQL
        sql_query = generate_sql_query(user_input)
        
        # Step 2: If AI fails, use fallback rules
        if not sql_query:
            sql_query = fallback_sql(user_input)
        
        # Step 3: Execute SQL if valid, else return error
        if sql_query:
            result = query_database(sql_query)
            final_response = format_response(user_input, result)
        else:
            final_response = "⚠️ Could not generate a valid SQL query."

        print("\n💡 Answer:", final_response)

# Run the AI console
if __name__ == "__main__":
    ai_console()

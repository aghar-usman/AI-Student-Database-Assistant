import os
import logging
import pyodbc
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
load_dotenv()

# Retrieve credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = "school"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-pro-latest"
model = genai.GenerativeModel(MODEL_NAME)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Database Schema Description
import google.generativeai as genai
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Database Schema Description
SCHEMA_DESCRIPTION = """
Tables:
1. Students(StudentID, Name, Age, ClassID, TuitionFees, TransportFees, ExamFees, FeesPaid, Address, PhoneNumber, Email, AdmissionDate, AttendancePercentage, ExamScore, Status, Remarks)
2. Classes(ClassID, ClassName)
3. Teachers(TeacherID, Name, SubjectID, PhoneNumber, Email)
4. Subjects(SubjectID, SubjectName)
5. Courses(CourseID, CourseName, Description, TeacherID)
6. Enrollments(EnrollmentID, StudentID, CourseID, Term, EnrollmentDate)
7. Exams(ExamID, SubjectID, Term)
8. ExamResults(ResultID, ExamID, StudentID, MarksObtained, TotalMarks)
9. Attendance(AttendanceID, StudentID, CourseID, Date, Status)
10. Payments(PaymentID, StudentID, AmountPaid, PaymentDate, PaymentMethod)
11. Parents(ParentID, StudentID, Name, Relationship, PhoneNumber, Email)
12. ExamTypes(ExamTypeID, ExamType, Weightage)
13. Grades(GradeID, MinMarks, MaxMarks, Grade)
14. HomeroomTeachers(HomeroomID, TeacherID, ClassID)
15. Logs(LogID, TableName, Action, ActionDate, UserID, UserRole, OldValue, NewValue, Details)
"""

def generate_sql_query(user_input):
    """Uses Gemini AI to generate a SQL query dynamically with accurate logic matching the user input.
       If the input is ambiguous, prompts the user for clarification. Handles greetings separately."""
    
    # List of greeting phrases
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]

    # Check if user input is a greeting
    if any(greeting in user_input.lower() for greeting in greetings):
        return "👋 Hello! How can I assist you today?"  # Return greeting response

    # Proceed with generating SQL query for non-greeting inputs
    prompt = f"""
### **📌 Database Schema Context**:
{SCHEMA_DESCRIPTION}

### **🔹 User Request**:
**"{user_input}"**

### **🚀 Generate a VALID SQL Server Query**
- Your task is to generate a **fully executable SQL query** based on the user request.
- Ensure that the query is **logically correct** and retrieves **accurate results**.

---

### **🔹 STRICT SQL RULES:**
✅ **1. Fully Executable SQL**
- The SQL query **MUST be directly runnable**—NO explanations, NO comments, NO markdown (` ```sql `).
- **RETURN ONLY PURE SQL CODE.**

✅ **2. Schema & Naming Consistency**
- Use **only valid table and column names** from the schema.
- If a user query uses synonyms, **map them correctly**:
  - **"Mom", "Mother" → 'Mother'** in the `Parents.Relationship` column.
  - **"Dad", "Father" → 'Father'** in the `Parents.Relationship` column.
  - **"Marks" → "MarksObtained"** in the `ExamResults` table.
  - **"Exam Results" → "ExamResults"** table.

✅ **3. Intelligent Filtering & Sorting**
- If filtering is needed, apply **`WHERE`, `BETWEEN`, or `LIKE` clauses**.
- If sorting is required, use **`ORDER BY`** with the correct column and order.

✅ **4. Handling Ranking Queries**
- For **top scores or ranks**, use **`RANK()` or `DENSE_RANK()`**.
- Ensure **ties are handled correctly**.

✅ **5. Fuzzy Matching for Names**
- If a user query contains **only part of a name**, apply **`LIKE '%name%'`** for partial matching.
- For **better accuracy**, use **`SOUNDEX(name) = SOUNDEX('John')`** to handle variations like *Jon Smith vs. John Smith*.

✅ **6. Proper Joins & Relationships**
- If relationships exist (e.g., student-exam mapping), **use explicit `JOIN` statements**.
- Ensure proper linking using **primary and foreign keys**.

✅ **7. Security Considerations**
- ❌ **No destructive queries** (`DROP`, `DELETE`, `ALTER`).
- ❌ **No modifications unless explicitly requested**.

---
### **🔹 Examples of Expected Query Patterns**
💡 **Find top 5 highest scorers:**
```sql
SELECT StudentID, Name, MarksObtained
FROM ExamResults
ORDER BY MarksObtained DESC
LIMIT 5;
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if not response.text:
            logger.error("Empty response from Gemini AI.")
            return None

        generated_query = response.text.strip()

        # 🚨 Remove Markdown Formatting (` ```sql ` blocks)
        if generated_query.startswith("```sql") and generated_query.endswith("```"):
            generated_query = generated_query[6:-3].strip()

        # 🚨 Remove AI-generated comments (Lines starting with `--`)
        query_lines = generated_query.split("\n")
        cleaned_query = "\n".join([line for line in query_lines if not line.strip().startswith("--")])

        # 🚨 Validate Query Integrity
        if not cleaned_query.lower().startswith("select") or "from" not in cleaned_query.lower():
            logger.warning(f"Invalid SQL query generated: {cleaned_query}")
            return None

        logger.info(f"Generated SQL query: {cleaned_query}")
        return cleaned_query

    except Exception as e:
        logger.error(f"Error generating SQL query: {e}")
        return None

# Execute SQL query
def execute_sql(query):
    conn = get_db_connection()
    if not conn:
        return "Database connection failed. Please try again later."

    cursor = conn.cursor()
    try:
        logger.info(f"Executing query: {query}")
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        
        # 🛠 DEBUG LOG
        logger.info(f"Raw SQL results: {rows}")

        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(f"Error executing SQL: {e}")
        return str(e)
    finally:
        cursor.close()
        conn.close()

# Format SQL results
def generate_ai_response(user_query, sql_results, column_names):
    if not sql_results or isinstance(sql_results, str):
        return f"⚠️ No matching records found for your query: \"{user_query}\". Please check if the data exists or try a different question."

    structured_results = []

    # Convert results into a structured format
    for row in sql_results:
        record = dict(zip(column_names, row))  # Map column names to values
        structured_results.append(record)

    # **AI-Driven Formatting Prompt**
    prompt = f"""
    Format the following student records in a **compact, human-friendly format**:
    
    User Query: "{user_query}"

    ## **Rules**:
    - **If the user query is a greeting (e.g., "hi", "hello", "hey", "good morning", good evening, good night, hellllooo, helo, hola, hiiiiiii, heyyyyy,.......etc)**, respond with:  
    - **"👋 Hello! How can I assist you today?"** 
    - **Group duplicate data** (e.g., same scores, same parent names).
    - **Summarize efficiently** (avoid listing identical details multiple times).
    - **Ensure readability** (emoji for key points, bullet points for clarity).
    - **No extra AI commentary**—just return the **formatted response**.
    - **Use all kinds of emoji** that can work relevant to details and works as bullet point
    -data to be represented beautifully see example template below 📢 Here are the student details you requested! 📝 Let me know if you need additional details or modifications. 🚀
    - only allowed to pass reply suitable for hi hello other than formatted structure 

━━━━━━━━━━━━━━━━━━━━━━━
📌 Student Details:  
🔹 Studentid: 19
🔹 Name: Student 19
🔹 Age: 6
🔹 Classid: 9
🔹 Tuitionfees: 50000.00
🔹 Transportfees: 5000.00
🔹 Examfees: 2000.00
🔹 Feespaid: 32229.21
🔹 Address: Address 19
🔹 Phonenumber: 9123466198
🔹 Email: student19@school.com
🔹 Admissiondate: 2025-03-08
🔹 Attendancepercentage: 98.00
🔹 Examscore: 88.00
🔹 Status: Active
🔹 Remarks: Good Progress
━━━━━━━━━━━━━━━━━━━━━━━ make sure it good looking and user f

    ## **Raw Data**:
    {structured_results}
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if response.text:
            return response.text.strip()

    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "⚠️ I encountered an issue while processing your request. Please try again!"

    return "⚠️ Could not format the response. Please try again!"

# Handle messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.strip()
    query = generate_sql_query(user_message)
    
    if query:
        # Check if the response is a greeting and return it directly
        if "Hello!" in query:
            await update.message.reply_text(query)  # Respond with the greeting
            return
        
        conn = get_db_connection()
        if not conn:
            response_message = "❌ Database connection failed. Please try again later."
        else:
            cursor = conn.cursor()
            try:
                logger.info(f"Executing query: {query}")
                cursor.execute(query)
                
                # Extract column names from cursor.description
                column_names = [column[0] for column in cursor.description]  

                rows = cursor.fetchall()
                raw_result = [tuple(row) for row in rows]  # Convert to list of tuples

                logger.info(f"Raw SQL results: {raw_result}")

                # Ensure we pass column_names correctly
                ai_response = generate_ai_response(user_message, raw_result, column_names)

                # 🚀 **Fix Long Message Issue**
                for chunk in [ai_response[i:i+4000] for i in range(0, len(ai_response), 4000)]:
                    await update.message.reply_text(chunk)

                return

            except Exception as e:
                logger.error(f"Error executing SQL: {e}")
                response_message = "⚠️ There was an error fetching data. Please try again."
            finally:
                cursor.close()
                conn.close()
    else:
        response_message = "😕 Sorry, I couldn’t understand your request. Try rephrasing it."
    
    await update.message.reply_text(response_message)

# Start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Hello! Send me a query, and I'll fetch the results from the database in a friendly way.")

# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()

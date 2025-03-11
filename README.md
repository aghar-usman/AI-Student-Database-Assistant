# 🎯 AI-Powered Student Database Assistant

An advanced console-based AI assistant that dynamically answers queries about student data using an MSSQL database. This powerful assistant combines **AI-driven SQL query generation** with a fallback **rule-based system** for optimal performance.

---

## 🚀 Features
✅ **Natural Language Processing:** Converts user queries into executable SQL queries.  
✅ **MSSQL Database Integration:** Retrieves accurate, real-time student data.  
✅ **AI & Rule-Based SQL Generation:** Combines Hugging Face AI and predefined patterns for precision.  
✅ **Smart Responses:** Provides structured, user-friendly results with emojis for improved readability.  

---

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
Ensure the following are installed:
- Python 3.x  
- MSSQL Server  
- Required Python packages:
  ```sh
  pip install pyodbc requests python-dotenv
  ```

---

### 2️⃣ Environment Variables Configuration
Create a `.env` file in your project directory and add these details:

```sh
DB_SERVER=your_sql_server
DB_NAME=your_database_name
HUGGINGFACE_API_KEY=your_huggingface_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

---

### 3️⃣ Create and Activate Virtual Environment
For clean dependency management:

```sh
# Create Virtual Environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

---

### 4️⃣ Run the Assistant
To start the bot, use:

```sh
python main.py
```

---

## 📋 Supported Queries
💬 Ask in natural language! Here are some examples:

🔹 Who has the highest exam score?  
🔹 Show me all students who have paid their fees.  
🔹 List students with pending fees.  
🔹 Find students with attendance below 75%.  

---

## 📌 Sample Output
📢 **Here are the student details you requested!**  
📝 Let me know if you need additional details or modifications. 🚀  

━━━━━━━━━━━━━━━━━━━━━━━  
🔹 **Student ID:** 19  
🔹 **Name:** Student 19  
🔹 **Age:** 6  
🔹 **Class ID:** 9  
🔹 **Tuition Fees:** ₹50,000  
🔹 **Transport Fees:** ₹5,000  
🔹 **Exam Fees:** ₹2,000  
🔹 **Fees Paid:** ₹32,229.21  
🔹 **Address:** Address 19  
🔹 **Phone Number:** 9123466198  
🔹 **Email:** student19@school.com  
🔹 **Admission Date:** 2025-03-08  
🔹 **Attendance %:** 98%  
🔹 **Exam Score:** 88  
🔹 **Status:** Active  
🔹 **Remarks:** Good Progress  
━━━━━━━━━━━━━━━━━━━━━━━  

---

## ❓ Troubleshooting
🔹 **Database Connection Error:** Ensure your `.env` file contains valid MSSQL credentials.  
🔹 **Query Not Understood:** Try rephrasing the query or providing clearer context.  
🔹 **Telegram Bot Not Responding:** Verify your `TELEGRAM_BOT_TOKEN` and ensure the bot is added to your chat.  

---

## 👨‍💻 Author
Developed by **Aghar Usman Kannanthodi**  
💬 Feel free to reach out for collaboration or queries!  
This version adds better formatting, improved readability, and clear instructions. Let me know if you'd like additional sections or adjustments! 😊

# TsundokuBot - A Book Recommendation Chatbot

## 📖 Overview

TsundokuBot is a Rasa-based chatbot that helps users explore books through **dynamic interactions and real-world API integrations**. The chatbot offers book recommendations, retrieves book details, and fetches books by specific authors using the **Google Books API**.

## 🎯 Motivation

The name **TsundokuBot** is inspired by the Japanese term *tsundoku* (積ん読), which refers to the habit of acquiring books and letting them pile up without reading them. This chatbot is designed to help users **overcome indecision** by recommending books based on their preferences, making it easier to decide what to read next.

It demonstrates:

✅ **Conversational AI capabilities** for engaging interactions  
✅ **Real-world API integration** (Google Books API) for live data  
✅ **Dynamic slot filling and entity extraction** in Rasa  

---

## 🔹 **Implemented Scenarios**

### 📚 **1. Book Recommendation by Genre**

- The chatbot suggests books based on the **user's preferred genre**.
- **Example:**
  - **User:** *Suggest me three sci-fi books.*
  - **Bot:** *Here are 3 sci-fi book recommendations:*\
    📖 *Dune* by Frank Herbert\
    📖 *Foundation* by Isaac Asimov\
    📖 *Neuromancer* by William Gibson

### 🖊️ **2. Find Books by a Specific Author**

- The chatbot fetches books **written by a given author**.
- **Example:**
  - **User:** *List two books by Agatha Christie.*
  - **Bot:** *Here are 2 books by Agatha Christie:*\
    📖 *Murder on the Orient Express*\
    📖 *And Then There Were None*

### 🔍 **3. Retrieve Book Information**

- Users can query book details **such as author, publication date, etc.**.
- **Example:**
  - **User:** *Who wrote The Hobbit?*
  - **Bot:**\
    📖 *The Hobbit*\
    ✍️ Author: *J.R.R. Tolkien*\
    📅 Published: *1937*

---

## 🔹 **Real-World Data Integration**

TsundokuBot dynamically interacts with the **Google Books API** to fetch live book data.

### 📡 **APIs Used**

1. **Google Books API** - Retrieves book titles, authors, and publication dates.
2. **Python Requests Library** - Handles API calls and error handling.

---

## 🛠️ **Technical Stack**

✅ **Rasa Open Source** (NLU, dialogue management)  
✅ **Python** (Backend & API requests)  
✅ **Google Books API** (Live book retrieval)  
✅ **Rasa SDK** (Custom actions for API interactions)  

---

## 🏗️ **Setup & Installation**

### 🔧 **1. Install Dependencies**

```bash
pip install rasa rasa-sdk requests
```

### 🚀 **2. Run Rasa Shell**

```bash
rasa train
rasa shell
```

### 🎭 **3. Start Rasa Actions Server**

```bash
rasa run actions
```

---

## ⚠️ **Error Handling & Robustness**

TsundokuBot includes:

- **API Timeout Handling** (Retries if Google Books API fails)
- **Entity Extraction Checks** (Fallback responses for unknown genres/authors)
- **Dynamic Slot Filling** (Ensuring conversational context remains natural)

---

## 📊 **Challenges Faced & Remaining Struggles**

### **Challenges Overcome**
✅ Improving **number extraction** (handling "two books" and "2 books")  
✅ Addressing **API inconsistencies** (e.g., missing author names)  
✅ Refining **entity recognition** for book titles vs. genres  

### **Where It Still Struggles**
❌ Occasionally **returns "Unknown Author"** for books (API limitations)  
❌ Handling **author name variations** (e.g., "J.K. Rowling" vs. "Rowling")  
❌ Filtering **duplicate or irrelevant book results**  

---

## 📌 **Future Improvements**

🚀 Expand to **multi-language support**   
🚀 Improve **book filtering options** (ratings, popularity, etc.)   
🚀 Integrate **user preferences** for personalized recommendations  

---

## 📤 **Submission & Repository Details**

- **GitHub Repository:** [Your Repository Link Here]
- **Presentation PDF:** [Your Presentation Link Here]

For any issues or questions, contact: **[Your Contact Info]** 📩

🚀 **Happy Reading with TsundokuBot!** 📚

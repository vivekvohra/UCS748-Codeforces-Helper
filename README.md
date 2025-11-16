# UCS748-Codeforces-Helper

---
## 📦 Features

* Fetches Codeforces problems dynamically
* Serves API endpoints for problem lookup
* Integrates Pathway streaming pipelines
* Clean Docker-based deployment
* Runs with Supervisor for stable background processes

---

## 📁 Project Structure

```
/app
 ├── main.py                # Entry point
 ├── examples/api/app.py    # API server logic
 ├── requirements.txt
 ├── supervisord.conf
 ├── Dockerfile
```

---

Live APP running on AWS :
**http://13.233.96.246:8501/**

# 📘 **README -(Executable Python Project)**



The project runs as a **Streamlit web app**.

---

# 🚀 **How to Run the Project (Executable .py instructions)**

### **Requirements**

* Python 3.10+
* pip installed

### **1. Install all dependencies**

Open terminal inside the project folder and run:

```
pip install -r requirements.txt
```

### **2. Run the executable Streamlit file**

Use this exact command:


```
streamlit run CodeForces/examples/ui/app.py
```

### **3. The app will open in the browser**

Usually at:

```
http://localhost:8501
```

---

# 📂 **Executable File**

The file that launches the whole project:

```
CodeForces/examples/ui/app.py
```

This is the “executable .py file” requested.

---




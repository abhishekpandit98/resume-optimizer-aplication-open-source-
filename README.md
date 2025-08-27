# 🧠 Smart ATS — Resume Optimizer (Open Source)

Smart ATS is a **Streamlit-based web app** that helps job seekers analyze their resumes against a job description using **Groq LLMs** (LLaMA 3, Mixtral).  
It acts like a smart recruiter: evaluating your strengths, identifying missing keywords, estimating your ATS match score, and suggesting improvement areas.

🚀 Perfect project to showcase **LLMs + Streamlit + Real-world Application** on my resume or portfolio.  

---

## ✨ Features

- 📄 **PDF Resume Parsing** — Upload your resume (PDF) and extract text automatically  
- 📝 **JD vs Resume Analysis** — Compare your resume against the job description  
- ✅ **ATS Missing Keywords** — Identify missing/weak keywords  
- 📈 **Match Percentage** — Get a match score (%) with actionable suggestions  
- 💡 **Skill Improvement Suggestions** — Personalized recommendations for hard skills, soft skills, and projects  
- 🎨 **Modern UI** — Built with Streamlit tabs and styled for professional use  

---
## Getting Started
To access the app, click [here](https://abhishekpandit98-5vzbjrzgthtdatum9k4jyy.streamlit.app/).


## 📸 Demo Screenshot
![Smart ATS Demo](https://github.com/abhishekpandit98/resume-optimizer-aplication-open-source-/blob/b7361ceacd0c049bbf53ada83f2dc2274eaa95cb/Smart%20ATS%20%E2%80%94%20Groq%20Powered%20%C2%B7%20Streamlit_page-0001.jpg))

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — for interactive UI  
- [Groq](https://groq.com/) — for ultra-fast LLM inference  
- [PyPDF2](https://pypi.org/project/PyPDF2/) — for PDF parsing  
- [Python 3.9+](https://www.python.org/)

---
## 🎯 Usage  

1. Paste a **Job Description (JD)** into the text box.  
2. Upload your **resume (PDF)**.  
3. Choose a **Groq Model** (default: llama3-8b).  
4. Explore tabs:  
   - **Evaluation** → HR-style resume review  
   - **Improve Skills** → Actionable suggestions  
   - **Missing Keywords** → ATS keyword analysis  
   - **Match %** → Estimated alignment score
   - 
## ⚡ Setup & Installation

**Clone the repository**
   ```bash
   git clone https://github.com/abhishekpandit98/resume-optimizer-aplication-open-source-.git
   ```
      
## 🔑 Setup  

You will need a **Groq API key**. Create one from your Groq account.  

    Add the key in `.streamlit/secrets.toml`
    GROQ_API_KEY = "your_api_key_here"
    
### Requirements
Make sure to install the required Python libraries by running:

```bash
pip install -r requirements.txt
```
     
   
## 🛠️ Tech Stack  

- [Streamlit](https://streamlit.io) – UI framework  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – Resume PDF parsing  
- [Groq API](https://groq.com/) – LLM inference  
- [OpenAI SDK](https://pypi.org/project/openai/) – Client management (pointing to Groq’s API endpoint)  
- Python 3.9+ 
   
**Project Structure**
resume-optimizer-aplication-open-source-/
```
│── app.py                # Main Streamlit app
│── requirements.txt      # Python dependencies
│── .gitignore            # Ignore secrets/venv
│── .streamlit/
│   └── secrets.toml      # API key (excluded from repo)
│── README.md             # Project documentation
```


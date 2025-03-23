import streamlit as st
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from langchain_community.llms import HuggingFaceEndpoint 
from langchain.prompts import PromptTemplate

# Load environment variables
huggingface_api_key = st.secrets["HUGGINGFACE_ACCESS_TOKEN"]

# Configure Hugging Face model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.2-3B-Instruct",
    task="text-generation",
    model_kwargs={"huggingface_api_key": huggingface_api_key}
)


def input_pdf_text(uploaded_file):
    """Extract text from uploaded PDF resume."""
    reader = pdf.PdfReader(uploaded_file)
    text = "".join([page.extract_text() or "" for page in reader.pages])
    return text

# Prompt Templates using LangChain
prompt_template1 = PromptTemplate(
    input_variables=["jd", "resume"],
    template="""
    You are an experienced Technical Human Resource Manager. Review the provided resume against the job description. 
    Highlight strengths, weaknesses, and alignment with the specified job requirements.
    Job Description: {jd}
    Resume: {resume}
    """
)

prompt_template2 = PromptTemplate(
    input_variables=["jd", "resume"],
    template="""
    As a Technical HR Manager with expertise in data science, analyze the resume. 
    Share insights on suitability, suggest skill improvements, and areas needing development.
    Job Description: {jd}
    Resume: {resume}
    """
)

prompt_template3 = PromptTemplate(
    input_variables=["jd", "resume"],
    template="""
    As an ATS scanner, evaluate the resume against the job description. 
    List missing keywords and provide skill enhancement recommendations.
    Job Description: {jd}
    Resume: {resume}
    """
)

prompt_template4 = PromptTemplate(
    input_variables=["jd", "resume"],
    template="""
    Analyze resume compatibility with job description. Provide a match percentage first, followed by missing keywords and final thoughts.
    Job Description: {jd}
    Resume: {resume}
    """
)

# Streamlit App
st.title("Smart ATS - Open Source Version")
st.text("Enhance Your Resume for ATS Compatibility")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Upload a PDF resume")

if st.button("Evaluate Resume"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = prompt_template1.format(jd=jd, resume=text)
        response = llm.invoke(prompt)
        st.subheader("Evaluation Result:")
        st.write(response)
    else:
        st.write("Please upload a resume.")

if st.button("Improve Skills"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = prompt_template2.format(jd=jd, resume=text)
        response = llm.invoke(prompt)
        st.subheader("Skill Enhancement Suggestions:")
        st.write(response)
    else:
        st.write("Please upload a resume.")

if st.button("Find Missing Keywords"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = prompt_template3.format(jd=jd, resume=text)
        response = llm.invoke(prompt)
        st.subheader("Missing Keywords:")
        st.write(response)
    else:
        st.write("Please upload a resume.")

if st.button("Percentage Match"):
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        prompt = prompt_template4.format(jd=jd, resume=text)
        response = llm.invoke(prompt)
        st.subheader("Resume Match Percentage:")
        st.write(response)
    else:
        st.write("Please upload a resume.")

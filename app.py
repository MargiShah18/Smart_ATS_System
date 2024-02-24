"""
1. older method
    PDF-->via pdf2img-->Image-->bytes of image-->API-->Response

2. New method
    PDF-->via Pypdf2-->Text-->API-->response
"""

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ## load all the env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro Response
def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += str(page.extract_text())
    return text


##Prompt Template
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on Jd and the missing keywords with high accuracy. 
resume:{text}
description:{jd}

I want the response in one single string having the structure

JD Match:"%"

MissingKeywords:[]

Profile Summary:" "
"""

##Streamlit App
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS Tracking System")
# input_text=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your Resume in PDF format...",type=["pdf"])

# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")

# submit1=st.button("Tell me About the Resume")
# #submit2=st.button("How can I improvise my skills")
# submit3=st.button("Percentage Match")

# input_prompt1="""
# You are an experienced Technical Human Resource Manager with Tech Experience in the field of Data Science,Machine Learning ,Data Analyst, your task is to review the provided resume against the job description. 
# Please share your professional evaluation on whether the candidate's profile aligns with the role. 
# Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

# input_prompt3="""
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science,Machine learning ,Data Analyst and deep ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         if uploaded_file is not None:
#             text=input_pdf_text(uploaded_file)
#             response=get_gemini_response(input_prompt1)
#             st.subheader(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit3:
#     if uploaded_file is not None:
#         text=input_pdf_text(uploaded_file)
#         response=get_gemini_response(input_prompt3)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

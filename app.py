import streamlit as st
import google.generativeai as genai
import PyPDF2
from typing import List, Dict

# Gemini 
genai.configure(api_key='api key')
model = genai.GenerativeModel('gemini-pro')

# HR Questions
HR_QUESTIONS = [
    {
        "question": "How do you handle disagreements with team members on technical decisions?",
        "options": [
            "I always stick to my approach as I trust my technical judgment",
            "I immediately escalate to the manager to resolve the conflict",
            "I discuss different viewpoints, share data/examples, and work towards consensus",
            "I give in to avoid conflict and maintain team harmony"
        ],
        "best_answer": 2  # best ans
    },
    {
        "question": "When faced with multiple urgent tasks, how do you prioritize your work?",
        "options": [
            "I work on whatever seems most interesting first",
            "I assess impact, deadlines, and dependencies to create a structured plan",
            "I try to do everything at once to get it all done",
            "I wait for my manager to tell me what to do first"
        ],
        "best_answer": 1
    },
    {
        "question": "How do you handle receiving constructive criticism?",
        "options": [
            "I take it personally and feel demotivated",
            "I defend my actions and explain why the criticism is wrong",
            "I listen actively, ask questions for clarity, and use it to improve",
            "I ignore it and continue working as before"
        ],
        "best_answer": 2
    },
    {
        "question": "What's your approach to learning new technologies or skills?",
        "options": [
            "I wait for formal training from my organization",
            "I learn only when absolutely required for a task",
            "I proactively learn through various resources and create practice projects",
            "I focus only on what I already know well"
        ],
        "best_answer": 2
    },
    {
        "question": "How do you ensure effective communication in a remote/hybrid work environment?",
        "options": [
            "I minimize communication to avoid disturbing others",
            "I use appropriate channels, maintain documentation, and follow up regularly",
            "I send lengthy emails explaining every detail",
            "I prefer to work independently without much communication"
        ],
        "best_answer": 1
    }
]

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_profile(resume_text: str, field: str, subfield: str, interview_score: float, gpa: float) -> Dict:
    """Analyze the complete profile using Gemini API."""
    prompt = f"""Analyze this candidate profile for a {field} position specializing in {subfield}.
    
    Profile details:
    - GPA: {gpa}/4.0
    - Behavioral Interview Score: {interview_score}%
    
    Resume text:
    {resume_text}
    
    Provide a detailed analysis covering:
    1. Technical skills alignment with {subfield}
    2. Academic performance assessment
    3. Behavioral competencies
    4. Areas for improvement
    5. Overall placement readiness score (0-100)
    
    Focus only on skills and experiences explicitly mentioned in the resume."""
    
    response = model.generate_content(prompt)
    return response.text

def calculate_interview_score(responses: List[int]) -> float:
    """Calculate the interview score based on responses."""
    correct_answers = sum(1 for q, resp in zip(HR_QUESTIONS, responses) 
                         if resp == q['best_answer'])
    return (correct_answers / len(HR_QUESTIONS)) * 100

# init session 
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'responses' not in st.session_state:
    st.session_state.responses = []

# UI
st.title("Placement Readiness Assessment")

# Basic info + HR Questions
if st.session_state.step == 1:
    # Field 
    field_options = [
        "Software Engineer", "Data Scientist", "Editor", "Animator", 
        "Computer Vision Engineer", "Robotics Engineer", "UI/UX Designer"
    ]
    field = st.selectbox("Select your field:", field_options)

    # Subfield 
    subfield_mapping = {
        "Software Engineer": ["Backend", "Frontend", "Full Stack", "Mobile", "Cloud"],
        "Editor": ["Video", "Content", "Technical", "News", "Creative"],
        "Animator": ["2D", "3D", "Motion Graphics", "Character", "Visual Effects"],
        "Computer Vision Engineer": ["Object Detection", "Image Processing", "Video Analytics"],
        "Robotics Engineer": ["Industrial", "Research", "AI", "Control Systems"]
    }
    subfields = subfield_mapping.get(field, ["General"])
    subfield = st.selectbox("Select your subfield:", subfields)

    # GPA 
    gpa = st.number_input("Enter your GPA (0-4.0):", min_value=0.0, max_value=4.0, step=0.1)

    st.subheader("📝 Behavioral Interview Questions")
    st.write("Please answer all questions to proceed.")

    responses = []
    for i, q in enumerate(HR_QUESTIONS):
        st.write(f"\n**Q{i+1}. {q['question']}**")
        response = st.radio(
            "Select your answer:",
            options=q['options'],
            key=f"q_{i}",
            index=None
        )
        if response is not None:
            responses.append(q['options'].index(response))

    if len(responses) == len(HR_QUESTIONS) and st.button("Continue to Resume Upload"):
        st.session_state.field = field
        st.session_state.subfield = subfield
        st.session_state.gpa = gpa
        st.session_state.responses = responses
        st.session_state.step = 2
        st.rerun()

# Resume Upload 
elif st.session_state.step == 2:
    st.subheader("📄 Resume Upload")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file and st.button("Analyze Profile"):
        with st.spinner("Analyzing your complete profile..."):
            # calculate intv score
            interview_score = calculate_interview_score(st.session_state.responses)
            
            # analyze resume
            resume_text = extract_text_from_pdf(uploaded_file)
            analysis = analyze_profile(
                resume_text,
                st.session_state.field,
                st.session_state.subfield,
                interview_score,
                st.session_state.gpa
            )

            # results
            st.subheader("🎯 Profile Analysis")
            
            # Intv Perform
            st.write("**Behavioral Interview Performance:**")
            st.progress(interview_score/100)
            st.write(f"Score: {interview_score:.1f}%")
            
            # GPA assessment
            st.write("\n**Academic Performance:**")
            gpa_score = (st.session_state.gpa / 4.0) * 100
            st.progress(gpa_score/100)
            st.write(f"GPA: {st.session_state.gpa}/4.0")
            
            # Resume Analysis
            st.write("\n**Detailed Analysis:**")
            st.write(analysis)
            
            if st.button("Start Over"):
                st.session_state.step = 1
                st.session_state.responses = []
                st.rerun()

st.sidebar.markdown("""
### Assessment Guidelines

1. **Field Expertise** 
   - Specific role alignment
   - Subfield specialization

2. **Academic Performance**
   - GPA evaluation

3. **Behavioral Assessment**
   - Communication skills
   - Team collaboration
   - Problem-solving approach
   - Learning attitude
   - Remote work capabilities

4. **Resume Analysis**
   - Technical skills
   - Project experience
   - Overall profile strength

Made by Agneya Pathare
""")

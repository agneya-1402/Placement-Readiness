# Placement Readiness SaaS App

A Streamlit application that assesses candidates' placement readiness by analyzing their profile through behavioral questions, academic performance, and resume analysis. The app provides comprehensive insights and a readiness score to help candidates understand their strengths and areas for improvement.

## Features

### 1. Profile Assessment
- Field and subfield selection for various roles
- GPA input and academic performance evaluation
- Behavioral HR questions
- Resume analysis using Gemini AI
- Comprehensive readiness score

### 2. Behavioral Assessment
The app includes carefully crafted questions focusing on key soft skills:
- Team collaboration and conflict resolution
- Task prioritization and time management
- Adaptability and learning attitude
- Communication effectiveness
- Feedback reception and implementation

### 3. Resume Analysis
- Technical skills evaluation
- Experience relevance assessment
- Project analysis
- Skills gap identification
- Personalized improvement recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/agneya-1402/Placement-Readiness.git
cd placement-readiness
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Get a Google Gemini API key from the Google AI Studio
2. Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the app through your web browser at `http://localhost:8501`

3. Follow the assessment steps:
   - Select your field and subfield
   - Enter your GPA
   - Answer the behavioral questions
   - Upload your resume (PDF format)
   - Review your comprehensive analysis

## Project Structure

```
placement-readiness-app/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies                 
├── README.md             # Project documentation
```

## Dependencies

- Python 3.8+
- streamlit
- google-generativeai
- python-dotenv
- PyPDF2

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Customization

### Adding New Fields
To add new professional fields and subfields, modify the `field_options` and `subfield_mapping` dictionaries in `app.py`:

```python
field_options = [
    "Software Engineer",
    "Data Scientist",
    # Add new fields here
]

subfield_mapping = {
    "Software Engineer": ["Backend", "Frontend", "Full Stack"],
    # Add new subfields here
}
```

### Modifying Questions
To modify the behavioral questions, update the `HR_QUESTIONS` list in `utils/questions.py`:

```python
HR_QUESTIONS = [
    {
        "question": "Your question here",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "best_answer": index_of_best_answer
    },
]
```

## Best Practices

1. **Resume Format**: Upload resumes in PDF format for best results
2. **Answer Honestly**: Provide genuine responses to behavioral questions
3. **Complete Profile**: Fill in all information for accurate assessment
4. **Regular Updates**: Keep your resume updated with latest skills and experiences

## Troubleshooting

Common issues and solutions:

1. **API Key Error**:
   - Verify your Gemini API key in the `.env` file
   - Check API key permissions and quota

2. **Resume Upload Issues**:
   - Ensure PDF format
   - Check file size (max 10MB)
   - Verify PDF is not password protected

3. **Analysis Timeout**:
   - Try reducing resume file size
   - Check internet connection
   - Retry the analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

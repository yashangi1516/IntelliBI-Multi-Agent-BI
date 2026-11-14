# IntelliBI — Multi-Agent Business Intelligence System

> Replace every bracketed field with your own verified details. Add screenshots from your working application.

## Title Page
**Project Title:** IntelliBI — Multi-Agent Business Intelligence System  
**Submitted by:** [Student name]  
**Course / Semester:** [Course and semester]  
**Institute:** [Institute name]  
**Academic Session:** [Session]  
**Project Guide:** [Guide name]

## Abstract
IntelliBI is a web-based academic prototype that helps users inspect business datasets. Users can upload CSV and Excel files through a browser interface. A FastAPI backend validates the file, stores it locally, computes basic data-quality statistics and a sample preview, and coordinates specialist analysis modules. The modules provide an initial view of dataset structure, likely sales and financial measures, categorical patterns, chart-suitable numeric fields, and general recommendations. SQLite stores upload metadata. The prototype demonstrates how a multi-agent architecture can divide a business-intelligence task into smaller responsibilities.

## 1. Introduction
Business datasets can contain many rows and columns, missing values, duplicate records and measures that are difficult to interpret quickly. IntelliBI provides a single interface for uploading a dataset and viewing an initial analysis. Its modular agent design separates the work into specialist tasks coordinated by an orchestrator.

## 2. Objectives
- Build a browser-based dataset upload interface.
- Accept CSV and Excel files with basic validation.
- Calculate row count, column count, missing values and duplicate rows.
- Display a sample of uploaded records.
- Coordinate specialist analysis modules.
- Store uploaded-file metadata in SQLite.

## 3. Technology Stack
- Frontend: HTML5, CSS3 and JavaScript.
- Backend: Python and FastAPI.
- Data processing: Pandas.
- Database: SQLite.
- API testing: FastAPI Swagger documentation.

## 4. System Design
The frontend sends the selected file to the FastAPI upload endpoint using a multipart form request. The backend validates the extension and size, saves the file, reads it with Pandas, calculates a summary, runs the specialist agents, and inserts the filename and file path into SQLite. The JSON response is rendered on the frontend.

### Main modules
1. User Interface
2. Dataset Upload and Validation
3. Data Processing
4. Specialist Business Agents
5. Agent Orchestrator
6. SQLite Metadata Storage
7. Results and Recommendations

## 5. Implementation
Describe the code you ran and explain important functions in your own words. Include screenshots of the home page, upload section, dataset preview, agent findings, and Swagger API.

## 6. Testing
Use the included `sales_data.csv` as a test input. Verify that the application reports 10 rows, 9 columns, 0 missing values and 0 duplicate rows. Also test an unsupported file extension and an empty file. Record the actual outcomes and screenshots.

## 7. Results
[Insert your actual screenshots and describe the observed output. Do not write that a test passed unless you ran it.]

## 8. Limitations
The current specialist agents use rule-based heuristics and common column-name patterns. They may not understand every business dataset. Recommendations are general and require human review. The application is a local academic prototype.

## 9. Future Enhancements
Gemini integration, charts, PDF report export, user authentication, richer business-specific metrics, improved data validation and cloud deployment.

## 10. Conclusion
Summarize what you implemented, what you learned about frontend-backend communication, API development, data processing, SQLite and modular agent design.

## References
- FastAPI documentation: https://fastapi.tiangolo.com/
- Pandas documentation: https://pandas.pydata.org/docs/
- Python documentation: https://docs.python.org/3/

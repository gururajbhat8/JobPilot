import streamlit as st
import requests
import os

st.set_page_config(page_title="JobPilot AI", page_icon="🚀", layout="wide")

st.title("🚀 JobPilot AI: Your Personal ATS")
st.subheader("Upload your resume and let our AI agents find the best matching jobs!")

# Drag and drop file uploader
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    if st.button("Find Matches"):
        with st.spinner("Agents are reading your resume and searching the Vector Database..."):
            
            # The URL of your local FastAPI server
            url = os.getenv("API_URL", "http://127.0.0.1:8000/match")
            
            # Package the file exactly how FastAPI expects it
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            
            try:
                # Send the POST request to FastAPI
                response = requests.post(url, files=files)
                
                # Check if we got an error (like a 500 or 404)
                if response.status_code != 200:
                    st.error(f"Error from backend: {response.text}")
                else:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    if not matches:
                        st.warning("No jobs found in the database.")
                    else:
                        st.success("Matches found!")
                        
                        # Loop through the matches and display them beautifully
                        for match in matches:
                            title = match.get("title", "Unknown Role")
                            company = match.get("company", "Unknown Company")
                            job_url = match.get("url", "")
                            
                            analysis = match.get("match_analysis", {})
                            # Our schema uses 'score' as a decimal (e.g. 0.85), so we multiply by 100
                            score = analysis.get("score", 0) * 100 
                            missing_skills = analysis.get("missing_skills", [])
                            matched_skills = analysis.get("matched_skills", [])
                            
                            # Create a dropdown card for each job
                            with st.expander(f"💼 {title} at {company} (AI Match Score: {score:.0f}/100)", expanded=True):
                                
                                if matched_skills:
                                    st.markdown("**🟢 Skills you matched:**")
                                    # Join them into a nice comma-separated list
                                    st.markdown(", ".join(matched_skills))
                                
                                if missing_skills:
                                    st.markdown("**🔴 Skills you need to learn:**")
                                    for skill in missing_skills:
                                        st.markdown(f"- {skill}")
                                        
                                if job_url:
                                    st.markdown(f"\n[🔗 Click here to Apply on LinkedIn]({job_url})")
                                    
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the FastAPI backend! Is it running? Error: {e}")

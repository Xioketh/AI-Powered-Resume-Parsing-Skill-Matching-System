import streamlit as st
from app import parse_scanned_cv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=st.secrets["CLOUDINARY"]["cloud_name"],
    api_key=st.secrets["CLOUDINARY"]["api_key"],
    api_secret=st.secrets["CLOUDINARY"]["api_secret"],
    secure = True
)

# Set page config
st.set_page_config(
    page_title="CV Parser Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .header {
        font-size: 36px !important;
        font-weight: bold !important;
        color: #2a3f5f !important;
        margin-bottom: 10px !important;
    }
    .subheader {
        font-size: 18px !important;
        color: #4a6b8a !important;
        margin-bottom: 30px !important;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .card-header {
        font-size: 20px;
        font-weight: bold;
        color: #2a3f5f;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .skill-match {
        font-size: 18px;
        font-weight: bold;
    }
    .match-high {
        color: #2e7d32;
    }
    .match-medium {
        color: #f9a825;
    }
    .match-low {
        color: #c62828;
    }
    .stProgress > div > div > div > div {
        background-color: #4a6b8a;
    }
    .stTextInput > div > div > input {
        padding: 10px !important;
    }
    .stFileUploader > div > div > div > button {
        padding: 10px 20px !important;
        width: 100%;
    }
    .stButton > button {
        width: 100%;
        padding: 10px !important;
    }
    .column-divider {
        border-left: 1px solid #e6e6e6;
        padding-left: 20px;
    }
    .skill-chip {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 5px 10px;
        border-radius: 20px;
        margin: 3px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


# Main app
def main():
    # Header
    st.markdown('<div class="header">📄 CV Parser Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Upload a scanned CV and extract key information with skill matching</div>',
                unsafe_allow_html=True)

    # Split layout into two columns
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # Upload CV card
        with st.container():
            st.markdown('<div class="card-header">📤 1. Upload CV</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")

        # Skills input card
        with st.container():
            st.markdown('<div class="card-header">🛠️ 2. Required Skills</div>', unsafe_allow_html=True)

            # Common skills dropdown
            common_skills = [
                "Python", "Java", "JavaScript", "React", "Angular", "Node.js",
                "SQL", "MongoDB", "Docker", "Kubernetes", "AWS", "Azure",
                "Machine Learning", "Data Analysis", "Git", "CI/CD", "Flask",
                "Django", "Spring Boot", "HTML/CSS", "TypeScript", "PHP",
                "C++", "C#", ".NET", "TensorFlow", "PyTorch", "Pandas",
                "NumPy", "REST API", "GraphQL", "Linux", "Windows Server",
                "PostgreSQL", "MySQL", "SQLite", "Firebase", "Redis",
                "RabbitMQ", "Apache Kafka", "Nginx", "Jenkins", "Ansible",
                "Terraform", "OpenShift", "GCP", "Heroku", "Jira",
                "Agile", "Scrum", "TDD", "Unit Testing", "Selenium",
                "Cypress", "Playwright", "Bootstrap", "Tailwind CSS"
            ]

            # Multiselect dropdown
            selected_skills = st.multiselect(
                "Select skills from common list",
                common_skills,
                placeholder="Choose skills...",
                label_visibility="collapsed"
            )

            # Text input for additional skills
            additional_skills_input = st.text_input(
                "Add custom skills (comma separated)",
                placeholder="e.g., Scala, Vue.js, Terraform",
                label_visibility="collapsed"
            )

            # Combine both inputs
            if additional_skills_input:
                additional_skills = [s.strip() for s in additional_skills_input.split(",") if s.strip()]
                required_skills = selected_skills + additional_skills
            else:
                required_skills = selected_skills if selected_skills else None

            # Display selected skills as chips
            if required_skills:
                st.markdown("**Selected skills:**")
                chips = "".join([f'<span class="skill-chip">{skill}</span>' for skill in required_skills])
                st.markdown(chips, unsafe_allow_html=True)

        # Parse button at the bottom of the left column
        parse_btn = st.button("Analyze CV", type="primary", use_container_width=True)

    with col2:
        st.markdown('<div class="column-divider">', unsafe_allow_html=True)

        if parse_btn and uploaded_file is not None:
            # Save uploaded file temporarily
            with open("temp_cv.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Parse the CV
            with st.spinner("Analyzing CV. This may take a moment..."):
                try:
                    upload_result = cloudinary.uploader.upload(
                        "temp_cv.pdf",
                        folder="cv_uploads",
                        resource_type="raw"  # For PDF files
                    )
            
                    # Store the Cloudinary URL in your result if needed
                    cloudinary_url = upload_result.get('secure_url')
            
                    result = parse_scanned_cv("temp_cv.pdf", required_skills)

                    # Display results in cards
                    st.markdown("### Analysis Results")

                    # Basic info card
                    with st.container():
                        st.markdown('<div class="card-header">👤 Basic Information</div>', unsafe_allow_html=True)
                        cols = st.columns([1, 2])
                        cols[0].markdown("**Name**")
                        cols[1].markdown(result.get('name', 'Not found'))

                        cols = st.columns([1, 2])
                        cols[0].markdown("**Email**")
                        cols[1].markdown(result.get('email', 'Not found'))

                        cols = st.columns([1, 2])
                        cols[0].markdown("**Phone**")
                        cols[1].markdown(result.get('phone', 'Not found'))

                    # About card
                    with st.container():
                        st.markdown('<div class="card-header">📝 Summary</div>', unsafe_allow_html=True)
                        st.write(result.get('about', 'No summary section found'))

                    # Skills card
                    with st.container():
                        st.markdown('<div class="card-header">🛠️ Detected Skills</div>', unsafe_allow_html=True)
                        st.write(f"**{len(result.get('skills', []))} skills found**")
                        if result.get('skills'):
                            chips = "".join(
                                [f'<span class="skill-chip">{skill}</span>' for skill in result.get('skills', [])])
                            st.markdown(chips, unsafe_allow_html=True)
                        st.caption(f"Average confidence: {result.get('skillsAverageConfidence', 0) * 100:.1f}%")

                    # Skill matching card
                    if required_skills:
                        with st.container():
                            st.markdown('<div class="card-header">✅ Skill Matching</div>', unsafe_allow_html=True)
                            match_percentage = result.get('matchPercentage', 0)

                            # Determine match level for styling
                            if match_percentage >= 70:
                                match_class = "match-high"
                            elif match_percentage >= 40:
                                match_class = "match-medium"
                            else:
                                match_class = "match-low"

                            st.markdown(f"""
                            <div class="skill-match {match_class}">
                                Match Percentage: {match_percentage}%
                            </div>
                            """, unsafe_allow_html=True)

                            st.progress(match_percentage / 100)

                            st.write("**Matched Skills:**")
                            if result.get('matchedSkills'):
                                matched_chips = "".join([f'<span class="skill-chip">{skill}</span>' for skill in
                                                         result.get('matchedSkills', [])])
                                st.markdown(matched_chips, unsafe_allow_html=True)
                            else:
                                st.write("No matches found")

                    # Clean up temp file
                    os.remove("temp_cv.pdf")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if os.path.exists("temp_cv.pdf"):
                        os.remove("temp_cv.pdf")

        elif parse_btn and uploaded_file is None:
            st.warning("Please upload a PDF file first")
        else:
            # Placeholder for empty state
            st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; text-align: center;">
                <div style="font-size: 72px;">📄</div>
                <h3>No CV Analyzed Yet</h3>
                <p style="color: #666;">Upload a CV and click "Analyze CV" to see results</p>
            </div>
            """, unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()

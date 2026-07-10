import streamlit as st
import requests
import re

API = "http://127.0.0.1:5000"

def apply_neon_style():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background-color: #060606;
            color: #e0e0e0;
        }

        /* Neon Header Styling */
        h1, h2, h3 {
            color: #00f2ff !important;
            text-shadow: 0 0 10px #00f2ff, 0 0 5px #00f2ff;
            letter-spacing: 2px;
        }

        /* Input Field Styling */
        .stTextInput div[data-baseweb="input"], 
        .stSelectbox div[data-baseweb="select"],
        .stMultiSelect div[data-baseweb="select"] {
            background-color: #1a1a1a !important;
            border: 1px solid #00f2ff !important;
            box-shadow: 0 0 8px #00f2ff;
            color: white !important;
        }

        /* Registration Button - Magenta Neon */
        .stButton>button {
            background-color: transparent !important;
            color: #ff00ff !important;
            border: 2px solid #ff00ff !important;
            box-shadow: 0 0 10px #ff00ff;
            font-weight: bold;
            width: 100%;
            transition: 0.3s;
            text-transform: uppercase;
        }

        .stButton>button:hover {
            background-color: #ff00ff !important;
            color: white !important;
            box-shadow: 0 0 25px #ff00ff;
        }

        /* Info/Credit Box Styling */
        .stAlert {
            background-color: rgba(0, 242, 255, 0.05) !important;
            border: 1px solid #00f2ff !important;
            color: #00f2ff !important;
            box-shadow: 0 0 5px rgba(0, 242, 255, 0.2);
        }

        /* Course List Card */
        .course-item {
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid #ff00ff;
            background: rgba(255, 255, 255, 0.03);
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_neon_style()
    
    st.header("Course Registration")

    # Grouping inputs into columns for a cleaner "Dashboard" look
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Name")
        department = st.selectbox("Department", ["CSE", "DSAI", "ECE"])
    
    with col2:
        roll = st.text_input("Roll Number")
        semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8])

    # --- Logic ---
    patterns = {
        "CSE": r"^\d{2}[bB][cC][sS]\d{3}$",
        "DSAI": r"^\d{2}[bB][dD][sS]\d{3}$",
        "ECE": r"^\d{2}[bB][eE][cC]\d{3}$"
    }

    if roll:
        if not re.match(patterns[department], roll):
            st.error(f"Invalid roll number format for {department}")

    semester_rules = {
        1:(18,2), 2:(18,5), 3:(21,5), 4:(21,5), 
        5:(22,6), 6:(21,6), 7:(11,2), 8:(8,2)
    }
    max_credit, max_elective_credit = semester_rules[semester]

    core_courses = []
    elective_courses = []

    try:
        r = requests.get(f"{API}/courses/{department}/{semester}")
        if r.status_code == 200:
            data = r.json()
            core_courses = data.get("core", [])
            elective_courses = data.get("elective", [])
    except Exception:
        st.error("Backend server not running")

    st.markdown("---")
    
    # --- UI Layout for courses ---
    left_body, right_body = st.columns([1, 1])

    with left_body:
        st.subheader("Core Courses (Automatically Registered)")
        core_credit = 0
        for c in core_courses:
            st.markdown(f'<div class="course-item">{c["course_name"]} ({c["credits"]} credits)</div>', unsafe_allow_html=True)
            core_credit += c["credits"]

    with right_body:
        st.subheader("Select Elective Courses")
        elective_labels = [f"{c['course_name']} ({c['credits']} credits)" for c in elective_courses]
        elective_map = {f"{c['course_name']} ({c['credits']} credits)": c for c in elective_courses}

        selected_electives = st.multiselect("Elective Courses", elective_labels)
        elective_credit = sum(elective_map[e]["credits"] for e in selected_electives)

    st.markdown("---")

    # --- Credit Summary Section ---
    total_credit = core_credit + elective_credit

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    stat_col1.info(f"Core Credits: {core_credit}")
    stat_col2.info(f"Elective Credits: {elective_credit} / {max_elective_credit}")
    stat_col3.info(f"Total Credits: {total_credit} / {max_credit}")

    if elective_credit > max_elective_credit:
        st.error("Elective credit limit exceeded")
    if total_credit > max_credit:
        st.error("Total credit limit exceeded")

    # --- Submit Action ---
    if st.button("Register Courses"):
        if not name or not roll:
            st.error("Please fill all fields")
            return

        if not re.match(patterns[department], roll):
            st.error("Invalid roll number format")
            return

        if elective_credit > max_elective_credit:
            st.error("Elective credit rule violated")
            return

        if total_credit > max_credit:
            st.error("Total credit rule violated")
            return

        course_ids = [c["course_id"] for c in core_courses] + [elective_map[e]["course_id"] for e in selected_electives]

        payload = {
            "name": name,
            "roll": roll,
            "department": department,
            "semester": semester,
            "courses": course_ids
        }

        try:
            response = requests.post(f"{API}/register_student", json=payload)
            if response.status_code == 200:
                st.success("Courses registered successfully")
            else:
                st.error("Registration failed")
        except Exception:
            st.error("Cannot connect to backend")

if __name__ == "__main__":
    show()
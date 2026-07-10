import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

def apply_neon_style():
    st.markdown("""
        <style>
        /* Main Dark Background */
        .stApp {
            background-color: #060606;
            color: #e0e0e0;
        }

        /* Neon Titles */
        h1, h2, h3 {
            color: #00f2ff !important;
            text-shadow: 0 0 12px #00f2ff, 0 0 5px #00f2ff;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        /* Input and Button Glow */
        .stTextInput div[data-baseweb="input"] {
            border: 1px solid #00f2ff !important;
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
        }

        .stButton>button {
            background-color: transparent !important;
            color: #ff00ff !important;
            border: 2px solid #ff00ff !important;
            box-shadow: 0 0 10px #ff00ff;
            font-weight: bold;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #ff00ff !important;
            color: white !important;
            box-shadow: 0 0 30px #ff00ff;
        }

        /* Metric Styling */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            border-left: 3px solid #00f2ff;
            padding: 15px;
            border-radius: 5px;
        }
        
        div[data-testid="stMetricValue"] {
            color: #39ff14 !important; /* Neon Green for numbers */
            text-shadow: 0 0 5px #39ff14;
        }

        /* Expanders & Dataframes */
        .streamlit-expanderHeader {
            background-color: #1a1a1a !important;
            border: 1px solid #333 !important;
            color: #00f2ff !important;
        }
        
        /* Line Chart Customization */
        .stAreaChart, .stLineChart {
            border: 1px solid #333;
            padding: 10px;
            background: #0a0a0a;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_neon_style()
    
    st.title("🎓 Student Academic Record")
    st.caption("Enter a student's roll number to view full academic history.")

    # Search Bar Section
    col_search, _ = st.columns([2, 1])
    with col_search:
        roll = st.text_input(
            "Roll Number",
            placeholder="e.g. 24BDS069"
        ).strip().upper()

    if not roll:
        st.info("Please enter roll number.")
        return

    if st.button("🔍 Fetch Record"):
        try:
            res = requests.get(f"{API}/student_record/{roll}")
            if res.status_code == 404:
                st.error("Student not found")
                return
            if res.status_code != 200:
                st.error("Server error")
                return
            data = res.json()
        except:
            st.error("Backend not running")
            return

        # ─────────────────────────────
        # Student Info Header
        # ─────────────────────────────
        st.markdown(f"### 👤 {data['name']}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Roll", data["roll"])
        c2.metric("Department", data["department"])

        cgpa_prog = data.get("cgpa_progression", [])
        current_cgpa = cgpa_prog[-1]["cgpa"] if cgpa_prog else "N/A"
        c3.metric("Current CGPA", current_cgpa)

        st.divider()

        # ─────────────────────────────
        # Semester Records
        # ─────────────────────────────
        st.subheader("Semester Records")
        semesters = data.get("semesters", [])

        if not semesters:
            st.warning("No marks entered yet")
            return

        for sem in semesters:
            sem_no = sem["semester"]
            sgpa = sem.get("sgpa", "N/A")

            # Neon-styled expander
            with st.expander(f"Semester {sem_no}  |  SGPA: {sgpa}", expanded=False):
                courses = sem.get("courses", [])

                if courses:
                    df = pd.DataFrame(courses)
                    df.columns = [
                        "Course Code", "Course Name", "Credits",
                        "Marks", "Grade", "Grade Points"
                    ]
                    # Styled dataframe
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No courses")

                col_s1, col_s2 = st.columns(2)
                col_s1.metric("SGPA", sgpa)
                col_s2.metric("CGPA after semester", sem.get("cgpa_after", "N/A"))

        # ─────────────────────────────
        # CGPA Chart
        # ─────────────────────────────
        if cgpa_prog:
            st.divider()
            st.subheader("CGPA Progression")

            chart_df = pd.DataFrame(cgpa_prog)
            chart_df = chart_df.set_index("semester")
            chart_df.index = [f"Sem {s}" for s in chart_df.index]

            # Line chart will inherit theme colors
            st.line_chart(
                chart_df["cgpa"],
                use_container_width=True
            )

if __name__ == "__main__":
    show()
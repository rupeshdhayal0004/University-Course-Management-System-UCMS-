import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

def apply_neon_style():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp { background-color: #060606; color: #e0e0e0; }

        /* Neon Header Styling */
        h1, h2, h3 {
            color: #00f2ff !important;
            text-shadow: 0 0 10px #00f2ff, 0 0 5px #00f2ff;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        /* Input Field Styling */
        .stTextInput div[data-baseweb="input"], 
        .stSelectbox div[data-baseweb="select"] {
            background-color: #1a1a1a !important;
            border: 1px solid #00f2ff !important;
            box-shadow: 0 0 8px rgba(0, 242, 255, 0.3);
            color: white !important;
        }

        /* Success & Info Alerts */
        .stAlert {
            background-color: rgba(0, 242, 255, 0.05) !important;
            border: 1px solid #00f2ff !important;
            color: #00f2ff !important;
            box-shadow: 0 0 5px rgba(0, 242, 255, 0.2);
        }

        /* Dataframe Neon Border */
        .stDataFrame {
            border: 1px solid rgba(255, 0, 255, 0.3);
            border-radius: 5px;
            padding: 5px;
        }

        /* Custom Divider */
        hr {
            border: 0;
            border-top: 1px solid #ff00ff;
            box-shadow: 0 0 10px #ff00ff;
            margin: 2em 0;
        }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_neon_style()
    
    st.title("👥 Registered Students")

    # ══════════════════════════════════════════════════════
    # STEP 1 — BATCH SELECTION
    # ══════════════════════════════════════════════════════
    st.markdown("---")
    st.subheader("Select Batch")
    st.caption("Enter the 2-digit batch year for system filtering.")

    col_batch, col_sem = st.columns([2, 1])

    with col_batch:
        batch_input = st.text_input(
            "Batch Year (2-digit prefix of roll number)",
            max_chars=2,
            placeholder="e.g. 25",
            key="vs_batch"
        ).strip()

    if not batch_input:
        st.info("⬆️ Awaiting Batch Year input...")
        return

    if not batch_input.isdigit() or len(batch_input) != 2:
        st.error("❌ Invalid Batch: Must be 2 digits (e.g. 24, 25).")
        return

    selected_batch = batch_input
    
    # ══════════════════════════════════════════════════════
    # STEP 2 — SEMESTER SELECTION
    # ══════════════════════════════════════════════════════
    with col_sem:
        selected_sem = st.selectbox(
            "Semester",
            options=list(range(1, 9)),
            format_func=lambda s: f"Semester {s}",
            key="vs_sem"
        )

    st.success(f"🔍 SEARCHING: Batch 20{selected_batch} | Semester {selected_sem}")
    st.markdown("---")

    # ══════════════════════════════════════════════════════
    # STEP 3 — SHOW EACH DEPARTMENT
    # ══════════════════════════════════════════════════════
    for dept in ["CSE", "DSAI", "ECE"]:
        st.subheader(f"{dept} Database")

        try:
            r = requests.get(f"{API}/students/{dept}/{selected_batch}/{selected_sem}")
            filtered = r.json() if r.status_code == 200 else []
        except Exception:
            st.error("📡 CONNECTION_ERROR: Backend server offline")
            return

        if filtered:
            display_df = pd.DataFrame(filtered)[["name", "roll", "department", "course_name"]]
            display_df.columns = ["Name", "Roll", "Department", f"Courses (Sem {selected_sem})"]
            
            # Using st.dataframe with high-contrast styling
            st.dataframe(
                display_df.reset_index(drop=True), 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(f"EMPTY_SET: No {dept} students found for 20{selected_batch}")

        st.divider()

if __name__ == "__main__":
    show()
import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

def apply_neon_style():
    st.markdown("""
        <style>
        .stApp { background-color: #060606; color: #e0e0e0; }
        h1, h2, h3 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-transform: uppercase; }
        
        /* Input Glows */
        .stSelectbox div[data-baseweb="select"], .stTextInput input, .stNumberInput input {
            background-color: #1a1a1a !important;
            border: 1px solid #00f2ff !important;
            color: white !important;
            box-shadow: 0 0 5px rgba(0, 242, 255, 0.2);
        }

        /* Neon Buttons */
        .stButton>button {
            background-color: transparent !important;
            color: #ff00ff !important;
            border: 2px solid #ff00ff !important;
            box-shadow: 0 0 10px #ff00ff;
            font-weight: bold;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #ff00ff !important;
            color: white !important;
            box-shadow: 0 0 25px #ff00ff;
        }

        /* Status Colors */
        .total-glow { color: #39ff14; text-shadow: 0 0 5px #39ff14; font-weight: bold; }
        .stAlert { background-color: rgba(0, 242, 255, 0.05) !important; border: 1px solid #00f2ff !important; color: #00f2ff !important; }
        </style>
    """, unsafe_allow_html=True)

def show():
    apply_neon_style()
    st.title("🎓 Teacher Portal")

   # --- STEP 1: SELECT TEACHER ---
    st.markdown("---")
    st.subheader("Step 1 — Select Teacher")
 
    try:
        r = requests.get(f"{API}/teachers")
        if r.status_code != 200:
            st.error("Failed to fetch teachers"); return
        all_teachers = r.json()
    except:
        st.error("Backend not running."); return
 
    if "teacher_courses_cache" not in st.session_state:
        cache = {}
        for t in all_teachers:
            try:
                tc = requests.get(f"{API}/teacher/{t['teacher_id']}/courses")
                cache[t["teacher_id"]] = tc.json() if tc.status_code == 200 else []
            except: cache[t["teacher_id"]] = []
        st.session_state["teacher_courses_cache"] = cache
    
    teacher_courses_cache = st.session_state["teacher_courses_cache"]
 
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        dept_filter = st.selectbox("Filter by Department", ["All Departments", "CSE", "DSAI", "ECE"], key="t_dept")
    
    # Always include teachers with department='ALL' (elective course teachers)
    # alongside the selected department's teachers
    if dept_filter == "All Departments":
        dept_filtered = all_teachers
    else:
        dept_filtered = [t for t in all_teachers if t["department"] == dept_filter or t["department"] == "ALL"]
    
    sems = sorted(set(c["semester"] for t in dept_filtered for c in teacher_courses_cache.get(t["teacher_id"], [])))
    with col2:
        sem_filter = st.selectbox("Filter by Semester", ["All Semesters"] + [f"Semester {s}" for s in sems], key="t_sem")
    
    chosen_sem = None if sem_filter == "All Semesters" else int(sem_filter.split(" ")[1])
    
    sem_filtered = [t for t in dept_filtered if chosen_sem is None or any(c["semester"] == chosen_sem for c in teacher_courses_cache.get(t["teacher_id"], []))]
    
    if not sem_filtered:
        st.warning("No teachers found."); return
 
    teacher_options = {f"{t['teacher_name']} ({t['department']})": t["teacher_id"] for t in sem_filtered}
    with col3:
        selected_label = st.selectbox("Select Teacher", list(teacher_options.keys()), key="t_select")
    
    selected_teacher_id = teacher_options[selected_label]
    st.info(f"✅ Active: **{selected_label.split(' (')[0]}**")
    # --- STEP 2: SELECT BATCH ---
    st.markdown("---")
    st.subheader("Step 2 — Select Batch")
    batch_input = st.text_input("Batch Year (2-digit)", max_chars=2, placeholder="e.g. 25", key="t_batch").strip()

    if not batch_input or not batch_input.isdigit() or len(batch_input) != 2:
        st.warning("Enter valid 2-digit batch to continue."); return
    
    selected_batch = batch_input

    # --- STEP 3: SELECT COURSE ---
    st.markdown("---")
    st.subheader("Step 3 — Select Course")
    courses_data = teacher_courses_cache.get(selected_teacher_id, [])
    if chosen_sem:
        courses_data = [c for c in courses_data if c["semester"] == chosen_sem]

    if not courses_data:
        st.warning("No courses found."); return

    course_options = {f"[Sem {c['semester']}] {c['course_code']} — {c['course_name']}": c["course_id"] for c in courses_data}
    selected_course_label = st.selectbox("Select Course", list(course_options.keys()))
    selected_course_id = course_options[selected_course_label]

    # --- STEP 4: CONFIGURE EXAM COMPONENTS ---
    st.markdown("---")
    st.subheader("Step 4 — Configure Exam Components")

    try:
        comp_r = requests.get(f"{API}/exam_components/{selected_course_id}")
        existing_components = comp_r.json() if comp_r.status_code == 200 else []
    except: existing_components = []

    comp_key = f"components_{selected_course_id}"
    if comp_key not in st.session_state:
        st.session_state[comp_key] = [{"name": c["component_name"], "max_marks": c["max_marks"]} for c in existing_components] if existing_components else [{"name": "Mid Semester", "max_marks": 30}, {"name": "End Semester", "max_marks": 50}, {"name": "Assignment", "max_marks": 20}]

    components = st.session_state[comp_key]
    
    c_add, c_rem, _ = st.columns([1, 1, 2])
    if c_add.button("➕ Add"): components.append({"name": "New", "max_marks": 0}); st.rerun()
    if c_rem.button("🗑️ Remove") and len(components) > 1: components.pop(); st.rerun()

    total_marks = 0
    updated_components = []
    for i, comp in enumerate(components):
        cols = st.columns([3, 2])
        name = cols[0].text_input(f"Name {i+1}", value=comp["name"], key=f"cn_{selected_course_id}_{i}")
        max_m = cols[1].number_input("Max", 0, 100, comp["max_marks"], key=f"cm_{selected_course_id}_{i}")
        total_marks += max_m
        updated_components.append({"name": name, "max_marks": max_m})

    st.markdown(f"**Total Weightage: <span class='total-glow'>{total_marks}/100</span>**", unsafe_allow_html=True)

    if st.button("💾 Save Components", disabled=(total_marks != 100)):
        try:
            payload = {"teacher_id": selected_teacher_id, "components": updated_components}
            resp = requests.post(f"{API}/exam_components/{selected_course_id}", json=payload)
            if resp.status_code == 200:
                st.success("✅ Configuration Saved!"); st.rerun()
            else:
                st.error(f"Save Failed: {resp.text}")
        except Exception as e:
            st.error(f"Request Error: {e}")

    # --- STEP 5: ENTER MARKS ---
    if not existing_components:
        st.info("Save valid components to unlock mark entry."); return

    st.markdown("---")
    st.subheader("Step 5 — Enter Marks")

    try:
        marks_r = requests.get(f"{API}/marks/{selected_course_id}")
        students_marks = [s for s in marks_r.json() if str(s["roll"]).startswith(selected_batch)] if marks_r.status_code == 200 else []
    except: return

    if not students_marks:
        st.warning(f"No students found for Batch {selected_batch}"); return

    # Grid Display
    h_cols = st.columns([2, 2] + [1] * len(existing_components) + [1])
    h_cols[0].write("**Roll**"); h_cols[1].write("**Name**")
    for i, comp in enumerate(existing_components): h_cols[2+i].caption(f"{comp['component_name']} ({comp['max_marks']})")
    h_cols[-1].write("**Total**")

    marks_state_key = f"ms_{selected_course_id}_{selected_batch}"
    if marks_state_key not in st.session_state:
        st.session_state[marks_state_key] = {s["roll"]: {str(c["id"]): float(s["marks"].get(str(c["id"]), 0)) for c in existing_components} for s in students_marks}
    
    marks_state = st.session_state[marks_state_key]

    for s in students_marks:
        roll = s["roll"]
        r_cols = st.columns([2, 2] + [1] * len(existing_components) + [1])
        r_cols[0].write(roll); r_cols[1].write(s["name"])
        ts = 0
        for i, comp in enumerate(existing_components):
            cid = str(comp["id"])
            val = r_cols[2+i].number_input("", 0.0, float(comp["max_marks"]), marks_state[roll].get(cid, 0.0), step=0.5, key=f"m_{roll}_{cid}", label_visibility="collapsed")
            marks_state[roll][cid] = val
            ts += val
        r_cols[-1].markdown(f"<span class='total-glow'>{round(ts, 1)}</span>", unsafe_allow_html=True)

    if st.button("💾 Save All Marks", type="primary"):
        payload_m = [{"roll": r, "component_id": int(cid), "marks": mv} for r, cm in marks_state.items() for cid, mv in cm.items()]
        try:
            r_save = requests.post(f"{API}/marks/{selected_course_id}", json={"teacher_id": selected_teacher_id, "marks": payload_m})
            if r_save.status_code == 200: st.success("✅ Marks Saved Successfully!")
            else: st.error(f"Error: {r_save.text}")
        except: st.error("Connection lost.")

if __name__ == "__main__":
    show()
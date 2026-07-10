import streamlit as st
import add_student
import view_students
import analytics
import teachers

# --- Global Page Config ---
st.set_page_config(
    page_title="University Course Management",
    page_icon="🎓",
    layout="wide"
)

# --- Cyberpunk Sidebar Styling ---
def apply_sidebar_style():
    st.markdown("""
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #060606 !important;
            border-right: 1px solid #00f2ff;
        }

        /* Sidebar Title Neon Glow */
        .sidebar-title {
            color: #00f2ff !important;
            text-shadow: 0 0 10px #00f2ff;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Radio Button Styling (Navigation) */
        div[data-testid="stSidebarNav"] {
            background-image: none !important;
        }
        
        /* Styling the radio options to look like glowing menu items */
        div[role="radiogroup"] label {
            background-color: transparent !important;
            color: #e0e0e0 !important;
            border: 1px solid transparent;
            padding: 10px !important;
            border-radius: 5px;
            transition: 0.3s;
        }

        div[role="radiogroup"] label:hover {
            color: #ff00ff !important;
            border: 1px solid #ff00ff !important;
            box-shadow: 0 0 10px #ff00ff;
        }

        /* Highlight the selected option */
        div[role="radiogroup"] label[data-selected="true"] {
            background-color: rgba(0, 242, 255, 0.1) !important;
            border: 1px solid #00f2ff !important;
            color: #00f2ff !important;
            box-shadow: 0 0 15px #00f2ff;
        }
        
        hr {
            border: 0;
            border-top: 1px solid #333;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the theme
apply_sidebar_style()

# --- Sidebar Header ---
st.sidebar.markdown('<div class="sidebar-title">🎓 UNIVERSITY CMS</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

menu_icons = {
    "📝 Add Student":   "Add Student",
    "👥 View Students": "View Students",
    "📊 Analytics":     "Analytics",
    "🏫 Teacher Portal": "Teachers",
}

# Navigation Menu
choice_label = st.sidebar.radio(
    "Navigation", 
    list(menu_icons.keys()), 
    label_visibility="collapsed"
)
choice = menu_icons[choice_label]

st.sidebar.markdown("---")
st.sidebar.caption("University Course Registration System")
st.sidebar.markdown('<p style="color:#00f2ff; font-size:10px; opacity:0.5;">STATUS: SYSTEM ONLINE</p>', unsafe_allow_html=True)

# --- Routing Logic ---
if choice == "Add Student":
    add_student.show()
elif choice == "View Students":
    view_students.show()
elif choice == "Analytics":
    analytics.show()
elif choice == "Teachers":
    teachers.show()
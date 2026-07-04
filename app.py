import streamlit as st
import pandas as pd
import urllib.parse
import requests
import re
import auth

# ===============================
# SESSION
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

auth.init_db()

# ===============================
# VIDEO FUNCTION (FIXED)
# ===============================
def get_video_link(query):
    try:
        search_query = urllib.parse.quote(query + " full course tutorial 1 hour english")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        html = requests.get(url).text

        video_ids = re.findall(r"watch\?v=(\S{11})", html)

        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"

    except:
        pass

    return f"https://www.youtube.com/results?search_query={search_query}"

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="SkillForge AI", layout="centered")

# ===============================
# UI (UNCHANGED DESIGN)
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fffef5, #fef9c3);
    color: #111827;
}
.block-container {
    max-width: 900px;
    margin: auto;
    text-align: center;
}
label {
    color: #111827 !important;
    font-weight: 800 !important;
}
.header {
    padding: 25px;
    border-radius: 16px;
    background: linear-gradient(to right, #fde68a, #facc15);
    margin-bottom: 25px;
}
.header h1 {
    color: #111827;
    font-size: 42px;
    font-weight: 900;
}
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
    border: 2px solid #facc15 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: #facc15 !important;
    color: black !important;
    font-weight: 700;
    border-radius: 10px;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 14px;
    margin: 10px;
}
.section {
    font-size: 24px;
    font-weight: 800;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOGIN
# ===============================
if st.session_state.user is None:

    st.markdown("""
    <div class="header">
        <h1>🔐 Welcome to SkillForge AI</h1>
        <p>Login to continue your learning journey</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            if auth.login_user(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Signup"):
            if auth.create_user(username, password):
                st.success("Account created")
            else:
                st.error("User exists")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ===============================
# MAIN UI
# ===============================
st.markdown(f"### 👋 Welcome, {st.session_state.user}")

st.markdown("""
<div class="header">
    <h1>🔥 SkillForge AI</h1>
    <p>Personalized AI Learning Platform</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# DATA
# ===============================
df = pd.read_csv("data/cleaned_courses.csv", encoding="latin1").dropna()
df.columns = df.columns.str.strip()

title_col = [c for c in df.columns if "title" in c.lower()][0]
subject_col = [c for c in df.columns if "subject" in c.lower()][0]

# ===============================
# INPUT
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    domain = st.selectbox("📚 Domain", sorted(df[subject_col].unique()))

with col2:
    level = st.selectbox("📈 Level", ["Beginner", "Intermediate", "Advanced"])

with col3:
    goal = st.selectbox("🎯 Goal", ["Job", "Internship", "Skill Growth", "Project"])

search = st.text_input("🔍 Search")

filtered = df[df[subject_col] == domain]

if search:
    filtered = filtered[
        filtered[title_col].str.contains(search, case=False)
    ]

filtered = filtered.reset_index(drop=True)

if len(filtered) == 0:
    st.warning("No courses found.")
    st.stop()

selected = st.selectbox("🎯 Select Course", filtered[title_col])

# ===============================
# BUTTON
# ===============================
if st.button("🚀 Get Recommendations"):

    auth.save_history(st.session_state.user, selected)

    response = requests.get(
        "http://127.0.0.1:8000/recommend",
        params={"course_name": selected}
    )

    data = response.json()

    st.markdown('<div class="section">🎯 Top Recommendations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    for count, item in enumerate(data["recommendations"]):

        title = item["title"]

        with (col1 if count % 2 == 0 else col2):

            st.markdown(f"""
            <div class="card">
                <b>{title}</b><br>
                Score: {item['score']}<br>
                {item['reason']}
            </div>
            """, unsafe_allow_html=True)

            link = get_video_link(title)
            st.markdown(f"[▶ Watch Full Video]({link})")

# ===============================
# HISTORY
# ===============================
st.markdown('<div class="section">📚 Your Learning List</div>', unsafe_allow_html=True)

history = auth.get_history(st.session_state.user)

for item in history[-5:][::-1]:
    st.write("•", item[0])
from fastapi import FastAPI
import pandas as pd
import re

app = FastAPI()

# ===============================
# LOAD + CLEAN DATA
# ===============================
df = pd.read_csv("data/cleaned_courses.csv", encoding="latin1").dropna()
df.columns = df.columns.str.strip()

title_col = [c for c in df.columns if "title" in c.lower()][0]
subject_col = [c for c in df.columns if "subject" in c.lower()][0]

# CLEAN FUNCTION
def clean_text(x):
    x = str(x).lower().strip()
    x = re.sub(r'[^a-z0-9 ]', '', x)
    return x

# APPLY CLEANING
df[title_col] = df[title_col].apply(clean_text)
df[subject_col] = df[subject_col].apply(clean_text)

# ===============================
# KEYWORD MATCH
# ===============================
def keyword_score(a, b):
    return len(set(a.split()) & set(b.split()))

# ===============================
# API
# ===============================
@app.get("/recommend")
def recommend(course_name: str):

    course_name_clean = clean_text(course_name)

    if course_name_clean not in df[title_col].values:
        return {"error": "Course not found"}

    selected = df[df[title_col] == course_name_clean].iloc[0]
    selected_title = selected[title_col]
    selected_subject = selected[subject_col]

    results = []

    for _, row in df.iterrows():

        title = row[title_col]
        subject = row[subject_col]

        # STRICT DOMAIN FILTER
        if subject != selected_subject:
            continue

        if title == selected_title:
            continue

        score = keyword_score(selected_title, title)

        if score < 1:
            continue

        results.append({
            "title": title,
            "score": score,
            "reason": "Same domain + keyword similarity"
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return {"recommendations": results[:6]}
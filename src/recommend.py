import pickle

# Load saved files
courses = pickle.load(open("../models/courses.pkl", "rb"))
similarity = pickle.load(open("../models/similarity.pkl", "rb"))

# Show some Python courses
python_courses = courses[
    courses["course_title"].str.contains("Python", case=False, na=False)
]

print("\nAvailable Python Courses:\n")
print(python_courses["course_title"].head(20))

# Choose the first Python course automatically
selected_course = python_courses.iloc[0]["course_title"]

print("\nSelected Course:")
print(selected_course)

# Find index of selected course
index = courses[courses["course_title"] == selected_course].index[0]

# Get similarity scores
distances = list(enumerate(similarity[index]))

# Sort by similarity
distances = sorted(distances, key=lambda x: x[1], reverse=True)

# Store recommendations
recommendations = []

# Top 20 similar courses
for i in distances[1:20]:

    title = courses.iloc[i[0]]["course_title"]
    similarity_score = i[1]

    subscribers = courses.iloc[i[0]]["num_subscribers"]
    reviews = courses.iloc[i[0]]["num_reviews"]

    # Popularity score
    popularity_score = subscribers * 0.7 + reviews * 0.3

    recommendations.append(
        (title, similarity_score, popularity_score)
    )

# Sort by popularity score
recommendations = sorted(
    recommendations,
    key=lambda x: x[2],
    reverse=True
)

# Print top 5 recommendations
print("\nRecommended Courses:\n")

for rec in recommendations[:5]:
    print(rec[0])
    print("Similarity Score:", round(rec[1], 3))
    print("Popularity Score:", int(rec[2]))
    print()
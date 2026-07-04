import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("../data/featured_courses.csv")

# Vectorize
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df["tags"])

# Similarity matrix
similarity = cosine_similarity(tfidf_matrix)

# Save files
pickle.dump(df, open("../models/courses.pkl", "wb"))
pickle.dump(tfidf, open("../models/tfidf.pkl", "wb"))
pickle.dump(similarity, open("../models/similarity.pkl", "wb"))

print("Models saved successfully!")
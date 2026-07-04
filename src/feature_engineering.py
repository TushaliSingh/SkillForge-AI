import pandas as pd

# Load cleaned dataset
df = pd.read_csv("../data/cleaned_courses.csv")

# Combine useful columns
df["tags"] = (
    df["course_title"] + " " +
    df["subject"] + " " +
    df["level"]
)

# Convert to lowercase
df["tags"] = df["tags"].str.lower()

# Save the new dataset
df.to_csv("../data/featured_courses.csv", index=False)

print("Feature engineering completed!")
print(df[["course_title", "tags"]].head())
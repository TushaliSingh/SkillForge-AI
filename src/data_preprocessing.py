import pandas as pd

# Load dataset
df = pd.read_excel("../data/Udemy Courses.xlsx")

# Remove duplicate rows
df = df.drop_duplicates()

# Convert price to numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Convert content duration to numeric
df["content_duration"] = (
    df["content_duration"]
    .str.replace(" hours", "", regex=False)
    .str.replace(" hour", "", regex=False)
)

df["content_duration"] = pd.to_numeric(
    df["content_duration"],
    errors="coerce"
)

# Save cleaned dataset
df.to_csv("../data/cleaned_courses.csv", index=False)

print("Data cleaned successfully!")
print(df.head())
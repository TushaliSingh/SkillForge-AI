import pandas as pd

df = pd.read_excel("../data/Udemy Courses.xlsx")

print(df.head())
print()
print(df.columns)
print()
print(df.info())
print()
print(df.isnull().sum())
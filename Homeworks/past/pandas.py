import pandas as pd

df = pd.read_csv('people.csv')

print("1. First 5 rows of the DataFrame:")
print(df.head())

print("\n2. DataFrame information:")
df.info()

print("\n3. Descriptive statistics:")
print(df.describe())

print("\n4. Missing values per column:")
print(df.isnull().sum())

print("\n5. Value counts for 'Profession':")
print(df['Profession'].value_counts())

print("\n6. Value counts for 'Gender':")
print(df['Gender'].value_counts())

print("\n7. Mean age by Gender:")
print(df.groupby('Gender')['Age'].mean())

print("\n8. Filtering for Females:")
female_df = df[df['Gender'] == 'Female']
print(female_df)

print("\n9. Adding a new column 'Age in 10 years':")
df['Age in 10 years'] = df['Age'] + 10
print(df.head())

print("\n10. Sorting the DataFrame by Age (descending):")
df_sorted = df.sort_values(by='Age', ascending=False)
print(df_sorted)

print("\n11. Checking for non-missing values with notna():")
print(df.notna())

print("\n12. Selecting the first row by label with loc[0]:")
print(df.loc[0])

print("\nSelecting the 'Profession' of the third person (index 2) with loc[2, 'Profession']:")
print(df.loc[2, 'Profession'])

print("\n13. Getting the dimensions (rows, columns) with shape:")
print(df.shape)

print("\n14. Filtering for Profession == 'plumber':")
plumber_df = df[df['Profession'] == 'Plumber']
print(plumber_df)

print("\n15. Names and Surnames of Plumbers")
plumber_df = df.loc[df['Profession'] == 'Plumber', ['Name', 'Surname']]
print(plumber_df)

print("\n16. Alphabetically Sorted:")
sorted_alphabetically = df.sort_values(by='Surname', ascending=True)
print(sorted_alphabetically)

print("\nExporting To Json:")
df.to_json('to.json', orient='records', indent=4)

# Script to clean event registration data

import pandas as pd

#Load the raw data
df = pd.read_csv('data.csv')

# Remove duplicate rows based on all columns
df = df.drop_duplicates()

# Convert variations of Yes/No (case-insensitive) to True/False
mapping = {
    'yes': True,
    'no': False,
    'y': True,
    'n': False
}

def normalize_joined(val):
    if pd.isna(val):
        return False
    v = str(val).strip().lower()
    return mapping.get(v, False)

df['has_joined_event'] = df['has_joined_event'].apply(normalize_joined)

# Flag missing or incomplete LinkedIn profiles
# We consider a profile incomplete if the field is empty or does not contain 'linkedin.com'

def flag_linkedin(profile):
    if pd.isna(profile) or not str(profile).strip():
        return True
    return 'linkedin.com' not in profile.lower()

# Create a new boolean column `linkedin_missing_or_incomplete`
df['linkedin_missing_or_incomplete'] = df['What is your LinkedIn profile?'].apply(flag_linkedin)

# Flag blank job titles
# Blank means NaN or empty string after stripping whitespace

def flag_job_missing(title):
    if pd.isna(title):
        return True
    return not bool(str(title).strip())

# Create a new boolean column `job_title_missing`
df['job_title_missing'] = df['Job Title'].apply(flag_job_missing)

# Save the cleaned dataframe to a new CSV
output_file = 'cleaned_output.csv'
df.to_csv(output_file, index=False)

print(f"Cleaned data saved to {output_file}")

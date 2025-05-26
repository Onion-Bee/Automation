# generate_messages.py
# Script to generate personalized follow-up messages based on event attendance and profile details

import pandas as pd

# 1. Load the cleaned data
# Replace 'cleaned_output.csv' with the path to your cleaned data file
df = pd.read_csv('cleaned_output.csv')

# 2. Define a function to craft messages
def craft_message(row):
    first_name = row.get('name', '').split()[0]
    job_title = row.get('Job Title', '')
    joined = bool(row.get('has_joined_event', False))
    linkedin_missing = bool(row.get('linkedin_missing_or_incomplete', False))

    # Base greetings and bodies
    if joined:
        greeting = f"Hey {first_name}, thanks for joining our session!"
        body = f"As a {job_title}, we think you’ll love our upcoming AI workflow tools."
        closing = "Want early access?"
    else:
        greeting = f"Hi {first_name}, sorry we missed you at the last event!"
        body = f"We’re preparing another session that might better suit your interests as a {job_title}."
        closing = ""

    # LinkedIn prompt
    if linkedin_missing:
        linkedin_note = "By the way, feel free to connect with us on LinkedIn to stay updated."
    else:
        linkedin_note = ""

    # Combine parts, filter out any empty strings
    parts = [greeting, body, linkedin_note, closing]
    message = " ".join([p for p in parts if p])
    return message

# 3. Apply the function to each row

df['message'] = df.apply(craft_message, axis=1)

# 4. Prepare the output dataframe with only email and message
output_df = df[['email', 'message']].copy()

# 5. Save to CSV
output_file = 'messages_output.csv'
output_df.to_csv(output_file, index=False)

print(f"Generated messages saved to {output_file}")

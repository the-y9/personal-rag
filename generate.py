import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_cover_letter(jd_text, retrieved_chunks):
    try:
        context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
        prompt = f"""
        Based on the following job description:\n{jd_text}\n
        And my background:\n{context}\n
        Write a personalized, compelling cover letter.
        """
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        else:
            return "Error: Could not generate cover letter.  Empty response."
    except Exception as e:
        return f"Error generating cover letter: {e}"

if __name__ == "__main__":
    load_dotenv()
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        # Example usage (replace with your actual data)
        jd_text = "Software Engineer with 5+ years of experience in Python and Java."
        retrieved_chunks = [
            {"text": "I have 6 years of experience in Python."},
            {"text": "I have 4 years of experience in Java."},
            {"text": "I worked on a team developing a large-scale web application."}
        ]

        cover_letter = generate_cover_letter(jd_text, retrieved_chunks) # added model_name
        print(cover_letter)
    except Exception as e:
        print(f"An error occurred: {e}")
    
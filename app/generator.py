from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

model = None
background_str = ""

def init_model():
    global model, background_str
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Load static data once
    background_str = f"""
    Personal Information: {load_json('data/about.json')}
    Education: {load_json('data/edu.json')}
    Projects: {load_json('data/projects.json')}
    Experience: {load_json('data/exp.json')}
    Skills: {load_json('data/skills.json')}
    """

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.dumps(json.load(f), indent=2)

def generate_cover_letter(job_description: str) -> dict:
    from datetime import date
    import time

    start = time.time()

    with open('text/instructions.md', 'r') as f:
        instructions = f.read()

    prompt = f"""
    {instructions}
    Use 'Dated: {date.today()}' as the date in the letter.

    ### Job Description: {job_description.strip()}
    ### Candidate Background: {background_str}
    """

    response = model.generate_content(prompt)
    text = response.text if response and response.text else ""

    if not text:
        raise ValueError("Empty response from model.")

    output_path = "cover_letter.txt"
    with open(output_path, "w") as f:
        f.write(text)

    return {
        "content": text,
        "file": output_path,
        "time_taken_seconds": round(time.time() - start, 2)
    }

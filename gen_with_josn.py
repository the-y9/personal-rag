import os
import subprocess
import json
import time
from datetime import date
from dotenv import load_dotenv
import google.generativeai as genai

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.dumps(json.load(f), indent=2)

def main():
    jd = input("Enter the job description: ").strip()
    # if not jd:
    #     print("No job description provided. Exiting.")
    #     return

    start = time.time()
    print("Start time:", time.strftime("%H:%M:%S", time.localtime(start)))

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in environment variables.")
        return
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")

    # Load data
    background_str = f"""
    Personal Information: {load_json('data/about.json')}
    Education: {load_json('data/edu.json')}
    Projects: {load_json('data/projects.json')}
    Experience: {load_json('data/exp.json')}
    Skills: {load_json('data/skills.json')}
    """
    with open('text/instructions.md', 'r') as f:
        instructions = f.read()
    
    lap1 = time.time()
    print("Loading time:", round(time.time() - lap1, 2), "s")

    # Build prompt
    prompt = f"""
    {instructions}
    Use 'Dated: {date.today()}' as the date in the letter.
    
    ### Job Description: {jd}
    ### Candidate Background: {background_str}
    """


    lap2 = time.time()
    print("Prompting Time:", round(lap2 - lap1, 2), "s")
    print("Prompt length:", len(prompt))

    # Generate content
    try:
        response = model.generate_content(prompt)
        lap3 = time.time()
        print("Response time:", round(lap3 - lap2, 2), "s")
        text = response.text if response and response.text else ""
        print("Response length:", len(text))

        if text:
            output_path = "cover_letter.txt"
            with open(output_path, "w") as f:
                f.write(text)
            print(f"Cover letter saved to {output_path}")

            # Open in VS Code
            vscode_path = r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            subprocess.run([vscode_path, output_path])
        else:
            print("Error: Could not generate cover letter. Empty response.")

    except Exception as e:
        print(f"Error generating cover letter: {e}")
    finally:
        print("Total time taken:", round(time.time() - start, 2), "s")

if __name__ == "__main__":
    main()

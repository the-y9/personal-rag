import requests
jds = ['ai engineer',
       'data scientist',
       'software engineer',
       'data analyst',
       ]
url = "https://personal-rag.onrender.com/generate-cover-letter/"

for i in jds:
    payload = {
        "job_description": i
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    print('-'*20)
    print()

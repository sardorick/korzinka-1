import requests

JSON_URL = "https://drive.google.com/uc?export=download&id=1vbHELLhLzr5VaDiaeesDQ6BRsEoFd9lK"
OUTPUT_FILE = "data/clicks.json"  

def extract_json():
    response = requests.get(JSON_URL)
    response.raise_for_status() 

    with open(OUTPUT_FILE, 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    extract_json()

import requests

# Extract the file using requests
# If it was an API endpoint, it could be automated to receive updated data each day for example.
JSON_URL = "https://drive.google.com/uc?export=download&id=1vbHELLhLzr5VaDiaeesDQ6BRsEoFd9lK"
OUTPUT_FILE = "data/clicks.json"  

def extract_json():
    response = requests.get(JSON_URL)
    response.raise_for_status() 

    # Save it to a local json file.
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    extract_json()

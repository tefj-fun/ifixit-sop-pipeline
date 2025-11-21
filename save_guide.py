import requests
import json

def save_guide_json(guide_id):
    url = f"https://www.ifixit.com/api/2.0/guides/{guide_id}"
    response = requests.get(url)
    data = response.json()
    
    with open(f"guide_{guide_id}.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved guide_{guide_id}.json")

if __name__ == "__main__":
    save_guide_json(10365)

import requests
import json

def inspect_guide(guide_id):
    url = f"https://www.ifixit.com/api/2.0/guides/{guide_id}"
    response = requests.get(url)
    data = response.json()
    
    if 'steps' in data and len(data['steps']) > 0:
        first_step = data['steps'][0]
        if 'media' in first_step and 'data' in first_step['media']:
            print("\n--- Image Data ---")
            # Print the first image object in full to check for markers
            print(json.dumps(first_step['media']['data'][0], indent=2))
    else:
        print("No steps found.")

if __name__ == "__main__":
    inspect_guide(10365)

import requests
import json

def get_image_id(guide_id):
    url = f"https://www.ifixit.com/api/2.0/guides/{guide_id}"
    response = requests.get(url)
    data = response.json()
    
    if 'steps' in data:
        for step in data['steps']:
            if 'media' in step and 'data' in step['media']:
                for media in step['media']['data']:
                    if media['type'] == 'image':
                        print(f"Image ID: {media['id']}")
                        return
    print("No image found.")

if __name__ == "__main__":
    get_image_id(10365)

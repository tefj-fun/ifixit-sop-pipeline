import requests

def list_categories():
    url = "https://www.ifixit.com/api/2.0/categories"
    response = requests.get(url)
    data = response.json()
    
    # Print top-level categories
    print("Top-level categories:")
    for key in data.keys():
        print(f"- {key}")

    # Check for "Appliance" specifically
    if "Appliance" in data:
        print("\n'Appliance' category found!")
    elif "Home and Garden" in data:
         print("\n'Home and Garden' category found!")

if __name__ == "__main__":
    list_categories()

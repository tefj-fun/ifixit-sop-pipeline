import requests
import json
import time
import os
from typing import List, Dict, Any, Optional

class IFixitClient:
    BASE_URL = "https://www.ifixit.com/api/2.0"

    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "SOP-Training-Bot/1.0 (Educational Purpose)"
        })

    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            time.sleep(0.5)  # Polite delay
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return {}

    def search_guides(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for guides by query."""
        results = []
        offset = 0
        while len(results) < limit:
            data = self._get(f"suggest/{query}", params={"limit": 20, "offset": offset})
            if not data or "results" not in data:
                break
            
            # Filter for guides only
            guides = [item for item in data["results"] if item.get("dataType") == "guide"]
            results.extend(guides)
            
            if len(data["results"]) < 20:
                break
            offset += 20
            
        return results[:limit]

    def get_guide_details(self, guide_id: int) -> Dict:
        """Fetch full details for a specific guide."""
        return self._get(f"guides/{guide_id}")

    def process_guide(self, guide_data: Dict) -> Optional[Dict]:
        """Transform raw guide data into our target schema."""
        if not guide_data or "steps" not in guide_data:
            return None

        processed = {
            "id": guide_data.get("guideid"),
            "title": guide_data.get("title"),
            "url": guide_data.get("url"),
            "category": guide_data.get("category"),
            "difficulty": guide_data.get("difficulty"),
            "time_required": guide_data.get("time_required"),
            "steps": []
        }

        # Extract steps
        for step in guide_data.get("steps", []):
            processed_step = {
                "order": step.get("orderby"),
                "instruction": "", # Constructed from lines
                "lines": [],
                "media": []
            }

            # Process Lines (Text & Logic)
            full_text = []
            for line in step.get("lines", []):
                line_data = {
                    "bullet": line.get("bullet"), # logic color (red, orange, etc.)
                    "level": line.get("level"),
                    "text": line.get("text_raw")
                }
                processed_step["lines"].append(line_data)
                full_text.append(line.get("text_raw"))
            
            processed_step["instruction"] = "\n".join(full_text)

            # Process Media (Images)
            if "media" in step and "data" in step["media"]:
                for media in step["media"]["data"]:
                    if media.get("type") == "image":
                        processed_step["media"].append({
                            "type": "image",
                            "id": media.get("id"),
                            "url": media.get("original"), # Full res
                            "thumbnail": media.get("thumbnail")
                        })

            processed["steps"].append(processed_step)

        return processed

    def download_dataset(self, queries: List[str], limit_per_query: int = 10):
        """Download guides for multiple queries and save to JSONL."""
        output_file = os.path.join(self.output_dir, "ifixit_dataset.jsonl")
        
        seen_ids = set()
        
        with open(output_file, "a", encoding="utf-8") as f:
            for query in queries:
                print(f"Searching for: {query}...")
                guides = self.search_guides(query, limit=limit_per_query)
                
                for guide_summary in guides:
                    guide_id = guide_summary.get("guideid")
                    if guide_id in seen_ids:
                        continue
                    
                    print(f"  Processing Guide ID: {guide_id} - {guide_summary.get('title')}")
                    raw_data = self.get_guide_details(guide_id)
                    processed_data = self.process_guide(raw_data)
                    
                    if processed_data:
                        f.write(json.dumps(processed_data) + "\n")
                        seen_ids.add(guide_id)
        
        print(f"\nDataset saved to {output_file}")
        print(f"Total unique guides: {len(seen_ids)}")

if __name__ == "__main__":
    client = IFixitClient()
    
    # Example queries covering requested categories
    queries = [
        "MacBook Battery", 
        "iPhone Screen", 
        "Washing Machine", 
        "Dryer", 
        "Toaster", 
        "Vacuum"
    ]
    
    client.download_dataset(queries, limit_per_query=5)

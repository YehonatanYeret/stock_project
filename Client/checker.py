import requests

BASE_URL = "http://localhost:6333"

def get_collections():
    url = f"{BASE_URL}/collections"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # Adjust extraction based on Qdrant response structure
    collections = data.get("result", {}).get("collections", [])
    return collections

def get_points_for_collection(collection_name, limit=10):
    """
    Retrieve a sample of points from the given collection using the scroll endpoint.
    """
    url = f"{BASE_URL}/collections/{collection_name}/points/scroll"
    payload = {"limit": limit}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    collections = get_collections()

    if not collections:
        print("No collections found in Qdrant.")
        return

    for coll in collections:
        collection_name = coll.get("name", "Unknown")
        print(f"Collection: {collection_name}")
        try:
            points_data = get_points_for_collection(collection_name)
            print("Points data:")
            print(points_data)
        except Exception as e:
            print(f"Error retrieving points for collection {collection_name}: {e}")
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()

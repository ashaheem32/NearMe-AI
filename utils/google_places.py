import requests
import os

def search_places(location, radius):
    """
    Get cafes/shops/venues near a location using Google Places API.

    Args:
        location (str): Human-readable address (e.g., "Koramangala, Bangalore")
        radius (int): Search radius in meters

    Returns:
        list: List of places (Google Places API format)
    """
    # Geocode the location to get lat/lng
    geo_url = (
        f"https://maps.googleapis.com/maps/api/geocode/json"
        f"?address={location}&key={os.getenv('GOOGLE_API_KEY')}"
    )
    geo_resp = requests.get(geo_url).json()
    if not geo_resp['results']:
        return []
    lat = geo_resp['results'][0]['geometry']['location']['lat']
    lng = geo_resp['results'][0]['geometry']['location']['lng']

    # Search for places of interest
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lng}&radius={radius}"
        f"&type=cafe|restaurant|shopping_mall|store|bar"
        f"&key={os.getenv('GOOGLE_API_KEY')}"
    )
    resp = requests.get(url).json()
    return resp.get('results', [])

def get_place_details(place_id):
    """
    Fetch reviews and description for a place using Google Places API.

    Args:
        place_id (str): Place ID from Google Places

    Returns:
        dict: {
            "reviews": [ { "author", "rating", "text", "time" }, ... ],
            "description": str
        }
    """
    url = (
        "https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={place_id}&fields=name,formatted_address,review,editorial_summary,photos,geometry,vicinity"
        f"&key={os.getenv('GOOGLE_API_KEY')}"
    )
    resp = requests.get(url).json()
    result = resp.get('result', {})
    # Collect detailed reviews
    reviews_list = []
    for r in result.get('reviews', []):
        reviews_list.append({
            "author": r.get("author_name", "Anonymous"),
            "rating": r.get("rating", ""),
            "text": r.get("text", ""),
            "time": r.get("relative_time_description", "")
        })
    desc = result.get('editorial_summary', {}).get('overview', '')
    return {
        "reviews": reviews_list,
        "description": desc,
    }
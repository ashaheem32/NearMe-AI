import streamlit as st
from dotenv import load_dotenv
import os
from utils.google_places import search_places, get_place_details
from utils.langchain_matcher import match_place_with_query

load_dotenv()

st.set_page_config(page_title="🔎 Smart Local Search", layout="wide")
st.title("🔎 Smart Local Search – Find Your Perfect Place")

query = st.text_input(
    "Describe your ideal cafe/shop/venue:",
    placeholder="e.g. 'Cafe with outdoor seating, live music, pet-friendly'"
)
location = st.text_input(
    "Enter your area or city:",
    placeholder="Koramangala, Bangalore"
)
search_radius = st.slider(
    "Search radius (km):",
    min_value=1, max_value=20, value=5
)

if st.button("Search"):
    if not (query and location):
        st.warning("Please enter both your requirements and location.")
    else:
        with st.spinner("Searching for the best matches..."):
            places = search_places(location, search_radius * 1000)
            if not places:
                st.error("No places found for your location. Try a different area.")
            results = []
            for place in places:
                details = get_place_details(place['place_id'])
                # --- Prepare reviews for AI matching ---
                ai_reviews = "\n".join(
                    [f"{r['author']} ({r['rating']}★): {r['text']}" for r in details['reviews']]
                )
                match_score, explanation = match_place_with_query(
                    query,
                    ai_reviews,
                    details.get('description', '')
                )
                results.append({
                    "name": place['name'],
                    "address": place.get('vicinity', place.get('formatted_address', '')),
                    "score": match_score,
                    "explanation": explanation,
                    "lat": place['geometry']['location']['lat'],
                    "lng": place['geometry']['location']['lng'],
                    "photo_ref": place.get('photos', [{}])[0].get('photo_reference', None),
                    "reviews_list": details['reviews'],
                })
            # Sort and display results
            results = sorted(results, key=lambda x: x['score'], reverse=True)
            for r in results[:10]:
                st.markdown(f"### {r['name']}")
                st.write(r['address'])
                st.write(r['explanation'])

                # Show real Google reviews in an expander
                if r['reviews_list']:
                    with st.expander("See Reviews"):
                        for rev in r['reviews_list']:
                            st.markdown(
                                f"**{rev['author']}** ({rev['rating']}★) — {rev['time']}<br>{rev['text']}",
                                unsafe_allow_html=True
                            )
                else:
                    st.write("_No reviews available._")

                # Show photo if available
                if r['photo_ref']:
                    photo_url = (
                        f"https://maps.googleapis.com/maps/api/place/photo"
                        f"?maxwidth=400&photoreference={r['photo_ref']}&key={os.getenv('GOOGLE_API_KEY')}"
                    )
                    st.image(photo_url)

                # Show map for this result
                st.map([{"lat": r["lat"], "lon": r["lng"]}])
                st.markdown("---")
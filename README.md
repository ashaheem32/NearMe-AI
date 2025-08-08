# NearMe AI 🚀

**AI-Driven Neighborhood Exploration Tool (Streamlit)**

NearMe AI is an intelligent local search and recommendation engine that helps users find the best places and experiences nearby. Built with Streamlit, it leverages AI to deliver personalized results and a smooth user experience.

---

## Features

- Personalized recommendations based on user input
- Natural language search for places and activities
- Interactive map visualization of results
- Real-time data fetching from external APIs
- Smart filtering by type, rating, and distance

---

## Tech Stack

- Streamlit (Python)
- Google Places API / Mapbox API
- NLP for query understanding
- Docker (optional for deployment)

---

## Getting Started

Follow these steps to set up and run NearMe AI locally.

### 1. Prerequisites

- Python 3.8+
- Streamlit
- API key for Google Places or Mapbox

---

### 2. Clone the Repository

```bash
git clone https://github.com/ashaheem32/NearMe-AI.git
cd NearMe-AI
```
3. Create and Activate a Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate


⸻

4. Install Dependencies

pip install -r requirements.txt


⸻

5. Configure API Keys 🔑

Create a file named .env in the project root directory and add your API keys:

GOOGLE_PLACES_API_KEY=your_google_api_key_here
# Or, if using Mapbox:
MAPBOX_API_KEY=your_mapbox_api_key_here


⸻

6. Run the Application

streamlit run app.py


⸻

Project Structure

NearMe-AI/
├── app.py
├── requirements.txt
├── .env
├── modules/
├── assets/
├── README.md
└── ...

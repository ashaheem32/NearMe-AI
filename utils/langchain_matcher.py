import os
from dotenv import load_dotenv

load_dotenv()  # Always load .env

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langsmith import traceable

# --- API Key loading & debugging ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
    # Uncomment the next line to hardcode your key for testing (remove for production)
    # OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print("⚠️  OPENAI_API_KEY not found! Please check your .env file and environment.")
else:
    print("✅ OPENAI_API_KEY loaded successfully.")

# --- LangChain OpenAI LLM Setup ---
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.4,
    openai_api_key=OPENAI_API_KEY
)

PROMPT_TEMPLATE = """
You are a helpful assistant for matching people with local venues based on reviews and descriptions.

User wants: "{query}"

Description: {description}
Reviews: {reviews}

1. List the main features, ambience, and facilities mentioned.
2. Does this place match what the user wants? Give a match score out of 10, and explain why or why not.
Return a JSON: {{"score": int, "explanation": str}}
"""

@traceable(name="PlaceMatchingChain")
def match_place_with_query(query, reviews, description):
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_parser=JsonOutputParser()
    )
    try:
        result = chain.invoke({
            "query": query,
            "description": description,
            "reviews": reviews,
        })
        # Defensive fallback
        if isinstance(result, dict):
            return result.get("score", 0), result.get("explanation", "No explanation.")
        # Sometimes output_parser returns just a string, handle it gracefully:
        import json, re
        json_match = re.search(r'\{.*\}', str(result), re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data.get("score", 0), data.get("explanation", "No explanation.")
        return 0, str(result)
    except Exception as e:
        return 0, f"Error: {e}"
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from dotenv import load_dotenv

from langchain_groq import ChatGroq  # ✅ NEW
from langchain_core.messages import HumanMessage, SystemMessage  # ✅ NEW

load_dotenv()

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SPOTIFY_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")  # put in .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # ✅ NEW

# ✅ Init Groq LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama3-70b-8192"  # You can change model if needed
)


@app.get("/search")
def search_music(query: str):
    headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}
    params = {"q": query, "type": "track", "limit": 10}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    return r.json()


@app.post("/interpret")
async def interpret_prompt(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")

    # ✅ Groq-compatible prompt structure
    response = llm.invoke([
        SystemMessage(content="You are a music recommendation engine."),
        HumanMessage(content=prompt)
    ])

    return {"parsed_query": response.content}

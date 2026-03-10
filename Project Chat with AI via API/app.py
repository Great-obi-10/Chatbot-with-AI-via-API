from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request schema
class ChatRequest(BaseModel):
    message: str


# Home page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request.message}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
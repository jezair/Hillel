import json
from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()


client = OpenAI(
    api_key="...",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROMPT = (
    "Generate random technical post ideas. "
    "Limit your response to 100 characters for the idea. "
    "Ideas must be relevant nowadays.\n"
    "Your response must be in next format:\n"
    '{"title": "title...", "idea": "content..."}\n\n'
    "Your response must be a valid string so it can be "
    "put into Python's `json.loads(...)`.\n"
)


@dataclass
class ArticleIdea:
    title: str
    content: str


def get_article_ideas(n: int = 10):
    results: list[dict] = []

    for _ in range(n):
        print("started generating post idea")
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="",
            input=f"{PROMPT}\n\nGenerate only {n} items",
        )
        results.append(json.loads(response.output_text))
        print("finished generating post idea")

    return results


@app.get("/article-idea")
def generate_idea():
    results = get_article_ideas(1)

    return results[0]

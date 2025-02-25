from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from ai_content_engine.prompts import planner_prompt
from pydantic import BaseModel
from ai_content_engine.process_paper import process_arxiv_paper


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class Section(BaseModel):
    title: str
    context: str
    instructions: str
    queries: list[str] | None


class Outline(BaseModel):
    sections: list[Section]


def generate_outline(paper_text):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[paper_text],
        config=types.GenerateContentConfig(
            system_instruction=planner_prompt,
            response_mime_type="application/json",
            response_schema=Outline,
            max_output_tokens=8192,
        ),
    )
    print(response.text)
    outline: Outline = response.parsed
    print(outline)
    with open("ai_content_engine/outline2.json", "w") as f:
        f.write(outline.model_dump_json())

    return outline


text = process_arxiv_paper("https://arxiv.org/pdf/2502.13923v1.pdf")
outline = generate_outline(text)

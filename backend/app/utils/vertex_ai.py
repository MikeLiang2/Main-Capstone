import os
import json
from typing import List
import google.generativeai as genai
from app.models.checklists import ProcessInstanceCreate

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = (
    "You are an assistant that generates process checklists as a JSON object "
    "matching the ProcessInstanceCreate schema. The object must contain:\n"
    "- name: string for the overall process name\n"
    "- description: string describing the process\n"
    "- category_id: integer and always 1\n"
    "- stages: array of stage objects. Each stage has name (string), order (int), \n"
    "  and steps (array of step objects). Each step has name (string), description (string),\n"
    "  completed (bool, default false), and resourceUrl (string).\n"
    "Return only valid JSON with no extra text."
)

def generate_checklist(prompt: str) -> ProcessInstanceCreate:
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser request: {prompt}"

    response = model.generate_content(
        contents=full_prompt,
        generation_config={"response_mime_type": "application/json"}
    )

    try:
        data = json.loads(response.text)
        process = ProcessInstanceCreate(**data)
        return process
    except Exception as e:
        raise ValueError(f"AI response parse failed: {e}, Raw: {response.text}")

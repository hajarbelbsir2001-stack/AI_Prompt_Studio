from fastapi import FastAPI
from prompt_generator import generate_prompt

app = FastAPI()


@app.get("/")
def accueil():
    return {"message": "Bienvenue dans AI Prompt Studio !"}


@app.get("/generate")
def generate(
        domain: str,
        subject: str,
        objective: str,
        level: str,
        language: str,
        tone: str
):
    prompt = generate_prompt(
        domain,
        subject,
        objective,
        level,
        language,
        tone
    )

    return {
        "prompt": prompt
    }
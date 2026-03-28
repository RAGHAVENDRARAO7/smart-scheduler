import os
from openai import OpenAI
import requests

API_BASE = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

client = OpenAI()

def run_task(task="easy"):
    obs = requests.post(f"{API_BASE}/reset", json={"task": task}).json()

    done = False
    total_score = 0

    while not done:
        action = {
            "proposed_time": "11:00",
            "duration": 60,
            "decision": "schedule",
            "message": "Scheduling meeting efficiently."
        }

        res = requests.post(f"{API_BASE}/step", json=action).json()

        total_score += res["reward"]["score"]
        done = res["done"]

    return total_score


if __name__ == "__main__":
    scores = []
    for task in ["easy", "medium", "hard"]:
        score = run_task(task)
        scores.append(score)

    print("Scores:", scores)
    print("Average:", sum(scores)/len(scores))
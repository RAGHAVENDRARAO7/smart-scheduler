from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Body
from env import SmartSchedulerEnv
from models import Action
import uvicorn
import os

app = FastAPI()
env = SmartSchedulerEnv()

# -------------------------------
# 🌐 Frontend UI
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "<h1>index.html not found</h1>"

# -------------------------------
# 🔄 Reset (GET - optional)
# -------------------------------
@app.get("/reset")
def reset_get():
    return env.reset().dict()

# -------------------------------
# 🔄 Reset (POST - REQUIRED)
# -------------------------------
from fastapi import Request

# 🔥 ONLY KEEP THIS VERSION
@app.post("/reset")
async def reset(request: Request):
    data = await request.json()
    task = data.get("task", "easy")

    obs = env.reset(task)
    return obs.dict()
# -------------------------------
# 📊 Get current state
# -------------------------------
@app.get("/state")
def state():
    return env.state()

# -------------------------------
# ⚙️ Step API
# -------------------------------
@app.post("/step")
async def step(request: Request):
    try:
        action = await request.json()
        action_obj = Action(**action)

        # Ensure env initialized
        if env.state_data is None:
            env.reset()

        obs, reward, done, _ = env.step(action_obj)

        return {
            "observation": obs.dict(),
            "reward": reward.dict(),
            "done": done,
            "turn": env.turn
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# 📋 Available tasks
# -------------------------------
@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            "easy_basic_scheduling",
            "medium_conflict_resolution",
            "hard_multi_turn"
        ]
    }

# -------------------------------
# 🧪 Grader
# -------------------------------
@app.post("/grader")
async def grader(request: Request):
    action = await request.json()

    temp_env = SmartSchedulerEnv()
    temp_env.reset()

    action_obj = Action(**action)
    _, reward, _, _ = temp_env.step(action_obj)

    return {
        "score": reward.score,
        "breakdown": reward.breakdown,
        "explanation": reward.explanation
    }

# -------------------------------
# 📈 Baseline
# -------------------------------
@app.get("/baseline")
def baseline():
    env.reset()

    action = {
        "proposed_time": "11:00",
        "duration": 60,
        "decision": "schedule",
        "message": "Meeting scheduled at 11:00 successfully."
    }

    _, reward, _, _ = env.step(Action(**action))

    return {
        "baseline_score": reward.score,
        "explanation": reward.explanation
    }

# -------------------------------
# ❤️ Health check
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# 🚀 Run (Hugging Face compatible)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
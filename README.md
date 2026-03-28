---
title: smart-scheduler-env
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: main.py
pinned: false
---

# Smart Scheduling Assistant (OpenEnv)

A real-world scheduling simulation environment for AI agents.

## Features
- Multi-turn interaction
- Conflict resolution
- Priority handling
- Partial information reasoning
- Reward-based evaluation

## API Endpoints

- GET /reset
- POST /step
- GET /state
- GET /tasks
- POST /grader
- GET /baseline

## Run Locally

pip install -r requirements.txt  
uvicorn main:app --reload

## Docker

docker build -t scheduler-env .  
docker run -p 7860:7860 scheduler-env
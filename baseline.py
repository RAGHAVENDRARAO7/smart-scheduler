from env import SmartSchedulerEnv
from models import Action
import random

random.seed(42)

def smart_baseline_agent(obs):
    if obs.request["preferred_time"] is None:
        return Action(
            proposed_time=None,
            duration=obs.request["duration"],
            decision="ask",
            message="Could you clarify your preferred meeting time so I can schedule optimally?"
        )

    busy = {e["start"] for e in obs.calendar}

    for slot in ["09:00", "11:00", "13:00", "15:00"]:
        if slot not in busy:
            return Action(
                proposed_time=slot,
                duration=obs.request["duration"],
                decision="schedule",
                message=f"I've scheduled your meeting at {slot} considering availability and preferences."
            )

    return Action(
        proposed_time=None,
        duration=obs.request["duration"],
        decision="reschedule",
        message="All slots are occupied. Would you like to reschedule?"
    )


if __name__ == "__main__":
    env = SmartSchedulerEnv()
    scores = []

    for _ in range(10):
        obs = env.reset(task=random.choice(["easy", "medium", "hard"]))
        done = False

        while not done:
            action = smart_baseline_agent(obs)
            obs, reward, done, _ = env.step(action)

        scores.append(reward.score)

    print("Scores:", scores)
    print("Average:", sum(scores) / len(scores))
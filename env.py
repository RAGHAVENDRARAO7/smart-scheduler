from models import Observation, Action, Reward
import random


class SmartSchedulerEnv:
    def __init__(self):
        self.state_data = None
        self.done = False
        self.turn = 0
        self.max_turns = 3
        self.task = "easy"

    # -------------------------
    # RESET
    # -------------------------
    def reset(self, task="easy"):
        self.done = False
        self.turn = 0
        self.task = task
        self.state_data = self._generate_scenario(task)
        return Observation(**self.state_data)

    # -------------------------
    # STATE
    # -------------------------
    def state(self):
        return self.state_data

    # -------------------------
    # STEP
    # -------------------------
    def step(self, action: Action):
        self.turn += 1

        score, breakdown, explanation = self._compute_reward(action)

        # Multi-turn support
        if action.decision == "ask" and self.turn < self.max_turns:
            self.state_data["history"].append(action.message)
            return (
                Observation(**self.state_data),
                Reward(score=score, breakdown=breakdown, explanation=explanation),
                False,
                {}
            )

        self.done = True
        return (
            Observation(**self.state_data),
            Reward(score=score, breakdown=breakdown, explanation=explanation),
            True,
            {}
        )

    # -------------------------
    # SCENARIO GENERATION
    # -------------------------
    def _generate_scenario(self, task):
        calendar = [
            {"start": "10:00", "end": "11:00"},
            {"start": "14:00", "end": "15:00"}
        ]

        if task == "medium":
            calendar.append({"start": "11:00", "end": "12:00"})

        if task == "hard":
            calendar.append({"start": "11:00", "end": "12:00"})
            calendar.append({"start": "16:00", "end": "17:00", "recurring": True})

        # Simulate cancellation
        if random.random() > 0.7 and len(calendar) > 1:
            calendar.pop(0)

        preferred_time = None if task == "hard" else random.choice(["morning", "afternoon"])

        return {
            "calendar": calendar,
            "request": {
                "duration": 60,
                "preferred_time": preferred_time,
                "priority": random.choice(["low", "medium", "high"]),
                "timezone": random.choice(["IST", "UTC", "PST"])
            },
            "preferences": {
                "work_hours": "9-18",
                "no_meetings_after": "18:00",
                "avoid_conflicts": True
            },
            "history": [],
            "current_time": "09:00"
        }

    # -------------------------
    # REWARD FUNCTION
    # -------------------------
    def _compute_reward(self, action: Action):
        score = 0.0
        breakdown = {}

        # Missing info handling
        if self.state_data["request"]["preferred_time"] is None:
            if action.decision == "ask":
                score += 0.25
                breakdown["handled_uncertainty"] = 0.25
            else:
                score -= 0.3
                breakdown["ignored_uncertainty"] = -0.3

        # Conflict check
        conflict = any(
            e["start"] == action.proposed_time
            for e in self.state_data["calendar"]
            if action.proposed_time
        )

        if conflict:
            score -= 0.4
            breakdown["conflict_penalty"] = -0.4
        else:
            score += 0.25
            breakdown["valid_slot"] = 0.25

        # Preference alignment
        pref = self.state_data["request"]["preferred_time"]
        if pref == "morning" and action.proposed_time:
            if int(action.proposed_time[:2]) < 12:
                score += 0.15
                breakdown["preference_match"] = 0.15

        # Priority handling
        if self.state_data["request"]["priority"] == "high":
            score += 0.15
            breakdown["priority_bonus"] = 0.15

        # Communication quality
        if len(action.message) > 20:
            score += 0.2
            breakdown["good_communication"] = 0.2
        else:
            score -= 0.15
            breakdown["poor_communication"] = -0.15

        # Explanation (separate field)
        explanation = "Agent evaluated scheduling constraints, uncertainty handling, and communication quality"

        return max(0.0, min(score, 1.0)), breakdown, explanation
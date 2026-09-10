import random
import pandas as pd
import joblib

random.seed(42)

MODEL_FILE = "event_recommender.pkl"
OUTPUT_FILE = "events_100.csv"

print("Loading model...")

model = joblib.load(MODEL_FILE)
SKILLS = list(model.skill_encoder.classes_)
INTERESTS = list(model.interest_encoder.classes_)
EVENT_TYPES = list(model.event_type_encoder.classes_)
MODES = list(model.mode_encoder.categories_[0])

print(f"Skills: {len(SKILLS)}")
print(f"Interests: {len(INTERESTS)}")
print(f"Event types: {len(EVENT_TYPES)}")
print(f"Modes: {len(MODES)}")

events = []

for i in range(1, 101):

    event_type = random.choice(EVENT_TYPES)
    mode = random.choice(MODES)

    skills = random.sample(
        SKILLS,
        random.randint(2, 4)
    )

    interests = random.sample(
        INTERESTS,
        random.randint(2, 4)
    )
    main_interest = random.choice(interests)

    events.append({
        "event_id": i,
        "event_name": f"{main_interest} {event_type} {i}",
        "skills": ", ".join(skills),
        "interests": ", ".join(interests),
        "event_type": event_type,
        "mode": mode
    })

df = pd.DataFrame(events)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Successfully generated 100 events.")
print()
print(df.head(10).to_string(index=False))
print()
print(f"Saved to: {OUTPUT_FILE}")
import pandas as pd
import joblib

print("Loading model...")

model = joblib.load("event_recommender.pkl")

print("Loading events...")

events = pd.read_csv("events_100.csv")

print(f"Loaded {len(events)} events.")

print("\nTesting recommendation...")
user_id = model.users.iloc[0]["user_id"]

print(f"\nTest User ID: {user_id}")

user = model.users[
    model.users["user_id"] == user_id
].iloc[0]

print("\nUSER PROFILE")
print("Skills:", user["skills"])
print("Interests:", user["interests"])
print("Event Type:", user["preferred_event_type"])
print("Mode:", user["preferred_mode"])

print("\nRECOMMENDATIONS")
print("=" * 80)

recommendations = model.recommend(
    user_id=user_id,
    events=events,
    top_n=10
)

print(
    recommendations[
        [
            "event_id",
            "event_name",
            "skills",
            "interests",
            "event_type",
            "mode",
            "recommendation_score"
        ]
    ].to_string(index=False)
)
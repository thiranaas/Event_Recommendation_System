import pandas as pd
from pathlib import Path

from recommender import EventRecommender

BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "event_recommender.pkl"
EVENT_FILE = BASE_DIR / "events_test.csv"

print("Loading trained model...")

model = EventRecommender.load(
    MODEL_FILE
)

print("Model loaded successfully.")

print("\nLoading events...")

events = pd.read_csv(
    EVENT_FILE
)

print(
    f"Loaded {len(events)} events."
)

user_ids = [
    "U001",
    "U002",
    "U003"
]

for user_id in user_ids:

    print("\n")
    print("=" * 70)

    print(
        f"RECOMMENDATIONS FOR {user_id}"
    )

    print("=" * 70)

    user = model.users[
        model.users["user_id"] == user_id
    ]

    print("\nUser Profile:")

    print(
        user[
            [
                "user_id",
                "skills",
                "interests",
                "preferred_event_type",
                "preferred_mode",
                "cluster"
            ]
        ].to_string(index=False)
    )

    recommendations = model.recommend(
        user_id=user_id,
        events=events,
        top_n=20
    )

    print("\nTop Recommendations:")

    print(
        recommendations[
            [
                "event_id",
                "event_name",
                "event_type",
                "mode",
                "recommendation_score"
            ]
        ].to_string(index=False)
    )
'''

user_exists = (
    model.users["user_id"] == user_id
).any()

if not user_exists:

    print(
        f"User {user_id} not found."
    )

    print("\nAvailable users:")

    print(
        model.users[
            "user_id"
        ].head(20).to_list()
    )

    exit()

print(
    f"\nGenerating recommendations for {user_id}..."
)

recommendations = model.recommend(
    user_id=user_id,
    events=events,
    top_n=20
)

print("\n")
print("=" * 70)

print(
    f"TOP 20 EVENT RECOMMENDATIONS FOR {user_id}"
)

print("=" * 70)


print(
    recommendations[
        [
            "event_id",
            "event_name",
            "event_type",
            "mode",
            "recommendation_score"
        ]
    ].to_string(index=False)
)
'''
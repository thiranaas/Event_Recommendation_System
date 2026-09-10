from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommender import EventRecommender


BASE_DIR = Path(__file__).resolve().parent

MODEL_FILE = BASE_DIR / "event_recommender.pkl"

model = EventRecommender.load(MODEL_FILE)

def to_list(value):
    """
    Convert different input formats into a clean list.

    Examples:

    ["Python", "Docker"]
        -> ["Python", "Docker"]

    "Python, Docker"
        -> ["Python", "Docker"]

    None
        -> []
    """

    if value is None:
        return []

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str):
        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return []


def get_value(data, *keys, default=None):
    """
    Return the first existing value from multiple possible keys.
    """

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return default

def get_recommendations_from_profile(
    user_profile,
    events_df,
    top_n=20
):
    """
    Generate recommendations for a real user profile.

    This does NOT require the real database user ID
    to exist inside the training dataset.
    """

    if not isinstance(user_profile, dict):
        raise ValueError(
            "user must be an object"
        )

    if not isinstance(events_df, pd.DataFrame):
        raise ValueError(
            "events must be a pandas DataFrame"
        )

    skills = to_list(
        get_value(
            user_profile,
            "skills",
            default=[]
        )
    )

    interests = to_list(
        get_value(
            user_profile,
            "interests",
            default=[]
        )
    )

    event_types = to_list(
        get_value(
            user_profile,
            "preferred_event_type",
            "preferredEventType",
            "event_type",
            "eventType",
            default=[]
        )
    )

    mode = get_value(
        user_profile,
        "preferred_mode",
        "preferredMode",
        "mode",
        default=""
    )

    mode = str(mode).strip()

    user_data = {
        "user_id": "REAL_USER",

        "skills": ", ".join(skills),

        "interests": ", ".join(interests),

        "preferred_event_type": ", ".join(
            event_types
        ),

        "preferred_mode": mode
    }

    user_df = pd.DataFrame([user_data])

    user_vector = model.encode_single_user(
        user_data
    )

    user_vector = np.asarray(
        user_vector,
        dtype=float
    )

    if user_vector.ndim == 1:
        user_vector = user_vector.reshape(
            1,
            -1
        )

    required_columns = [
        "event_id",
        "event_name",
        "skills",
        "interests",
        "event_type",
        "mode"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in events_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing event columns: "
            + ", ".join(missing_columns)
        )

    events = events_df.copy()

    for column in [
        "skills",
        "interests",
        "event_type",
        "mode"
    ]:
        events[column] = events[column].fillna("").astype(str)

    event_vectors = model.encode_events(
        events
    )

    event_vectors = np.asarray(
        event_vectors,
        dtype=float
    )

    if event_vectors.ndim == 1:
        event_vectors = event_vectors.reshape(
            1,
            -1
        )

    similarities = cosine_similarity(
        user_vector,
        event_vectors
    )[0]

    events["recommendation_score"] = (
        similarities
    )

    events = events.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return events.head(
        int(top_n)
    ).reset_index(
        drop=True
    )
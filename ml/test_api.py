import pandas as pd

from recommend_api import get_recommendations
events = pd.read_csv(
    "events_test.csv"
)
user_id = "U001"
recommendations = get_recommendations(
    user_id=user_id,
    events_df=events,
    top_n=20
)
print("\nTOP 20 RECOMMENDATIONS")
print("=" * 60)

print(
    recommendations.to_string(
        index=False
    )
)
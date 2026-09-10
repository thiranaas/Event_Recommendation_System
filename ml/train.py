import pandas as pd

from recommender import EventRecommender

USER_FILE = "college_students_synthetic_dataset.csv"

MODEL_FILE = "event_recommender.pkl"

print("Loading user dataset...")

users = pd.read_csv(USER_FILE)

print(f"Loaded {len(users)} users.")

recommender = EventRecommender()

print("\nEncoding user features...")

recommender.prepare_users(users)

print("\nFinding optimal number of clusters...")

optimal_k = recommender.elbow_method(
    min_k=2,
    max_k=10,
    show_plot=True
)

print(
    f"\nOptimal K selected: {optimal_k}"
)

print("\nTraining K-Means...")

recommender.train(
    k=optimal_k
)

print("\nSample cluster assignments:")

print(
    recommender.users[
        ["user_id", "cluster"]
    ].head(20)
)

recommender.save(
    MODEL_FILE
)

print(
    "\nTraining completed!"
)

print(
    f"Model saved as: {MODEL_FILE}"
)
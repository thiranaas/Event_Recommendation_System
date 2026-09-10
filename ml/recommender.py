import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

USER_FILE = "college_students_synthetic_dataset.csv"

TOP_N = 20
SKILL_WEIGHT = 1.5
INTEREST_WEIGHT = 1.5
EVENT_TYPE_WEIGHT = 1.2
MODE_WEIGHT = 0.8

def split_values(value):
    """
    Convert:
        'Python, Machine Learning, SQL'

    into:
        ['Python', 'Machine Learning', 'SQL']
    """

    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]

class EventRecommender:

    def __init__(self):
        self.skill_encoder = MultiLabelBinarizer()
        self.interest_encoder = MultiLabelBinarizer()
        self.event_type_encoder = MultiLabelBinarizer()

        self.mode_encoder = OneHotEncoder(
            sparse_output=False,
            handle_unknown="ignore"
        )
        self.kmeans = None
        self.users = None
        self.user_features = None
        self.optimal_k = None

    def encode_users(self, users):
        skills = users["skills"].apply(split_values)

        interests = users["interests"].apply(split_values)

        event_types = users["preferred_event_type"].apply(
            split_values
        )

        skill_matrix = self.skill_encoder.fit_transform(
            skills
        ).astype(float)

        interest_matrix = self.interest_encoder.fit_transform(
            interests
        ).astype(float)

        event_type_matrix = self.event_type_encoder.fit_transform(
            event_types
        ).astype(float)

        mode_matrix = self.mode_encoder.fit_transform(
            users[["preferred_mode"]]
        ).astype(float)

        skill_matrix *= SKILL_WEIGHT

        interest_matrix *= INTEREST_WEIGHT

        event_type_matrix *= EVENT_TYPE_WEIGHT

        mode_matrix *= MODE_WEIGHT

        X = np.hstack([
            skill_matrix,
            interest_matrix,
            event_type_matrix,
            mode_matrix
        ])

        return X

    def prepare_users(self, users):

        required_columns = [
            "user_id",
            "skills",
            "interests",
            "preferred_event_type",
            "preferred_mode"
        ]
        missing = [
            column
            for column in required_columns
            if column not in users.columns
        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )
        self.users = users.copy()
        self.user_features = self.encode_users(
            self.users
        )

        print(
            f"User feature matrix shape: "
            f"{self.user_features.shape}"
        )

    def elbow_method(
        self,
        min_k=2,
        max_k=10,
        show_plot=True
    ):

        if self.user_features is None:
            raise ValueError(
                "Prepare users before running elbow method."
            )
        max_k = min(
            max_k,
            len(self.users) - 1
        )

        k_values = range(
            min_k,
            max_k + 1
        )

        inertias = []

        for k in k_values:

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=20
            )

            model.fit(self.user_features)

            inertias.append(
                model.inertia_
            )

        suggested_k = self._find_elbow(
            list(k_values),
            inertias
        )

        if show_plot:

            plt.figure(figsize=(8, 5))

            plt.plot(
                list(k_values),
                inertias,
                marker="o"
            )

            plt.axvline(
                suggested_k,
                linestyle="--"
            )

            plt.xlabel(
                "Number of Clusters (K)"
            )

            plt.ylabel(
                "Inertia"
            )

            plt.title(
                "Elbow Method for K-Means"
            )

            plt.xticks(
                list(k_values)
            )

            plt.grid(True)

            plt.show()

        print(
            f"Suggested number of clusters: {suggested_k}"
        )

        return suggested_k

    def _find_elbow(self, k_values, inertias):

        """
        Finds the point farthest from the line
        connecting the first and last points.
        """

        x = np.array(k_values, dtype=float)

        y = np.array(inertias, dtype=float)
        x_norm = (
            (x - x.min()) /
            (x.max() - x.min())
        )

        y_norm = (
            (y - y.min()) /
            (y.max() - y.min())
        )
        p1 = np.array([
            x_norm[0],
            y_norm[0]
        ])

        p2 = np.array([
            x_norm[-1],
            y_norm[-1]
        ])

        distances = []

        for i in range(len(x_norm)):

            p = np.array([
                x_norm[i],
                y_norm[i]
            ])

            distance = np.abs(
                np.cross(
                    p2 - p1,
                    p - p1
                )
            ) / np.linalg.norm(
                p2 - p1
            )

            distances.append(distance)

        elbow_index = np.argmax(
            distances
        )

        return k_values[elbow_index]

    def train(self, k=None):

        if self.user_features is None:

            raise ValueError(
                "Prepare users first."
            )
        if k is None:

            k = self.elbow_method()

        self.optimal_k = k

        print(
            f"Training K-Means with K = {k}"
        )

        self.kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20
        )

        clusters = self.kmeans.fit_predict(
            self.user_features
        )

        self.users["cluster"] = clusters

        print("\nCluster distribution:")

        print(
            self.users["cluster"]
            .value_counts()
            .sort_index()
        )

        return self.users

    def encode_single_user(self, user):

        skills = [
            split_values(
                user.get("skills", "")
            )
        ]

        interests = [
            split_values(
                user.get("interests", "")
            )
        ]

        event_types = [
            split_values(
                user.get(
                    "preferred_event_type",
                    ""
                )
            )
        ]

        mode = pd.DataFrame({
            "preferred_mode": [
                user.get(
                    "preferred_mode",
                    ""
                )
            ]
        })

        skill_matrix = self._safe_transform(
            self.skill_encoder,
            skills
        )

        interest_matrix = self._safe_transform(
            self.interest_encoder,
            interests
        )

        event_type_matrix = self._safe_transform(
            self.event_type_encoder,
            event_types
        )

        mode_matrix = self.mode_encoder.transform(
            mode
        )

        skill_matrix = (
            skill_matrix *
            SKILL_WEIGHT
        )

        interest_matrix = (
            interest_matrix *
            INTEREST_WEIGHT
        )

        event_type_matrix = (
            event_type_matrix *
            EVENT_TYPE_WEIGHT
        )

        mode_matrix = (
            mode_matrix *
            MODE_WEIGHT
        )

        X = np.hstack([
            skill_matrix,
            interest_matrix,
            event_type_matrix,
            mode_matrix
        ])

        return X.astype(float)

    def _safe_transform(
        self,
        encoder,
        values
    ):

        """
        MultiLabelBinarizer normally throws an error
        for unseen labels.

        This function ignores new/unknown labels.
        """

        known_classes = set(
            encoder.classes_
        )

        cleaned_values = []

        for value_list in values:

            cleaned_values.append([
                value
                for value in value_list
                if value in known_classes
            ])

        return encoder.transform(
            cleaned_values
        ).astype(float)
    def encode_events(self, events):

        required_columns = [
            "event_id",
            "event_name",
            "skills",
            "interests",
            "event_type",
            "mode"
        ]

        missing = [
            column
            for column in required_columns
            if column not in events.columns
        ]

        if missing:

            raise ValueError(
                f"Events table missing columns: "
                f"{missing}"
            )

        skills = events["skills"].apply(
            split_values
        )

        interests = events["interests"].apply(
            split_values
        )

        event_types = events["event_type"].apply(
            split_values
        )
        skill_matrix = self._safe_transform(
            self.skill_encoder,
            skills
        )

        interest_matrix = self._safe_transform(
            self.interest_encoder,
            interests
        )

        event_type_matrix = self._safe_transform(self.event_type_encoder,event_types)
        event_mode = events[["mode"]].rename(columns={"mode": "preferred_mode"})
        mode_matrix = self.mode_encoder.transform(event_mode).astype(float)

        skill_matrix *= SKILL_WEIGHT

        interest_matrix *= INTEREST_WEIGHT

        event_type_matrix *= EVENT_TYPE_WEIGHT

        mode_matrix *= MODE_WEIGHT
        X_events = np.hstack([
            skill_matrix,
            interest_matrix,
            event_type_matrix,
            mode_matrix
        ])

        return X_events.astype(float)

    def recommend(
        self,
        user_id,
        events,
        top_n=20
    ):

        if self.kmeans is None:

            raise ValueError(
                "Train the model first."
            )

        if events.empty:

            return pd.DataFrame()

        user_rows = self.users[
            self.users["user_id"] == user_id
        ]

        if user_rows.empty:

            raise ValueError(
                f"User '{user_id}' not found."
            )

        user_index = user_rows.index[0]

        user_vector = self.user_features[
            user_index
        ].reshape(1, -1)

        user_cluster = self.kmeans.predict(
            user_vector
        )[0]

        cluster_mask = (
            self.users["cluster"]
            == user_cluster
        )

        cluster_indices = (
            self.users.index[
                cluster_mask
            ]
        )

        cluster_features = (
            self.user_features[
                cluster_indices
            ]
        )

        cluster_profile = (
            cluster_features.mean(axis=0)
            .reshape(1, -1)
        )

        event_features = self.encode_events(
            events
        )

        user_similarity = cosine_similarity(
            user_vector,
            event_features
        )[0]

        cluster_similarity = cosine_similarity(
            cluster_profile,
            event_features
        )[0]

        final_score = (
            0.7 * user_similarity
            +
            0.3 * cluster_similarity
        )

        recommendations = events.copy()

        recommendations[
            "user_similarity"
        ] = user_similarity

        recommendations[
            "cluster_similarity"
        ] = cluster_similarity

        recommendations[
            "recommendation_score"
        ] = final_score

        recommendations = (
            recommendations
            .sort_values(
                "recommendation_score",
                ascending=False
            )
            .head(top_n)
            .reset_index(drop=True)
        )

        return recommendations

    def save(self, filename="event_recommender.pkl"):

        joblib.dump(
            self,
            filename
        )

        print(
            f"Model saved to {filename}"
        )

    @staticmethod
    def load(
        filename="event_recommender.pkl"
    ):

        model = joblib.load(
            filename
        )

        print(
            f"Model loaded from {filename}"
        )

        return model



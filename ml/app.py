from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from recommend_api import get_recommendations_from_profile

app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.post("/recommend")
def recommend():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        user = data.get("user")
        events = data.get("events")

        if user is None:
            return jsonify({
                "success": False,
                "error": "user is required"
            }), 400

        if not isinstance(events, list):
            return jsonify({
                "success": False,
                "error": "events must be a list"
            }), 400
        if len(events) == 0:
            return jsonify({
                "success": True,
                "data": []
            }), 200

        events_df = pd.DataFrame(events)

        top_n = data.get("top_n", 20)

        try:
            top_n = int(top_n)
        except (TypeError, ValueError):
            top_n = 20

        if top_n <= 0:
            top_n = 20

        recommendations = get_recommendations_from_profile(
            user_profile=user,
            events_df=events_df,
            top_n=top_n
        )

        return jsonify({
            "success": True,
            "data": recommendations.to_dict(
                orient="records"
            )
        }), 200

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )
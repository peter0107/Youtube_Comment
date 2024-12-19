from flask import Flask, request
from flask_cors import CORS
from rest import getSummary
import json


app = Flask(__name__)
CORS(app)

@app.route("/api/summary", methods=["GET"])
def summary():
    video_id = request.args.get("id")
    keywords, summary = getSummary(video_id)
    result = None
    if keywords:    
        result  = {
            "status": True,
            "clusterN": len(keywords),
            "clusters": keywords,
            "summary": summary
        }
        result = json.dumps(result)
    else:
        result = json.dumps({"status": False})

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

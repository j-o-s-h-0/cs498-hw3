from flask import Flask, request, jsonify
from pymongo import MongoClient, WriteConcern, ReadPreference

app = Flask(__name__)
client = MongoClient("mongodb+srv://joshuan9_db_user:Bpao9jMFnMIKewQe@ev-cluster.ifxfrdf.mongodb.net/?appName=EV-cluster")
db = client["ev_db"]
collection = db["vehicles"]

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
  data = request.get_json()
  result = collection.with_options(write_concern=WriteConcern(w=1)).insert_one(data)
  return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
  data = request.get_json()
  result = collection.with_options(write_concern=WriteConcern("majority")).insert_one(data)
  return jsonify({"inserted_id": str(result.inserted_id)})

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
  total_count = collection.with_options(read_preference=ReadPreference.PRIMARY).count_documents({"Make": "TESLA"})
  return jsonify({"count": total_count})

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
  total_count = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED).count_documents({"Make": "BMW"})
  return jsonify({"count": total_count})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

"""Minimal Flask app for exploring spoonerisms in the browser."""

from pathlib import Path

from flask import Flask, jsonify, render_template, request

from spooner import spoon_details

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/spoon", methods=["POST"])
def api_spoon():
    data = request.get_json(silent=True) or {}
    phrase = (data.get("phrase") or "").strip()
    debug = bool(data.get("debug"))
    if not phrase:
        return jsonify({"error": "Please provide two words to swap."}), 400
    try:
        details = spoon_details(phrase, debug=debug)
    except ValueError as exc:  # from spooner utilities
        return jsonify({"error": str(exc)}), 400

    if not details.get("swapped_phonemes"):
        return jsonify({"error": "These words cannot form a spoonerism. Usually this means you entered a word that starts with a sound that cannot be swapped, or one or both words are not recognized."}), 400

    return jsonify(details)


if __name__ == "__main__":
    app.run(debug=True)

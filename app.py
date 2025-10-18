from flask import Flask, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

cached_note = "Note not cached yet."

@app.route("/")
def home():
    return "✅ Scrape Notes App is live."

@app.route("/scrape-and-cache")
def scrape_and_cache():
    global cached_note
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://davyhulme.intelligentgolf.co.uk/visitorbooking/", timeout=60000)
            page.wait_for_selector(".noteContent", timeout=15000)
            content = page.locator(".noteContent").inner_text()
            browser.close()
            cached_note = content.strip()
            return jsonify({"note": cached_note})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/cached")
def get_cached():
    return jsonify({"note": cached_note})

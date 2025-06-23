import os
import logging
import warnings
from config import Config
from flask import Flask
# Suppress warnings and noisy logs
warnings.filterwarnings("ignore")
logging.getLogger("nltk").setLevel(logging.ERROR)
logging.getLogger("google_adk").setLevel(logging.ERROR)
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

# Get Gemini model info from config
GEMINI_MODEL = getattr(Config, 'GEMINI_MODEL_NAME', 'unknown')
GEMINI_KEY = getattr(Config, 'GEMINI_API_KEY', None)
GEMINI_STATUS = "🔑 Set" if GEMINI_KEY and 'AIza' in GEMINI_KEY else "❌ Not Set"

# ADK status (will be updated by coordinator)
ADK_STATUS = "🟢 Enabled" if getattr(Config, 'USE_ADK_AGENTS', False) else "⚪ Disabled"
ADK_PROGRESS = "⏳ Initializing..." if getattr(Config, 'USE_ADK_AGENTS', False) else ""

# Exciting, emoji-rich startup banner with service callouts and status
print(f"""
🚀✈️  Flight Operations Disruption Management System ✈️🚀\n
Welcome to the next-generation, AI-powered airline disruption management and coordination platform!

✨ Key Services & Features:

🤖  Multi-Agent Orchestration: Crew, Rebooking, Maintenance, Airport, Communication
🧠  Gemini AI Integration: Smart decision support, natural language, analytics
📈  Business Metrics Engine: Real-time impact, ROI, customer satisfaction
🧪  Scenario Simulator: Realistic flight, disruption, and crisis simulation
🔗  Coordination Engine: Seamless agent collaboration for rapid response
📊  Live Dashboard: Real-time status, metrics, and scenario outcomes
🛠️  RESTful API: Integrate, automate, and extend with ease
🧑‍💻  ADK Agents: Advanced, modular, and ready for experimentation

---
🧠 Gemini Model: {GEMINI_MODEL}   |   API Key: {GEMINI_STATUS}
🧑‍💻 ADK Agents: {ADK_STATUS}   {ADK_PROGRESS}
---

🌐  Web UI: http://127.0.0.1:5000
📊  API docs: See README.md for endpoints
🧑‍💻  Need help? Reach out to the system architect or check the README

Initializing system... Please wait! 🛫
""")

# Configure logging using config
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))

# Create the Flask app directly
app = Flask(__name__)

# Import routes and initialize agent coordinator
from routes import init_app

with app.app_context():
    # Initialize agent coordinator and specialized agents
    init_app(app)

print("Starting app.py...")

if __name__ == '__main__':
    print("About to run Flask app...")
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 
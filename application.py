import os
import requests
import unicodedata
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from utils import get_force_content, get_relevant_context
from huggingface_hub import InferenceClient

# Charger .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("La variable d’environnement HF_TOKEN n’est pas définie.")

client = InferenceClient(token=HF_TOKEN)

app = Flask(__name__)
CORS(app)

# Charger contenu une fois au démarrage
full_text = get_force_content()

INSCRIPTION_URL = "https://forcen.jotform.com/form/231154488427359"

def ask_force_n_bot(message, context_text):
    system_prompt = (
        "Tu es AWA, la voix officielle du programme FORCE-N. "
        "Sois institutionnelle, claire, sans inventer. "
        "Réponds uniquement à partir des informations suivantes :\n\n"
        f"{context_text}\n\n"
        "Si l’information n’est pas présente, dis : "
        "'Je suis désolée, je n’ai pas cette information, veuillez reformuler votre question s'il vous plaît.'"
    )

    if "inscription" in message.lower() or "s'inscrire" in message.lower():
        return (
            "Pour t'inscrire aux formations de FORCE-N, merci de remplir ce formulaire officiel :\n"
            f"{INSCRIPTION_URL}\n\n"
            "Tu y trouveras toutes les informations nécessaires à ta pré-candidature."
        )

    try:
        response = client.chat_completion(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("[Erreur chatbot]", e)
        return "Une erreur est survenue, merci de reformuler votre question."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "Message manquant"}), 400

    context = get_relevant_context(user_message, full_text)
    response = ask_force_n_bot(user_message, context)
    return jsonify({"response": response})

@app.route("/")
def home():
    return send_file("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


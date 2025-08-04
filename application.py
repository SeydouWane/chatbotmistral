import os
import requests
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

# Client HF
client = InferenceClient(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    token=HF_TOKEN
)

app = Flask(__name__)
CORS(app)

# Contenu utilisé pour construire le contexte (optionnel si utilisé)
full_text = get_force_content()

INSCRIPTION_URL = "https://forcen.jotform.com/form/231154488427359"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    return data
    if not data or "message" not in data:
        return jsonify({"error": "Message manquant"}), 400

    question = data["message"].strip()

    # Redirection spéciale : lien d’inscription
    if "inscription" in question.lower() or "s'inscrire" in question.lower():
        return jsonify({
            "response": (
                "Pour t'inscrire aux formations de FORCE-N, merci de remplir ce formulaire officiel :\n"
                f"{INSCRIPTION_URL}\n\n"
                "Tu y trouveras toutes les informations nécessaires à ta pré-candidature."
            )
        })

    # Ajouter contexte (optionnel)
    context = get_relevant_context(question, full_text)

    prompt = (
        f"<s>[INST] Tu es AWA, la voix officielle du programme FORCE-N. "
        f"Réponds de manière institutionnelle et claire uniquement à partir du contexte suivant :\n\n"
        f"{context}\n\n"
        f"Question : {question} [/INST]"
    )

    try:
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
        )
        return jsonify({"response": response})
    except Exception as e:
        print("[Erreur chatbot]", e)
        return jsonify({"response": "Une erreur est survenue, merci de reformuler votre question."})

@app.route("/")
def home():
    return send_file("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host=127.0.0.1, port=port)

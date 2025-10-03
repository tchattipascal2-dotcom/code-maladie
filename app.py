import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# Vérifie que la clé OpenAI est définie
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("La variable d'environnement OPENAI_API_KEY n'est pas définie !")

# Création du client OpenAI
client = OpenAI(api_key=API_KEY)

# Création de l'application Flask
app = Flask(__name__)

def structured_request(user_input: str) -> str:
    """
    Demande au modèle de répondre uniquement dans le format 'code : maladie' ou 'maladie : code'.
    Convertit automatiquement les lettres en majuscules pour les codes.
    """
    # Convertir en majuscules si c'est un code (commence par une lettre)
    if user_input and user_input[0].isalpha():
        user_input = user_input.upper()
    
    system_message = (
        "Tu es un assistant spécialisé en codes médicaux et maladies. "
        "Réponds strictement dans le format 'code : maladie' ou 'maladie : code'. "
        "Ne donne pas d'explications supplémentaires. "
        "Pour les codes médicaux, utilise toujours des lettres majuscules."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erreur API : {e}"

# Page HTML
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint AJAX
@app.route("/api/lookup", methods=["POST"])
def lookup():
    data = request.json
    user_input = data.get("query", "").strip()
    
    # Conversion automatique en majuscules pour les codes
    if user_input and user_input[0].isalpha() and any(c.isdigit() for c in user_input):
        user_input = user_input.upper()
    
    result = structured_request(user_input)
    return jsonify({"result": result})

if __name__ == "__main__":
    print("Pour la production, lance run_prod.py avec Waitress.")

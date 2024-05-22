from flask import Flask, request, jsonify
import requests
import openai, os

app = Flask(__name__)

# Configurações da API OpenAI
openai.api_key = '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'

@app.route('/webhook', methods=['GET'])
def webhook():
    data = request.json
    lead_data = data.get('leads', [])[0]
    lead_name = lead_data.get('name')
    prompt = f"Analise a descrição do lead: {lead_name}"
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150
    )
    gpt_response = response.choices[0].text.strip()
    return jsonify({'suggestions': gpt_response})

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, render_template_string, request, jsonify
import requests

# Esta linha é a mais importante! O Render precisa deste nome 'app'
app = Flask(__name__)

API_KEY = 'AIzaSyBHJ6arSXoevvw5ru9Z3bw7zgdYaKdxymw'

def gemini_chat(pergunta):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": pergunta}]}]}
    try:
        res = requests.post(url, json=payload)
        return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "IA: Estou a pensar... tenta perguntar outra vez."

HTML = '''
<!DOCTYPE html>
<html>
<head><title>IA do Luis</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding:20px;">
    <h2>🤖 Assistente do Luis</h2>
    <div id="chat" style="height:300px; overflow:auto; background:#1e1e1e; padding:15px; border-radius:10px; text-align:left; margin-bottom:10px;"></div>
    <input type="text" id="msg" placeholder="Escreve aqui..." style="width:70%; padding:10px; border-radius:5px; border:none;">
    <button onclick="enviar()" style="padding:10px; background:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;">Enviar</button>
    <script>
        async function enviar(){
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            if(!i.value) return;
            c.innerHTML += "<div><b>Tu:</b> "+i.value+"</div>";
            let res = await fetch('/chat?msg='+encodeURIComponent(i.value));
            let data = await res.json();
            c.innerHTML += "<div style='color:#00ff00; margin-top:5px;'><b>IA:</b> "+data.res+"</div>";
            i.value = "";
            c.scrollTop = c.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    return jsonify({"res": gemini_chat(msg)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, render_template_string, request, jsonify
import g4f

app = Flask(__name__)

def chat_ia(pergunta):
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": pergunta}],
        )
        return response
    except Exception as e:
        return "IA: Tive um pequeno problema técnico... tenta perguntar outra vez!"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>IA do Luis</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding:20px;">
    <h2>🤖 Assistente do Luis (Versão B)</h2>
    <div id="chat" style="height:350px; overflow:auto; background:#1e1e1e; padding:15px; border-radius:10px; text-align:left; margin-bottom:10px; border: 1px solid #333;"></div>
    <input type="text" id="msg" placeholder="Escreve aqui..." style="width:70%; padding:12px; border-radius:5px; border:none; outline:none;">
    <button onclick="enviar()" style="padding:12px; background:#007bff; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">Enviar</button>
    <script>
        async function enviar(){
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            if(!i.value) return;
            let userMsg = i.value;
            c.innerHTML += "<div style='margin-bottom:10px;'><b>Tu:</b> "+userMsg+"</div>";
            i.value = "A processar...";
            i.disabled = true;
            
            try {
                let res = await fetch('/chat?msg='+encodeURIComponent(userMsg));
                let data = await res.json();
                c.innerHTML += "<div style='color:#00d4ff; margin-bottom:15px;'><b>IA:</b> "+data.res+"</div>";
            } catch(e) {
                c.innerHTML += "<div style='color:red;'>Erro ao ligar ao servidor.</div>";
            }
            
            i.value = "";
            i.disabled = false;
            i.focus();
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
    resposta = chat_ia(msg)
    return jsonify({"res": resposta})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, render_template_string, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

def perguntar_ia(texto):
    try:
        with DDGS() as ddgs:
            # Usando o modelo GPT-4o que é muito potente
            respostas = ddgs.chat(texto, model='gpt-4o-mini')
            return respostas
    except Exception as e:
        return "IA: Ocorreu um erro na ligação. Tenta perguntar outra vez em 5 segundos."

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IA do Luis</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding:20px;">
    <h2>🤖 Assistente do Luis</h2>
    <div id="chat" style="height:350px; overflow:auto; background:#1e1e1e; padding:15px; border-radius:10px; text-align:left; margin-bottom:10px; border:1px solid #333;"></div>
    <input type="text" id="msg" placeholder="Pergunta-me qualquer coisa..." style="width:70%; padding:12px; border-radius:5px; border:none; outline:none;">
    <button onclick="enviar()" style="padding:12px; background:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;">Enviar</button>

    <script>
        async function enviar(){
            let input = document.getElementById('msg');
            let chat = document.getElementById('chat');
            if(!input.value) return;

            let mensagemUsuario = input.value;
            chat.innerHTML += "<div style='margin-bottom:10px;'><b>Tu:</b> "+mensagemUsuario+"</div>";
            
            let aguarde = document.createElement("div");
            aguarde.innerHTML = "<b>IA:</b> A pensar...";
            aguarde.style.color = "#888";
            chat.appendChild(aguarde);
            
            input.value = "";
            chat.scrollTop = chat.scrollHeight;

            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(mensagemUsuario));
                let data = await res.json();
                aguarde.innerHTML = "<b>IA:</b> " + data.res;
                aguarde.style.color = "#00ff00";
            } catch(e) {
                aguarde.innerHTML = "<b>IA:</b> Erro ao conectar.";
            }
            chat.scrollTop = chat.scrollHeight;
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
    user_msg = request.args.get('msg')
    resposta = perguntar_ia(user_msg)
    return jsonify({"res": resposta})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, render_template_string, request, jsonify
import freeGPT
import asyncio

app = Flask(__name__)

# Função para falar com a IA usando o Plano C
async def pedir_ia(pergunta):
    try:
        resp = await getattr(freeGPT, "gpt3").Completion.create(pergunta)
        return resp
    except:
        return "IA: Estou a tentar ligar os motores... tenta perguntar outra vez agora!"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>IA do Luis</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding:20px;">
    <h2>🤖 Assistente do Luis</h2>
    <div id="chat" style="height:350px; overflow:auto; background:#1e1e1e; padding:15px; border-radius:10px; text-align:left; margin-bottom:10px; border:1px solid #333;"></div>
    <input type="text" id="msg" placeholder="Escreve aqui..." style="width:70%; padding:12px; border-radius:5px; border:none;">
    <button onclick="enviar()" style="padding:12px; background:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;">Enviar</button>
    <script>
        async function enviar(){
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            if(!i.value) return;
            let m = i.value;
            c.innerHTML += "<div><b>Tu:</b> "+m+"</div>";
            i.value = "A responder...";
            let res = await fetch('/chat?msg='+encodeURIComponent(m));
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
    # Corre o código assíncrono para a IA responder
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    resposta = loop.run_until_complete(pedir_ia(msg))
    return jsonify({"res": resposta})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

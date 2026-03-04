import os
from flask import Flask, render_template_string, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

def perguntar_ia(texto):
    try:
        with DDGS() as ddgs:
            # Modelo estável e rápido
            respostas = ddgs.chat(texto, model='gpt-4o-mini')
            return respostas
    except:
        return "IA: Estou a processar... tenta novamente!"

HTML = '''
<!DOCTYPE html>
<html>
<head><title>IA do Luis</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding:20px;">
    <h2>🤖 Assistente do Luis</h2>
    <div id="chat" style="height:300px; overflow:auto; background:#1e1e1e; padding:15px; border-radius:10px; text-align:left; margin-bottom:10px; border:1px solid #333;"></div>
    <input type="text" id="msg" placeholder="Escreve aqui..." style="width:70%; padding:10px; border-radius:5px; border:none;">
    <button onclick="enviar()" style="padding:10px; background:#28a745; color:white; border:none; border-radius:5px;">Enviar</button>
    <script>
        async function enviar(){
            let i = document.getElementById('msg');
            let c = document.getElementById('chat');
            if(!i.value) return;
            let m = i.value;
            c.innerHTML += "<div><b>Tu:</b> "+m+"</div>";
            i.value = "A pensar...";
            let res = await fetch('/chat?msg='+encodeURIComponent(m));
            let data = await res.json();
            c.innerHTML += "<div style='color:#00ff00;'><b>IA:</b> "+data.res+"</div>";
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
    return jsonify({"res": perguntar_ia(msg)})

if __name__ == '__main__':
    # ESTA PARTE É O QUE RESOLVE O ERRO DA PORTA
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

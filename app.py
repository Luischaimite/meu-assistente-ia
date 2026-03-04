def falar_com_gemini(pergunta):
    # Mudámos para v1 e gemini-1.5-flash que é mais moderno
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY_GEMINI}"
    
    payload = {"contents": [{"parts": [{"text": pergunta}]}]}
    
    try:
        res = requests.post(url, json=payload)
        data = res.json()
        
        # Se o Google devolver um erro, ele vai aparecer no chat
        if 'error' in data:
            return f"Erro do Google: {data['error']['message']}"
            
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Erro técnico: {str(e)}"

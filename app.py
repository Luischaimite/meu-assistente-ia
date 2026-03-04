def chat_ia(pergunta):
    try:
        # Mudamos para o modelo 'gpt-4o' ou 'claude' que costumam ser mais estáveis no g4f
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=[{"role": "user", "content": pergunta}],
            provider=g4f.Provider.ChatGptEs, # Forçamos um provedor específico
        )
        return response
    except Exception as e:
        # Se falhar o primeiro, ele tenta um plano de reserva automático
        try:
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": pergunta}],
            )
            return response
        except:
            return "IA: Estou a processar muita informação... tenta escrever 'Olá' novamente em 10 segundos!"

from flask import Flask, request, jsonify

from bot.aibot import AIBot
from services.waha import Waha


app = Flask(__name__)

user_interactions = {}

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    print(f'EVENTO RECEBIDO: {data}')

    waha = Waha()
    aibot = AIBot()

    chat_id = data['payload']['from']
    received_message = data['payload']['body']

    # Verifica se é a primeira interação
    if chat_id not in user_interactions:
        # Marcar o usuário como já interagido
        user_interactions[chat_id] = True

        # Enviar mensagem de boas-vindas
        waha.send_message(
            chat_id=chat_id,
            message="Bem-vindo(a)! Sou o TurisBot e estou aqui para ajudá-lo a conhecer melhor a cidade de São Luís."
        )

    waha.start_typing(chat_id=chat_id)

    response = aibot.invoke(question=received_message)

    waha.send_message(
        chat_id=chat_id,
        message=response,
    )

    waha.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

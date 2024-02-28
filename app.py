from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import Practo_Scrap
import GeminiAI

app = Flask(__name__)
socketio = SocketIO(app, ping_interval=50, cors_allowed_origins='*')


@socketio.on('connect')
def handle_connect():
    sid = request.sid
    print(f"Client {sid} connected")

    emit('receive_sid', {'message': sid}, to=sid)


@socketio.on('practo_scrap')
def handle_practo_scrap_message(received_message):
    sid = received_message['sid']
    loc_cat = received_message['message']
    location = loc_cat['location']
    category = loc_cat['category']
    scraped_data = Practo_Scrap.Scrap(location, category)  # Practo Scraping
    emit('receive_message', {'message': scraped_data}, to=sid)
    print(f"MESSAGE:\n{scraped_data}\nSent to Client {sid}")


@socketio.on('appointment_info')
def handle_appointment_info_message(received_message):
    sid = received_message['sid']
    appointment_info = "To book an appointment with the registered doctors on Prognosify,\nFollow these simple steps:\n- Go to your profile and click on one of the predicted potential disease.\n- Then scroll down until you find the symptoms of that disease.\n- If you actually suffer most of the symtpoms described there, go ahead with booking an appointment by clicking on the button."
    emit('receive_message', {'message': appointment_info}, to=sid)
    print(f"MESSAGE:\n{appointment_info}\nSent to Client {sid}")


@socketio.on('ask_gemini')
def handle_ask_gemini_message(received_message):
    sid = received_message['sid']
    query = received_message['message']
    answer = GeminiAI.Ask_Gemini(query)
    emit('receive_message', {'message': answer}, to=sid)
    print(f"MESSAGE:\n{answer}\nSent to Client {sid}")


@socketio.on('inform_patient')
def handle_inform_patient_message(received_message):
    info = received_message['message']
    sid = received_message['sid']
    socketio.emit('receive_message', {'message': info}, to=sid)
    print(f"MESSAGE:\n{info}\nSent to Client {sid}")


if __name__ == '__main__':
    socketio.run(app, debug=True)

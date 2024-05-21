import gradio
from memory.core import Process
from memory.utils.sql import SQL
from config import globals

MESSAGES = []
MEMORIES = ''
CHAT = gradio.Chatbot()
INPUT = gradio.Textbox()
LOG = gradio.Textbox()

def get_history():
    sql = SQL(f'{globals.user}.db')
    history = sql.get_history(30)
    message_array = []
    for message in history:
        message_array.append(message['content'])
    for i in range(0, len(message_array)-1, 2):
        MESSAGES.append((message_array[i], message_array[i+1]))
    return MESSAGES

def submit_messages(user_message):
    global MESSAGES
    global MEMORIES
    chat = Process()
    agent_message, memory = chat.run(user_message)
    MESSAGES.append((user_message, agent_message))
    MEMORIES = memory or ''
    print(MEMORIES)
    return gradio.Chatbot(value=MESSAGES), gradio.Textbox(value=MEMORIES)

def render():
    global CHAT
    global INPUT
    global LOG
    get_history()
    with gradio.Column(elem_classes='chat-container'):
        CHAT = gradio.Chatbot(value=MESSAGES)
        INPUT = gradio.Textbox(show_label=False, placeholder='input message', container=False)
        LOG = gradio.Textbox(label='memories', container=False)

def listen():
    INPUT.submit(fn=submit_messages, inputs=INPUT, outputs=[CHAT, LOG])
    INPUT.submit(fn=lambda: '', inputs=None, outputs=INPUT)
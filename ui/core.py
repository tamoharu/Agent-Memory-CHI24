import gradio
from ui.components import chat

css = '''
.chat-container {
    overflow-y: hidden; !important
    height: 100vh;
}
'''

def listen():
    chat.listen()

def render() -> gradio.Blocks:
    with gradio.Blocks(fill_height=True) as ui:
        chat.render()
        listen()
    return ui

def launch():
    render().launch()
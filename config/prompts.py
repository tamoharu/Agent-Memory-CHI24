from config import globals

prompt =\
'''
{history}
{memories}
'''
def get_prompt(history, memories):
    return prompt.format(history=history, memories=memories)
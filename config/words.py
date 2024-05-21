WORDS = {
'init_log': 'Time: {time}\nCount: {count}',
'user_input': 'User Input: {input}',
'added_data': 'Added {role} Data: {data}',
'history': 'History:\n{history}',
'fired_memory': 'Fired Memory:\n{memories}',
'prompt': 'Prompt:\n{prompt}',
'agent_output': 'Agent Output:\n{response}',
}

def get(key, **kwargs):
    template = WORDS.get(key, '')
    return template.format(**kwargs)
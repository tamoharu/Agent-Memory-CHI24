import numpy
import datetime
from config import globals, parameters, words
from config.prompts import get_prompt
from memory.utils.memory_model import MemoryModel
from memory.utils.faiss import Faiss
from memory.utils.sql import SQL
from memory.utils.request import Request
from memory.utils.log import Log


class Process:
    def __init__(self):
        self.memory = MemoryModel()
        self.faiss = Faiss(dimension=1536, index_path=f'{globals.user}.index')
        self.sql = SQL(f'{globals.user}.db')
        self.request = Request()
        self.log = Log(log_level=globals.log_level, log_path=f'{globals.user}.log')
        self.count: int = self.sql.get_last_id() + 1 if self.sql.get_last_id() is not None else 0
        self.current_time: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.log.info(words.get('init_log', time=self.current_time, count=self.count))

    def run(self, input: str) -> tuple:
        self.log.info(words.get('user_input', input=input))
        user_data = self._prepare_data('user', input)
        history, memories = self._prepare_memory(user_data)
        prompt = self._prepare_prompt(input=input, history=history, memories=memories)
        response = self.request.agent(prompt)
        self.log.info(words.get('agent_output', response=response))
        self._prepare_data('assistant', response)
        return response, memories
    
    def _recall_memory(self, data: dict) -> dict | None:
        results = self.faiss.search_embeddings(query_vector=data['vector'], threshold=parameters.cos_th, exclude_ids=[data['id']])
        max_p = 0
        fired_memory = None
        for result in results:
            id, distance = result
            memory = self.sql.get_data_by_index(id)
            g = self.memory.calc_g(data=memory, count=self.count)
            memory['grad'] = g
            p = self.memory.calc_p(input_data=data, memory_data=memory, distance=distance)
            print(p)
            if p > max_p:
                max_p = p
                fired_memory = memory
        if fired_memory:
            fired_memory['time'] = self.count
            self.sql.update_data_in_database(fired_memory)
            return fired_memory['message']
        return None
    
    def _prepare_data(self, role: str, content: str) -> dict:
        vector = self.request.embed(content)
        count = self.count if role == 'user' else self.count + 1
        data =\
        {
            'id': count,
            'vector': vector,
            'message': {'role': role, 'content': content, 'time': self.current_time},
            'time': count,
            'grad': 1.0,
        }
        self.faiss.add_embeddings(embedding=data['vector'], id=self.count)
        self.sql.add_data_to_database(data)
        self.log.debug(words.get('added_data', role=role, data=data))
        return data
    
    def _prepare_memory(self, data: dict) -> tuple:
        history = self.sql.get_history(globals.history_count)
        self.log.info(words.get('history', history=history))
        fired_memory = self._recall_memory(data)
        self.log.info(words.get('fired_memories', memories=fired_memory))
        return history, fired_memory
    
    def _prepare_prompt(self, input: str, history: list, memories: list) -> list:
        system_prompt = get_prompt(history=history, memories=memories)
        prompt = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': input}]
        self.log.debug(words.get('prompt', prompt=prompt))
        return prompt
import os
import sqlite3
import json


class SQL:
    def __init__(self, db_path: str):
        self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../assets/{db_path}'))
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.table_name = os.path.splitext(os.path.basename(self.db_path))[0]
        if not os.path.exists(self.db_path):
            open(self.db_path, 'a').close()
        self.create_database()

    def create_database(self) -> sqlite3.Connection:
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY, vector TEXT, message TEXT, time INTEGER, grad REAL)')
        self.conn.commit()
        return self.conn

    def add_data_to_database(self, data: dict) -> sqlite3.Connection:
        id: int = data['id']
        vector: str = json.dumps(data['vector'])
        message: str = json.dumps(data['message'])
        time: int = data['time']
        grad: float = data['grad']
        self.cursor.execute(f'INSERT INTO {self.table_name} (id, vector, message, time, grad) VALUES (?, ?, ?, ?, ?)', (id, vector, message, time, grad))
        self.conn.commit()
        return self.conn

    def update_data_in_database(self, data: dict) -> sqlite3.Connection:
        id: int = data['id']
        vector: str = json.dumps(data['vector'])
        message: str = json.dumps(data['message'])
        time: int = data['time']
        grad: float = data['grad']
        self.cursor.execute(f'UPDATE {self.table_name} SET vector = ?, message = ?, time = ?, grad = ? WHERE id = ?', (vector, message, time, grad, id))
        self.conn.commit()
        return self.conn

    def get_data_by_index(self, index: int) -> dict:
        index = int(index)
        self.cursor.execute(f'SELECT id, vector, message, time, grad FROM {self.table_name} WHERE id = ?', (index,))
        result = self.cursor.fetchone()
        return\
        {
            'id': result[0],
            'vector': json.loads(result[1]),
            'message': json.loads(result[2]),
            'time': result[3],
            'grad': result[4]
        }

    def get_history(self, k: int):
        self.cursor.execute(f'SELECT * FROM {self.table_name} ORDER BY id DESC LIMIT ?', (k,))
        results = self.cursor.fetchall()
        results = results[::-1]
        history = []
        for result in results:
            message = json.loads(result[2])
            history.append(message)
        return history

    def get_last_id(self) -> int:
        self.cursor.execute(f'SELECT MAX(id) FROM {self.table_name}')
        result = self.cursor.fetchone()
        return result[0]
    
    def delete_table(self) -> sqlite3.Connection:
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.table_name}')
        self.conn.commit()
        return self.conn
    
    def delete_database(self) -> sqlite3.Connection:
        os.remove(self.db_path)
        self.conn.close()
        return self.conn
import sqlite3
from datetime import date


class Sqlite:
    def __init__(self, name_file: str):
        self.name_file = name_file + '.db'
        self.table = None

    def cursor(self, execute, output=False):
        conn = sqlite3.connect(self.table)
        cur = conn.cursor()
        cur.execute(execute)
        if output:
            cur.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
            output = cur.fetchall()
        conn.commit()
        conn.close()
        return output

    def create(self, **kwargs):
        Create = ["id INTEGER PRIMARY KEY NOT NULL"]
        for k, v in kwargs.items():
            res = k
            t = type(v)
            if t == bytes: res += ' BLOB'
            elif t == int: res += ' INTEGER'
            elif t == float: res += ' REAL'
            elif t == str or t: res += ' TEXT'; kwargs[k] = str(v)
            Create.append(res)
        self.cursor(f"CREATE TABLE IF NOT EXISTS {self.table} ({','.join(Create)})")
        self.cursor(f"INSERT INTO {self.table} ({','.join(kwargs.keys())}) VALUES {tuple(kwargs.values())};")

    def table_delete(self):
        self.cursor(f"DROP TABLE IF EXISTS {self.table}")

    def delete(self, rowid: int):
        self.cursor(f"DELETE FROM {self.table} WHERE rowid={rowid}")

    def update(self, rowid: int, **kwargs):
        data = ''
        for k, v in kwargs.items():
            if type(v) == str: v = f"'{v}'"
            data += f"{k}={v}, "
        self.cursor(f"UPDATE {self.table} SET {data[:-2]} WHERE rowid={rowid}")

    def get(self, columns=[], **kwargs):
        columns = ','.join(columns) if columns else '*'
        cur = f"SELECT {columns} FROM {self.table}"
        where = ''
        for k, v in kwargs.items():
            if type(v) == str: v = f"'{v}'"
            where += f"{k}={v} AND "
        return self.cursor(f"{cur} WHERE {where[:-5]}", output=True)

    def search(self, columns=[], order=[], character=True, **kwargs):
        columns = ','.join(columns) if columns else '*'
        cur = f"SELECT {columns} FROM {self.table}"
        order = f" ORDER BY {','.join(order)}" if order else ''
        where = ''
        for k, v in kwargs.items():
            if type(v) != tuple: v = tuple([v])
            if character:
                for val in v: where += f"{k} LIKE '%{val}%' OR "
            else:
                where += f"{k} in {v} OR "
        where = where[:-4].replace(',)', ')')
        return self.cursor(f"{cur} WHERE {where} {order}", output=True)

    def views(self, rows=[], order=[]):
        rows = ','.join(rows) if rows else '*'
        cur = f"SELECT {rows} FROM {self.table}"
        if order: cur += f" ORDER BY {','.join(order)}"
        result = self.cursor(cur, output=True)
        return result

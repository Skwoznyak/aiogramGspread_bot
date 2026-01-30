import sqlite3
from typing import Optional, List, Tuple
from storage.channel import Channel
from datetime import datetime


class DB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_db()

    def _get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_db(self):  # db_path='storage/database/database.db'
        conn = self._get_conn()
        c = conn.cursor()
        c.executescript("""CREATE TABLE IF NOT EXISTS channels_info(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                channel_id INTEGER NOT NULL,
                sheet_name TEXT NOT NULL,
                table_link TEXT NOT NULL,
                cell TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_channels ON channels_info(name);
                
                CREATE TABLE IF NOT EXISTS time_do(
                time_complite TIMESTAMP
                );
                """)

        conn.commit()
        c.close()
        conn.close()


    def del_channel(self, name: str) -> str:
        op = "storage.db.del_channel"
        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("""DELETE FROM channels_info WHERE name = ? """, (name,))
            conn.commit()
            if c.rowcount > 0:
                print(f"Вы успешно удалили: {name}, op = {op}")
                msg = f"Вы успешно удалили: {name}"
                return msg
            else:
                print(f"С именем {name} ничего не найдено, op = {op}")
                msg = f"С именем {name} ничего не найдено"
                return msg
        except Exception as e:
            msg = f"Ошибка = {e}, op = {op}"
            return msg
        finally:
            c.close()
            conn.close()


    def get_all_channels(self) -> List[Tuple]:
        op = "storage.db.get_all_channels"
        
        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("""
                          SELECT * FROM channels_info; 
                          """,)
            row = c.fetchall()
            print(f"{row}, op = {op}")
            return row
        except Exception as e:
            print("Ошибка при получении каналов: {e}, op = {op}")
            return []
        finally:
            c.close()
            conn.close()


    def create_channel(self, name: str, channel_id: int,
                           sheet_name: str, cell: str, table_link: str) -> Channel:
        op = "storage.db.create_channel_new"

        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("""
                          INSERT INTO channels_info(name, channel_id, sheet_name, table_link, cell) VALUES(?, ?, ?, ?, ?)
                          """, (name, channel_id, sheet_name, table_link, cell))
            conn.commit()
            channel_id_db = c.lastrowid

            channel = Channel(
                id=channel_id_db,
                name=name,
                channel_id=channel_id,
                sheet_name=sheet_name,
                table_link=table_link,
                cell=cell,
            )

            print(f"Канал создан: {channel.name}, op = {op}")
            return channel

        except Exception as e:
            print(f"Ошибка при добавлении канала: {e}, op = {op}")
            return Channel()
        finally:
            c.close()
            conn.close()
            
            
    def get_one_channel(self, name: str) -> Channel:
        op = "storage.db.get_one_channel_new"

        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("""
                          SELECT id, name, channel_id, sheet_name, table_link, cell FROM channels_info WHERE name = ?
                          """, (name,))
            row = c.fetchone()
            if row:
                print(f"Возвращаю объект: {name}, op = {op}")
                return Channel(
                    id=row[0],
                    name=row[1],
                    channel_id=row[2],
                    sheet_name=row[3],
                    table_link=row[4],
                    cell=row[5]
                )
            print(f"Объект не вернулся/создался, op = {op}")
            return None
        except Exception as e:
            print(f"Ошибка: {e}, op = {op}")
            return None
        finally:
            c.close()
            conn.close()
            
            
    def update_name(self, old_name:str, new_name:str) -> str:
        op = "storage.db.update_name"
        
        conn = self._get_conn()
        c = conn.cursor()
        
        try:
            c.execute("""
                    UPDATE channels_info SET name = ? WHERE name = ?
                    """, (new_name, old_name))
            conn.commit()
            
            if c.rowcount == 0:
                print(f"Канал с именем = {old_name}, не найден, op = {op}")
                msg = f"Канал с именем = {old_name}, не найден"
                return msg
            
            print(f"Старое имя = {old_name}, новое имя = {new_name}, op = {op}")
            msg = f"Старое имя = {old_name}, новое имя = {new_name}"
            return msg
        except Exception as e:
            print(f"Ошибка: e = {e}, op = {op}")
            
        finally:
            c.close()
            conn.close()
        
    
    
    def update_channel_id(self, name:str, new_channel_id:str):
        op = "storage.db.update_channel_id"
        
        conn = self._get_conn()
        c = conn.cursor()
        
        try:
            c.execute("""
                    UPDATE channels_info SET channel_id = ? WHERE name = ?
                    """, (new_channel_id, name))
            conn.commit()
            
            if c.rowcount == 0:
                print(f"Канал с именем = {name}, не найден, op = {op}")
                msg = f"Канал с именем = {name}, не найден"
                return msg
            
            print(f"channel_id для {name} изменен на {new_channel_id}, op = {op}")
            msg = f"channel_id для {name} изменен на {new_channel_id}"
            return msg
        except Exception as e:
            print(f"Ошибка: e = {e}, op = {op}")
            
        finally:
            c.close()
            conn.close()
    
    
    def update_sheet_name(self, name:str, new_sheet_name) -> str:
        op = "storage.db.update_sheet_name"
        
        conn = self._get_conn()
        c = conn.cursor()
        
        try:
            c.execute("""
                    UPDATE channels_info SET sheet_name = ? WHERE name = ?
                    """, (new_sheet_name, name))
            conn.commit()
            
            if c.rowcount == 0:
                print(f"Канал с именем = {name}, не найден, op = {op}")
                msg = f"Канал с именем = {name}, не найден"
                return msg
            
            print(f"sheet_name для {name} изменен на {new_sheet_name}, op = {op}")
            msg = f"название страницы для {name} изменен на {new_sheet_name}"
            return msg
        except Exception as e:
            print(f"Ошибка: e = {e}, op = {op}")
            
        finally:
            c.close()
            conn.close()
    
    
    def update_table_link(self, name:str, new_table_link:str) -> str:
        op = "storage.db.update_table_link"
        conn = self._get_conn()
        c = conn.cursor()
        
        try:
            c.execute("""
                    UPDATE channels_info SET table_link = ? WHERE name = ?
                    """, (new_table_link, name))
            conn.commit()
            
            if c.rowcount == 0:
                print(f"Канал с именем = {name}, не найден, op = {op}")
                msg = f"Канал с именем = {name}, не найден"
                return msg
            
            print(f"sheet_name для {name} изменен на {new_table_link}, op = {op}")
            msg = f"Ссылка для {name} изменена на {new_table_link}"
            return msg
        except Exception as e:
            print(f"Ошибка: e = {e}, op = {op}")
            
        finally:
            c.close()
            conn.close()
    
    
    def update_cell(self, name, new_cell):
        op = "storage.db.update_cell"
        conn = self._get_conn()
        c = conn.cursor()
        
        try:
            c.execute("""
                    UPDATE channels_info SET cell = ? WHERE name = ?
                    """, (new_cell, name))
            conn.commit()
            
            if c.rowcount == 0:
                print(f"Канал с именем = {name}, не найден, op = {op}")
                msg = f"Канал с именем = {name}, не найден"
                return msg
            
            print(f"sheet_name для {name} изменен на {new_cell}, op = {op}")
            msg = f"Ссылка для {name} изменена на {new_cell}"
            return msg
        except Exception as e:
            print(f"Ошибка: e = {e}, op = {op}")
            
        finally:
            c.close()
            conn.close()
    

    def set_next_run_time(self, dt: datetime) -> None:
        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("DELETE FROM time_do;")  # храним только одно время
            c.execute(
                "INSERT INTO time_do (time_complite) VALUES (?)",
                (dt.strftime("%Y-%m-%d %H:%M:%S"),),
            )
            conn.commit()
        finally:
            c.close()
            conn.close()
            

    def get_next_run_time(self) -> Optional[datetime]:
        conn = self._get_conn()
        c = conn.cursor()
        try:
            c.execute("SELECT time_complite FROM time_do LIMIT 1;")
            row = c.fetchone()
            if not row or not row[0]:
                return None
            # row[0] — строка "2026-01-26 14:30:00"
            return datetime.fromisoformat(row[0])
        finally:
            c.close()
            conn.close()
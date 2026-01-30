from typing import Optional

class Channel:
    def __init__(self, id: int, name:str, channel_id:int,
                 sheet_name:str, table_link:str, cell: str):
        self.id = id
        self.name = name
        self.channel_id = channel_id
        self.sheet_name = sheet_name
        self.table_link = table_link
        self.cell = cell
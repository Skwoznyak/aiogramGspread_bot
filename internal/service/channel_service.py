from typing import Optional, List, Tuple, Union
from internal.service.sheets_client import SheetsClient
from storage.db import DB
from storage.channel import Channel


class ChannelService:
    def __init__(self, db: DB, sheets: SheetsClient):
        self._db = db
        self._sheets = sheets

    def get_channel_stat_new(self, channel_name: str) -> Optional[str]:
        op = "internal.service.channel_service.get_channel_stat"

        try:
            channel = self._db.get_one_channel(channel_name)
            print(f"Получил данные тг канала, op = {op}")

        except Exception as e:
            print(f"Не получил канал: {channel_name},op = {op} ,e = {e}")
            return "Что-то пошло не так..."

        try:
            cell_value = self._sheets.get_data(
                table_link=channel.table_link, cell=channel.cell, sheet_name=channel.sheet_name)
        except Exception as e:
            print(f"Не получил значение из таблицы {e}, op = {op}")
            return None

        print(f"канал: ({channel.name}), op = {op}")
        return f"{cell_value} (канал: {channel.name})"

    def get_one_channel_new(self, name):
        op = "internal.service.channel_service.get_one_channels_new"

        try:
            chan = self._db.get_one_channel(name=name)
            print(f"Получил канал {name}, op =", op)
        except Exception as e:
            print(f"Ошибка: {e}, op = {op}")
            msg = f"Ошибка: {e}"
            return msg

        return chan

    def get_all_channels_new(self) -> Optional[Union[List[Tuple], str]]:
        op = "internal.service.channel_service.get_all_channels_new"

        try:
            channels = self._db.get_all_channels()
            print("Получил все каналы какие есть, op =", op)
        except Exception as e:
            print(f"Ошибка: {e}, op = {op}")
            return None

        if channels == []:
            msg = "Я не нашел ничего в бд, нужно их создать"
            return msg

        text = "📋 Каналы:\n\n"
        for ch in channels:
            # name=индекс1, channel_id=индекс2
            text += f"• {ch[1]} (ID: {ch[2]})\n Название листа: {ch[3]}\n Ссылка: {ch[4]}\n Ячейка: {ch[5]}\n"
        return text

    def create_channel_new(self, name: str, channel_id: int, sheet_name: str, cell: str, table_link: str) -> str:
        op = "internal.service.channel_service.create_channel_new"

        try:
            print("Получил все значения для данные для парсинга, op = ", op)
            channel = self._db.create_channel(
                name=name, channel_id=channel_id, sheet_name=sheet_name, cell=cell, table_link=table_link)
        except Exception as e:
            msg = f"Ошибка = {e}"
            print(f"Ошибка = {e}, op = {op}")
            return msg

        print(f"Создал {channel.name}, op = {op}")
        msg = f"Создал {channel.name}"
        return msg

    def delete_channel_new(self, delete_name) -> str:
        op = "internal.service.channel_service.delete_channel_new"

        try:
            print("Получил название канала, сейчас буду удалять, op = ", op)
            res = self._db.del_channel(delete_name)
            return res
        except Exception as e:
            msg = f"Ошибка {e}"
            print(f"Ошибка {e}, op = {op}")
            return msg

    def get_all_channels_new_list(self) -> Optional[Union[List[Tuple], str]]:
        op = "internal.service.channel_service.get_all_channels_new"

        try:
            channels = self._db.get_all_channels()
            print("Получил все каналы какие есть, op =", op)
        except Exception as e:
            print(f"Ошибка: {e}, op = {op}")
            return None

        return channels

    def update_name_new(self, old_name: str, new_name: str) -> str:
        op = "internal.service.channel_service.update_name_new"

        try:
            res = self._db.update_name(old_name=old_name, new_name=new_name)
            print(f"меняю имя, op = {op}")
        except Exception as e:
            print(f"e = {e}, op = {op}")
            msg = f"Ошибка: {e}"
            return msg

        return res

    def update_channel_id_new(self, name: str, new_channel_id: str) -> str:
        op = "internal.service.channel_service.update_channel_id_new"

        try:
            res = self._db.update_channel_id(
                name=name, new_channel_id=new_channel_id)
            print(f"меняю channel_id, op = {op}")
        except Exception as e:
            print(f"e = {e}, op = {op}")
            msg = f"Ошибка: {e}"
            return msg

        return res

    def update_sheet_name_new(self, name: str, sheet_name: str) -> str:
        op = "internal.service.channel_service.update_channel_id_new"

        try:
            res = self._db.update_sheet_name(
                name=name, new_sheet_name=sheet_name)
            print(f"меняю sheet_name, op = {op}")
        except Exception as e:
            print(f"e = {e}, op = {op}")
            msg = f"Ошибка: {e}"
            return msg

        return res

    def update_table_link_new(self, name: str, table_link: str) -> str:
        op = "internal.service.channel_service.update_table_link_new"

        try:
            res = self._db.update_table_link(
                name=name, new_table_link=table_link)
            print(f"меняю table_link, op = {op}")
        except Exception as e:
            print(f"e = {e}, op = e {e}")
            msg = f"Ошибка: {e}"
            return msg

        return res

    def update_cell_new(self, name: str, cell: str) -> str:
        op = "internal.service.channel_service.update_cell_new"

        try:
            res = self._db.update_cell(name=name, new_cell=cell)
            print(f"Меняю cell, op = {op}")
        except Exception as e:
            print(f"e = {e}, op = e {e}")
            msg = f"Ошибка: {e}"
            return msg

        return res

        # channel = self._db.get_one_channel_new(channel_name)
        # if not channel:
        #     print("Не было объекта channel: ", op)
        #     return None

        # stat_value = self._sheets.get_data(self,
        #     table_link=channel.table_link,
        #     cell=channel.cell,
        #     sheet_name=channel.sheet_name
        # )


# db = DB('storage/database/database.db')
# sc = SheetsClient('internal/service/maxtgbottg-7720279c9ab8.json')
# service = ChannelService(db, sc)  # пока без sheets для теста БД
# service.get_channel_stat("AvtoEuBest_orig")

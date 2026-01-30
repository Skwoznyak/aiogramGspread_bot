# test_db.py
from db import DB
from channel import Channel


if __name__ == "__main__":
    print(123)
    db = DB('storage/database/database.db')
    # channel = db.create_channel_new(
    #     name="AvtoEuBest10",
    #     channel_id=-5016643115,
    #     sheet_name="Структура - Парсер - Канал",
    #     cell="B463",
    #     table_link="https://docs.google.com/..."
    # )
    # print("Созданный канал: ,", channel)

    found = db.get_one_channel_new("AvtoEuBest10")
    print(f"мэйн панель Канад по поиску: AvtoEuBest10, {found.name}")

    db.del_channel("AvtoEuBest10")
    print(f"Удалил канал мэйн панель")

    db.get_all_channels()
    print(f"Все каналы")
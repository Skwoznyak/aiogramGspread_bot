# services/test_service.py
from internal.service.channel_service import ChannelService
from internal.service.sheets_client import SheetsClient
from storage.db import DB

if __name__ == "__main__":
    db = DB('storage/database/database.db')
    sc = SheetsClient('internal/service/maxtgbottg-7720279c9ab8.json')
    service = ChannelService(db, sc)  # пока без sheets для теста БД
    
    # Тест только БД
    try:
        channel = db.create_channel(
            name="AvtoEuBest_orig",
            channel_id=-5016643115,
            sheet_name="Структура - Парсер",
            cell="B140",
            table_link="https://docs.google.com/spreadsheets/d/19enXGBoOoWkfNakuCnEKLLibuyTbK15dncJpw71PLIE/edit?gid=1169725712#gid=1169725712",
        )
    except Exception as e:
        print(e)
    
    try:
        result = service.get_channel_stat(channel_name=channel.name)
        print("Результат:", result)
    except Exception as e:
        print(e)
        
    db.del_channel(name=channel.name)
    
# print(123)
# sc = SheetsClient('internal/service/maxtgbottg-7720279c9ab8.json')
# res = sc.get_data(cell="B140", sheet_name="Структура - Парсер",
#                   table_link="https://docs.google.com/spreadsheets/d/19enXGBoOoWkfNakuCnEKLLibuyTbK15dncJpw71PLIE/edit?gid=1169725712#gid=1169725712")
# print(res)
# print(123)
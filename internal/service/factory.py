from storage.db import DB
from internal.service.sheets_client import SheetsClient
from internal.service.channel_service import ChannelService
from internal.service.schedule_service import ScheduleService


def create_db_new() -> DB:
    return DB('storage/database/database.db')


def create_channel_service() -> ChannelService:
    """Создает готовый сервис для слой хендлеров"""
    db = create_db_new()
    sc = SheetsClient('json')
    return ChannelService(db, sc)


def create_schedule_service() -> ScheduleService:
    db = create_db_new()
    return ScheduleService(db)

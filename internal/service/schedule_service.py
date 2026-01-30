# internal/service/schedule_service.py
from datetime import datetime, timedelta, timezone
from typing import Optional

from storage.db import DB

MSK = timezone(timedelta(hours=3))


class ScheduleService:
    def __init__(self, db: DB):
        self._db = db

    def set_next_run_today_msk(self, hh: int, mm: int) -> datetime:
        op = "internal.service.schedulle_service.set_next_run_today_msk"
        """
        Устанавливает время запуска на сегодня (по Москве),
        если время уже прошло — переносит на завтра.
        Возвращает установленный datetime.
        """
        now = datetime.now(MSK)
        try:
            target = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=hh,
                minute=mm,
                tzinfo=MSK,
            )
        except Exception as e:
            print(f"Error = {e}, op = {op}")
            msg = f"Ошибка: {e}"
            return msg
        if target <= now:
            target = target + timedelta(days=1)

        # пишем в БД как naive-строку "YYYY-MM-DD HH:MM:SS"
        try:
            self._db.set_next_run_time(target)
            return target
        except Exception as e:
            msg = f"Ошибка: {e}"
            print(f"Error: {e}, op = {op}")
            return msg

    def get_next_run_msk(self) -> Optional[datetime]:
        """
        Возвращает время следующего запуска (с таймзоной МСК),
        или None, если оно не задано.
        """
        dt = self._db.get_next_run_time()
        if dt is None:
            return None

        # считаем, что в БД хранится naive-время в МСК
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=MSK)
        return dt

    def shift_next_run_by_days(self, days: int = 1) -> Optional[datetime]:
        """
        Сдвигает время следующего запуска на N дней вперёд.
        Возвращает новое время или None, если старого не было.
        """
        current = self.get_next_run_msk()
        if current is None:
            return None

        new_dt = current + timedelta(days=days)
        self._db.set_next_run_time(new_dt)
        return new_dt

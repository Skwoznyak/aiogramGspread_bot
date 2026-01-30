from datetime import datetime, timedelta, timezone
from aiogram import Bot, Dispatcher, types
import logging
import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


from internal.service.factory import create_schedule_service, create_channel_service
from internal.handlers.handlers_sheets import router_buttons
from internal.handlers.handler_command import router_comand


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


MSK = timezone(timedelta(hours=3))


async def scheduler(bot: Bot):
    schedule_service = create_schedule_service()
    channel_service = create_channel_service()

    while True:
        await asyncio.sleep(10)

        next_run = schedule_service.get_next_run_msk()
        if not next_run:
            continue

        now = datetime.now(MSK)
        if now < next_run:
            continue

        channels = channel_service.get_all_channels_new_list()
        print("channels in scheduler =", channels, type(channels))

        for ch in channels:
            print("one ch in scheduler =", ch, type(ch))

            if not isinstance(ch, (tuple, list)) or len(ch) < 3:
                print("НЕОЖИДАННЫЙ формат ch =", ch)
                continue

            name = ch[1]
            channel_id = ch[2]

            try:
                res = channel_service.get_channel_stat_new(name)
                await bot.send_message(
                    chat_id=channel_id,
                    text=f"Статистика доков для {name}: {res}",
                )
            except Exception as e:
                print(
                    f"Не получил канал: {name}, "
                    f"op = internal.service.channel_service.get_channel_stat_new, "
                    f"e = {e}"
                )
                continue

        schedule_service.shift_next_run_by_days(1)


# Запуск процесса поллинга новых апдейтов
async def main():
    # Объект бота
    bot = Bot(token="")
    # Диспетчер
    dp = Dispatcher()
    dp.include_router(router=router_buttons)
    dp.include_router(router=router_comand)

    asyncio.create_task(scheduler(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt):
        logging.error("Bot stopped!")

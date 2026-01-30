from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from internal.service.factory import create_channel_service, create_schedule_service

from internal.handlers.mini_middleware import is_allowed

router_comand = Router()


new_chanel_service = create_channel_service()
new_schedule_service = create_schedule_service()

class UpdateForm(StatesGroup):
    waiting_up_name_old = State()
    waiting_up_name_new = State()
    waiting_up_channel_id_old = State()
    waiting_up_channel_id_new = State()
    waiting_up_sheet_name_old = State()
    waiting_up_sheet_name_new = State()
    waiting_up_cell_old = State()
    waiting_up_cell_new = State()
    waiting_up_table_link_old = State()
    waiting_up_table_link_new = State()


class DeleteForm(StatesGroup):
    waiting_delete = State()


class CreateChannelForm(StatesGroup):
    waiting_name = State()
    waiting_channel_id = State()
    waiting_sheet_name = State()
    waiting_cell = State()
    waiting_table_link = State()


class GetOneStat(StatesGroup):
    waiting_get_one_stat = State()


@router_comand.message(Command("show_one"))
async def cmd_show_one(message: types.Message):
    op = "internal.handlers.handlers_sheets.show_one"
    print(op)
    if not is_allowed(message.from_user.id):
        return
    chan = new_chanel_service.get_one_channel_new()

    await message.answer()


@router_comand.message(Command("show_all"))
async def cmd_show_all(message: types.Message):
    op = "internal.handlers.handlers_sheets.show_all"
    print(op)
    if not is_allowed(message.from_user.id):
        return
    channels = new_chanel_service.get_all_channels_new()

    await message.answer(channels)


@router_comand.message(Command("delete"))
async def cmd_delete(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await message.answer("Введите название канала, что бы его удалить")
    await state.set_state(DeleteForm.waiting_delete)


@router_comand.message(DeleteForm.waiting_delete)
async def get_delete(message: types.Message, state: FSMContext):
    op = "internal.handlers.handlers_sheets.delete"
    if not is_allowed(message.from_user.id):
        return
    print(op)
    await state.update_data(delete=message.text)

    del_name = await state.get_data()
    res = new_chanel_service.delete_channel_new(delete_name=del_name["delete"])

    await message.answer(res)

    await state.clear()


@router_comand.message(Command("create"))
async def cmd_create(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await message.answer("Введите название (для вашего удобного использования)")
    await state.set_state(CreateChannelForm.waiting_name)


@router_comand.message(CreateChannelForm.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(name=message.text)

    await message.answer("Введите айди тг-группы, куда будет отправляться сообщение")
    await state.set_state(CreateChannelForm.waiting_channel_id)


@router_comand.message(CreateChannelForm.waiting_channel_id)
async def get_channel_id(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(channel_id=message.text)

    await message.answer("Введите название страницы гуглы таблицы")
    await state.set_state(CreateChannelForm.waiting_sheet_name)


@router_comand.message(CreateChannelForm.waiting_sheet_name)
async def get_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(sheet_name=message.text)

    await message.answer("Введите нужную ячейку")
    await state.set_state(CreateChannelForm.waiting_cell)


@router_comand.message(CreateChannelForm.waiting_cell)
async def get_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(cell=message.text)

    await message.answer("Введите ссылку на таблицу")
    await state.set_state(CreateChannelForm.waiting_table_link)


@router_comand.message(CreateChannelForm.waiting_table_link)
async def get_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    
    op = "internal.handlers.handlers_sheets.show_all"
    print(op)
    await state.update_data(table_link=message.text)

    data = await state.get_data()
    await message.answer(f"✅ Канал *{data['name']}* создан!\n"
                         f"🆔 Группа: `{data['channel_id']}`\n"
                         f"📊 Лист: `{data['sheet_name']}`\n"
                         f"📍 Ячейка: `{data['cell']}`")

    try:
        channel = new_chanel_service.create_channel_new(**data)
        await message.answer(f"✅ Канал {channel} создан!")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

    await state.clear()


@router_comand.message(Command("complite_one"))
async def cmd_complite_one(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    
    await message.answer("Введите название канала, откуда хотите получить информацию")
    await state.set_state(GetOneStat.waiting_get_one_stat)


@router_comand.message(GetOneStat.waiting_get_one_stat)
async def get_one_stat(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    
    op = "internal.handlers.handlers_sheets.show_all"
    print(op)
    await state.update_data(get_one_stat=message.text)

    data = await state.get_data()
    await state.clear()

    res = new_chanel_service.get_channel_stat_new(data['get_one_stat'])
    await message.answer(res)


@router_comand.message(Command("complite_all"))
async def cmd_complite_all(message: types.Message):
    if not is_allowed(message.from_user.id):
        return
    
    op = "internal.handlers.handlers_sheets.complite_all"
    print(op)
    text = ""

    channels = new_chanel_service.get_all_channels_new_list()
    print("Получил все каналы какние есть, op = ", op)

    if not channels:
        await message.answer("📭 В БД нет ни одного канала")
        return

    for ch in channels:
        name = ch[1]

        try:
            res = new_chanel_service.get_channel_stat_new(name)
            await message.bot.send_message(chat_id=ch[2], text=f"Статистика доков: {res}")
        except Exception as e:
            print(
                f"Не получил канал: {name}, op = internal.service.channel_service.get_channel_stat_new ,e = {e}")
            text += f"• {name}: ❌ ошибка получения статистики\n"
            continue

        if not res:
            text += f"• {name}: ❌ нет данных\n"
        else:
            text += f"• {name}: - ok\n"

    await message.answer(text)


@router_comand.message(Command("set_time"))
async def cmd_set_time(message: types.Message):
    op = "internal.handlers.handlers_sheets.set_time"
    if not is_allowed(message.from_user.id):
        return
    
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Формат: /set_time ЧЧ:ММ\nНапример: /set_time 14:30")
        return

    try:
        hh, mm = map(int, parts[1].split(":"))
    except ValueError:
        await message.answer("Не понял время. Формат: /set_time ЧЧ:ММ")
        return

    try:
        target = new_schedule_service.set_next_run_today_msk(hh, mm)
        await message.answer(
            f"🕒 Время запуска установлено: {target.strftime('%Y-%m-%d %H:%M')} (МСК)"
        )
    except Exception as e:
        msg = f"Ошибка: {e}"
        if "'str' object has no attribute 'strftime'" in str(e):
            await message.answer("Введите время в формате ЧЧ:ММ")
            return
        print(f"Error = {e}, op = {op}")
        await message.answer(msg)


@router_comand.message(Command("update_name"))
async def cmd_update_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_name"
    await message.answer("Введите имя, которое хотите поменять")
    await state.set_state(UpdateForm.waiting_up_name_old)


@router_comand.message(UpdateForm.waiting_up_name_old)
async def get_name_old(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(old_name=message.text)

    await message.answer("Введите имя, на которое хотите поменять")

    await state.set_state(UpdateForm.waiting_up_name_new)


@router_comand.message(UpdateForm.waiting_up_name_new)
async def get_name_new(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_name=message.text)

    data = await state.get_data()

    print(op)

    res = new_chanel_service.update_name_new(
        data['old_name'], data['new_name'])
    await message.answer(res)


@router_comand.message(Command("update_channel_id"))
async def cmd_update_channel_id(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.cmd_update_channel_id"
    await message.answer("Введите название канала,на котором хотите поменять id группы телеграмма")
    await state.set_state(UpdateForm.waiting_up_channel_id_old)


@router_comand.message(UpdateForm.waiting_up_channel_id_old)
async def get_channel_id_old(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(old_channel_id=message.text)

    await message.answer("Введите желаемый id")

    await state.set_state(UpdateForm.waiting_up_channel_id_new)


@router_comand.message(UpdateForm.waiting_up_channel_id_new)
async def get_channel_id_new(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_channel_id"
    await state.update_data(new_channel_id=message.text)

    data = await state.get_data()

    print(op)

    res = new_chanel_service.update_channel_id_new(
        data['old_channel_id'], data['new_channel_id'])
    await message.answer(res)


@router_comand.message(Command("update_sheet_name"))
async def cmd_update_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.cmd_update_sheet_name"
    await message.answer("Введите название канала,на котором хотите поменять название страницы")
    await state.set_state(UpdateForm.waiting_up_sheet_name_old)


@router_comand.message(UpdateForm.waiting_up_sheet_name_old)
async def get_sheet_name_old(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(old_sheet_name=message.text)

    await message.answer("Введите желаемое имя страницы")

    await state.set_state(UpdateForm.waiting_up_sheet_name_new)


@router_comand.message(UpdateForm.waiting_up_sheet_name_new)
async def get_sheet_name_new(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_sheet_name"
    await state.update_data(new_sheet_name=message.text)

    data = await state.get_data()

    print(op)

    res = new_chanel_service.update_sheet_name_new(
        data['old_sheet_name'], data['new_sheet_name'])
    await message.answer(res)


@router_comand.message(Command("update_table_link"))
async def cmd_update_table_link(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.cmd_update_sheet_name"
    await message.answer("Введите название канала,в котором хотите поменять ссылку")
    await state.set_state(UpdateForm.waiting_up_table_link_old)


@router_comand.message(UpdateForm.waiting_up_table_link_old)
async def get_table_link_old(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(old_table_link=message.text)

    await message.answer("Введите желаемую ссылку")

    await state.set_state(UpdateForm.waiting_up_table_link_new)


@router_comand.message(UpdateForm.waiting_up_table_link_new)
async def get_table_link_new(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_table_link"
    await state.update_data(new_table_link=message.text)

    data = await state.get_data()

    print(op)

    res = new_chanel_service.update_table_link_new(
        data['old_table_link'], data['new_table_link'])
    await message.answer(res)


@router_comand.message(Command("update_cell"))
async def cmd_update_cell(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.cmd_update_cell_name"
    await message.answer("Введите название канала,в котором хотите поменять ячейку")
    await state.set_state(UpdateForm.waiting_up_cell_old)


@router_comand.message(UpdateForm.waiting_up_cell_old)
async def get_cell_old(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(old_cell=message.text)

    await message.answer("Введите желаемую ячейку")

    await state.set_state(UpdateForm.waiting_up_cell_new)


@router_comand.message(UpdateForm.waiting_up_cell_new)
async def get_cell_new(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    op = "internal.handlers.handlers_sheets.update_cell"
    await state.update_data(new_cell=message.text)

    data = await state.get_data()

    print(op)

    res = new_chanel_service.update_cell_new(
        data['old_cell'], data['new_cell'])
    await message.answer(res)
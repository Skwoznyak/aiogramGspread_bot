from aiogram.filters.command import Command
from aiogram import types
from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import callback_data

from internal.service.factory import create_channel_service, create_schedule_service
from internal.handlers.mini_middleware import is_allowed

router_buttons = Router()

new_chanel_service = create_channel_service()
new_schedule_service = create_schedule_service()


class UpdateForm2(StatesGroup):
    waiting_up_name_old2 = State()
    waiting_up_name_new2 = State()
    waiting_up_channel_id_old2 = State()
    waiting_up_channel_id_new2 = State()
    waiting_up_sheet_name_old2 = State()
    waiting_up_sheet_name_new2 = State()
    waiting_up_cell_old2 = State()
    waiting_up_cell_new2 = State()
    waiting_up_table_link_old2 = State()
    waiting_up_table_link_new2 = State()


class ChannelCB(CallbackData, prefix="ch"):
    action: str   # "list", "info", "run", "back"
    name: str | None = None  # для list можно без имени


@router_buttons.message(Command("start"))
async def cmd_start(message: types.Message):
    if not is_allowed(message.from_user.id):
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📋 Показать все каналы",
                callback_data=ChannelCB(action="list").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Выполнить все",
                callback_data=ChannelCB(action="run_all").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="➕ Создать канал",
                callback_data=ChannelCB(action="create_channel").pack() # потом свяжешь с /create
            )
        ],
    ])
    await message.answer("Главное меню", reply_markup=kb)


@router_buttons.callback_query(ChannelCB.filter(F.action == "list"))
async def cb_list_channels(callback: types.CallbackQuery):
    if not is_allowed(callback.from_user.id):
        return

    channels = new_chanel_service.get_all_channels_new_list()
    if not channels:
        await callback.message.edit_text("📭 В БД нет ни одного канала")
        await callback.answer()
        return

    rows = [
        [
            InlineKeyboardButton(
                text=f"📺 {ch[1]}",  # name
                callback_data=ChannelCB(action="info", name=ch[1]).pack()
            )
        ]
        for ch in channels
    ]

    rows.append(
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(action="back_main").pack()
            )
        ]
    )

    kb = InlineKeyboardMarkup(inline_keyboard=rows)

    await callback.message.edit_text("Выберите канал:", reply_markup=kb)


@router_buttons.callback_query(ChannelCB.filter(F.action == "back_main"))
async def cb_back_main(callback: types.CallbackQuery):
    if not is_allowed(callback.from_user.id):
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📋 Показать все каналы",
                callback_data=ChannelCB(action="list").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Выполнить все",
                callback_data=ChannelCB(action="run_all").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="➕ Создать канал",
                callback_data=ChannelCB(action="create_channel").pack()
            )
        ],
    ])
    await callback.message.edit_text("Главное меню:", reply_markup=kb)
    await callback.answer()
    

# @router_buttons.callback_query(ChannelCB.filter(F.action == "info"))
# async def cmd_create(message: types.Message, state: FSMContext):
#     if not is_allowed(message.from_user.id):
#         return
#     await message.answer("Введите название (для вашего удобного использования)")
#     await state.set_state(CreateChannelForm.waiting_name)


@router_buttons.callback_query(ChannelCB.filter(F.action == "info"))
async def cb_channel_info(callback: types.CallbackQuery, callback_data: ChannelCB):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name

    ch = new_chanel_service.get_one_channel_new(
        name)

    text = (
        f"📺 *{ch.name}*\n"
        f"🆔 `{ch.channel_id}`\n"
        f"📊 Лист: `{ch.sheet_name}`\n"
        f"📍 Ячейка: `{ch.cell}`\n"
        f"🔗 {ch.table_link}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="▶️ Выполнить один в рабочий чат",
                callback_data=ChannelCB(action="run_in_workspace", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="▶️ Выполнить один",
                callback_data=ChannelCB(action="run", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 Удалить",
                callback_data=ChannelCB(action="delete", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(action="list").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text=" Изменить",
                callback_data=ChannelCB(action="update", name=name).pack()
            )
        ],
    ])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update"))
async def cb_channel_update_menu(callback: types.CallbackQuery, callback_data: ChannelCB):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name

    ch = new_chanel_service.get_one_channel_new(
        name)

    text = (
        f"📺 *{ch.name}*\n"
        f"🆔 `{ch.channel_id}`\n"
        f"📊 Лист: `{ch.sheet_name}`\n"
        f"📍 Ячейка: `{ch.cell}`\n"
        f"🔗 {ch.table_link}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Имя",
                callback_data=ChannelCB(action="update_name", name=name).pack()
            ),
            InlineKeyboardButton(
                text="ID",
                callback_data=ChannelCB(
                    action="update_channel_id", name=name).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="Лист",
                callback_data=ChannelCB(
                    action="update_sheet", name=name).pack()
            ),
            InlineKeyboardButton(
                text="Ячейка",
                callback_data=ChannelCB(action="update_cell", name=name).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔗 Ссылку",
                callback_data=ChannelCB(action="update_link", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(action="info", name=name).pack()
            )
        ],
    ])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update_name"))
async def cb_ask_new_name(
    callback: types.CallbackQuery,
    callback_data: ChannelCB,
    state: FSMContext,
):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    await state.update_data(old_name=name)
    await state.set_state(UpdateForm2.waiting_up_name_new2)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(
                    action="cancel_update", name=name).pack()
            )
        ]
    ])

    await callback.message.edit_text(
        f"Старое имя: *{name}*\n\nВведи новое имя:",
        reply_markup=kb,
        parse_mode="Markdown",
    )
    await callback.answer()


@router_buttons.message(UpdateForm2.waiting_up_name_new2)
async def get_name_new(message: types.Message, state: FSMContext):

    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_name=message.text)

    data = await state.get_data()
    print(op)

    res = new_chanel_service.update_name_new(
        data["old_name"], data["new_name"])
    await message.answer(res)

    await state.clear()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update_channel_id"))
async def cb_ask_new_channel_id(
        callback: types.CallbackQuery,
        callback_data: ChannelCB,
        state: FSMContext):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    await state.update_data(old_channel_id=name)
    await state.set_state(UpdateForm2.waiting_up_channel_id_new2)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(
                    action="cancel_update", name=name).pack()
            )
        ]
    ])

    await callback.message.edit_text(
        f"*{name}*\n\nВведите новое айди тг группы:",
        reply_markup=kb,
        parse_mode="Markdown",
    )
    await callback.answer()


@router_buttons.message(UpdateForm2.waiting_up_channel_id_new2)
async def get_channel_id_new(message: types.Message, state: FSMContext):
    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_channel_id=message.text)

    data = await state.get_data()
    print(op)

    res = new_chanel_service.update_channel_id_new(
        data["old_channel_id"], data["new_channel_id"])
    await message.answer(res)

    await state.clear()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update_sheet"))
async def cb_ask_new_update_sheet(
        callback: types.CallbackQuery,
        callback_data: ChannelCB,
        state: FSMContext):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name

    await state.update_data(old_sheet_name=name)
    await state.set_state(UpdateForm2.waiting_up_sheet_name_new2)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(
                    action="cancel_update", name=name).pack()
            )
        ]
    ])

    await callback.message.edit_text(
        f"*{name}*\n\nВведи новое название листа:",
        reply_markup=kb,
        parse_mode="Markdown",
    )
    await callback.answer()


@router_buttons.message(UpdateForm2.waiting_up_sheet_name_new2)
async def get_sheet_new(message: types.Message, state: FSMContext):
    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_sheet_name=message.text)

    data = await state.get_data()
    print(op)

    res = new_chanel_service.update_sheet_name_new(
        data["old_sheet_name"], data["new_sheet_name"])
    await message.answer(res)

    await state.clear()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update_cell"))
async def cb_ask_new_update_cell(
        callback: types.CallbackQuery,
        callback_data: ChannelCB,
        state: FSMContext):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    await state.update_data(old_cell=name)
    await state.set_state(UpdateForm2.waiting_up_cell_new2)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(
                    action="cancel_update", name=name).pack()
            )
        ]
    ])

    await callback.message.edit_text(
        f"*{name}*\n\nВведи новое название ячейки",
        reply_markup=kb,
        parse_mode="Markdown",
    )
    await callback.answer()


@router_buttons.message(UpdateForm2.waiting_up_cell_new2)
async def get_cell_new(message: types.Message, state: FSMContext):
    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_cell=message.text)

    data = await state.get_data()
    print(op)

    res = new_chanel_service.update_cell_new(
        data["old_cell"], data["new_cell"])
    await message.answer(res)

    await state.clear()


@router_buttons.callback_query(ChannelCB.filter(F.action == "update_link"))
async def cb_ask_new_update_link(
        callback: types.CallbackQuery,
        callback_data: ChannelCB,
        state: FSMContext):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name

    await state.update_data(old_link=name)
    await state.set_state(UpdateForm2.waiting_up_table_link_new2)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ChannelCB(
                    action="cancel_update", name=name).pack()
            )
        ]
    ])

    await callback.message.edit_text(
        f"*{name}*\n\nВведите новую ссылку:",
        reply_markup=kb,
        parse_mode="Markdown",
    )
    await callback.answer()


@router_buttons.message(UpdateForm2.waiting_up_table_link_new2)
async def get_link_new(message: types.Message, state: FSMContext):
    op = "internal.handlers.handlers_sheets.update_name"
    await state.update_data(new_link=message.text)

    data = await state.get_data()
    print(op)

    res = new_chanel_service.update_table_link_new(
        data["old_link"], data["new_link"])
    await message.answer(res)

    await state.clear()


##
@router_buttons.callback_query(ChannelCB.filter(F.action == "cancel_update"))
async def cb_cancel_update(
        callback: types.CallbackQuery,
        callback_data: ChannelCB,
        state: FSMContext):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    await state.clear()

    ch = new_chanel_service.get_one_channel_new(name)

    text = (
        f"📺 *{ch.name}*\n"
        f"🆔 `{ch.channel_id}`\n"
        f"📊 Лист: `{ch.sheet_name}`\n"
        f"📍 Ячейка: `{ch.cell}`\n"
        f"🔗 {ch.table_link}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="▶️ Выполнить один",
                callback_data=ChannelCB(action="run", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 Удалить",
                callback_data=ChannelCB(action="delete", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="✏️ Изменить",
                callback_data=ChannelCB(action="update", name=name).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад к списку",
                callback_data=ChannelCB(action="list").pack()
            )
        ],
    ])

    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer("Изменение отменено")


@router_buttons.callback_query(ChannelCB.filter(F.action == "delete"))
async def cb_run_one(callback: types.CallbackQuery, callback_data: ChannelCB):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    res = new_chanel_service.delete_channel_new(name)
    await callback.message.answer(f"📊 {name}: {res}")
    await callback.answer("✅ Удалено")


@router_buttons.callback_query(ChannelCB.filter(F.action == "run_in_workspace"))
async def cb_run_one(callback: types.CallbackQuery, callback_data: ChannelCB):
    op = "internal.handlers.handlers_sheets.run_in_workspace"
    if not is_allowed(callback.from_user.id):
        return
    

    name = callback_data.name
    try:
        chat_id = new_chanel_service.get_one_channel_new(name)
        print("chat_id ", chat_id.channel_id )
        res = new_chanel_service.get_channel_stat_new(name)
        # print("res ", res)
        try:
            await callback.bot.send_message(chat_id=chat_id.channel_id, text=f"Статистика доков: {res}")
        except Exception as e:
            await callback.message.answer(f"Ошибка: {e}")
    except Exception as e:
        print(f"Error: {e}, op = {op}")
        text = f"• {name}: ошибка: {e}\n"
        await callback.answer(text=text)
        


@router_buttons.callback_query(ChannelCB.filter(F.action == "run"))
async def cb_run_one(callback: types.CallbackQuery, callback_data: ChannelCB):
    if not is_allowed(callback.from_user.id):
        return

    name = callback_data.name
    res = new_chanel_service.get_channel_stat_new(name)
    await callback.message.answer(f"📊 {name}: {res}")


@router_buttons.callback_query(ChannelCB.filter(F.action == "run_all"))
async def cb_run_all(callback: types.CallbackQuery):
    if not is_allowed(callback.from_user.id):
        return

    channels = new_chanel_service.get_all_channels_new_list()
    if not channels:
        await callback.message.answer("📭 В БД нет ни одного канала")
        await callback.answer()
        return

    text = ""
    for ch in channels:
        name = ch[1]
        try:
            res = new_chanel_service.get_channel_stat_new(name)
            await callback.bot.send_message(chat_id=ch[2], text=f"Статистика доков: {res}")
        except Exception as e:
            text += f"• {name}: ❌ ошибка\n"
            continue

        text += f"• {name}: ✅ ok\n"

    await callback.message.answer(text)
    await callback.answer("✅ Готово")
    
    
class CreateChannelFormButt(StatesGroup):
    waiting_name = State()
    waiting_channel_id = State()
    waiting_sheet_name = State()
    waiting_cell = State()
    waiting_table_link = State()
    
    
@router_buttons.callback_query(ChannelCB.filter(F.action == "create_channel"))
async def cmd_create_button(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await message.answer("Введите название (для вашего удобного использования)")
    await state.set_state(CreateChannelFormButt.waiting_name)


@router_buttons.message(CreateChannelFormButt.waiting_name)
async def get_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(name=message.text)

    await message.answer("Введите айди тг-группы, куда будет отправляться сообщение")
    await state.set_state(CreateChannelFormButt.waiting_channel_id)


@router_buttons.message(CreateChannelFormButt.waiting_channel_id)
async def get_channel_id(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(channel_id=message.text)

    await message.answer("Введите название страницы гуглы таблицы")
    await state.set_state(CreateChannelFormButt.waiting_sheet_name)


@router_buttons.message(CreateChannelFormButt.waiting_sheet_name)
async def get_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(sheet_name=message.text)

    await message.answer("Введите нужную ячейку")
    await state.set_state(CreateChannelFormButt.waiting_cell)


@router_buttons.message(CreateChannelFormButt.waiting_cell)
async def get_sheet_name(message: types.Message, state: FSMContext):
    if not is_allowed(message.from_user.id):
        return
    await state.update_data(cell=message.text)

    await message.answer("Введите ссылку на таблицу")
    await state.set_state(CreateChannelFormButt.waiting_table_link)


@router_buttons.message(CreateChannelFormButt.waiting_table_link)
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

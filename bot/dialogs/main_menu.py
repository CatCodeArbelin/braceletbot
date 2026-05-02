from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.config import TEXTS
from bot.dialogs.states import MainMenuSG


async def on_bracelets_click(_, __, manager: DialogManager):
    # Переходим в каталог браслетов.
    await manager.switch_to(MainMenuSG.catalog)


async def on_chokers_click(_, __, manager: DialogManager):
    # Переходим на экран-заглушку чокеров.
    await manager.switch_to(MainMenuSG.chokers_stub)


async def on_back_from_stub(_, __, manager: DialogManager):
    # Возвращаемся в главное меню из заглушки.
    await manager.switch_to(MainMenuSG.start)


main_menu_dialog = Dialog(
    Window(
        Const(TEXTS["start"]),
        Button(Const("браслеты✨"), id="bracelets", on_click=on_bracelets_click),
        Button(Const("чокеры✨"), id="chokers", on_click=on_chokers_click),
        state=MainMenuSG.start,
    ),
    Window(
        Const(TEXTS["chokers_stub"]),
        Button(Const("назад"), id="back_stub", on_click=on_back_from_stub),
        state=MainMenuSG.chokers_stub,
    ),
)

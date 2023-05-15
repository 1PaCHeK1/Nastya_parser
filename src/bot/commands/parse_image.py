from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from dependency_injector.wiring import Provide, inject

from core.containers import Container
from core.image.services import ImageProcessService


router = Router()


@router.message(Command("get-text"))
@inject
async def get_text_from_image_handler(
    message: types.Message,
    bot: Bot,
    image_process: ImageProcessService = Provide[Container.image_process]
):
    photos = message.photo
    if photos == []:
        return

    large_photo = photos[-1]
    file_info = await bot.get_file(str(large_photo.file_id))
    image = await bot.download_file(file_info.file_path)
    if image is None:
        return

    text = image_process.get_text_from_image(image)
    await message.reply(text)

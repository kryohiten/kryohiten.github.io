# meta developer: @ghosvxmodules
# requires: moviepy

import os
import random
import string
from moviepy.editor import ImageClip
from .. import loader, utils

@loader.tds
class ImageToGifMod(loader.Module):
    """Делает смишнявки ( гифки ) с фоточек """
    
    strings = {
        "name": "ImageToGif",
        "no_photo": "<emoji document_id=5472131451451349048>🤷‍♂️</emoji> <b>Ответьте на сообщение с пикчей</b>",
        "download_error": "<emoji document_id=5472267631979405211>🚫</emoji> <b>Ошибка при загрузке пикчи:</b> <code>{}</code>",
        "download_failed": "<emoji document_id=5472267631979405211>🚫</emoji> <b>Не удалось скачать пикчу</b>",
        "convert_error": "<emoji document_id=5472267631979405211>🚫</emoji> <b>Ошибка при конвертации:</b> <code>{}</code>",
        "processing": "<emoji document_id=5451732530048802485>⏳</emoji> <b>Обработка...</b>"
    }

    def __init__(self):
        self.name = self.strings["name"]
        
    def _generate_random_string(self, length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @loader.command()
    async def itg(self, message):
        """(ответ на фото)"""
        reply = await message.get_reply_message()

        if not reply or not reply.media:
            await utils.answer(message, self.strings["no_photo"])
            return

        await utils.answer(message, self.strings["processing"])

        random_suffix = self._generate_random_string()
        file_name = f"ghosvxitg_{random_suffix}"
        
        try:
            photo = await message.client.download_media(reply, f"downloads/{file_name}.jpg")
        except Exception as e:
            await utils.answer(message, self.strings["download_error"].format(str(e)))
            return

        if not photo or not os.path.exists(photo):
            await utils.answer(message, self.strings["download_failed"])
            return

        video_path = f"downloads/{file_name}.mp4"

        try:
            clip = ImageClip(photo).set_duration(2)
            clip.write_videofile(video_path, fps=24)
            clip.close()

            await message.client.send_file(message.chat_id, video_path)
            await message.delete()

            os.remove(photo)
            os.remove(video_path)

        except Exception as e:
            await utils.answer(message, self.strings["convert_error"].format(str(e)))
            return

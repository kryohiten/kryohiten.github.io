# meta developer: @ghosvxmodules
# requires: requests bs4

from .. import loader, utils
from bs4 import BeautifulSoup
import requests

@loader.tds
class TonBalanceCheckMod(loader.Module):
    """Чекает баланс кошелька TON"""
    
    strings = {
        "name": "TonBalanceCheck",
        "invalid_address": "<emoji document_id=5472267631979405211>🚫</emoji> Пожалуйста, укажите правильный TON адрес",
        "checking": "<emoji document_id=5188217332748527444>🔍</emoji> Проверяю баланс адреса...",
        "balance": "<emoji document_id=5827851745396527317>💎</emoji> Баланс кошелька <code>{}</code>:\n<b>{}</b> <b>{}</b>",
        "error": "<emoji document_id=5472125180799098428>😭</emoji> Произошла ошибка при получении данных"
    }

    async def tonbalcmd(self, message):
        """<адрес>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["invalid_address"])
            return

        await utils.answer(message, self.strings["checking"])
        
        try:
            url = f"https://tonviewer.com/{args}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            balance_element = soup.find('div', {'class': 'bdtytpm b1l85tie'})
            usd_element = soup.find('div', {'class': 'bdtytpm bwoofkz'})
            
            if balance_element and usd_element:
                balance = balance_element.text.strip()
                usd = usd_element.text.strip()
                await utils.answer(
                    message,
                    self.strings["balance"].format(args, balance, usd)
                )
            else:
                await utils.answer(message, self.strings["error"])
                
        except Exception as e:
            await utils.answer(message, self.strings["error"]) 

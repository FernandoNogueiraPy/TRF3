import asyncio
import aiohttp
import re

from asyncio import Task
from typing import Any

class AsyncRequestsScrapper:

    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()

    async def controler_class(self):

        list_task: list[Task[Any]] = []
        document = await self.get_document_text()
        matches = self.regex_trf3(document) 

        for match in matches:
            correct_process = match[0:7] + "-" + match[7:9] + "." + match[9:13] + "." + match[13] + "." + match[14:16] + "." + match[16:20]
            print(correct_process)
            list_task.append(asyncio.create_task(self.call_api(correct_process)))

            if len(list_task) > 50:
                await asyncio.gather(*list_task)
                list_task = []

        await asyncio.gather(*list_task)
        await self.close_session()

    async def call_api(self,id: str):

        url = f'https://addebitare-trf3-ckak5yvqwa-rj.a.run.app/trf3/v1/oficio/{id}'
       
        async with self.session.get(url=url) as response:
            if response.status == 200:
            
                data = await response.json()
                print(f"Processo: {id}, API: OK")
                    
    async def get_document_text(self):
        with open('processos.txt', 'r', encoding='utf-8') as file:
            return file.read()

    def regex_trf3(self, document: str):
        regex = r"\d{20}"
        matches = re.findall(regex, document, re.MULTILINE)
        return matches

    async def register_document(self):
        with open("controler_register.txt", "a") as file:
            file.write(f"{id}\n")
        print(f"Documento registrado com sucesso")

    async def close_session(self):
        await self.session.close()
        print("Sessão fechada com sucesso")



async def main():
    scrapper = AsyncRequestsScrapper()
    await scrapper.controler_class()


# Execute o loop de eventos para esperar que a função assíncrona 'main' seja concluída
asyncio.run(main())

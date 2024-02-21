

import asyncio
import io
import aiohttp
import json
import os

API_TOKEN = "79s8sfgdwe"
MAX_CONCURRENT_REQUESTS = 100
REQUEST_TIMEOUT = 60

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

JSON_FILE = "id_requisitados.json"

contador_sucesso = 0
contador_erro = 0

def load_requested_numbers():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as json_file:
                return set(json.load(json_file))
        except FileNotFoundError:
            return set()
    else:
        return set()


def save_requested_numbers(requested_numbers):
    with open(JSON_FILE, "w") as json_file:
        json.dump(list(requested_numbers), json_file)


async def fetch(session, url, number, timeout=REQUEST_TIMEOUT):
    global contador_sucesso, contador_erro

    async with semaphore:
        try:
            async with session.get(url, headers={
                "accept": "application/json",
                "Authorization": f"Bearer {API_TOKEN}"
            }, timeout=timeout) as response:
                if response.status == 200:
                    contador_sucesso += 1
                    content_type = response.headers.get("Content-Type", "").lower()
                    if "application/json" in content_type:
                        data = await response.json()
                        print(f"Processo: {number}, API: OK")
                        requested_numbers.add(number)
                        save_requested_numbers(requested_numbers)
                    else:
                        print(f"Processo: {number}, Erro: Resposta com Content-Type inesperado: {content_type}")
                else:
                    contador_erro += 1
                    print(f"Processo: {number}, Erro: Status de resposta não 200: {response.status}")
        except asyncio.TimeoutError:
            contador_erro += 1
            print(f"Processo: {number}, Erro: Timeout (Tempo Limite Excedido)")
        except aiohttp.ClientError as e:
            contador_erro += 1
            print(f"Processo: {number}, Erro: {e}")


def read_process_numbers_from_file(file_path):
    process_numbers = []
    with open(file_path, "r") as txt_file:
        for line in txt_file:
            process_numbers.append(line.strip())
    return process_numbers


async def process_and_request_numbers(process_numbers):
    connector = aiohttp.TCPConnector(limit_per_host=MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for number in process_numbers:
            if number not in requested_numbers:
                tasks.append(fetch(session, f"http://34.67.110.142:8080/search/background/{number}", number))
                await asyncio.sleep(1)  
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    requested_numbers = load_requested_numbers()
    file_path = "ids.txt"
    process_numbers = read_process_numbers_from_file(file_path)

    if not process_numbers:
        print("Nenhum número de processo encontrado no arquivo.")
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(process_and_request_numbers(process_numbers))
        
    print(f"Requisições com sucesso: {contador_sucesso}")
    print(f"Requisições com erro: {contador_erro}")
import requests
import json
import base64
import logging
import mimetypes
import random
import time
from typing import Dict, List
from colorama import init, Fore, Style

# Initialize colorama
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = 'https://cluster.apigratis.com/api/v2/whatsapp/sendFile64'
DEVICE_TOKEN = 'SEU DEVICE TOKEN'
AUTH_TOKEN = 'Bearer SEUTOKEN'

def read_phone_numbers(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except IOError as e:
        logger.error(f"Error reading the numbers file: {e}")
        return []

def image_to_base64(image_path: str) -> str:
    try:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            raise ValueError(f"Unable to determine MIME type for {image_path}")
        
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded}"
    except (IOError, ValueError) as e:
        #logger.error(f"Error processing the image: {e}")
        return ""

def send_whatsapp_message(number: str, text: str, image_base64: str) -> Dict:
    headers = {
        'Content-Type': 'application/json',
        'DeviceToken': DEVICE_TOKEN,
        'Authorization': AUTH_TOKEN
    }
    
    data = {
        'number': number,
        'path': image_base64,
        'caption': text
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return {'success': True, 'number': number}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'number': number}

def main():
    numbers_file = 'numeros.txt'
    image_file = './img/a.jpeg'
    message_text = (
        "📢 OFERTA ESPECIAL DE CRÉDITO 📢\n\n"
        "Dinheiro rápido e sem complicação para quem recebe Bolsa Família,\n"
        "BPC/LOAS ou quer empréstimo na conta de luz! 🚀\n\n"
        "✅ Até R$ 2.000,00 na sua conta de forma simples e rápida!\n"
        "✅ Parcelas que cabem no seu bolso, sem burocracia.\n"
        "✅ Aprovação fácil e sem consulta ao SPC/Serasa!\n\n"
        "👉 Aproveite essa oportunidade e realize seus planos hoje mesmo!\n\n"
        "📞 Responda \"QUERO\" e te ajudamos a liberar o crédito agora!"
    )
    
    print(f"{Fore.GREEN}*************************************{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**       WhatsApp Messenger        **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}** Disparador de mensagens com     **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}** imagem e descrição WhatsApp     **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}*************************************{Style.RESET_ALL}")
    print(f"{Fore.GREEN}** Powered by Julio Rodrigues 2024 **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**    WhatsApp: +55 75991625816    **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**    Gmail: massabig48@gmail.com  **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}*************************************{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**             COMANDOS            **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**Use: python zap.py para iniciar  **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}**Use:     Ctrl+C para parar       **{Style.RESET_ALL}")
    print(f"{Fore.GREEN}*************************************{Style.RESET_ALL}")

    phone_numbers = read_phone_numbers(numbers_file)
    if not phone_numbers:
        print("No valid phone numbers found.")
        return

    image_base64 = image_to_base64(image_file)
    if not image_base64:
        print("Failed to convert image to Base64.")
        return

    allowed_numbers = []
    denied_numbers = []

    try:
        for number in phone_numbers:
            result = send_whatsapp_message(number, message_text, image_base64)
            if result['success']:
                print(f"{Fore.GREEN}Allow: {number}{Style.RESET_ALL}")
                allowed_numbers.append(number)
            else:
                print(f"{Fore.CYAN}Deny: {number}{Style.RESET_ALL}")
                denied_numbers.append(number)

            delay = random.randint(1, 2)
            print(f"Waiting {delay} seconds...")
            time.sleep(delay)

    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Programa interrompido pelo usuário.{Style.RESET_ALL}")
    
    finally:
        print(f"\n{Fore.CYAN}Salvando números permitidos...{Style.RESET_ALL}")
        with open('allowed.txt', 'w') as f:
            for number in allowed_numbers:
                f.write(f"{number}\n")

        print(f"{Fore.GREEN}Programa encerrado.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

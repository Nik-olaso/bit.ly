import os
import requests
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv


def shorten_link(apikey, user_url):
    headers = {
        "Authorization" : f"Bearer {apikey}"
    }
    params = {
        "long_url" : user_url
    }
    response_shorten = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=headers, json=params)
    response_shorten.raise_for_status()
    return response_shorten.json()["id"]


def count_clicks(apikey, bitlink):
    url_summary = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {
        "Authorization" : f"Bearer {apikey}"
    }
    response_sum = requests.get(url_summary, headers = headers)
    response_sum.raise_for_status()
    bitlink_sum = response_sum.json()["total_clicks"]
    return bitlink_sum


def is_bitlink(apikey, bitlink):
    bitlink_response = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"

    headers = {
        "Authorization" : f"{apikey}",
    }

    response_bitlink = requests.get(bitlink_response, headers = headers)
    return response_bitlink.ok


def main():
    load_dotenv()
    apikey = os.environ['BITLY_APIKEY']
    parser = argparse.ArgumentParser(
        description='Выдает сокращенную ссылку или показывает сколько было переходов по сокращенной ссылке!'
    )
    parser.add_argument('user_url', help='Введите ссылку для сокращения или битлинк:\n')
    args = parser.parse_args()
    print(args.user_url)
    parse_url = urlparse(args.user_url)
    new_url = f"{parse_url.netloc}{parse_url.path}"
    try: 
        if is_bitlink(apikey, new_url):
            print(f"Количество переходов по ссылкам: {count_clicks(apikey, new_url)}")
        else:
            print(f"Битлинк: {shorten_link(apikey, args.user_url)}")
    except requests.exceptions.HTTPError:
        print("*Ошибка, возможно вы ввели неправильную ссылку, или же вы не имеете доступа к битлинку!*")


if __name__ == "__main__":    
    main()

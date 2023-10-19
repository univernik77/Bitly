from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse
import requests
import os


def is_bitlink(token, url):
    parsed_url = urlparse(url)
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.netloc}{parsed_url.path}',
                            headers={'Authorization': f'Bearer {token}'})
    return response.ok


def shorten_link(token, url):
    payload = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers={'Authorization': f'Bearer {token}'},
                             json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    parsed_url = urlparse(link)
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{parsed_url.netloc}{parsed_url.path}/clicks/summary',
        headers={'Authorization': f'Bearer {token}'})
    response.raise_for_status()
    return response.json()['total_clicks']


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    parser = argparse.ArgumentParser(description='Возвращает короткую ссылку или количество переходов')
    parser.add_argument('url', help='Введите ссылку или короткую ссылку')
    input_url = parser.parse_args().url
    try:
        if is_bitlink(bitly_token, input_url):
            print(f'По вашей ссылке перешли {count_clicks(bitly_token, input_url)} раз(а)')
        else:
            print(f'Битлинк: {shorten_link(bitly_token, input_url)}')
    except requests.exceptions.HTTPError:
        print('"Вы ввели неправильную ссылку или неверный токен."')


if __name__ == "__main__":
    main()

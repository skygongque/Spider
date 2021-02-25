import requests
import json


# 校验cookie ci_session 为服务器直接返回使用保持会话 requests.Session()
s = requests.Session()
general_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
s.headers.update(general_header)


def get_session_code(chapter_id):
    url = "https://www.ciweimao.com/chapter/ajax_get_session_code"

    payload = f"chapter_id={str(chapter_id)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': f'https://www.ciweimao.com/chapter/{str(chapter_id)}',
    }
    # 有对Referer进行校验
    response = s.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()


def get_book_chapter_detail_info(chapter_id, chapter_access_key):
    url = "https://www.ciweimao.com/chapter/get_book_chapter_detail_info"

    payload = f"chapter_id={str(chapter_id)}&chapter_access_key={chapter_access_key}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': f'https://www.ciweimao.com/chapter/{str(chapter_id)}',
    }
    response = s.post(url, data=payload, headers=headers)
    return response.json()


def decrypt_content(e, access_key):
    e['access_key'] = access_key
    response = requests.post('http://localhost:3000/decrypt', data=e)
    if response.status_code == 200:
        return response.text


def main():
    # chapter_id = 103759082
    chapter_id = 100329088
    session_code = get_session_code(chapter_id)
    chapter_access_key = session_code['chapter_access_key']
    encrypt_content = get_book_chapter_detail_info(
        chapter_id, chapter_access_key)
    content = decrypt_content(encrypt_content, chapter_access_key)
    print(content)

if __name__ == "__main__":
    main()

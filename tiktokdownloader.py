def download_tiktok_video(link, id):
    from bs4 import BeautifulSoup
    from urllib.request import urlopen
    import requests
    from time import sleep
    import savevideo

    try:
        headers = {
            'authority': 'ssstik.io',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'hx-current-url': 'https://ssstik.io/en',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/en',
            'sec-ch-ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        }
        
        params = {
            'url': 'dl',
        }
        
        data = {
            'id': link,
            'locale': 'en',
            'tt': 'NHBveDE5',
        }
        
        sleep(2)
        response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
        download = BeautifulSoup(response.text, 'lxml')
        sleep(2)
        videolink = download.find('a')['href']
        print(videolink)
        status = savevideo.savevideofile(videolink, id)
        return [status["status"], videolink, status['path']]
    except Exception as e:
        return f"An error occurred: {e}"
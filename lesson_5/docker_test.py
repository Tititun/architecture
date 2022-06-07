import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30',
}

data = {
    'category_name': 'Тармпампам',
    'category_id': '3',
}

response = requests.post('http://127.0.0.1:8001/category_edit', headers=headers, data=data)

print(response.content[0])
print(response.status_code)
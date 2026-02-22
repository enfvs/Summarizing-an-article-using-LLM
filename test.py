import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload={
  'scope': 'GIGACHAT_API_PERS'
}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': 'bfed4f2a-96a4-4997-9e32-63eb39c1568a',
  'Authorization': 'Basic MDE5YTkxM2QtMDUyYy03MjAzLTk4ZjktZWZlZmUzYTViZmY3OjIzOWI1ZGQzLTA0NzgtNGQ0MC05ODI4LTRlNDQ0NzEwZGQ0ZQ=='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)


print(response.text)

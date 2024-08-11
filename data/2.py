import requests

url = "https://ebank.mbbank.com.vn/corp/bulk/v2/uploadFile"

payload = {'param': '{"refNo":"TAOLENH-2024080718051097","sessionId":"0694a231-70c4-4daf-b3c3-b8c20366ace2","serviceCode":"GCM_MFT_PROLL"}'}
files = {
    'file': ('transfer_1722894017.xlsx', open('upload_files/transfer_1722894017.xlsx', 'rb'), 'applic123ation/vnd.openxmlformats-officedocument.spreadsheetml.sheet1')
}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
  'Accept': 'application/json',
  'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Authorization': 'Bearer 0694a231-70c4-4daf-b3c3-b8c20366ace2',
  'biz-tracking': '/cp/mass-payment/bulk-payment/create-bulk-transaction/1',
  'biz-version': '1.02082024.1680',
  'biz-platform': 'biz-1.0',
#   'biz-trace-id': 'dbb739fe-9b87-4b51-af53-2b8763291d0a',
#   'elastic-apm-traceparent': '00-326997b8c57997d44d906e5d90665fea-b4c9e6a3bd05cf9f-01',
  'Origin': 'https://ebank.mbbank.com.vn',
  'Connection': 'keep-alive',
  'Referer': 'https://ebank.mbbank.com.vn/cp/mass-payment/bulk-payment/create-bulk-transaction',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)

import requests

url = "https://ebank.mbbank.com.vn/corp/bulk/v2/uploadFile"

payload = {'param': '{"refNo":"TAOLENH-2024080710223576","sessionId":"409d5b23-223e-41ea-83ba-ade45749ea78","serviceCode":"GCM_MFT_PROLL"}'}
files=[
  ('file',('file',open('upload_files\\transfer_1722894017.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
]
headers = {
  'Accept': 'application/json',
  'Accept-Language': 'en-US,en;q=0.9',
  'Authorization': 'Bearer 409d5b23-223e-41ea-83ba-ade45749ea78',
  'Connection': 'keep-alive',
  # 'Cookie': '_ga_R3XMN343KH=GS1.1.1720915196.2.0.1720915196.60.0.0; _ga_T1003L03HZ=GS1.1.1722705028.15.1.1722706676.0.0.0; _ga=GA1.1.141508142.1718963010; BIGipServerk8s_rsocket-broker_pool_11009=1696334090.299.0000; BIGipServerapm_live_pool_8200=3189506314.2080.0000; _ga_QFJ32LKGHD=GS1.1.1722992517.17.1.1722994600.0.0.0; EBANKCORP=!4wAPGkzSKA2kNSbZV75WosIyWRQyhUB3XLioC6IRsPk2F1Aa4sOz196X4/pTW7y5DdGPHnKqyQP80+M=; MB01c18e05=01bb14ea42aa03e28cf75bfe135bf3d591587f7833979e608724d4764e856d675d588244c00e8f87c8f79af8117b08c16dca2e33a7cde7e7d21b842c008aec7cb30c5a594beda878c0c3054fb8bdf665c92356f19d; EBANKCORP=!g+BKBUx0+zxWfeTZV75WosIyWRQyhUJun+IBJPq3PbkCEMwAGxeIvePweUJ+I+wf/fwHPHjAEPQs; MB01c18e05=01bb14ea424d03d043e0715cb506cf30f91623400b63c531bb5cf453f4d4e9d2a1c4fe2db1a1ed84c981100cbb130ba1a427030ba19d66640ad640ff44da34de8bbe9c0978c24499d18ccc0ef1fcf8b966541fb558',
  'Origin': 'https://ebank.mbbank.com.vn',
  'Referer': 'https://ebank.mbbank.com.vn/cp/mass-payment/bulk-payment/create-bulk-transaction',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
  'biz-platform': 'biz-1.0',
  'biz-tracking': '/cp/mass-payment/bulk-payment/create-bulk-transaction/1',
  'biz-version': '1.02082024.1680',
  # 'elastic-apm-traceparent': '00-3bb4e386af715f02402ffee84fd72b32-78c2f987ae75bea6-01',
  'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)

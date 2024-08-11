
import hashlib
import requests
import json
import base64
import random
import string
import os
import time
from datetime import datetime
import pandas as pd
import unidecode
import logging
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import uvicorn
import sys
import traceback
from starlette.responses import Response

def setup_logger(file_name):
    current_date = datetime.now().strftime("%Y/%m/%d")
    current_date_2 = datetime.now().strftime("%d_%m_%Y")
    log_folder_path = os.path.join('logs', current_date)

    os.makedirs(log_folder_path, exist_ok=True)

    log_file_path = os.path.join(log_folder_path, f"{file_name}-{current_date_2}.log")
    
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d | %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
    
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(str(file_name))  # Use thread identifier as the logger name
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
def convert_to_uppercase_no_accents(text):
    # Remove accents
    no_accents = unidecode.unidecode(text)
    # Convert to uppercase
    return no_accents.upper()
error_data = []
banks_mapping = {
    "MB": "MB - Ngan hang TMCP Quan Doi",
    "BANGKOK": "BANGKOK - Ngan hang Bangkok Bank tai Viet Nam CN TP HCM",
    "BIDC": "BIDC - Ngan hang Dau Tu va Phat trien Campuchia tai Viet Nam CN TP HCM",
    "BNP PARIBAS": "BNP PARIBAS - Ngan hang BNP Paribas tai Viet Nam CN TP HCM",
    "CCB": "CCB - Ngan hang China Construction Bank tai Viet Nam CN TP HCM",
    "CHINA": "CHINA - Ngan hang Bank Of China tai Viet Nam CN TP HCM",
    "CHINATRUST": "CHINATRUST - Ngan hang Chinatrust Commercial Bank (Dai Loan) tai Viet Nam CN TP HCM",
    "CHINESE": "CHINESE - Ngan hang Oversea-Chinese Banking Corp (OCBC) tai Viet Nam CN TP HCM",
    "CIMB": "CIMB - Ngan hang TNHH MTV CIMB tai Viet Nam CN Ha Noi",
    "CIMB_HCM": "CIMB - Ngan hang TNHH MTV CIMB tai Viet Nam CN TP HCM",
    "CITIBANK": "CITIBANK - Ngan hang Citibank tai Viet Nam CN Ha Noi",
    "CITIBANK_HCM": "CITIBANK - Ngan hang Citibank tai Viet Nam CN TP HCM",
    "COMERCIAL": "COMERCIAL - Ngan hang First Commercial Bank CN Ha Noi",
    "COMMUNICATION": "COMMUNICATION - Ngan hang Bank Of Communications tai Viet Nam CN TP HCM",
    "DBS": "DBS - Ngan hang DBS Bank Limited tai Viet Nam CN TP HCM",
    "DEUTSCHE": "DEUTSCHE - Ngan hang Deutsche Bank tai Viet Nam CN TP HCM",
    "ESUN": "ESUN - Ngan hang E.Sun Commercial Bank (Dai Loan) tai Viet Nam CN Dong Nai",
    "HLBVN": "HLB - Ngan hang Hong Leong Viet Nam Hoi so chinh",
    "HSBC": "HSBC - Ngan hang TNHH MTV HSBC (Viet Nam)",
    "HUA NAN": "HUA NAN - Ngan hang Hua Nan Commercial Bank, Ltd (Dai Loan) tai Viet Nam CN TP HCM",
    "IBK": "IBK - Ngan hang Industrial Bank Of Korea (Han Quoc) tai Viet Nam CN Ha Noi",
    "ICBC": "ICBC - Ngan hang Industrial and Commercial Bank of China Limited tai Viet Nam CN Ha Noi",
    "INDIA": "INDIA - Ngan hang Bank Of India (An Do) tai Viet Nam CN TP HCM",
    "KOOKMIN_HCM": "KOOKMIN - Ngan hang Kookmin Bank (Han Quoc) tai Viet Nam CN TP HCM",
    "KOREA": "KOREA - Ngan hang KEB HANA (Han Quoc) tai Viet Nam CN Ha Noi",
    "MAYBANK": "MAYBANK - Ngan hang Maybank tai Viet Nam CN Ha Noi",
    "MCB": "MCB - Ngan hang JP Morgan Chase Bank (My) tai Viet Nam CN TP HCM",
    "MIZUHO": "MIZUHO - Ngan hang Mizuho tai Viet Nam CN Ha Noi",
    "MIZUHO_HCM": "MIZUHO - Ngan hang Mizuho tai Viet Nam CN TP HCM",
    "NATIXIS": "NATIXIS - Ngan hang Natixis Banque BPCE (Phap) tai Viet Nam CN TP HCM",
    "Nong Hyup": "Nong Hyup - Ngan hang Nonghyup Bank CN Ha Noi",
    "SHANGHAI": "SHANGHAI - Ngan hang The Shanghai Commercial And Savings tai Viet Nam CN Dong Nai",
    "SHBVN": "SHBVN - Ngan hang TNHH MTV SHINHAN Viet Nam Hoi So Chinh",
    "SIAM": "SIAM - Ngan hang Commercial Siam Bank tai Viet Nam CN TP HCM",
    "SMBC": "SMBC - Ngan hang Sumitomo Mitsui Banking Corporation (SMBC) tai Viet Nam CN Ha Noi",
    "SMBC_HCM": "SMBC - Ngan hang Sumitomo Mitsui Banking Corporation (SMBC) tai Viet Nam CN TP HCM",
    "STANDARDCHARTERED": "STANDARDCHARTERED - Ngan hang Standard Chartered tai Viet Nam Hoi so chinh",
    "SinoPac": "SinoPac - Ngan hang Bank Sinopac (Dai Loan) tai Viet Nam CN TP HCM",
    "TAIPEI_HCM": "TAIPEI - Ngan hang Taipei Fubon Commercial Bank Co Ltd CN TP HCM",
    "TokyoMitsubishiHN": "TokyoMitsubishiHN - Ngan hang MUFG Bank tai Viet Nam CN Ha Noi",
    "UOB": "UOB - Ngan hang United Overseas tai Viet Nam Hoi so CN TP HCM",
    "KOREA_HCM": "KOREA - Ngan hang KEB Hana CN TP HCM",
    "MAYBANK_HCM": "MAYBANK - Ngan hang Malayan Banking Berhad CN TP HCM",
    "MegaICBC": "MegaICBC - Ngan hang Mega International Commercial Bank Co., Ltd tai Viet Nam CN TP HCM",
    "PBVN": "VID - Ngan hang Public Bank Viet Nam Hoi so chinh",
    "WVN": "Woori - Ngan hang Woori Bank tai Viet Nam Hoi so chinh",
    "BIDC": "BIDC - Ngan hang Dau Tu va Phat trien Campuchia tai Viet Nam CN Ha Noi",
    "Busan": "Busan - Ngan hang Busan (Han Quoc) tai Viet Nam CN TP HCM",
    "BNP PARIBAS": "BNP PARIBAS - Ngan hang BNP Paribas tai Viet Nam CN Ha Noi",
    "COMERCIAL": "COMERCIAL - Ngan hang First Commercial Bank CN TP HCM",
    "HLB": "HLB - Ngan hang Hong Leong Viet Nam PGD Cho Lon",
    "IBK": "IBK - Ngan hang Industrial Bank Of Korea (Han Quoc) tai Viet Nam CN TP HCM",
    "KOOKMIN": "KOOKMIN - Ngan hang Kookmin Bank (Han Quoc) tai Viet Nam CN Ha Noi",
    "TokyoMitsubishiHCM": "TokyoMitsubishiHCM - Ngan hang MUFG Bank tai Viet Nam CN TP HCM",
    "TAIPEI": "TAIPEI - Ngan hang Taipei Fubon Commercial Bank Co Ltd CN Ha Noi",
    "TCB": "TCB - Ngan hang TMCP Ky Thuong Viet Nam",
    "ABBANK": "ABBANK - Ngan hang TMCP An Binh",
    "VIB": "VIB - Ngan hang TMCP Quoc Te",
    "EIB": "EIB - Ngan hang TMCP Xuat Nhap Khau Viet Nam",
    "MSB": "MSB - Ngan hang TMCP Hang Hai Viet Nam",
    "SHB": "SHB - Ngan hang TMCP Sai Gon - Ha Noi",
    "TPB": "TPB - Ngan hang TMCP Tien Phong",
    "GPB": "GPB - Ngan hang TM TNHH MTV Dau Khi Toan Cau",
    "HDB": "HDB - Ngan hang TMCP Phat trien TP Ho Chi Minh",
    "OJB": "OJB - Ngan hang TM TNHH MTV Dai Duong",
    "BVB": "BVB - Ngan hang TMCP Bao Viet",
    "NCB": "NCB - Ngan hang TMCP Quoc Dan",
    "BIDV": "BIDV - Ngan hang TMCP Dau Tu va Phat trien Viet Nam",
    "VPB": "VPB - Ngan hang TMCP Viet Nam Thinh Vuong",
    "VAB": "VAB - Ngan hang TMCP Viet A",
    "OCB": "OCB - Ngan hang TMCP Phuong Dong",
    "VIETINBANK": "VIETINBANK - Ngan hang TMCP Cong Thuong Viet Nam",
    "SEAB": "SEAB - Ngan hang TMCP Dong Nam A",
    "SCB": "SCB - Ngan hang TMCP Sai Gon",
    "LPB": "LPB - Ngan hang TMCP Buu Dien Lien Viet",
    "DAB": "DAB - Ngan hang TMCP Dong A",
    "NASB": "NASB - Ngan hang TMCP Bac A",
    "VBA": "VBA - Ngan hang Nong Nghiep va Phat Trien Nong Thon Viet Nam",
    "SGB": "SGB - Ngan hang TMCP Sai Gon Cong Thuong",
    "VIETBANK": "VIETBANK - Ngan hang TMCP Viet Nam Thuong Tin",
    "VCCB": "VCCB - Ngan hang TMCP Ban Viet",
    "KLB": "KLB - Ngan hang TMCP Kien Long",
    "PGB": "PGB - Ngan hang TMCP Xang Dau Petrolimex",
    "PVC": "PVC - Ngan hang TMCP Dai Chung Viet Nam",
    "VRB": "VRB - Ngan hang Lien Doanh Viet - Nga",
    "ACB": "ACB - Ngan hang TMCP A Chau",
    "ANZ": "ANZ - Ngan hang TNHH MTV ANZ (Viet Nam)",
    "CCF": "CCF - Ngan hang Hop Tac Xa Viet Nam",
    "CSXH": "CSXH - Ngan hang Chinh sach Xa hoi",
    "TRUSTBANK": "TRUSTBANK - Ngan hang TM TNHH MTV Xay Dung",
    "VCB": "VCB - Ngan hang TMCP Ngoai Thuong Viet Nam",
    "VDB": "VDB - Ngan hang Phat trien Viet Nam",
    "NAMABANK": "NAMABANK - Ngan hang TMCP Nam A",
    "IVB": "IVB - Ngan hang TNHH Indovina",
    "STB": "STB - Ngan hang TMCP Sai Gon Thuong Tin"
}
def convert_bank_code(data):
    for item in data:
        item['benName'] = convert_to_uppercase_no_accents(item['benName'])
        if item['bankCode'] in banks_mapping:
            item['bankCode'] = banks_mapping[item['bankCode']]
        else:
            print(error_data)
            error_data.append(item)
    for item in error_data:
        data.remove(item)
    return data
def generate_upload_file_error(data):
    if not data:
        return None
    df_output = pd.DataFrame(data)
    # Map the data to the structure of the input Excel file
    df_output_formatted = pd.DataFrame({
        'STT': range(1, len(df_output) + 1),  # Adding STT column
        'So tai khoan': df_output['benAccount'],
        'Ho va ten': df_output['benName'],
        'Ngan hang': df_output['bankCode'],
        'So tien': df_output['amount'],  # Placeholder        
        'Dien giai': df_output['description'],
        'Error': df_output['message_details'],
    })

    # File path to save the new Excel file
    time_stamp = datetime.now().strftime("%Y%m%d%H%M")
    output_excel_file = f'generated_files/transfer_error_{time_stamp}.xlsx'

    # Write the DataFrame to an Excel file
    df_output_formatted.to_excel(output_excel_file, index=False)
    return output_excel_file
def generate_upload_file_success(data):
    if not data:
        return None
    data = convert_bank_code(data)
    df_output = pd.DataFrame(data)
    # Map the data to the structure of the input Excel file
    df_output_formatted = pd.DataFrame({
        'STT': range(1, len(df_output) + 1),  # Adding STT column
        'So tai khoan': df_output['benAccount'],
        'Ho va ten': df_output['benName'],
        'Ngan hang': df_output['bankCode'],
        'So tien': df_output['amount'],  # Placeholder        
        'Dien giai': df_output['description'],
    })

    # File path to save the new Excel file
    time_stamp = datetime.now().strftime("%Y%m%d%H%M")
    output_excel_file = f'generated_files/transfer_success_{time_stamp}.xlsx'

    # Write the DataFrame to an Excel file
    df_output_formatted.to_excel(output_excel_file, index=False,startrow=1)
    with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
        df_output_formatted.to_excel(writer, index=False, startrow=1)
        
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        
        worksheet.write('A1', '')  
        worksheet.write('B1', 'DANH SÁCH GIAO DỊCH(LIST OF TRANSACTIONS)')
    return output_excel_file


class MBBANK:
    def __init__(self,corpId, username, password, account_number):
        proxy_list=None
        with open('proxies.txt', 'r') as file:
            proxy_list = [line.strip() for line in file if line.strip()]
        proxy_list = proxy_list if proxy_list else None
        self.proxy_list = proxy_list
        if self.proxy_list:
            self.proxy_info = self.proxy_list.pop(0)
            proxy_host, proxy_port, username_proxy, password_proxy = self.proxy_info.split(':')
            self.proxies = {
                'http': f'socks5://{username_proxy}:{password_proxy}@{proxy_host}:{proxy_port}',
                'https': f'socks5://{username_proxy}:{password_proxy}@{proxy_host}:{proxy_port}'
            }
        else:
            self.proxies = None
        self.error_messages = {
            "INNO_ERR_01": "Please enter complete information",
            "INNO_ERR_02": "Invalid data",
            "INNO_ERR_03": "Beneficiary bank code not found",
            "INNO_ERR_04": "Beneficiary bank not found",
            "INNO_ERR_05": "Beneficiary bank branch not found",
            "INNO_ERR_06": "Incorrect format",
            "INNO_ERR_07": "Negative amount not allowed",
            "INNO_ERR_08": "Exceeded allowed number of characters",
            "INNO_ERR_09": "Please enter an amount between 1 VND and 10,000,000,000,000 VND",
            "INNO_ERR_11": "Please enter an amount between 1 VND and 10,000,000,000,000 VND",
            "INNO_ERR_111": "Duplicate account number",
            "INNO_ERR_112": "Duplicate information with source account number not allowed",
            "INNO_ERR_113": "The system does not support transactions with this card number according to international card organization regulations.",
            "INNO_ERR_114": "Beneficiary name does not match the data returned by the system. Please check the account number and beneficiary name and correct them if necessary",
            "INNO_ERR_115": "Unable to verify, please check later or continue the transaction",
            "INNO_ERR_116": "Account does not exist",
            "INNO_ERR_117": "Currency accounts are not allowed for transactions",
            "INNO_ERR_118": "Amount exceeds the allowed limit",
            "INNO_ERR_119": "The beneficiary account must be a payment account",
            "INNO_ERR_120": "Minimum amount is 1 million VND per beneficiary account",
            "INNO_ERR_121": "Unable to verify",
            "INNO_ERR_124": "Duplicate invoice number",
            "INNO_ERR_125": "Buyer’s tax code does not match the corporation's tax code",
            "INNO_ERR_126": "Buyer’s tax code duplicates the seller’s tax code",
            "INNO_ERR_127": "Loan amount exceeds the invoice amount",
            "INNO_ERR_128": "No payment disbursement for related parties.",
            "INNO_ERR_140": "Disbursed amount at other banks exceeds the invoice amount",
            "INNO_ERR_141": "Invoice does not exist",
            "INNO_ERR_142": "Invoice has been adjusted",
            "INNO_ERR_143": "Invoice has been replaced",
            "INNO_ERR_144": "Invoice has been canceled",
            "INNO_ERR_145": "Please check again",
            "INNO_ERR_146": "Disbursed amount exceeds the remaining disbursement amount"
        }
        self.session = requests.Session()
        self.is_login = False
        self.file = f"data/{username}.txt"
        self.url = {
    "getCaptcha": "https://ebank.mbbank.com.vn/corp/common/generateCaptcha",
    "login": "https://ebank.mbbank.com.vn/corp/common/do-login-v2",
    "getHistories": "https://ebank.mbbank.com.vn/corp/transaction/v2/getTransactionHistoryV3",
    "getlistAccount": "https://ebank.mbbank.com.vn/corp/balance/v2/getBalance",
    "uploadFile": "https://ebank.mbbank.com.vn/corp/bulk/v2/uploadFile",
    "checkBulkProcess": "https://ebank.mbbank.com.vn/corp/bulk/v2/checkBulkProcess",
    "getBulkTransaction": "https://ebank.mbbank.com.vn/corp/bulk/v2/getBulkTransaction",
    "checkNameBulkFile": "https://ebank.mbbank.com.vn/corp/bulk/v2/check-name",
    "checkNameStatus": "https://ebank.mbbank.com.vn/corp/checkname/checkNameStatus",
    "verifyBulk": "https://ebank.mbbank.com.vn/corp/bulk/v2/verifyBulk",
    "saveBulk": "https://ebank.mbbank.com.vn/corp/bulk/v2/saveBulk",
}
        self.lang = 'VN'
        self._timeout = 60
        self.appVersion = ""
        self.clientOsVersion = "WINDOWS"
        self.browserVersion = "126.0.0.0"
        self.browserName = "Edge"
        self.deviceCode = ""
        self.deviceName = "" 
        self.checkAcctPkg = "1"
        self.captcha1st = ""
        self.challenge = ""
        if not os.path.exists(self.file):
            self.username = username
            self.password = password
            self.account_number = account_number
            self.corpId = corpId
            self.sessionId = ""
            self.deviceId = ""
            self.refNo = ""
            self.mobileId = ""
            self.clientId = ""
            self.cif = ""
            self.res = ""
            self.browserToken = ""
            self.browserId = ""
            self.E = ""
            self.tranId = ""
            self.accountName = ""
            self.browserId = hashlib.md5(self.username.encode()).hexdigest()
            self.save_data()
            
        else:
            self.parse_data()
            self.username = username
            self.password = password
            self.account_number = account_number
            self.corpId = corpId
        self.init_guid()
    def save_data(self):
        data = {
            
            'corpId': self.corpId,
            'username': self.username,
            'password': self.password,
            'account_number': self.account_number,
            'sessionId': getattr(self, 'sessionId', ''),
            'mobileId': getattr(self, 'mobileId', ''),
            'clientId': self.clientId,
            'cif': getattr(self, 'cif', ''),
            'E': getattr(self, 'E', ''),
            'res': getattr(self, 'res', ''),
            'tranId': getattr(self, 'tranId', ''),
            'browserToken': getattr(self, 'browserToken', ''),
            'browserId': self.browserId,
            'refNo': self.refNo,
            'deviceId': self.deviceId,
            'accountName': self.accountName,
            
        }
        with open(self.file, 'w') as f:
            json.dump(data, f)

    def parse_data(self):
        with open(self.file, 'r') as f:
            data = json.load(f)
        self.corpId = data.get('corpId', '')    
        self.username = data.get('username', '')
        self.password = data.get('password', '')
        self.account_number = data.get('account_number', '')
        self.sessionId = data.get('sessionId', '')
        self.mobileId = data.get('mobileId', '')
        self.clientId = data.get('clientId', '')
        self.token = data.get('token', '')
        self.accessToken = data.get('accessToken', '')
        self.cif = data.get('cif', '')
        self.res = data.get('res', '')
        self.tranId = data.get('tranId', '')
        self.browserToken = data.get('browserToken', '')
        self.browserId = data.get('browserId', '')
        self.E = data.get('E', '')
        self.refNo = data.get('refNo', '')
        self.deviceId = data.get('deviceId', '')
        self.accountName = data.get('accountName', '')
    def init_guid(self):
        self.refNo = self.make_ref_no(self.username)
        self.deviceId = "9bf859cabf682d737516bafba5c6d051"
        self.save_data()
        
    def random_trace_id(self):
        hex_digits = "0123456789abcdef"
        trace_id = ''.join(random.choice(hex_digits) for _ in range(16))
        return str(int(trace_id, 16))
    
    def createTaskCaptcha(self, base64_img):
        url_0 = 'https://mbbiz.pay2world.vip/predict'
        url_1 = 'https://captcha.pay2world.vip//mbbiz'
        url_2 = 'https://captcha1.pay2world.vip//mbbiz'
        url_3 = 'https://captcha2.pay2world.vip//mbbiz'
        
        payload = json.dumps({
        "image_base64": base64_img
        })
        headers = {
        'Content-Type': 'application/json'
        }
        
        for _url in [url_0,url_1, url_2, url_3]:
            try:
                response = requests.request("POST", _url, headers=headers, data=payload, timeout=10)
                if response.status_code in [404, 502]:
                    continue
                return json.loads(response.text)
            except:
                continue
        return {}
    
    def make_ref_no(self,user_id=None):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-4]  # This will truncate to 6 digits for the microseconds
        if user_id:
            return f"{user_id}-{timestamp}"
        return f"TAOLENH-{timestamp}"
    
    def generate_captcha(self):
        url = self.url['getCaptcha']
        payload = {
            'deviceId': self.deviceId,
            'refNo': self.refNo
        }
        response = self.curlPost(url,data=payload)
        return (response)
        
    def solveCaptcha(self):
        generate_captcha = self.generate_captcha()
        if 'encryptedCaptcha' in generate_captcha:
            self.encryptedCaptcha = generate_captcha['encryptedCaptcha']
            base64_captcha_img = generate_captcha['imageBase64']
        else:
            return {"status": False, "msg": "Error generate_captcha"}
        result = self.createTaskCaptcha(base64_captcha_img)
        if 'prediction' in result and result['prediction']:
            captcha_value = result['prediction']
            return {"status": True,  "captcha": captcha_value}
        else:
            return {"status": False, "msg": "Error solve captcha", "data": result}

    def curlPost(self, url, data,headers = None, files = None,jsontype = False):
        if not headers:
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://ebank.mbbank.com.vn/cp/pl/login',
            'Origin': 'https://ebank.mbbank.com.vn',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'biz-tracking': '/cp/pl/login/1',
            'biz-version': '1.02082024.1680',
            'biz-platform': 'biz-1.0',
            'Content-Type': 'application/json; charset=utf-8',
            'X-Request-Id': self.refNo,
            'Priority': 'u=4',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            }
        if self.sessionId and 'Authorization' not in headers:
            headers['Authorization'] = 'Bearer ' + self.sessionId
        data = data if jsontype else json.dumps(data)
        if files:
            response = self.session.post(url, headers=headers, data=data, files=files,proxies=self.proxies)
        else:
            response = self.session.post(url, headers=headers, data=data,proxies=self.proxies)
        try:
            result = response.json()
        except:
            result = response.text
        return result

    def doLogin(self):
        solveCaptcha = self.solveCaptcha()
        if not solveCaptcha["status"]:
            return solveCaptcha
        param = {
            
            "corpId": self.corpId,
            "deviceId": self.deviceId,
            "encryptedCaptcha": self.encryptedCaptcha,
            "password": hashlib.md5(self.password.encode()).hexdigest(),
            "captcha": solveCaptcha["captcha"],
            "refNo": self.refNo,
            "userId": self.username,
        }

        result = self.curlPost(self.url['login'], param)
        if 'result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == "00":
            self.sessionId = result['sessionId']
            # print(self.sessionId)
            self.refNo = result['refNo']
            # print(self.refNo)
            self.accountName = result['cust']['acct_list'][self.account_number]['acctNm']
            session = {
                "sessionId": self.sessionId,
            }
            self.save_data()
            self.is_login = True
            return {
                'code': 200,
                'success': True,
                'message': "success",
                'session': session,
                'data': result if result else ""
            }
        elif 'result' in result and 'message' in result['result']:
            return {
                'code': 500,
                'success': False,
                'message': result['result']['message'],
                "param": param,
                'data': result if result else ""
            }     
        else:
            return {
                'code': 500,
                'success': False,
                'message': "Unknow error",
                "param": param,
                'data': result if result else ""
            }

    def saveData(self):
        data = {
            'username': self.username,
            'password': self.password,
            'account_number': self.account_number,
            'sessionId': self.sessionId,
            'mobileId': self.mobileId,
            'clientId': self.clientId,
            'cif': self.cif,
            'E': self.E,
            'res': self.res,
            'tranId': self.tranId,
            'browserToken': self.browserToken,
            'browserId': self.browserId,
        }
        with open(f"data/{self.username}.txt", "w") as file:
            json.dump(data, file)

    def parseData(self):
        with open(f"data/{self.username}.txt", "r") as file:
            data = json.load(file)
            self.username = data["username"]
            self.password = data["password"]
            self.account_number = data.get("account_number", "")
            self.sessionId = data.get("sessionId", "")
            self.mobileId = data.get("mobileId", "")
            self.clientId = data.get("clientId", "")
            self.token = data.get("token", "")
            self.accessToken = data.get("accessToken", "")
            self.cif = data.get("cif", "")
            self.res = data.get("res", "")
            self.tranId = data.get("tranId", "")
            self.browserToken = data.get("browserToken", "")
            self.browserId = data.get("browserId", "")
            self.E = data.get("E", "")

    def getE(self):
        ahash = hashlib.md5(self.username.encode()).hexdigest()
        imei = '-'.join([ahash[i:i+4] for i in range(0, len(ahash), 4)])
        return imei.upper()

    def getCaptcha(self):
        captchaToken = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
        url = self.url['getCaptcha'] + captchaToken
        response = requests.get(url)
        result = base64.b64encode(response.content).decode('utf-8')
        return result

    def getlistAccount(self):
        if not self.is_login:
            login = self.doLogin()
            if 'success' not in login or not login['success']:
                return login
        param = {
            'refNo': self.refNo
        }
        result = self.curlPost(self.url['getlistAccount'], param)
        if 'acct_list' in result and 'refNo' in result:
            for account in result['acct_list']:
                if self.account_number == account['acctNo']:
                    if float(account['currentBalance']) < 0 or account['blockedAmount']:
                        return {'code':448,'success': False, 'message': 'Blocked account!',
                                'data': {
                                    'balance':float(account['currentBalance'])
                                }
                                }
                    else:
                        return {'code':200,'success': True, 'message': 'Thành công',
                                'data':{
                                    'account_number':self.account_number,
                                    'balance':float(account['currentBalance'])
                        }}
            return {'code':404,'success': False, 'message': 'account_number not found!'} 
        else: 
            return {'code':520 ,'success': False, 'message': 'Unknown Error!'} 

    def getHistories(self, fromDate="16/06/2023", toDate="16/06/2023", account_number='', page=1,size=15,limit = 100):
        if not self.is_login:
                login = self.doLogin()
                if 'success' not in login or not login['success']:
                    return login
        param = {
            "accountName": self.accountName,
            "accountNo": account_number if account_number else self.account_number,
            "currency": "VND",
            "fromDate": fromDate,
            "refNo": self.refNo,
            "toDate": toDate,
            "page": page,
            "size": size,
            "top": limit
        }
        result = self.curlPost(self.url['getHistories'], param)
        if 'result' in result and 'responseCode' in result['result'] and  result['result']['responseCode'] == '00' and 'transactionHistoryList' in result:
            return {'code':200,'success': True, 'message': 'Thành công',
                            'data':{
                                'transactions':result['transactionHistoryList'],
                    }}
        else:
            return  {
                    "success": False,
                    "code": 503,
                    "message": "Service Unavailable!"
                }

    def checkBulkProcess(self,bulkId,totalRecord):
        param = {
            "bulkId": bulkId,
            "refNo": self.refNo,
            "totalRecord": totalRecord,
        }
        result = self.curlPost(self.url['checkBulkProcess'], param)
        return result
    def getBulkTransaction(self,bulkId):
        param = {
            "bulkId": bulkId,
            "from": 0,
            "isCheckName": "Y",
            "isError": "N",
            "isOrdered": "N",
            "isPayRollUpfile": "N",
            "isWarning": "N",
            "keyword": None,
            "refNo": self.refNo,
        }
        result = self.curlPost(self.url['getBulkTransaction'], param)
        return result
    def verifyBulk(self,bulkId,totalRecord,fileName,fileDescription):
        param = {
            "bulkId": bulkId,
            "bulkUploadFileInfo": {
                "fileDescription":fileDescription,
                "fileExtension": ".xlsx",
                "fileName": fileName
                },
            "isCitadChecked": "N",
            "isPayRollUpfile": "Y",
            "refNo": self.refNo,
            "serviceCode": "GCM_MFT_PROLL",
            "sourceAccount": self.account_number,
            "totalRecord": totalRecord,
            
        }
        result = self.curlPost(self.url['verifyBulk'], param)
        return result
    def saveBulk(self,bulkId,totalRecord,fileName,fileDescription,checkNameFileId):
        param = {
            "bulkId": bulkId,
            "bulkUploadFileInfo": {
                "fileDescription":fileDescription,
                "fileExtension": ".xlsx",
                "fileName": fileName
                },
            "checkNameFileId": checkNameFileId,
            "language": "vi",
            "isPayRollUpfile": "Y",
            "refNo": self.refNo,
            "serviceCode": "GCM_MFT_PROLL",
            "sourceAccount": self.account_number,
            "totalRecord": totalRecord,
            
        }
        result = self.curlPost(self.url['saveBulk'], param)
        return result
    def checkNameBulkFile(self,bulkId,fileName):
        param = {
            "bulkId": bulkId,
            "fileName": fileName,
            "refNo": self.refNo,
            "serviceCode": "GCM_MFT_PROLL"
        }
        result = self.curlPost(self.url['checkNameBulkFile'], param)
        return result
    def checkNameStatus(self,bulkId):
        param = {
            "markAsRead": True,
            "pageNumber": 1,
            "pageSize": 10,
            "refNo": self.refNo,
            "status": ""
        }
        result = self.curlPost(self.url['checkNameStatus'], param)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00' and 'listFile' in result):
            return result
        listFile = result['listFile']
        for file in listFile:
            if file['bulkId'] == bulkId:
                if file['statusCheckName'] == 'CHECKING' or  file['statusCheckName'] == 'WAITING':
                    time.sleep(2)
                    return self.checkNameStatus(bulkId)
                elif file['statusCheckName'] == 'FINISHED':
                    return file['checkNameFileId']
        return result
    def upload_file(self, file_path,fileName):
        if not self.is_login:
                login = self.doLogin()
                if 'success' not in login or not login['success']:
                    return login

        payload = {'param': '{"refNo":"'+self.refNo+'","sessionId":"'+self.sessionId+'","serviceCode":"GCM_MFT_PROLL"}'}
        files = {
            'file': (fileName, open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'application/json',
        'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'biz-tracking': '/cp/mass-payment/bulk-payment/create-bulk-transaction/1',
        'biz-version': '1.02082024.1680',
        'biz-platform': 'biz-1.0',
        'Origin': 'https://ebank.mbbank.com.vn',
        'Connection': 'keep-alive',
        'Referer': 'https://ebank.mbbank.com.vn/cp/mass-payment/bulk-payment/create-bulk-transaction',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
        }
        result = self.curlPost(self.url['uploadFile'], data = payload,headers=headers,files=files, jsontype = True)
        return result
    def transfer_bulk_file(self,file_path,fileDescription):
        fileName = file_path.replace('upload_files/','')
        self.logger = setup_logger(fileName+'_'+str(int(time.time())))
        self.logger.info('-------------------------------------------------------------------------------')
        self.logger.info(f'file {fileName}')
        self.logger.info(f'proxy_used {self.proxies}')
        result = self.upload_file(file_path,fileName)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00' and 'totalRow' in result and 'bulkId' in result):
            self.logger.error(f"upload_file: {result}", exc_info=True)
            return result
        self.logger.info(f"upload_file: {result}")
        bulkId = result['bulkId']
        totalRow = result['totalRow']
        result = self.checkBulkProcess(bulkId,totalRow)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
            self.logger.error(f"check_bulk_process: {result}", exc_info=True)
            return result
        self.logger.info(f"check_bulk_process: {result}")
        result = self.checkNameBulkFile(bulkId,fileName)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
            self.logger.error(f"check_name_bulk_file: {result}", exc_info=True)
            return result
        self.logger.info(f"check_name_bulk_file: {result}")
        result = self.checkNameStatus(bulkId)
        if not isinstance(result, str):
            time.sleep(1)
            result = self.checkNameStatus(bulkId)
            if not isinstance(result, str):
                self.logger.error(f"check_name_status: {result}", exc_info=True)
                return result
            self.logger.info(f"check_name_status: {result}")
            return result
        self.logger.info(f"check_name_status: {result}")
        checkNameFileId = result
        result = self.getBulkTransaction(bulkId)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00' and 'bulkTransactions' in result):
            self.logger.error(f"get_bulk_transation: {result}", exc_info=True)
            return result
        self.logger.info(f"get_bulk_transation: {result}")
        bulkTransactions = result['bulkTransactions']
        error_transactions = []
        success_transactions = []
        for transaction in bulkTransactions:
            success_transactions.append(transaction)
            if transaction['errorScore'] == 1 or transaction['warningScore'] == 1 or len(transaction['warningCodes']) > 0 or len(transaction['errorCodes']) > 0:
                list_warning = []
                list_error = []
                if transaction['warningCodes']:
                    list_warning = [x.split(':')[1] for x in ("" if transaction['warningCodes'] is None else transaction['warningCodes']).rstrip(';').split(';')] if transaction['warningCodes'] else []
                if transaction['errorCodes']:
                    list_error = [x.split(':')[1] for x in ("" if transaction['errorCodes'] is None else transaction['errorCodes']).rstrip(';').split(';')] if transaction['errorCodes'] else []
                list_warning_error = list_warning + list_error
                if not list_warning_error:
                    transaction['message'] = ['unknow error!']
                else:
                    transaction['message'] = []
                    transaction['message_details'] = ""
                    for item_error in list_warning_error:
                        error_code = "INNO_ERR_"+item_error
                        if error_code in self.error_messages:
                            transaction['message'].append(self.error_messages[error_code])
                transaction['message_details'] = '; '.join(str(item) for item in transaction['message'])
                error_transactions.append(transaction)
                success_transactions.remove(transaction)
            elif transaction['benNameAfterCheck'].strip() != transaction['benName'].strip():
                transaction['message'] = ['Beneficiary name does not match the data returned by the system. Please check the account number and beneficiary name and correct them if necessary']
                transaction['message_details'] = 'Beneficiary name does not match the data returned by the system. Please check the account number and beneficiary name and correct them if necessary'
                error_transactions.append(transaction)
                success_transactions.remove(transaction)
        if error_transactions:
            self.logger.info(f"success_transactions: {len(success_transactions)}", exc_info=True)
            self.logger.error(f"error_transactions: {len(error_transactions)}", exc_info=True)
            file_success = generate_upload_file_success(success_transactions)
            file_error = generate_upload_file_error(error_transactions)
            return  {
                    "success": False,
                    "code": 400,
                    "message": "Error!",
                    "file_success": file_success,
                    "file_error": file_error,
                }
        else:
            result = self.verifyBulk(bulkId,totalRow,fileName,fileDescription)
            if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
                self.logger.error(f"verify_bulk: {result}", exc_info=True)
                return result
            self.logger.info(f"verify_bulk: {result}")
            result = self.saveBulk(bulkId,totalRow,fileName,fileDescription,checkNameFileId)
            if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
                self.logger.error(f"save_bulk: {result}", exc_info=True)
                return result
            self.logger.info(f"save_bulk: {result}")
        result['success'] = True
        result['code'] = 200
        if 'totalAmount' in result:
            result['totalAmount'] = f"{int(result['totalAmount']):,}"
        self.logger.info(f"result: {result}")
        return result


class APIResponse():
        def json_format(response,internal_error=False):
            
            if internal_error:
                response = {'code': 500, 'success': False, 'message': response}
                status_code = 500

            else:
                if 'code' in response:
                    status_code = response['code']
                    if int(status_code) < 200:
                        status_code = 500
                else:
                    response = {'code': 500, 'success': False, 'message': response}
                    status_code = 500
                
            return  Response(content=json.dumps(response),
                status_code=status_code,
                media_type="application/json"
                )


app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello": "World"}
class LoginDetails(BaseModel):
    corp_id: str
    username: str
    password: str
    account_number: str
@app.post('/login', tags=["login"])
def login_api(input: LoginDetails):
    try:
        mbbank = MBBANK(input.corp_id,input.username, input.password, input.account_number)
        response = mbbank.doLogin()
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)    
@app.post('/balance', tags=["balance"])
def confirm_api(input: LoginDetails):
    try:
        mbbank = MBBANK(input.corp_id,input.username, input.password, input.account_number)
        response = mbbank.getlistAccount()
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)
    
class Transactions(BaseModel):
    corp_id: str
    username: str
    password: str
    account_number: str
    from_date: str
    to_date: str
    page: int
    size: int
    limit: int
    
@app.post('/get_transactions', tags=["get_transactions"])
def get_transactions_api(input: Transactions):
    try:
        mbbank = MBBANK(input.corp_id,input.username, input.password, input.account_number)
        response = mbbank.getHistories(input.from_date, input.to_date, input.account_number,input.page,input.size,input.limit)
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)

@app.post('/transfer_batch_file', tags=["transfer_batch_file"])
async def transfer_batch_file_api(
    corp_id: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    account_number: str = Form(...),
    file: UploadFile = File(...),
    file_description: str = Form(...),
):
    try:
        file_location = f"upload_files/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        
        mbbank = MBBANK(corp_id, username, password, account_number)
        response = mbbank.transfer_bulk_file(file_location,file_description)
        
        return APIResponse.json_format(response)
    except Exception as e:
        response = str(e)
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return APIResponse.json_format(response)
    
if __name__ == "__main__":
    uvicorn.run(app ,host='0.0.0.0', port=3000)
    
    
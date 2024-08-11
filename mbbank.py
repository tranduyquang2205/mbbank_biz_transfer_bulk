
import hashlib
import requests
import json
import base64
import random
import string
import base64
import json
import os
import hashlib
import time
import uuid
from datetime import datetime
import random
from file_handle import *


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
        self.error_messages_vi = {
            "INNO_ERR_01": "Please enter full information",
            "INNO_ERR_02": "Dữ liệu không hợp lệ",
            "INNO_ERR_03": "Không tìm thấy Mã ngân hàng thụ hưởng",
            "INNO_ERR_04": "Không tìm thấy ngân hàng thụ hưởng",
            "INNO_ERR_05": "Không tìm thấy Chi nhánh ngân hàng thụ hưởng",
            "INNO_ERR_06": "Thông tin sai định dạng",
            "INNO_ERR_07": "Không được phép nhập Số tiền âm",
            "INNO_ERR_08": "Vượt quá số ký tự cho phép",
            "INNO_ERR_09": "Vui lòng nhập số tiền ít nhất 1 VND và nhỏ hơn 10,000,000,000,000 VND",
            "INNO_ERR_11": "Vui lòng nhập số tiền ít nhất 1 VND và nhỏ hơn 10,000,000,000,000 VND",
            "INNO_ERR_111": "Số tài khoản bị trùng",
            "INNO_ERR_112": "Không được phép nhập thông tin trùng với Số tài khoản nguồn",
            "INNO_ERR_113": "Hệ thống không hỗ trợ giao dịch với Số thẻ này theo quy định của Tổ chức thẻ quốc tế.",
            "INNO_ERR_114": "Tên đơn vị thụ hưởng không trùng khớp với dữ liệu hệ thống trả về. Vui lòng kiểm tra lại số tài khoản và tên đơn vị thụ hưởng sau đó sửa lại (nếu cần)",
            "INNO_ERR_115": "Chưa kiểm tra được, vui lòng kiểm tra sau hoặc tiếp tục giao dịch",
            "INNO_ERR_116": "Tài khoản không tồn tại",
            "INNO_ERR_117": "Không được giao dịch đối với tài khoản ngoại tệ",
            "INNO_ERR_118": "Không được phép nhập số tiền quá hạn mức",
            "INNO_ERR_119": "Tài khoản thụ hưởng phải là tài khoản thanh toán",
            "INNO_ERR_120": "Số tiền tối thiểu là 1 triệu đồng cho mỗi tài khoản thụ hưởng",
            "INNO_ERR_121": "Không kiểm tra được",
            "INNO_ERR_124": "Số hóa đơn bị trùng",
            "INNO_ERR_125": "Mã số thuế bên mua không trùng với mã số thuế của corp",
            "INNO_ERR_126": "Mã số thuế bên mua bị trùng mã số thuế bên bán",
            "INNO_ERR_127": "Số tiền vay lớn hơn số tiền hóa đơn",
            "INNO_ERR_128": "Không giải ngân thanh toán cho bên liên quan.",
            "INNO_ERR_140": "Số tiền giải ngân ở các ngân hàng khác lớn hơn số tiền hóa đơn",
            "INNO_ERR_141": "Hóa đơn không tồn tại",
            "INNO_ERR_142": "Hóa đơn đã bị điều chỉnh",
            "INNO_ERR_143": "Hóa đơn đã bị thay thế",
            "INNO_ERR_144": "Hóa đơn đã bị hủy",
            "INNO_ERR_145": "Vui lòng kiểm tra lại",
            "INNO_ERR_146": "Số tiền giải ngân lớn hơn số tiền còn được giải ngân"
        }
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
        self.authToken = ""
        self.clientIp = ""
        self.guid = ""
        self.uuid = ""
        self.is_login = False
        self.key_captcha = "CAP-6C2884061D70C08F10D6257F2CA9518C"
        self.file = f"data/{username}.txt"
        self.url = {
    "getCaptcha": "https://ebank.mbbank.com.vn/corp/common/generateCaptcha",
    "login": "https://ebank.mbbank.com.vn/corp/common/do-login-v2",
    "getHistories": "https://ebank.mbbank.com.vn/corp/transaction/v2/getTransactionHistoryV3",
    "getlistAccount": "https://ebank.mbbank.com.vn/corp/balance/v2/getBalance",
    "apigee":  "https://ebank.mbbank.com.vn/corp/common/get-token-apigee",
    "firstlogin":  "https://ebank.mbbank.com.vn/corp/new-onboard/get-first-login",
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
        self.authToken = data.get('authToken', '')
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
        # self.deviceId = self.generate_random_string()
        self.deviceId = "9bf859cabf682d737516bafba5c6d051"
        self.save_data()
        
    def random_trace_id(self):
        hex_digits = "0123456789abcdef"
        trace_id = ''.join(random.choice(hex_digits) for _ in range(16))
        return str(int(trace_id, 16))
    
    def generate_random_string(self,length=32):
        characters = '0123456789abcdefghijklmnopqrstuvwxyz'
        characters_length = len(characters)
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
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
        # captchaText = self.checkProgressCaptcha(json.loads(task)['taskId'])
        if 'prediction' in result and result['prediction']:
            captcha_value = result['prediction']
            return {"status": True, "key": self.guid, "captcha": captcha_value}
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
        # print(headers)
        data = data if jsontype else json.dumps(data)
        if files:
            response = self.session.post(url, headers=headers, data=data, files=files,proxies=self.proxies)
        else:
            response = self.session.post(url, headers=headers, data=data,proxies=self.proxies)
        try:
            result = response.json()
        except:
            result = response.text
        # print(result)
        return result

    def checkBrowser(self, type=1):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3008,
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3008", param)
        if "tranId" in result["transaction"]:
            return self.chooseOtpType(result["transaction"]["tranId"], type)
        else:
            return {
                'code': 400,
                'success': True,
                'message': "checkBrowser failed",
                "param": param,
                'data': result or ""
            }

    def chooseOtpType(self, tranID, type=1):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3010,
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "tranId": tranID,
            "type": type,  # 1 la sms,5 la smart
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3010", param)
        if result["code"] == "00":
            self.tranId = tranID
            self.saveData()
            self.challenge = result.get("challenge", "")
            return {
                    'code': 200,
                    'success': True,
                    'message': 'Thành công',
                "result": {
                    "browserToken": self.browserToken,
                    "tranId": result.get("tranId", ""),
                    "challenge": result.get("challenge", "")
                },
                "param": param,
                'data': result or ""
            }
        else:
            return {
                'code': 400,
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }

    def submitOtpLogin(self, otp):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "mid": 3011,
            "cif": "",
            "clientId": "",
            "mobileId": "",
            "sessionId": "",
            "browserToken": self.browserToken,
            "tranId": self.tranId,
            "otp": otp,
            "challenge": self.challenge,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3011", param)
        if result["data"]["code"] == "00":
            self.sessionId = result["sessionId"]
            self.mobileId = result["userInfo"]["mobileId"]
            self.clientId = result["userInfo"]["clientId"]
            self.cif = result["userInfo"]["cif"]
            session = {"sessionId": self.sessionId, "mobileId": self.mobileId, "clientId": self.clientId, "cif": self.cif}
            self.res = result
            self.saveData()
            
            if result["allowSave"]:
                sv = self.saveBrowser()
                if sv["code"] == "00":
                    self.is_login = True
                    return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': True,
                        "d": sv,
                        'session': session,
                        'data': result or ""
                    }
                else:
                    return {
                        'code': 400,
                        'success': False,
                        'message': sv["des"],
                        "param": param,
                        'data': sv or ""
                    }
            else:
                return {
                        'code': 200,
                        'success': True,
                        'message': 'Thành công',
                        'saved_browser': False,
                        'session': session,
                        'data': result or ""
                    }
        else:
            return {
                'code': 500,
                'success': False,
                'message': result["des"],
                "param": param,
                'data': result or ""
            }

    def saveBrowser(self):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "browserName": "Microsoft Edge 125.0.0.0",
            "lang": self.lang,
            "mid": 3009,
            "cif": self.cif,
            "clientId": self.clientId,
            "mobileId": self.mobileId,
            "sessionId": self.sessionId,
            "user": self.username
        }
        result = self.curlPost(self.url['authen-service'] + "3009", param)
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
            self.authToken = data.get("authToken", "")
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
        
    def get_token_apigee(self):
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost(self.url['apigee'], param)
        self.token = result['apigeeAuthResponse']['accessToken']
        return result
    def get_first_login(self):
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost(self.url['firstlogin'], param)
        return result
    def get_get(self):
        param = {
            "password": hashlib.md5(self.password.encode()).hexdigest(),
            "refNo": self.refNo,
            "userId": self.corpId+':'+self.username
        }
        result = self.curlPost("https://ebank.mbbank.com.vn/corp/keycloak/token/get", param)
        return result
    def get_tracking_info(self):
        param = {
            "menuCode": "MNU_GCME_100100",
            "refNo": self.refNo,
        }
        result = self.curlPost("https://ebank.mbbank.com.vn/corp/common/get-tracking-info", param)
        return result
    def getSourceAccountList(self):
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost("https://ebank.mbbank.com.vn/corp/common/v2/getSourceAccountList", param)
        return result
    def activate_account_sync(self):
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer '+self.token,
        'Authorization-Url': '/activate-account-sync',
        'ClientMessageId': self.refNo,
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://ebank.mbbank.com.vn',
        'RefNo': self.refNo,
        'Referer': 'https://ebank.mbbank.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'biz-platform': 'biz-1.0',
        'biz-tracking': '/cp/pl/login/1',
        'biz-version': '1.02082024.1680',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sessionId': self.sessionId
        }
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost("https://api-public.mbbank.com.vn/ms/activate-account-sync", param,headers)
        return result
    def get_corp_migration(self):
        url = "https://api-public.mbbank.com.vn/ms/ms-user-config/get-corp-migration"
        payload = {}
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer '+self.token,
        'Authorization-Url': '/get-bills',
        'ClientMessageId': self.refNo,
        'Connection': 'keep-alive',
        'Origin': 'https://ebank.mbbank.com.vn',
        'RefNo': self.refNo,
        'Referer': 'https://ebank.mbbank.com.vn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'biz-platform': 'biz-1.0',
        'biz-tracking': '/cp/pl/login/1',
        'biz-version': '1.02082024.1680',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sessionId': self.sessionId
        }

        response = self.session.get(url, headers=headers, data=payload)
        try:
            result = response.json()
        except:
            result = response.text
        return result
    def check_signed_ca(self):
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost("https://ebank.mbbank.com.vn/corp/new-onboard/check-signed-ca", param)
        return result
    def check_rm(self):
        param = {
            "refNo": self.refNo,
        }
        result = self.curlPost("https://ebank.mbbank.com.vn/corp/new-onboard/check-rm", param)
        return result

    def getlistDDAccount(self):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "browserId": self.browserId,
            "E": self.getE() or "",
            "mid": 35,
            "cif": self.cif,
            "serviceCode": "0551",
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getlistDDAccount'], param)
        return result

    def getAccountDeltail(self):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "accountNo": self.account_number,
            "accountType": "D",
            "mid": 13,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getAccountDeltail'], param)
        return result

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

    def getBanks(self):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "fastTransfer": "1",
            "mid": 23,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['getBanks'], param)
        return result
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
        result = self.upload_file(file_path,fileName)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00' and 'totalRow' in result and 'bulkId' in result):
            return result
        bulkId = result['bulkId']
        totalRow = result['totalRow']
        result = self.checkBulkProcess(bulkId,totalRow)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
            return result
        # result = self.getBulkTransaction(bulkId)
        # if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
        #     return result
        result = self.checkNameBulkFile(bulkId,fileName)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
            return result
        result = self.checkNameStatus(bulkId)
        if not isinstance(result, str):
            return result
        checkNameFileId = result
        result = self.getBulkTransaction(bulkId)
        if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00' and 'bulkTransactions' in result):
            return result
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
                return result
            result = self.saveBulk(bulkId,totalRow,fileName,fileDescription,checkNameFileId)
            if not ('result' in result and 'responseCode' in result['result'] and result['result']['responseCode'] == '00'):
                return result
        result['success'] = True
        result['code'] = 200
        return result
    def createTranferOutMBBANK(self, bankCode, account_number, amount, message):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": self.getE() or "",
            "browserId": self.browserId,
            "lang": self.lang,
            "debitAccountNo": self.account_number,
            "creditAccountNo": account_number,
            "creditBankCode": bankCode,
            "amount": amount,
            "feeType": 1,
            "content": message,
            "ccyType": "1",
            "mid": 62,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['tranferOut'], param)
        return result

    def createTranferInMBBANK(self, account_number, amount, message):
        param = {
            "clientOsVersion": self.clientOsVersion,
            "browserVersion": self.browserVersion,
            "browserName": self.browserName,
            "E": "",
            "browserId": self.browserId,
            "lang": self.lang,
            "debitAccountNo": self.account_number,
            "creditAccountNo": account_number,
            "amount": amount,
            "activeTouch": 0,
            "feeType": 1,
            "content": message,
            "ccyType": "",
            "mid": 16,
            "cif": self.cif,
            "user": self.username,
            "mobileId": self.mobileId,
            "clientId": self.clientId,
            "sessionId": self.sessionId
        }
        result = self.curlPost(self.url['tranferIn'], param)
        return result

    def genOtpTranFer(self, tranId, type="OUT", otpType=5):
        if otpType == 1:
            solveCaptcha = self.solveCaptcha()
            if not solveCaptcha["status"]:
                return solveCaptcha
            param = {
                "clientOsVersion": self.clientOsVersion,
                "browserVersion": self.browserVersion,
                "browserName": self.browserName,
                "E": self.getE() or "",
                "lang": self.lang,
                "tranId": tranId,
                "type": otpType,  # 1 là SMS,5 là smart otp
                "captchaToken": solveCaptcha["key"],
                "captchaValue": solveCaptcha["captcha"],
                "browserId": self.browserId,
                "mid": 17,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }
        else:
            param = {
                "clientOsVersion": self.clientOsVersion,
                "browserVersion": self.browserVersion,
                "browserName": self.browserName,
                "E": self.getE() or "",
                "lang": self.lang,
                "tranId": tranId,
                "type": otpType,  # 1 là SMS,5 là smart otp
                "mid": 17,
                "browserId": self.browserId,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }

        if type == "IN":
            result = self.curlPost(self.url['genOtpIn'], param)
        else:
            result = self.curlPost(self.url['genOtpOut'], param)
        return result

    def confirmTranfer(self, tranId, challenge, otp, type="OUT", otpType=5):
        if otpType == 5:
            param = {
                "clientOsVersion": self.clientOsVersion,
                "browserVersion": self.browserVersion,
                "browserName": self.browserName,
                "E": self.getE() or "",
                "lang": self.lang,
                "tranId": tranId,
                "otp": otp,
                "challenge": challenge,
                "mid": 18,
                "cif": self.cif,
                "user": self.username,
                "browserId": self.browserId,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }
        else:
            param = {
                "clientOsVersion": self.clientOsVersion,
                "browserVersion": self.browserVersion,
                "browserName": self.browserName,
                "E": self.getE() or "",
                "browserId": self.browserId,
                "lang": self.lang,
                "tranId": tranId,
                "otp": otp,
                "challenge": challenge,
                "mid": 18,
                "cif": self.cif,
                "user": self.username,
                "mobileId": self.mobileId,
                "clientId": self.clientId,
                "sessionId": self.sessionId
            }

        if type == "IN":
            result = self.curlPost(self.url['confirmTranferIn'], param)
        else:
            result = self.curlPost(self.url['confirmTranferOut'], param)
        return result
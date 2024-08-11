from mbbank import MBBANK
import json
import requests
import json
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import uvicorn
import sys
import traceback
from api_response import APIResponse


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
# @app.post('/get_balance', tags=["get_balance"])
# def get_balance_api(input: LoginDetails):
#         mbbank = MBBANK(input.username, input.password, input.account_number)
#         verify_otp = mbbank.submitOtpLogin(input.otp)
#         return verify_otp
    
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
    
    
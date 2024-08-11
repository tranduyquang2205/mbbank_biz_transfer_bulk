


import pandas as pd
import time
import uuid
import unidecode

def convert_to_uppercase_no_accents(text):
    # Remove accents
    no_accents = unidecode.unidecode(text)
    # Convert to uppercase
    return no_accents.upper()
from datetime import datetime
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
        
        # Insert the custom header row
        worksheet.write('A1', '')  # Empty cell
        worksheet.write('B1', 'DANH SÁCH GIAO DỊCH(LIST OF TRANSACTIONS)')
    return output_excel_file

transaction = {
    "warningCodes": "benacc:111;benacc:116;"
}

aaa = [x.split(':')[1] for x in ("" if transaction['warningCodes'] is None else transaction['warningCodes']).rstrip(';').split(';')] if transaction['warningCodes'] else []
print(transaction['warningCodes'])

print(len(""))
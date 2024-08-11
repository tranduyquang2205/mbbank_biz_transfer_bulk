import json

# Load the JSON file
with open('test.json', 'r',encoding="utf-8") as file:
    data = json.load(file)

# Iterate through the bulkTransactions
for transaction in data['bulkTransactions']:
    ben_name = transaction.get('benName')
    ben_name_raw = transaction.get('benNameRaw')
    ben_name_after_check = transaction.get('benNameAfterCheck')
    
    # Check if the names do not match
    if ben_name != ben_name_raw or ben_name != ben_name_after_check or ben_name_raw != ben_name_after_check:
        print(transaction)

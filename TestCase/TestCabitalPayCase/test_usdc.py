import http.client
import json
import uuid
import sys
import time
import webbrowser

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))


def help():
   print('''Instruction:
==========================================================
python3 pay_usdct.py address amount
address TRC20 must start with T
address ERC20 must start with 0x
amount must between 0.0 and 500.000
----------------------------------------------------------
Output is the transfer id
it will pending until get the transaction hash
''')
   sys.exit(-1)


if len(sys.argv) != 3:
   help()

address=sys.argv[1]
if address.startswith("T"):
   chain = 'TRX'
elif address.startswith("0x"):
   chain = 'ETH'
else:
   print("invalid address and chain")
   help()

amount=sys.argv[2]
try:
   a = float(amount)
   if a > 500.0 or a < 0.0:
      help()
except:
   print("invalid amount must be a number")

conn = http.client.HTTPSConnection("api-sandbox.circle.com")
payload = json.dumps({
   "source": {
      "type": "wallet",
      "id": "1001042066"
   },
   "destination": {
      "type": "blockchain",
      "address": address,
      "chain": chain
   },
   "amount": {
      "amount": amount,
      "currency": "USD"
   },
   "idempotencyKey": str(uuid.uuid4())
})
headers = {
   'Accept': 'application/json',
   'User-Agent': 'curl',
   'Content-Type': 'application/json',
   'Authorization': 'Bearer QVBJX0tFWTo2ZDM5N2IwNTk3YmFkY2Y2YTY0NTYzNmM2NmU0OGZjNTpiNjgwMmIwM2QzZWUyY2IwZmZiZmZlNTI0OWI1MDFhNA='
}
conn.request("POST", "/v1/transfers", payload, headers)
res = conn.getresponse()
data = res.read()
result = json.loads(data)
if res.status > 299:
   print(data.decode("utf-8"))
   exit(-1)
payout = result['data']['id']
retry = 0
while True:
   time.sleep(5)
   conn = http.client.HTTPSConnection("api-sandbox.circle.com")
   conn.request("GET", "/v1/transfers/"+payout, None, headers)
   get_res = conn.getresponse()
   get_data = get_res.read()
   if res.status > 299:
      retry = retry + 1
      if retry < 12:
         continue
      else:
         exit(-1)
   get_result = json.loads(get_data)
   # print(get_result)
   if "transactionHash" in get_result['data']:
      if chain=="ETH":
            webbrowser.open("https://goerli.etherscan.io/tx/"+get_result['data']["transactionHash"])
            break
      elif chain == "TRX":
            webbrowser.open("https://shasta.tronscan.org/#/transaction/"+get_result['data']["transactionHash"])
            break
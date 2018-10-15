from fastquery import FastQuery
import json
import requests

def query_iss_pos(end_pt):
    url = 'http://api.open-notify.org/' + end_pt
    resp = requests.get(url)
    return json.loads(resp.text)

print(query_iss_pos('iss-now.json'))
print('-----')

input_data = ['iss-now.json' for i in range(200)]

fast = FastQuery(target=query_iss_pos, args=(input_data,))
output = fast.run()
print(len(output), 'results using the Fast Query.')

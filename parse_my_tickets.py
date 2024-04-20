import requests
import urllib3
import httpx
COOKIES = {
"session":"MTcxMzU3NDA3NnxEWDhFQVFMX2dBQUJFQUVRQUFBaF80QUFBUVp6ZEhKcGJtY01DUUFIZFhObGNsOXBaQVIxYVc1MEJnUUFfZ3RUfMweL2-PDi5UTLqrfLmsD4XlnwD7TB0C6NXpwnSZUDvN"}
DOMAIN = 'https://t-luckyticket-w8mg6qr0.spbctf.ru'
http = urllib3.PoolManager()
MY_TICKETS_URL = DOMAIN + '/api/user/tickets'

def is_luck_ticket(number: str) -> bool:
    int_number = [int(i) for i in number]
    if sum(int_number[:3]) == sum(int_number[3:]):
        return True
    return False

good = []
bad = []
def parse_tickets():
    #response = requests.get(MY_TICKETS_URL, cookies=COOKIES).json()
    #response = http.request('GET', MY_TICKETS_URL, headers=COOKIES)
    response = httpx.request('GET', MY_TICKETS_URL, cookies=COOKIES).json()



    for i in response:
        if is_luck_ticket(i['number']):
            good.append(i["number"])
            #print(i["number"])
        else:
            bad.append(i["number"])

parse_tickets()

print('Куплено счастливых билетов:', len(good))
print('Куплено обычных билетов:', len(bad))
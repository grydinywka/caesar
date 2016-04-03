import os

import redis
from rq import Worker, Queue, Connection

# listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    # with Connection(conn):
    #     worker = Worker(map(Queue, listen))
    #     worker.work()
    with open('./caesar/caesarapp/static/txt/wordsEn.txt', 'r') as en_words_file:
        for line in en_words_file:
            conn.sadd('setEn', line.strip())

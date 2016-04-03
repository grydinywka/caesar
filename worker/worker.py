import os
import redis

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with open('../caesarapp/static/txt/words.txt', 'r') as en_words_file:
        for line in en_words_file:
            conn.sadd('setEn', line.strip())

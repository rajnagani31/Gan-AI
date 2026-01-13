from redis import Redis
from rq import Queue

# Use for inside Docker
# queue = Queue(connection=Redis(host="valkey"))

queue = Queue(
    connection=Redis(host="valkey")
)

import logging

import redis
from redis import ConnectionPool
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisConnector:
    def __init__(self, host, port, max_connections=1000):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.pool = None

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_fixed(5),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN),
    )
    def connect_with_retry(self):
        try:
            self.pool = ConnectionPool(host=self.host, port=self.port, max_connections=self.max_connections)
            r = redis.Redis(connection_pool=self.pool)
            r.ping()
            return r
        except redis.ConnectionError:
            logger.error(redis.ConnectionError)
        raise Exception(f"Failed to connect to Redis after {self.max_retries} attempts")

    def get_redis_connection(self):
        if not self.pool:
            self.connect_with_retry()
        return redis.Redis(connection_pool=self.pool)


try:
    redis_connector = RedisConnector(settings.REDIS_HOST, settings.REDIS_PORT)
    redis_conn = redis_connector.get_redis_connection()
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Failed to connect to Redis: {str(e)}")

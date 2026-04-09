from enum import Enum


class Scope(str, Enum):
    PoolStatusRead = "interuss.pool_status.read"
    PoolStatusHeartbeatWrite = "interuss.pool_status.heartbeat.write"

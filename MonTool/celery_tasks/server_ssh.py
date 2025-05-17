import paramiko
from queue import Queue


class SSHPool:
    def __init__(self, host, username, password, size=5):
        self.pool = Queue(maxsize=size)
        for _ in range(size):
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, password=password)
            self.pool.put(ssh)

    def get_conn(self):
        return self.pool.get()

    def release_conn(self, conn):
        self.pool.put(conn)

    def close_all(self):
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()

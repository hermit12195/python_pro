import asyncio
import os
import time

import redis
from celery import shared_task
from cryptography.fernet import Fernet
from ping3 import ping
from telegram.error import NetworkError

from app.models import Server, MonUser
from telegram import Bot
from telegram.constants import ParseMode

from celery_tasks.server_ssh import SSHPool

EXCEPTIONS = False

TOKEN = os.getenv("TOKEN")
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

bot = Bot(token=TOKEN)

r = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)


async def tg_notification(ip, tg_id):
    try:
        await bot.send_message(
            chat_id=tg_id,
            text=f"The server with IP '{ip}' is down! Check immediately!!!'",
            parse_mode=ParseMode.HTML,
        )
    except (RuntimeError, NetworkError) as e:
        pass


@shared_task
def connection_quality() -> None:
    server_ips = Server.objects.values_list('server_ip', 'id')
    for record in server_ips:
        ping_res = ping(record[0])
        if ping_res:
            ping_res *= 1000
            if ping_res <= 30:
                Server.objects.filter(id=record[1]).update(status="🌟Excellent")
            elif 100 <= ping_res > 30:
                Server.objects.filter(id=record[1]).update(status="✅Good")
            elif 1000 <= ping_res > 100:
                Server.objects.filter(id=record[1]).update(status="⚠️Poor")
        else:
            Server.objects.filter(id=record[1]).update(status="❌Offline")
            user_email = Server.objects.get(id=record[1]).owner
            tg_id = MonUser.objects.get(email=user_email).tg_id
            if tg_id:
                asyncio.run(tg_notification(record[0], tg_id))


active_monitoring_tasks = {}


@shared_task(bind=True)
def server_stats(self, server_id):
    if server_id in active_monitoring_tasks and active_monitoring_tasks[server_id] != self.request.id:
        return

    creds = Server.objects.filter(id=server_id).values_list('server_ip', 'user_name', 'password').first()
    password = fernet.decrypt(creds[2].encode()).decode()
    ssh_pool = SSHPool(creds[0], creds[1], password, size=5)
    conn = ssh_pool.get_conn()
    try:
        if Server.objects.get(id=server_id).os_name == 'Linux':
            stdin, stdout, stderr = conn.exec_command(
                "echo $(free -m | awk '/^Mem:/ {print $4}') $(df -BG / | awk 'NR==2 {gsub(/G/, \"\", $4); print $4}') $(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)")
            output = stdout.read().decode().strip()
            free_mem, disk_space, cpu_load = output.split()
            r_key = f"server:{server_id}"
            r.hset(r_key, mapping={
                'free_memory': free_mem,
                'free_disk': disk_space,
                'cpu_load': cpu_load
            })
            r.expire(r_key, 3600)
        elif Server.objects.get(id=server_id).os_name == 'Windows':
            command = 'Write-Output "$([math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1024)) $([math]::Round((Get-CimInstance Win32_LogicalDisk -Filter \\"DeviceID=\'C:\'\\" ).FreeSpace / 1GB)) $([math]::Round((Get-Counter \\\'\Processor(_Total)\\\% Processor Time\\\').CounterSamples[0].CookedValue, 2))"'
            stdin, stdout, stderr = conn.exec_command(f"powershell -Command {command}")
            output = stdout.read().decode().strip()
            free_mem, disk_space, cpu_load = output.split()
            r_key = f"server:{server_id}"
            r.hset(r_key, mapping={
                'free_memory': free_mem,
                'free_disk': disk_space,
                'cpu_load': cpu_load
            })
            r.expire(r_key, 3600)
    finally:
        ssh_pool.release_conn(conn)
    time.sleep(30)

    if server_id in active_monitoring_tasks and active_monitoring_tasks[server_id] == self.request.id:
        server_stats.delay(server_id)

import aiohttp
import datetime
import socket
import asyncio
import time
import platform
import psutil
import speedtest
from pyrogram import types


# ЭТОТ КОД НАПИСАН ЧАТОМГПТ, НЕ БЕЙТЕ МЕНЯ ПАЛКОЙ, ПОЖАЛУЙСТА!!!


def get_cpu_temperature():
    system = platform.system()
    if system == 'Linux':
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return "🌡️ Temperature: unknown"
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        return f"🌡️ Temperature {name}: {entry.current}°C"
            return "🌡️ Temperature: unknown"
        except Exception as e:
            return f"🌡️ Temperature: unknown"
    elif system == 'Windows':
        return f"🌡️ Temperature: windows moment"
    else:
        return "🌡️ Temperature: unknown"


async def status_command(client, message: types.Message):
    me = await client.get_me()
    if message.from_user and message.from_user.id == me.id:
        await message.delete()

    status_lines = []

    message = await message.reply('Wait a minute...')

    # Uptime
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    status_lines.append(f"⏱️ System uptime: {uptime_str}")

    # CPU & RAM
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    status_lines.append(f"⚙️ CPU: {cpu_usage}%")
    status_lines.append(f"📈 RAM: {ram_usage}%")

    # Temperature
    status_lines.append(get_cpu_temperature())

    # Free memory
    disk = psutil.disk_usage('/')
    status_lines.append(
        f"💽 Disk: {round(disk.used / 1024 ** 3, 1)}GB / {round(disk.total / 1024 ** 3, 1)}GB ({disk.percent}%) busy")

    # Internet
    internet_available = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://1.1.1.1', timeout=5):
                internet_available = True
                status_lines.append("🔌 Internet: available")
    except Exception:
        status_lines.append("🔌 Internet: not available")

    # Local IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        status_lines.append(f"💻 Local IP: {local_ip}")
    except Exception:
        status_lines.append("💻 Local IP: unknown")

    # Ping
    if internet_available:
        try:
            start = time.time()
            reader, writer = await asyncio.open_connection('astatdeglebantiy.github.io', 80)
            end = time.time()
            writer.close()
            await writer.wait_closed()
            ping_ms = round((end - start) * 1000, 2)
            status_lines.append(f"📡 Ping to astatdeglebantiy.github.io: {ping_ms} ms")
        except Exception:
            status_lines.append("📡 Ping to astatdeglebantiy.github.io: unknown")
    else:
        status_lines.append("📡 Ping to astatdeglebantiy.github.io: no internet")

    # Time
    utc_now = datetime.datetime.now(datetime.UTC)
    local_now = datetime.datetime.now()
    status_lines.append(f"🕒 Time (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    status_lines.append(f"🕒 Time (local): {local_now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Location
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip-api.com/json/') as resp:
                data = await resp.json()
                if data['status'] == 'success':
                    location = f"{data['country']}, {data['regionName']}, {data['city']}"
                    status_lines.append(f"📍 Location: {location}")
                else:
                    status_lines.append("📍 Location: unknown")
    except Exception:
        status_lines.append("📍 Location: unknown")

    # System info
    try:
        uname = platform.uname()
        cpu_count = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        status_lines.append(f"🖥️ OS: {uname.system} {uname.release} ({uname.machine})")
        status_lines.append(f"🧠 CPU: {uname.processor} | Kernel(s): {cpu_count}")
        status_lines.append(f"💾 RAM: {ram} GB")
    except Exception:
        status_lines.append("🖥️ System info: unknown")

    # Speedtest
    if internet_available:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000  # Mbps
            upload = st.upload() / 1_000_000
            status_lines.append(f"⬇️ Download: {download:.2f} Mbps")
            status_lines.append(f"⬆️ Upload: {upload:.2f} Mbps")
        except Exception as e:
            status_lines.append("📶 Speedtest: error")
    else:
        status_lines.append("📶 Speedtest: no internet")

    await message.edit("\n".join(status_lines))

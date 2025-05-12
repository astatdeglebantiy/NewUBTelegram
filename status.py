import aiohttp
import datetime
import socket
import asyncio
import time
import platform
import psutil
import speedtest
from pyrogram import types


def get_cpu_temperature():
    system = platform.system()
    if system == 'Linux':
        try:
            temps = psutil.sensors_temperatures()
            if not temps:
                return "🌡️ Температура: данные недоступны"
            for name, entries in temps.items():
                for entry in entries:
                    if entry.current:
                        return f"🌡️ Температура {name}: {entry.current}°C"
            return "🌡️ Температура: данные недоступны"
        except Exception as e:
            return f"🌡️ Температура: ошибка при получении данных ({e})"
    elif system == 'Windows':
        return f"🌡️ Температура: виндовс момент"
    else:
        return "🌡️ Температура: не поддерживается на этой платформе"


async def status_command(client, message: types.Message):
    me = await client.get_me()
    if message.from_user and message.from_user.id == me.id:
        await message.delete()

    status_lines = []

    message = await message.reply('Wait a minute...')

    # Аптайм системы
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
    status_lines.append(f"⏱️ Аптайм системы: {uptime_str}")

    # Загрузка CPU & RAM
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    status_lines.append(f"⚙️ Загрузка CPU: {cpu_usage}%")
    status_lines.append(f"📈 Загрузка RAM: {ram_usage}%")

    # Температура
    status_lines.append(get_cpu_temperature())

    # Свободное место на диске
    disk = psutil.disk_usage('/')
    status_lines.append(
        f"💽 Диск: {round(disk.used / 1024 ** 3, 1)}ГБ / {round(disk.total / 1024 ** 3, 1)}ГБ ({disk.percent}%) занято")

    # Проверка интернета
    internet_available = False
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://1.1.1.1', timeout=5):
                internet_available = True
                status_lines.append("🔌 Интернет: доступен")
    except Exception:
        status_lines.append("🔌 Интернет: недоступен")

    # Локальный IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        status_lines.append(f"💻 Локальный IP: {local_ip}")
    except Exception:
        status_lines.append("💻 Локальный IP: не удалось определить")

    # Пинг
    if internet_available:
        try:
            start = time.time()
            reader, writer = await asyncio.open_connection('astatdeglebantiy.github.io', 80)
            end = time.time()
            writer.close()
            await writer.wait_closed()
            ping_ms = round((end - start) * 1000, 2)
            status_lines.append(f"📡 Пинг до astatdeglebantiy.github.io: {ping_ms} мс")
        except Exception:
            status_lines.append("📡 Пинг до astatdeglebantiy.github.io: ошибка")
    else:
        status_lines.append("📡 Пинг до astatdeglebantiy.github.io: нет интернета")

    # Время
    utc_now = datetime.datetime.now(datetime.UTC)
    local_now = datetime.datetime.now()
    status_lines.append(f"🕒 Время (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")
    status_lines.append(f"🕒 Время (локальное): {local_now.strftime('%Y-%m-%d %H:%M:%S')}")

    # Местоположение
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip-api.com/json/') as resp:
                data = await resp.json()
                if data['status'] == 'success':
                    location = f"{data['country']}, {data['regionName']}, {data['city']}"
                    status_lines.append(f"📍 Местоположение: {location}")
                else:
                    status_lines.append("📍 Местоположение: не удалось определить")
    except Exception:
        status_lines.append("📍 Местоположение: ошибка при получении данных")

    # Системная информация
    try:
        uname = platform.uname()
        cpu_count = psutil.cpu_count(logical=True)
        ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        status_lines.append(f"🖥️ ОС: {uname.system} {uname.release} ({uname.machine})")
        status_lines.append(f"🧠 CPU: {uname.processor} | Ядер: {cpu_count}")
        status_lines.append(f"💾 RAM: {ram} ГБ")
    except Exception:
        status_lines.append("🖥️ Системная информация: ошибка")

    # Скорость интернета
    if internet_available:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000  # Mbps
            upload = st.upload() / 1_000_000
            status_lines.append(f"⬇️ Скорость загрузки: {download:.2f} Мбит/с")
            status_lines.append(f"⬆️ Скорость выгрузки: {upload:.2f} Мбит/с")
        except Exception as e:
            status_lines.append("📶 Скорость интернета: ошибка")
    else:
        status_lines.append("📶 Скорость интернета: нет интернета")

    await message.edit("\n".join(status_lines))

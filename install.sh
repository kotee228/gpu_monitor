#!/bin/bash

# install.sh - Автоматическая установка GPU монитора для Hive OS
# Запуск: bash <(curl -s https://raw.githubusercontent.com/ваш-аккаунт/репозиторий/main/install.sh)

set -e  # Прерывать выполнение при ошибках

echo "========================================"
echo " Установка GPU монитора для Hive OS"
echo "========================================"

# Шаг 1. Создаем папки
echo "[1/5] Создание папок..."
mkdir -p /hive/python_scripts/gpu_monitor
cd /hive/python_scripts/gpu_monitor
echo "✓ Папка создана: /hive/python_scripts/gpu_monitor"

# Шаг 2. Обновляем пакеты и устанавливаем зависимости
echo "[2/5] Установка зависимостей..."
apt update > /dev/null 2>&1
apt install -y python3-venv screen > /dev/null 2>&1
echo "✓ Python3-venv и screen установлены"

# Шаг 3. Создаем виртуальное окружение
echo "[3/5] Создание виртуального окружения..."
python3 -m venv venv
echo "✓ Виртуальное окружение создано"

# Шаг 4. Скачиваем и настраиваем скрипт
echo "[4/5] Загрузка и настройка скрипта..."

# Скачиваем скрипт с GitHub
curl -s -o gpu_monitor.py https://raw.githubusercontent.com/ваш-аккаунт/репозиторий/main/gpu_monitor.py

# Делаем скрипт исполняемым
chmod +x gpu_monitor.py
echo "✓ Скрипт загружен и настроен"

# Шаг 5. Запуск через screen
echo "[5/5] Запуск мониторинга..."

# Создаем запускающий скрипт
cat > start_monitor.sh << 'EOL'
#!/bin/bash
cd /hive/python_scripts/gpu_monitor
source venv/bin/activate
python gpu_monitor.py
EOL

chmod +x start_monitor.sh

# Запускаем в screen
screen -dmS gpu_monitor bash -c 'cd /hive/python_scripts/gpu_monitor && ./start_monitor.sh'

echo "✓ Мониторинг запущен в screen сессии"
echo ""
echo "========================================"
echo " Установка завершена успешно!"
echo "========================================"
echo ""
echo "Команды для управления:"
echo "  Просмотр логов:        tail -f /hive/python_scripts/gpu_monitor/log_status.txt"
echo "  Подключиться к screen: screen -r gpu_monitor"
echo "  Остановить:            screen -XS gpu_monitor quit"
echo ""
echo "Настройки по умолчанию:"
echo "  Проверка каждые: 60 сек"
echo "  Порог мощности:   100W"
echo "  GPU индекс:       0"
echo ""
echo "Для изменения настроек отредактируйте:"
echo "  /hive/python_scripts/gpu_monitor/gpu_monitor.py"

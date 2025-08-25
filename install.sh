#!/bin/bash

# install.sh - Автоматическая установка GPU монитора для Hive OS
# Запуск: bash <(curl -s https://raw.githubusercontent.com/kotee228/gpu_monitor/main/install.sh)

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
curl -s -o gpu_monitor.py https://raw.githubusercontent.com/kotee228/gpu_monitor/main/gpu_monitor.py

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
echo "📋 КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ И МОНИТОРИНГА:"
echo "================================================"
echo ""
echo "⚙️  ДОПОЛНИТЕЛЬНО:"
echo "  cd /hive/python_scripts/gpu_monitor • Перейти в папку скрипта"
echo "  nano gpu_monitor.py          • Редактировать настройки скрипта"
echo ""
echo "🎯 ОСНОВНЫЕ КОМАНДЫ SCREEN:"
echo "  screen -S gpu_monitor        • Создать сессию"
echo "  screen -ls                   • Список всех сессий"
echo "  screen -r gpu_monitor        • Подключиться к сессии"
echo "  screen -XS gpu_monitor quit  • Остановить сессию"
echo ""
echo "📊 МОНИТОРИНГ ЛОГОВ В РЕАЛЬНОМ ВРЕМЕНИ:"
echo "  • В log_status.txt все логи (новые сверху)"
echo "  watch -n 1 \"head -n 10 log_status.txt\"   • Последние 10 событий (где -n 1 обновление 1 сек)"
echo ""
echo "  • В log_restart.txt только перезапуски (новые сверху)"
echo "  watch -n 1 \"head -n 5 log_restart.txt\"   • Последние 5 перезапусков (где -n 1 обновление 1 сек)"
echo ""
echo "  • watch обновляет экран каждую секунду"
echo "  • head показывает первые N строк (самые свежие)"
echo ""
echo "================================================"
echo ""
echo "Настройки по умолчанию:"
echo "  Проверка каждые: 60 сек"
echo "  Порог мощности:   100W"
echo "  GPU индекс:       0"
echo ""
echo "Для изменения настроек отредактируйте:"
echo "  /hive/python_scripts/gpu_monitor/gpu_monitor.py"

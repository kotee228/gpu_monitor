# GPU Monitor for Hive OS

Автоматический мониторинг мощности GPU и перезапуск майнера при падении мощности.

## Быстрая установка

```bash
bash <(curl -s https://raw.githubusercontent.com/kotee228/gpu_monitor/main/install.sh)
```

Если был reboot или перезапуск контейнера Clore, то открыть screen и запустить в нем скрипт нужно вручную самому
```bash
screen -S gpu_monitor -dm bash -c 'cd /hive/python_scripts/gpu_monitor && source venv/bin/activate && python gpu_monitor.py'
```

Доп памятка:
📋 КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ И МОНИТОРИНГА:
================================================

⚙️  ДОПОЛНИТЕЛЬНО:
```bash
cd /hive/python_scripts/gpu_monitor``` • Перейти в папку скрипта
nano gpu_monitor.py          • Редактировать настройки скрипта

🎯 ОСНОВНЫЕ КОМАНДЫ SCREEN:
  screen -S gpu_monitor        • Создать сессию
  screen -ls                   • Список всех сессий
  screen -r gpu_monitor        • Подключиться к сессии
  screen -XS gpu_monitor quit  • Остановить сессию

📊 МОНИТОРИНГ ЛОГОВ В РЕАЛЬНОМ ВРЕМЕНИ:
  • В log_status.txt все логи (новые сверху)
  watch -n 1 \"head -n 10 log_status.txt\"   • Последние 10 событий (где -n 1 обновление 1 сек)

  • В log_restart.txt только перезапуски (новые сверху)
  watch -n 1 \"head -n 5 log_restart.txt\"   • Последние 5 перезапусков (где -n 1 обновление 1 сек)

  • watch обновляет экран каждую секунду
  • head показывает первые N строк (самые свежие)

================================================

Настройки по умолчанию:
  Проверка каждые: 60 сек
  Порог мощности:   100W
  GPU индекс:       0

Для изменения настроек отредактируйте:
 /hive/python_scripts/gpu_monitor/gpu_monitor.py"

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

📋 КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ И МОНИТОРИНГА:
================================================

⚙️  ДОПОЛНИТЕЛЬНО:
• Перейти в папку скрипта
```bash
cd /hive/python_scripts/gpu_monitor
```
• Редактировать настройки скрипта
```bash
nano gpu_monitor.py          
```

🎯 ОСНОВНЫЕ КОМАНДЫ SCREEN:
  • Создать сессию
```bash
  screen -S gpu_monitor
```
  • Список всех сессий
```bash
  screen -ls
```   
  • Подключиться к сессии
```bash
  screen -r gpu_monitor
```     
  • Остановить сессию
```bash
  screen -XS gpu_monitor quit
```

📊 МОНИТОРИНГ ЛОГОВ В РЕАЛЬНОМ ВРЕМЕНИ:
  • В log_status.txt все логи (новые сверху)
  • Последние 10 событий (где -n 1 обновление 1 сек)
```bash
  watch -n 1 \"head -n 10 log_status.txt\"
```

  • В log_restart.txt только перезапуски (новые сверху)
  • Последние 5 перезапусков (где -n 1 обновление 1 сек)
```bash
  watch -n 1 \"head -n 5 log_restart.txt\"
```

  • watch обновляет экран каждую секунду
  • head показывает первые N строк (самые свежие)

================================================

Настройки по умолчанию:
  Проверка каждые: 60 сек
  Порог мощности:   100W
  GPU индекс:       0

Для изменения настроек отредактируйте:
** /hive/python_scripts/gpu_monitor/gpu_monitor.py"**

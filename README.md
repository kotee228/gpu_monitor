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

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

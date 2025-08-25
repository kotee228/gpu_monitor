#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime
import os

# ==================== НАСТРОЙКИ ====================
# Меняйте эти значения по необходимости
INITIAL_DELAY = 120        # Задержка при старте (секунды)
CHECK_INTERVAL = 60        # Интервал проверки (секунды)
CONFIRMATION_DELAY = 60    # Задержка для подтверждения (секунды)
POWER_THRESHOLD = 100      # Порог мощности (Вт)
GPU_INDEX = 0              # Индекс видеокарты (0, 1, 2...)
# ===================================================

# Пути к лог-файлам
LOG_STATUS = '/hive/python_scripts/gpu_monitor/log_status.txt'
LOG_RESTART = '/hive/python_scripts/gpu_monitor/log_restart.txt'

def get_current_time():
    """Возвращает текущее время в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_with_time(message):
    """Выводит сообщение в консоль с временной меткой"""
    print(f"[{get_current_time()}] {message}")

def reverse_append(filename, message):
    """Добавляет строку в начало файла (новые записи сверху)"""
    timestamped_msg = f"[{get_current_time()}] {message}"
    if os.path.exists(filename):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(timestamped_msg + "\n" + content)
    else:
        with open(filename, 'w') as f:
            f.write(timestamped_msg + "\n")

def get_gpu_power(gpu_index=GPU_INDEX):
    """Получаем текущую мощность GPU по указанному индексу"""
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=power.draw", "--format=csv,noheader,nounits", f"--id={gpu_index}"],
            capture_output=True,
            text=True,
            check=True
        )
        power = float(result.stdout.strip())
        return power
    except Exception as e:
        error_msg = f"Ошибка при получении данных GPU {gpu_index}: {e}"
        print_with_time(error_msg)
        reverse_append(LOG_STATUS, error_msg)
        return None

def restart_miner():
    """Перезапускаем майнер и логируем событие"""
    try:
        restart_msg = f"Мощность ниже порога {POWER_THRESHOLD}W, инициирую перезапуск майнера..."
        print_with_time(restart_msg)
        reverse_append(LOG_STATUS, restart_msg)
        reverse_append(LOG_RESTART, restart_msg)
        
        subprocess.run(["miner", "restart"], check=True)
        
        success_msg = "Майнер успешно перезапущен"
        print_with_time(success_msg)
        reverse_append(LOG_STATUS, success_msg)
        reverse_append(LOG_RESTART, success_msg)
    except Exception as e:
        error_msg = f"Ошибка при перезапуске майнера: {e}"
        print_with_time(error_msg)
        reverse_append(LOG_STATUS, error_msg)
        reverse_append(LOG_RESTART, error_msg)

def main():
    """Основная функция мониторинга с улучшенной логикой"""
    # Вывод текущих настроек
    start_msg = f"=== Запуск GPU монитора ==="
    print_with_time(start_msg)
    reverse_append(LOG_STATUS, start_msg)
    
    config_msg = (f"Конфигурация: GPU {GPU_INDEX}, порог {POWER_THRESHOLD}W, "
                 f"стартовая задержка {INITIAL_DELAY}сек, "
                 f"проверка каждые {CHECK_INTERVAL}сек, "
                 f"подтверждение {CONFIRMATION_DELAY}сек")
    print_with_time(config_msg)
    reverse_append(LOG_STATUS, config_msg)
    
    # Начальная задержка 2 минуты
    initial_delay_msg = f"Начальная задержка {INITIAL_DELAY} секунд..."
    print_with_time(initial_delay_msg)
    reverse_append(LOG_STATUS, initial_delay_msg)
    time.sleep(INITIAL_DELAY)
    
    print_with_time("Начальная задержка завершена, начинаю мониторинг")
    reverse_append(LOG_STATUS, "Начальная задержка завершена, начинаю мониторинг")
    
    # Основной цикл мониторинга
    while True:
        try:
            # Первая проверка мощности
            power = get_gpu_power()
            if power is not None:
                power_msg = f"GPU {GPU_INDEX} текущая мощность: {power:.1f}W"
                print_with_time(power_msg)
                reverse_append(LOG_STATUS, power_msg)
                
                # Если мощность ниже порога - ждем подтверждения
                if power < POWER_THRESHOLD:
                    low_power_msg = (f"Мощность ниже порога {POWER_THRESHOLD}W! "
                                   f"Жду {CONFIRMATION_DELAY}сек для подтверждения...")
                    print_with_time(low_power_msg)
                    reverse_append(LOG_STATUS, low_power_msg)
                    
                    time.sleep(CONFIRMATION_DELAY)
                    
                    # Вторая проверка для подтверждения
                    confirm_power = get_gpu_power()
                    if confirm_power is not None:
                        confirm_msg = f"Подтверждающая проверка: {confirm_power:.1f}W"
                        print_with_time(confirm_msg)
                        reverse_append(LOG_STATUS, confirm_msg)
                        
                        # Если подтвердилось - перезапускаем
                        if confirm_power < POWER_THRESHOLD:
                            restart_miner()
                            # Пауза после перезапуска
                            time.sleep(CHECK_INTERVAL)
                        else:
                            recovery_msg = "Мощность восстановилась, перезапуск отменен"
                            print_with_time(recovery_msg)
                            reverse_append(LOG_STATUS, recovery_msg)
                    else:
                        error_msg = "Ошибка при подтверждающей проверке мощности"
                        print_with_time(error_msg)
                        reverse_append(LOG_STATUS, error_msg)
                
                # Если мощность в норме - просто ждем следующий цикл
                else:
                    time.sleep(CHECK_INTERVAL)
            
            # Если не удалось получить данные о мощности
            else:
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            stop_msg = "Мониторинг остановлен пользователем"
            print_with_time(stop_msg)
            reverse_append(LOG_STATUS, stop_msg)
            break
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {e}"
            print_with_time(error_msg)
            reverse_append(LOG_STATUS, error_msg)
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Создаем пустые лог-файлы при первом запуске
    if not os.path.exists(LOG_STATUS):
        with open(LOG_STATUS, 'w') as f: pass
    if not os.path.exists(LOG_RESTART):
        with open(LOG_RESTART, 'w') as f: pass
    
    main()

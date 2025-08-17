#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime
import os

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
    """Добавляет строку в начало файла"""
    timestamped_msg = f"[{get_current_time()}] {message}"
    if os.path.exists(filename):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(timestamped_msg + "\n" + content)
    else:
        with open(filename, 'w') as f:
            f.write(timestamped_msg + "\n")

def get_gpu_power(gpu_index=0):
    """Получаем текущую мощность GPU"""
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
        error_msg = f"Ошибка при получении данных GPU: {e}"
        print_with_time(error_msg)
        reverse_append(LOG_STATUS, error_msg)
        return None

def restart_miner():
    """Перезапускаем майнер"""
    try:
        restart_msg = "Мощность ниже порога, инициирую перезапуск майнера..."
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
    """Основная функция мониторинга"""
    start_msg = "=== Запуск GPU монитора ==="
    print_with_time(start_msg)
    reverse_append(LOG_STATUS, start_msg)
    
    config_msg = "Конфигурация: проверка каждые 30 сек, порог 100W"
    print_with_time(config_msg)
    reverse_append(LOG_STATUS, config_msg)
    
    while True:
        try:
            power = get_gpu_power()
            if power is not None:
                power_msg = f"GPU 0 текущая мощность: {power:.1f}W"
                print_with_time(power_msg)
                reverse_append(LOG_STATUS, power_msg)
                
                if power < 100:
                    restart_miner()
                    time.sleep(60)  # Пауза после перезапуска
            
            time.sleep(30)
            
        except KeyboardInterrupt:
            stop_msg = "Мониторинг остановлен пользователем"
            print_with_time(stop_msg)
            reverse_append(LOG_STATUS, stop_msg)
            break
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {e}"
            print_with_time(error_msg)
            reverse_append(LOG_STATUS, error_msg)
            time.sleep(30)

if __name__ == "__main__":
    # Создаем пустые лог-файлы при первом запуске
    if not os.path.exists(LOG_STATUS):
        with open(LOG_STATUS, 'w') as f: pass
    if not os.path.exists(LOG_RESTART):
        with open(LOG_RESTART, 'w') as f: pass
    
    main()

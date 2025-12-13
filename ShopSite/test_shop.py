#!/usr/bin/env python3
"""
Простой скрипт для запуска магазина с кнопками очистки и выхода
"""
import sys
import os
from shop_processor import open_shop

def main():
    # Определяем путь к магазину
    if len(sys.argv) > 1:
        shop_path = sys.argv[1]
    else:
        # Автоматически ищем index.html в текущей папке
        shop_path = os.path.join("C:", "Users", "defen", "YandexDisk", "Private", "Projects", "Coddy", "Python", "PyGame", "Square And Coins", "ShopSite", "index.html")
    
    # Начальный баланс
    initial_balance = 50000  # Можно изменить
    
    # Таймаут (5 минут)
    timeout = 600_000
    
    # Запускаем сессию магазина
    result = open_shop(
        shop_path=shop_path,
        initial_balance=initial_balance,
        timeout=timeout
    )
    
    # Возвращаем код завершения
    return 0 if result['status'] in ['success', 'exit'] else 1

if __name__ == "__main__":
    main()
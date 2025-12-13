"""
Магазинный процессор для интеграции с React магазином
Интерфейс для внешних программ
"""
import json
import time
import os
import sys
import urllib.parse
from datetime import datetime
from typing import Dict, Optional, Any, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="reports.log", encoding="utf-8"
)
logger = logging.getLogger(__name__)


class ShopSession:
    """
    Сессия работы с магазином
    """
    
    def __init__(self, driver, initial_balance: int = 30000):
        self.driver = driver
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.purchases = []
        self.session_data = {}
        self.is_active = True
    
    def execute_js(self, script: str, *args) -> Any:
        """Выполняет JavaScript в контексте страницы"""
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            logger.error(f"JS execution error: {e}")
            return None
    
    def get_local_storage(self, key: str) -> Optional[str]:
        """Получает значение из localStorage"""
        script = f"return localStorage.getItem('{key}');"
        return self.execute_js(script)
    
    def set_local_storage(self, key: str, value: str):
        """Устанавливает значение в localStorage"""
        script = f"localStorage.setItem('{key}', arguments[0]);"
        self.execute_js(script, value)
    
    def remove_local_storage(self, key: str):
        """Удаляет значение из localStorage"""
        script = f"localStorage.removeItem('{key}');"
        self.execute_js(script)
    
    def wait_for_element(self, selector: str, by=By.CLASS_NAME, timeout: int = 10):
        """Ожидает появления элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, selector)))
        except Exception as e:
            logger.error(f"Element wait error: {e}")
            return None
    
    def update_balance_display(self):
        """Обновляет отображение баланса в магазине"""
        try:
            script = """
                const balanceEl = document.querySelector('.balance-amount');
                if (balanceEl) {
                    return balanceEl.textContent;
                }
                return null;
            """
            return self.execute_js(script)
        except Exception as e:
            logger.error(f"Balance update error: {e}")
            return None


class ShopProcessor:
    """
    Основной процессор для работы с магазином
    """
    
    def __init__(self):
        self.driver = None
        self.session = None
    
    def initialize_driver(self, headless: bool = True) -> bool:
        """
        Инициализирует WebDriver
        
        Args:
            headless: Запуск без графического интерфейса
            
        Returns:
            bool: Успешность инициализации
        """
        try:
            options = Options()
            
            if headless:
                options.add_argument("--headless")
            
            # Базовые опции для стабильной работы
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280,800")
            
            # Отключение предупреждений и блокировок
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--log-level=3")
            
            # Настройки для локальных файлов
            options.add_argument("--allow-file-access-from-files")
            options.add_argument("--disable-web-security")
            
            # Автоматическая установка драйвера
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            logger.info("WebDriver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            return False
    
    def open_shop(self, shop_path: str, initial_balance: int = 30000) -> Tuple[bool, str]:
        """
        Открывает магазин и устанавливает начальный баланс
        
        Args:
            shop_path: Путь к index.html магазина
            initial_balance: Начальный баланс пользователя
            
        Returns:
            Tuple[bool, str]: (успешность, сообщение об ошибке)
        """
        try:
            # Преобразуем путь в URL
            if not shop_path.startswith(('http://', 'https://', 'file://')):
                url = self._path_to_url(shop_path)
            else:
                url = shop_path
            
            logger.info(f"Opening shop at: {url}")
            
            # Открываем магазин
            self.driver.get(url)
            
            # Ждем загрузки магазина
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
            )
            
            if not element:
                return False, "Shop failed to load"
            
            # Создаем сессию
            self.session = ShopSession(self.driver, initial_balance)
            
            # Устанавливаем начальный баланс
            self._set_initial_balance(initial_balance)
            
            # Обновляем страницу для применения баланса
            self.driver.refresh()
            time.sleep(2)
            
            logger.info("Shop opened successfully")
            return True, "Shop opened"
            
        except Exception as e:
            logger.error(f"Failed to open shop: {e}")
            return False, str(e)
    
    def _path_to_url(self, filepath: str) -> str:
        """Конвертирует путь к файлу в file:// URL"""
        normalized = os.path.normpath(filepath)
        
        if sys.platform == 'win32':
            # Windows
            if ':' in normalized:
                drive, path = normalized.split(':', 1)
                encoded_path = urllib.parse.quote(path.replace('\\', '/'), safe='/')
                return f"file:///{drive}:{encoded_path}"
            else:
                encoded_path = urllib.parse.quote(normalized.replace('\\', '/'), safe='/')
                return f"file:///{encoded_path}"
        else:
            # Unix/Linux/Mac
            encoded_path = urllib.parse.quote(normalized, safe='/')
            return f"file://{encoded_path}"
    
    def _set_initial_balance(self, balance: int) -> bool:
        """Устанавливает начальный баланс в магазине"""
        try:
            data = {
                'balance': balance,
                'timestamp': datetime.now().isoformat()
            }
            
            script = f"""
                localStorage.setItem('python_initial_balance', '{json.dumps(data)}');
                return true;
            """
            
            result = self.session.execute_js(script)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Failed to set initial balance: {e}")
            return False
    
    def wait_for_action(self, timeout: int = 300) -> Dict[str, Any]:
        """
        Ожидает действий пользователя в магазине
        
        Args:
            timeout: Максимальное время ожидания в секундах
            
        Returns:
            Dict с результатом операции
        """
        start_time = time.time()
        logger.info(f"Waiting for user action (timeout: {timeout}s)")
        
        while time.time() - start_time < timeout:
            try:
                # Проверяем, не закрыто ли окно
                if not self.driver.window_handles:
                    logger.info("Browser window was closed")
                    return self._create_result("window_closed", "User closed the browser window")
                
                # Проверяем запрос на выход
                exit_data = self.session.get_local_storage('shop_exit_requested')
                if exit_data:
                    logger.info("Exit requested by user")
                    self.session.remove_local_storage('shop_exit_requested')
                    return self._handle_exit_request(exit_data)
                
                # Проверяем готовность покупки
                if self._is_purchase_ready():
                    logger.info("Purchase ready for processing")
                    return self._handle_purchase()
                
                # Небольшая пауза между проверками
                time.sleep(0.5)
                
            except NoSuchWindowException:
                logger.info("Browser window was closed (exception)")
                return self._create_result("window_closed", "Browser window was closed")
                
            except WebDriverException as e:
                if "chrome not reachable" in str(e).lower():
                    logger.info("Connection to browser lost")
                    return self._create_result("connection_lost", "Connection to browser was lost")
                logger.debug(f"WebDriver exception: {e}")
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(1)
        
        # Таймаут
        logger.warning("Action timeout reached")
        return self._create_result("timeout", "Action timeout reached")
    
    def _is_purchase_ready(self) -> bool:
        """Проверяет, готова ли покупка к обработке"""
        try:
            script = "return document.body.getAttribute('data-purchase-ready') === 'true';"
            return bool(self.session.execute_js(script))
        except:
            return False
    
    def _handle_purchase(self) -> Dict[str, Any]:
        """Обрабатывает готовую покупку"""
        try:
            # Получаем данные о покупке
            purchase_data = self.session.get_local_storage('python_purchase_data')
            if not purchase_data:
                return self._create_result("error", "No purchase data found")
            
            # Парсим данные
            data = json.loads(purchase_data)
            
            # Обновляем статус на "в процессе"
            data['status'] = 'processing'
            self.session.set_local_storage('python_purchase_data', json.dumps(data))
            
            # Извлекаем информацию
            cart = data.get('cart', [])
            total = data.get('total', 0)
            initial_balance = data.get('initial_balance', self.session.initial_balance)
            
            # Проверяем корректность
            if not cart:
                return self._create_result("error", "Cart is empty")
            
            # Проверяем баланс
            if initial_balance < total:
                return self._create_result(
                    "error",
                    f"Insufficient funds: need {total}, have {initial_balance}",
                    {"required": total, "available": initial_balance}
                )
            
            # Выполняем покупку
            new_balance = initial_balance - total
            self.session.current_balance = new_balance
            
            # Создаем запись о покупке
            purchase_record = {
                "session_id": data.get('sessionId', 'unknown'),
                "timestamp": data.get('timestamp', datetime.now().isoformat()),
                "items": cart,
                "total_amount": total,
                "balance_before": initial_balance,
                "balance_after": new_balance,
                "processed_at": datetime.now().isoformat()
            }
            
            self.session.purchases.append(purchase_record)
            
            # Обновляем статус в браузере
            data['status'] = 'completed'
            data['processing_result'] = {
                "status": "success",
                "message": "Purchase processed successfully"
            }
            
            self.session.set_local_storage('python_purchase_data', json.dumps(data))
            
            # Ждем, чтобы магазин обработал обновление
            time.sleep(1)
            
            # Очищаем данные о покупке
            self.session.remove_local_storage('python_purchase_data')
            
            # Создаем результат
            result = self._create_result(
                "purchase_completed",
                "Purchase completed successfully",
                {
                    "purchase": purchase_record,
                    "summary": {
                        "items_count": len(cart),
                        "total_spent": total,
                        "remaining_balance": new_balance
                    }
                }
            )
            
            logger.info(f"Purchase processed: {len(cart)} items, total {total}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return self._create_result("error", "Invalid purchase data format")
            
        except Exception as e:
            logger.error(f"Purchase processing error: {e}")
            return self._create_result("error", f"Purchase processing failed: {str(e)}")
    
    def _handle_exit_request(self, exit_data: str) -> Dict[str, Any]:
        """Обрабатывает запрос на выход"""
        try:
            data = json.loads(exit_data)
            
            # Создаем сводку сессии
            session_summary = {
                "session_id": data.get('sessionId', 'unknown'),
                "timestamp": data.get('timestamp', datetime.now().isoformat()),
                "initial_balance": self.session.initial_balance,
                "final_balance": self.session.current_balance,
                "total_spent": self.session.initial_balance - self.session.current_balance,
                "purchases_count": len(self.session.purchases),
                "cart_cleared": data.get('cartCleared', False)
            }
            
            # Даем время на закрытие окна
            time.sleep(2)
            
            result = self._create_result(
                "exit",
                "User exited the shop",
                {"session_summary": session_summary}
            )
            
            logger.info(f"Exit processed: {session_summary}")
            return result
            
        except Exception as e:
            logger.error(f"Exit processing error: {e}")
            return self._create_result("exit", "User exited with errors")
    
    def _create_result(self, status: str, message: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Создает стандартизированный результат
        
        Args:
            status: Статус операции
            message: Сообщение
            data: Дополнительные данные
            
        Returns:
            Стандартизированный словарь результата
        """
        result = {
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if data:
            result["data"] = data
        
        return result
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Возвращает сводку текущей сессии"""
        if not self.session:
            return {}
        
        return {
            "initial_balance": self.session.initial_balance,
            "current_balance": self.session.current_balance,
            "total_spent": self.session.initial_balance - self.session.current_balance,
            "purchases_count": len(self.session.purchases),
            "purchases": self.session.purchases
        }
    
    def cleanup(self):
        """Очищает ресурсы"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver resources cleaned up")
        except:
            pass


# ============================================================================
# Публичный интерфейс для внешних программ
# ============================================================================

def open_shop(
    shop_path: str,
    initial_balance: int = 30000,
    timeout: int = 300,
    headless: bool = False
) -> Dict[str, Any]:
    """
    Основная функция для обработки сессии магазина
    
    Args:
        shop_path: Путь к файлу index.html магазина
        initial_balance: Начальный баланс пользователя
        timeout: Таймаут ожидания в секундах
        headless: Запуск браузера без графического интерфейса
        
    Returns:
        Dict с результатом сессии в формате:
        {
            "status": "success|exit|error|timeout|window_closed|connection_lost",
            "message": "Описание результата",
            "timestamp": "ISO timestamp",
            "data": {
                // Дополнительные данные в зависимости от статуса
            }
        }
    """
    processor = ShopProcessor()
    
    try:
        # Инициализируем драйвер
        if not processor.initialize_driver(headless):
            return {
                "status": "error",
                "message": "Failed to initialize browser",
                "timestamp": datetime.now().isoformat()
            }
        
        # Открываем магазин
        success, message = processor.open_shop(shop_path, initial_balance)
        if not success:
            return {
                "status": "error",
                "message": f"Failed to open shop: {message}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Ждем действий пользователя
        result = processor.wait_for_action(timeout)
        
        # Добавляем сводку сессии в данные
        if "data" not in result:
            result["data"] = {}
        
        result["data"]["session_summary"] = processor.get_session_summary()
        
        return result
        
    except Exception as e:
        logger.error(f"Shop session error: {e}")
        return {
            "status": "error",
            "message": f"Shop session failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        
    finally:
        processor.cleanup()


def quick_shop_test(shop_path: str, initial_balance: int = 50000) -> Dict[str, Any]:
    """
    Быстрый тест магазина (для отладки)
    
    Args:
        shop_path: Путь к магазину
        initial_balance: Начальный баланс
        
    Returns:
        Результат теста
    """
    logger.info("Starting quick shop test")
    
    result = open_shop(
        shop_path=shop_path,
        initial_balance=initial_balance,
        timeout=120,
        headless=False
    )
    
    # Для теста также сохраняем результат в файл
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shop_test_result_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Test result saved to {filename}")
        
    except Exception as e:
        logger.error(f"Failed to save test result: {e}")
    
    return result


# ============================================================================
# Вспомогательные функции для интеграции
# ============================================================================

def validate_shop_files(shop_path: str) -> Tuple[bool, str]:
    """
    Проверяет наличие всех необходимых файлов магазина
    
    Args:
        shop_path: Путь к папке магазина или index.html
        
    Returns:
        Tuple[bool, str]: (валидность, сообщение)
    """
    try:
        # Если передан путь к папке, добавляем index.html
        if os.path.isdir(shop_path):
            index_path = os.path.join(shop_path, "index.html")
        else:
            index_path = shop_path
        
        # Проверяем существование index.html
        if not os.path.exists(index_path):
            return False, f"File not found: {index_path}"
        
        # Определяем папку магазина
        shop_dir = os.path.dirname(index_path)
        
        # Проверяем наличие остальных файлов
        required_files = ["index.html", "styles.css", "shop.js", "texts.js", "products.js"]
        missing_files = []
        
        for file in required_files:
            file_path = os.path.join(shop_dir, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if missing_files:
            return False, f"Missing files: {', '.join(missing_files)}"
        
        return True, "All shop files found"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def get_shop_info(shop_path: str) -> Dict[str, Any]:
    """
    Получает информацию о магазине
    
    Args:
        shop_path: Путь к магазину
        
    Returns:
        Информация о магазине
    """
    try:
        # Определяем папку магазина
        if os.path.isdir(shop_path):
            shop_dir = shop_path
            index_path = os.path.join(shop_dir, "index.html")
        else:
            index_path = shop_path
            shop_dir = os.path.dirname(index_path)
        
        # Читаем products.js для получения списка товаров
        products_path = os.path.join(shop_dir, "products.js")
        products_data = {}
        
        if os.path.exists(products_path):
            with open(products_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Извлекаем данные из JS файла
                import re
                match = re.search(r'const products = ({.*?});', content, re.DOTALL)
                if match:
                    try:
                        products_data = json.loads(match.group(1))
                    except:
                        pass
        
        # Собираем информацию
        info = {
            "shop_directory": shop_dir,
            "index_file": index_path,
            "files": {
                "index.html": os.path.exists(os.path.join(shop_dir, "index.html")),
                "styles.css": os.path.exists(os.path.join(shop_dir, "styles.css")),
                "shop.js": os.path.exists(os.path.join(shop_dir, "shop.js")),
                "texts.js": os.path.exists(os.path.join(shop_dir, "texts.js")),
                "products.js": os.path.exists(os.path.join(shop_dir, "products.js"))
            },
            "products_count": len(products_data.get("items", [])),
            "products": [p.get("showName", "Unknown") for p in products_data.get("items", [])[:5]],
            "validation": validate_shop_files(shop_path)
        }
        
        return info
        
    except Exception as e:
        return {
            "error": str(e),
            "validation": (False, f"Error: {str(e)}")
        }


# ============================================================================
# Точка входа для командной строки (только для тестирования)
# ============================================================================

if __name__ == "__main__":
    # Эта часть только для ручного тестирования
    # При интеграции используйте process_shop_session напрямую
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Shop Processor')
    parser.add_argument('--path', '-p', required=True, help='Path to shop index.html')
    parser.add_argument('--balance', '-b', type=int, default=50000, help='Initial balance')
    parser.add_argument('--timeout', '-t', type=int, default=300, help='Timeout in seconds')
    parser.add_argument('--headless', '-H', action='store_true', help='Run in headless mode')
    parser.add_argument('--validate', '-V', action='store_true', help='Validate shop files only')
    parser.add_argument('--info', '-i', action='store_true', help='Get shop info only')
    
    args = parser.parse_args()
    
    if args.validate:
        valid, message = validate_shop_files(args.path)
        print(f"Validation: {'PASS' if valid else 'FAIL'}")
        print(f"Message: {message}")
        sys.exit(0 if valid else 1)
    
    if args.info:
        info = get_shop_info(args.path)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Запускаем тест
    print("Starting shop session...")
    result = open_shop(
        shop_path=args.path,
        initial_balance=args.balance,
        timeout=args.timeout,
        headless=args.headless
    )
    
    print("\n" + "="*60)
    print("SESSION RESULT:")
    print("="*60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Код завершения
    if result["status"] in ["purchase_completed", "exit"]:
        sys.exit(0)
    else:
        sys.exit(1)
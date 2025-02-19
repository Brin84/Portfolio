import logging  # Импортируем модуль logging для ведения журнала событий.
import time  # Импортируем модуль time для измерения времени выполнения запроса.

logger = logging.getLogger('project_logger')  # Создаем или получаем логгер с именем 'project_logger'.


class LoggingMiddleware:  # Определяем класс middleware под названием LoggingMiddleware.
    def __init__(self, get_response):  # Метод инициализации, который принимает параметр get_response.
        self.get_response = get_response  # Сохраняем переданную функцию get_response для дальнейшего использования.

    def __call__(self, request):  # Метод, который будет вызываться при каждом запросе.
        ip = request.META.get('REMOTE_ADDR', '')  # Получаем IP-адрес клиента из метаданных запроса.
        method = request.method  # Получаем метод HTTP (например, GET, POST) из запроса.
        path = request.path  # Получаем путь запрашиваемого URL.

        # Логируем информацию о входящем запросе.
        logger.info(f"Request: {method} {path} from {ip}")

        start_time = time.time()  # Записываем текущее время для измерения длительности обработки запроса.
        response = self.get_response(request)  # Передаем запрос следующему в цепочке middleware или обработчику.
        duration = time.time() - start_time  # Вычисляем, сколько времени заняла обработка запроса.

        # Логируем информацию об ответе и времени обработки.
        logger.info(f'Response: {method} {path}: {response.status_code} (took {duration:.2f} seconds)')

        return response  # Возвращаем ответ, который был получен от следующего middleware или обработчика.

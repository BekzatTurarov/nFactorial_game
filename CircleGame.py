import pygame  # Импорт модуля Pygame для создания игр и графических приложений
import math  # Импорт модуля math для математических функций и констант
import os  # Импорт модуля os для работы с операционной системой

pygame.init()  # Инициализация всех подсистем Pygame

WIDTH, HEIGHT = 1000, 800  # Задание ширины и высоты окна игры
WINDOW_SIZE = (WIDTH, HEIGHT)  # Создание кортежа с размерами окна игры
BLACK = (0, 0, 0)  # Задание цвета черного в формате RGB
RED = (255, 0, 0)  # Задание цвета красного в формате RGB
YELLOW = (255, 255, 0)  # Задание цвета желтого в формате RGB
GREEN = (0, 255, 0)  # Задание цвета зеленого в формате RGB
WHITE = (255, 255, 255)  # Задание цвета белого в формате RGB

screen = pygame.display.set_mode(WINDOW_SIZE)  # Создание окна игры заданного размера
pygame.display.set_caption("The Circle Game")  # Задание заголовка окна

background_image_path = os.path.join(os.path.dirname(__file__), "background_photo.jpg")
# Создание пути к фоновому изображению игры

background_image = pygame.image.load(background_image_path)  # Загрузка фонового изображения
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
# Изменение размера фонового изображения до размеров окна игры


def distance(point1, point2):
    # Функция для расчета расстояния между двумя точками
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_between(p1, p2):
    # Функция для расчета угла между двумя точками
    x1, y1 = p1
    x2, y2 = p2
    return math.atan2(y2 - y1, x2 - x1)


class PerfectCircleGame:
    # Класс игры "The Circle Game"

    def __init__(self):
        # Метод-конструктор класса
        # Инициализация переменных и состояний игры

        self.center = (WIDTH // 2, HEIGHT // 2)  # Определение координат центра окна игры
        self.error_radius = 10  # Определение радиуса погрешности для точек
        self.points = []  # Список точек, задающих отрезки нарисованной фигуры
        self.colors = []  # Список цветов для каждого отрезка
        self.clock = pygame.time.Clock()  # Создание объекта Clock для контроля FPS
        self.too_close = False  # Флаг, указывающий на наличие точки, слишком близкой к центру
        self.percentage = 0  # Процент правильных точек
        self.start_time = None  # Время начала отрисовки
        self.drawing = False  # Флаг, указывающий на отрисовку фигуры
        self.time_up = False  # Флаг, указывающий на окончание времени отрисовки
        self.total_angle = 0  # Общий угол фигуры
        self.last_point = None  # Последняя нарисованная точка
        self.best_result = 0  # Лучший результат игры

    def handle_events(self):
        # Метод для обработки событий Pygame

        for event in pygame.event.get():
            # Перебор всех событий, полученных от Pygame

            if event.type == pygame.QUIT:
                # Обработка события закрытия окна игры
                pygame.quit()  # Завершение работы Pygame
                quit()  # Завершение работы программы

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка события нажатия кнопки мыши

                self.points = []  # Очистка списка точек
                self.colors = []  # Очистка списка цветов
                self.too_close = False  # Сброс флага слишком близкой точки
                self.time_up = False  # Сброс флага окончания времени
                self.start_time = pygame.time.get_ticks()  # Запись текущего времени
                self.drawing = True  # Установка флага отрисовки
                self.total_angle = 0  # Сброс общего угла
                self.last_point = None  # Сброс последней точки

            elif event.type == pygame.MOUSEBUTTONUP:
                # Обработка события отпускания кнопки мыши

                self.drawing = False  # Снятие флага отрисовки

                if self.total_angle >= 1.5 * math.pi:
                    # Если общий угол фигуры больше или равен 1.5 * pi (полный круг)
                    self.calculate_percentage()  # Расчет процента правильных точек
                    self.update_best_result()  # Обновление лучшего результата

            elif event.type == pygame.MOUSEMOTION and self.drawing and not self.time_up:
                # Обработка события движения мыши при нажатой кнопке

                if distance(event.pos, self.center) <= self.error_radius:
                    # Если расстояние от текущей точки до центра окна меньше или равно радиусу погрешности
                    self.too_close = True  # Установка флага слишком близкой точки
                elif distance(event.pos, self.center) > self.error_radius * 10:
                    # Если расстояние от текущей точки до центра окна больше 10 раз радиуса погрешности
                    self.points.append(event.pos)  # Добавление точки в список
                    self.colors.append(self.get_line_color(event.pos))  # Получение цвета для отрезка
                    if self.last_point is not None:
                        angle1 = angle_between(self.last_point, self.center)
                        angle2 = angle_between(event.pos, self.center)
                        angle_diff = angle2 - angle1
                        if angle_diff < -math.pi:
                            angle_diff += 2 * math.pi
                        elif angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        self.total_angle += abs(angle_diff)
                    self.last_point = event.pos

                self.calculate_percentage()

    def calculate_percentage(self):
        # Метод для расчета процента правильных точек

        num_points = len(self.points)  # Количество точек
        num_correct_points = 0  # Количество правильных точек

        for point in self.points:
            dist_from_center = distance(point, self.center)  # Расстояние от точки до центра
            if abs(dist_from_center - distance(self.points[0], self.center)) <= self.error_radius:
                # Если расстояние от текущей точки до центра окна примерно равно расстоянию от первой точки до центра
                num_correct_points += 1  # Увеличение количества правильных точек

        percentage = (num_correct_points / num_points) * 100 if num_points > 0 else 0
        # Расчет процента правильных точек, если есть точки, иначе 0
        self.percentage = percentage  # Запись процента правильных точек

    def check_time_limit(self):
        # Метод для проверки временного ограничения

        if self.start_time and self.drawing:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            # Расчет прошедшего времени с начала отрисовки в секундах

            if elapsed_time > 5:
                # Если прошло больше 5 секунд
                self.time_up = True  # Установка флага окончания времени
                self.start_time = None  # Сброс времени
                self.points = []  # Очистка списка точек
                self.colors = []  # Очистка списка цветов
                self.drawing = False  # Снятие флага отрисовки

    def get_line_color(self, point):
        # Метод для получения цвета отрезка в зависимости от расстояния до центра

        dist_from_center = distance(point, self.center)  # Расстояние от точки до центра

        if abs(dist_from_center - distance(self.points[0], self.center)) <= self.error_radius:
            # Если расстояние от точки до центра примерно равно расстоянию от первой точки до центра
            return GREEN  # Зеленый цвет

        elif abs(dist_from_center - distance(self.points[0], self.center)) <= self.error_radius * 2:
            # Если расстояние от точки до центра примерно в 2 раза больше расстояния от первой точки до центра
            return YELLOW  # Желтый цвет

        else:
            return RED  # Красный цвет

    def update_best_result(self):
        # Метод для обновления лучшего результата

        if self.percentage > self.best_result:
            # Если текущий результат лучше лучшего
            self.best_result = self.percentage  # Обновление лучшего результата

    def draw(self):
        # Метод для отрисовки элементов игры на экране

        screen.blit(background_image, (0, 0))  # Отрисовка фонового изображения на экране

        font = pygame.font.Font(None, 50)  # Создание объекта шрифта размером 50

        header_text = font.render("The Circle Game", True, WHITE)  # Создание текстовой поверхности заголовка
        header_rect = header_text.get_rect(center=(WIDTH // 2, 50))  # Получение прямоугольника заголовка
        screen.blit(header_text, header_rect)  # Отрисовка заголовка на экране

        pygame.draw.circle(screen, WHITE, self.center, 20)  # Отрисовка белой окружности в центре экрана

        for i in range(1, len(self.points)):
            # Перебор всех отрезков в списке точек
            pygame.draw.line(screen, self.colors[i - 1], self.points[i - 1], self.points[i], 15)
            # Отрисовка отрезка между текущей и предыдущей точками с заданным цветом и толщиной

        font = pygame.font.Font(None, 25)  # Создание объекта шрифта размером 25

        self.check_time_limit()  # Проверка временного ограничения

        if self.time_up:
            # Если время истекло
            text = font.render("TOO SLOW", True, WHITE)  # Создание текстовой поверхности "TOO SLOW"
        elif self.too_close:
            # Если есть точка, слишком близкая к центру
            text = font.render("Too close to dot", True, WHITE)  # Создание текстовой поверхности "Too close to dot"
        elif not self.drawing and self.total_angle < 1.5 * math.pi:
            # Если фигура не была полностью нарисована
            text = font.render("Draw a full circle", True, WHITE)  # Создание текстовой поверхности "Draw a full circle"
        else:
            text = font.render(f"{self.percentage:.2f}%", True, WHITE)
            # Создание текстовой поверхности с текущим процентом правильных точек

        text_rect = text.get_rect(center=(self.center[0], self.center[1] + 50))
        # Получение прямоугольника для текста
        screen.blit(text, text_rect)  # Отрисовка текста на экране

        best_result_text = font.render(f"Best result: {self.best_result:.2f}%", True, WHITE)
        # Создание текстовой поверхности с лучшим результатом
        best_result_rect = best_result_text.get_rect(center=(self.center[0], self.center[1] + 90))
        # Получение прямоугольника для лучшего результата
        screen.blit(best_result_text, best_result_rect)  # Отрисовка лучшего результата на экране

        made_by_text = font.render("Made by Bekzat Turarov", True, WHITE)
        # Создание текстовой поверхности с информацией об авторе
        made_by_rect = made_by_text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
        # Получение прямоугольника для информации об авторе
        screen.blit(made_by_text, made_by_rect)  # Отрисовка информации об авторе на экране

        pygame.display.update()  # Обновление содержимого окна

    def run(self):
        # Метод для запуска игры

        while True:
            # Бесконечный цикл игры

            self.handle_events()  # Обработка событий
            self.draw()  # Отрисовка элементов игры


game = PerfectCircleGame()  # Создание объекта игры
game.run()  # Запуск игры

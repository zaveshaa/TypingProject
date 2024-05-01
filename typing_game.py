import pygame
import random
import time
from menu import Menu  # Импортируем класс Menu из отдельного файла

# Размеры окна
WIDTH, HEIGHT = 800, 600
BG_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
MISTAKE_COLOR = (255, 0, 0)

class TypingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Тренажер слепой печати")

        self.font = pygame.font.Font(None, 36)
        self.target_sentence = None
        self.typing_start_time = None
        self.typing_input = ""
        self.score = 0
        self.mistakes = []

        self.last_update_time = 0
        self.update_interval = 1  # Обновление раз в секунду

        # Меню
        self.menu = True
        self.result_text = ""
        self.menu_info = ""
        self.start_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, 50)

    def load_sentences(self):
        with open("sentences.txt", "r", encoding="utf-8") as file:
            sentences = [line.strip() for line in file if line.strip()]
        return sentences

    def new_sentence(self):
        sentences = self.load_sentences()
        self.target_sentence = random.choice(sentences)
        self.typing_start_time = time.time()
        self.typing_input = ""
        self.result_text = ""
        self.menu_info = ""
        self.mistakes = []

    def check_mistakes(self):
        self.mistakes = [i for i in range(len(self.typing_input)) if i < len(self.target_sentence) and self.typing_input[i] != self.target_sentence[i]]

    def calculate_speed(self):
        if self.typing_start_time:
            typing_time = time.time() - self.typing_start_time
            if typing_time > 0:
                self.score = int(len(self.typing_input) / (typing_time / 60))
            else:
                self.score = 0
        else:
            self.score = 0

    def draw_text(self):
        self.check_mistakes()
        self.calculate_speed()

        text_surface = self.font.render(self.target_sentence, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)

        for i in range(len(self.target_sentence)):
            if i < len(self.typing_input):
                if i in self.mistakes:
                    color = MISTAKE_COLOR
                else:
                    color = TEXT_COLOR
                char_surface = self.font.render(self.typing_input[i], True, color)
                char_rect = char_surface.get_rect(center=(WIDTH // 2 + (i - len(self.typing_input) / 2) * 20, HEIGHT // 2 + 50))
                self.screen.blit(char_surface, char_rect)
            else:
                break

        score_surface = self.font.render(f"Скорость: {self.score} зн/мин", True, TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(score_surface, score_rect)

    def draw_result(self):
        result_font = pygame.font.Font(None, 48)
        result_surface = result_font.render(self.result_text, True, TEXT_COLOR)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(result_surface, result_rect)

        input_surface = self.font.render(self.typing_input, True, TEXT_COLOR)
        input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(input_surface, input_rect)

        info_surface = self.font.render(self.menu_info, True, TEXT_COLOR)
        info_rect = info_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(info_surface, info_rect)

    def draw_menu(self):
        menu = Menu(self.screen, self.start_button, self.font)
        menu.draw(self.result_text, self.menu_info)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif self.menu:
                        if event.key == pygame.K_RETURN:
                            self.menu = False
                            self.new_sentence()
                            self.menu_info = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.typing_input = self.typing_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.typing_input == self.target_sentence:
                            typing_end_time = time.time()
                            typing_time = typing_end_time - self.typing_start_time
                            self.calculate_speed()
                            self.result_text = f"Набор завершен! Скорость: {self.score} зн/мин"
                            self.menu_info = "Нажмите Enter, чтобы начать новую тренировку."
                            self.menu = True
                        else:
                            self.result_text = "Ошибка! Попробуйте снова."
                    else:
                        self.typing_input += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if self.start_button.collidepoint(mouse_x, mouse_y):
                            self.menu = False
                            self.new_sentence()
                            self.menu_info = ""

            self.screen.fill(BG_COLOR)

            if self.menu:
                self.draw_menu()
            elif self.result_text:
                self.draw_result()
            else:
                self.draw_text()

            pygame.display.flip()
            clock.tick(60)

            # Обновление зн/мин раз в секунду
            if time.time() - self.last_update_time >= self.update_interval:
                self.calculate_speed()
                self.last_update_time = time.time()

if __name__ == "__main__":
    game = TypingGame()
    game.run()

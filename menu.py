import pygame

class Menu:
    def __init__(self, screen, start_button, font):
        self.screen = screen
        self.start_button = start_button
        self.font = font

    def draw(self, result_text, menu_info):
        self.screen.fill((255, 255, 255))
        
        title_font = pygame.font.Font(None, 64)
        title_surface = title_font.render("Меню", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(title_surface, title_rect)

        result_surface = self.font.render(result_text, True, (0, 0, 0))
        result_rect = result_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(result_surface, result_rect)

        info_surface = self.font.render(menu_info, True, (0, 0, 0))
        info_rect = info_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50))
        self.screen.blit(info_surface, info_rect)

        pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)
        start_font = self.font.render("Начать", True, (0, 0, 0))
        start_rect = start_font.get_rect(center=self.start_button.center)
        self.screen.blit(start_font, start_rect)

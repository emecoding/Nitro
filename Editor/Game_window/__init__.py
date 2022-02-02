import pygame

class Game_Window:
    def __init__(self, project_data):
        self.__project_data = project_data

        self.__window = pygame.display.set_mode((self.__project_data["EDITOR"]["GAME_WINDOW_WIDTH"], self.__project_data["EDITOR"]["GAME_WINDOW_HEIGHT"]))
        pygame.display.set_caption("Game Window")

        self.__should_close = False

    def close(self):
        self.__should_close = True

    def main_loop(self, editor_win):
        while self.__should_close == False:
            if editor_win.isVisible():
                self.close()
            self.__window.fill((255, 255, 255))
            pygame.display.update()
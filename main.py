import sys
import pygame
import scenes


class Game:
    def __init__(self, width=960, height=540, title="GGJ_2026"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        # SceneManager will instantiate the initial scene
        self.manager = scenes.SceneManager(scenes.MenuScene, self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    if self.manager.current_scene:
                        self.manager.current_scene.handle_event(event)

            if self.manager.current_scene:
                self.manager.current_scene.run_frame(self.screen, dt)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()

import pygame
import game


class Display():
    running = True

    screen_res = (1000, 800)

    def __init__(self):
        self.screen = pygame.display.set_mode(self.screen_res)
        pygame.display.set_caption('Wave')
        clock = pygame.time.Clock()

        self.game = game.Game(self)

        self.components = [self.game]

        while self.running:
            events = pygame.event.get()
            self.inputs(events)
            self.update()
            self.render()

            clock.tick(30)

        pygame.quit()

    def update(self):
        for c in self.components:
            c.update()

    def render(self):
        self.screen.fill((0, 0, 0))

        for c in self.components:
            c.render(self.screen)

        pygame.display.flip()

    def inputs(self, events):
        for event in events:
            if event.type == pygame.QUIT: quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 27: quit()

        for c in self.components:
            c.inputs(events)

    def quit(self):
        self.running = False

if __name__ == '__main__':
    Display()

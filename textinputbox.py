import sys
import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, correct_answer, game):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = pygame.font.SysFont('Arial', 30)
        self.active = False
        self.text = "Vastus: "
        self.correct_answer = correct_answer
        self.render_text()
        self.game = game

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()

    def check_answer(self):
        if self.text == "Vastus: " + self.correct_answer:
            self.game.points += 2
        if self.text == "Proovi uuesti: " + self.correct_answer:
            self.game.points += 1
        if self.text == "Vastus: " + self.correct_answer or self.text == "Proovi uuesti: " + self.correct_answer:
            self.kill()
        else:
            self.text = "Proovi uuesti: "

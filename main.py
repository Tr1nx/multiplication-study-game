import pygame
import random
import sys
import base64

from player import Player
from question import QuestionSprite
from star import Star
from textinputbox import TextInputBox
from questions import level_1_questions, level_2_questions
from obstacle import Asteroid
from buttons import Button, Button2, Button3
from io import BytesIO
from PIL import Image
from pic2str import background
from pic2str import background_music


class Game:
    def __init__(self, x, y, speed):
        self.intro = True
        self.end = False
        self.points = 0
        self.level = 0
        self.questions_list = []
        self.text_boxes = []
        self.screen = pygame.display.set_mode([width, height])

        # Load byte data
        byte_data = base64.b64decode(background)
        image = Image.open(BytesIO(byte_data))
        background_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        self.background = background_image
        self.bg = pygame.transform.scale(self.background, (width, height))

        # Player setup
        player_sprite = Player((width / 2, height), width, speed)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Star setup
        star_sprite = Star(x, y, speed)
        self.star = pygame.sprite.GroupSingle(star_sprite)

        # Asteroids setup
        self.asteroids = []
        asteroid_y = 5
        for _ in range(6):
            asteroid = Asteroid(random.randint(10, width), asteroid_y, speed, self)
            # Set lag so that wouldn't appear all at once
            asteroid_y -= 30
            asteroid_sprite = pygame.sprite.GroupSingle(asteroid)
            asteroid_sprite.draw(self.screen)
            self.asteroids.append(asteroid_sprite)

    def run(self):
        self.player.update()
        self.star.update(height, width, self.player.sprite.rect.x, self.player.sprite.rect.y)
        self.player.draw(self.screen)
        self.star.draw(self.screen)

        for asteroid in self.asteroids:
            asteroid.update(height, width, self.player.sprite.rect.x, self.player.sprite.rect.y)
            asteroid.draw(self.screen)

    def collision(self):
        return (-40 <= self.player.sprite.rect.x - self.star.sprite.rect.x <= 20) \
                and abs(self.player.sprite.rect.y - self.star.sprite.rect.y) <= 20

    def ask_question(self, event_list):
        # Take first question and textbox with correct answer from list
        question = self.questions_list[0]
        text_box = self.text_boxes[0]
        question.draw(self.screen)
        text_box.draw(self.screen)
        text_box.update(event_list)

        # Check if sprite has been killed
        if len(text_box.sprites()) == 0:
            # Remove question sprite
            question.sprite.kill()

            # Make star appear
            self.star.sprite.rect.x = random.randint(10, width)
            self.star.sprite.rect.y = 5
            self.star.draw(self.screen)

            # Remove used question and text box from questions list
            self.questions_list.pop(0)
            self.text_boxes.pop(0)

    def intro_screen(self):
        button = Button("Mängi", (300, 260), 50, game, self.screen, "navy")
        button2 = Button2("Välju", (305, 380), 50, game, self.screen, "navy")
        while self.intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if button.mouse_click(event):
                    button.close(0)
                if button2.mouse_click(event):
                    button2.close()
            button.pack()
            button2.pack()
            time.tick(40)
            pygame.display.update()

    def end_screen(self):
        self.end = True
        self.screen = pygame.display.set_mode([width, height])

        font = pygame.font.SysFont('Arial', 50)
        text = font.render("Punktid: " + str(game.points), True, (255, 255, 255))
        button_play_again = Button3("Mängi uuesti", (260, 305), 50, game, self.screen, "navy")
        button_exit = Button2("Välju", (320, 405), 50, game, self.screen, "navy")
        while self.end:
            for event in pygame.event.get():
                self.screen.blit(text, (250, 205))
                if event.type == pygame.QUIT:
                    pygame.quit()
                if button_play_again.mouse_click(event):
                    button_play_again.close()
                if button_exit.mouse_click(event):
                    button_exit.close()
            button_play_again.pack()
            button_exit.pack()
            time.tick(40)
            pygame.display.update()

    def choose_level(self):
        button_level_1 = Button("Tase 1", (290, 140), 50, game, self.screen, "navy")
        button_level_2 = Button("Tase 2", (290, 260), 50, game, self.screen, "navy")
        button_exit = Button2("Välju", (305, 380), 50, game, self.screen, "navy")
        while self.level == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if button_level_1.mouse_click(event):
                    button_level_1.close(1)
                if button_level_2.mouse_click(event):
                    button_level_2.close(2)
                if button_exit.mouse_click(event):
                    button_exit.close()
            button_level_1.pack()
            button_level_2.pack()
            button_exit.pack()
            time.tick(40)
            pygame.display.update()
        game.load_questions()

    def load_questions(self):
        # Questions list setup
        if self.level == 1:
            questions = level_1_questions
        else:
            questions = level_2_questions
        random.shuffle(questions)

        # Create group of all questions and group of answer boxes
        questions_list = []
        text_boxes = []
        for q in questions:
            q_sprite = QuestionSprite(350, 300, q.question)
            t_sprite = TextInputBox(200, 350, 300, q.answer, self)
            questions_list.append(pygame.sprite.GroupSingle(q_sprite))
            text_boxes.append(pygame.sprite.GroupSingle(t_sprite))
        self.questions_list = questions_list
        self.text_boxes = text_boxes

    def play(self):
        self.screen = pygame.display.set_mode([width, height])
        music_data = base64.b64decode(background_music)
        pygame.mixer.music.load(BytesIO(music_data))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        n = 0

        game.intro_screen()
        game.choose_level()


        while len(game.questions_list) > 0:
            time.tick(40)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg, (0, n))
            self.screen.blit(self.bg, (0, -height + n))

            if n == height:
                self.screen.blit(self.bg, (0, -height + n))
                n = 0
            n += 1

            font = pygame.font.SysFont('Arial', 25)
            text = font.render("Punktid: " + str(game.points), True, (255, 255, 255))
            self.screen.blit(text, (0, 0))

            event_list = pygame.event.get()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if game.collision():
                game.ask_question(event_list)
            else:
                game.run()

            pygame.display.update()

        game.end_screen()


if __name__ == '__main__':
    pygame.init()
    width = 700
    height = 700
    star_x = random.randint(10, width)
    star_y = 5
    speed = 3
    game = Game(star_x, star_y, speed)
    time = pygame.time.Clock()

    while not game.end:
        game.play()

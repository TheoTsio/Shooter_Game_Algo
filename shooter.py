
from pygame import * 
from random import *


window = display.set_mode((700, 500))

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

font.init()
font1 = font.Font(None, 31)
score_text = font1.render("Score:", True, (255, 255, 255))
missed_text = font1.render("Missed:", True, (255, 255, 255))
# mixer.init()
# mixer.music.load("space.ogg")
# mixer.music.play()

bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (65 ,65))

        self.speed = speed 

        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):
    def update(self):

        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 635: 
            self.rect.x += self.speed 

        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 9) 
        bullets.add(bullet)

missed = 0
class UFO(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed 

        if self.rect.y > 435:
            missed += 1
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            self.speed  = randint(6, 15)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

rocket = Rocket("rocket.png", 200, 430, 5)

monsters = sprite.Group()
for i in range(2):
    ufo = UFO("ufo.png", randint(0, 450), 10, 6)
    monsters.add(ufo)

score = 0
FPS = 60
clock = time.Clock()
game = True 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    # keys = key.get_pressed()
    # if keys[K_SPACE]:
    #     rocket.fire()


    window.blit(background, (0, 0))

    missed_text = font1.render("Missed:"+str(missed), True, (255, 255, 255))
    window.blit(missed_text, (10, 10))
    score_text = font1.render("Score:"+str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 40))

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for i in collides:
        score += 1
        ufo = UFO("ufo.png", randint(0, 450), 10, 6)
        monsters.add(ufo)
        

    rocket.draw()
    rocket.update()

    monsters.draw(window)
    monsters.update()

    bullets.draw(window)
    bullets.update()



    clock.tick(FPS)
    display.update()

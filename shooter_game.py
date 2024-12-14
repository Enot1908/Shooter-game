#Create your own shooter

from pygame import *
from random import randint

font.init( )
font1 = font.Font(None,80)
font2 = font.Font(None,36)
win = font1.render('YOU WIN!',True,(255,255,255))
lose = font1.render('YOU LOSE!',True,(188,0,0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back),(win_width, win_height))

score=0
goal=3
lost=0
max_lost=10

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x, player_y,size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullet.add(bullet)

#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       global lost
       #disappears upon reaching the screen edge
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1


#bullet sprite class  
class Bullet(GameSprite):
   # enemy movement
   def update(self):
       self.rect.y += self.speed
       # disappears upon reaching the screen edge
       if self.rect.y < 0:
           self.kill()


ship = Player(img_hero,5,win_height-100,80,100,10)
monsters = sprite.Group()

for i in range(1,6):
    monster = Enemy(img_enemy, randint(80,win_width-80),-40,80,50,randint(1,3))
    monsters.add(monster)

bullets = sprite.Group()

finish = False

run = True

clock = time.Clock()

FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        
        text = font2.render("Score:" + str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Missed:" + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))


        display.update()
        clock.tick(FPS)
else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)


time.delay(50)
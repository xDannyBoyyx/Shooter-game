from pygame import *
from random import randint
from time import time as timer

class GamePlayer(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.life = 3
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GamePlayer):
    def update(self):
        
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x>5:
            self.rect.x -= self.speed
        
        if keys[K_d] and self.rect.x<win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx-8,self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GamePlayer):
    def update(self):
        global lost
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)

            self.rect.y =- 10
            lost += 1


class Bullet(GamePlayer):
    def update(self):
        self.rect.y+=self.speed#self.speed = -10

        if self.rect.y<0:
            self.kill()

class BulletImage(GamePlayer):



class Asteroid(GamePlayer):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y=-10


lost = 0 #! ships missed
score = 0 #//! ships destroyed
win_width = 700
win_height = 500

font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,80)

win = font2.render("You Win!",True,(255,255,255))
lose = font2.render("You Lose",True,(255,255,255))

Rocket = Player("spaceship.png",5,win_height-100,80,100,10)
UFOs = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(3):
    asteroid = Asteroid("asteroid.png",randint(30,win_width-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)

for i in range(6):
    UFO = Enemy("ufo.png",randint(80,win_width-80),-40,80,50,randint(1,3))
    UFOs.add(UFO)

window = display.set_mode((win_width , win_height))
display.set_caption("Shooter Game")

background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))

mixer.init()
mixer.music.load("fire.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
#lose_sound = mixer.Sound("")


clock = time.Clock()
finish = False
run = True

bs = []
b1 = GamePlayer("bullet.png",10+0*10,80,15,20,0)
b2 = GamePlayer("bullet.png",10+1*10,80,15,20,0)
b3 = GamePlayer("bullet.png",10+2*10,80,15,20,0)
b4 = GamePlayer("bullet.png",10+3*10,80,15,20,0)
b5 = GamePlayer("bullet.png",10+4*10,80,15,20,0)
bs.append(b1)
bs.append(b2)
bs.append(b3)
bs.append(b4)
bs.append(b5)

num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN :
            if e.key == K_SPACE:
                if num_fire<5 and rel_time == False:
                    num_fire+=1
                    fire_sound.play()
                    Rocket.fire()
                    bs.pop()            
                if num_fire>=5 and rel_time==False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_q:
                exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire<5 and rel_time == False:
                    num_fire+=1
                    fire_sound.play()
                    Rocket.fire()
                    bs.pop()
                if num_fire>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True

    if not finish:

        window.blit(background,(0,0))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time<1:
                reloading = font1.render("Wait , reloading . . .",1,(150,0,0))
                window.blit(reloading,(260,460))
            else:
                num_fire=0
                rel_time=False

        for x in range(5-num_fire):
            window.blit(b,(10+x*10,80))

        #text_end = font1.render("YOU LOSE!",1,(255,255,255))

        if sprite.spritecollide(Rocket,UFOs,False) or lost >=3 or Rocket.life<1:
            finish = True
            #lose_sound.play()
            window.blit(lose,(200,350))

        if sprite.spritecollide(Rocket,asteroids,True):
            Rocket.life-=1
            asteroid = Asteroid("asteroid.png",randint(30,win_width-30),-40,80,50,randint(1,7))
            asteroids.add(asteroid)

        colided = sprite.groupcollide(bullets, UFOs , True , True)
    
        if score >= 10 :
            finish = True
            window.blit(win,(200,350))


        for c in colided:
            score+=1
            UFO = Enemy("ufo.png" , randint(80,620), -40,80,50,randint(1,5))
            UFOs.add(UFO)


        text_lose = font1.render("Missed: " + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        text = font1.render("Score: "+ str(score),1,(255,255,255))
        window.blit(text,(10,20))

        lives = font1.render(str(Rocket.life),1,(63,169,35))
        window.blit(lives,(win_width-60,20))

        #UFO.reset()
        bs.update()
        bullets.update()
        asteroids.update()
        UFOs.update()
        UFOs.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        Rocket.update()
        Rocket.reset()
        bs.draw(window)
        #Rocket.fire()

    else:
        finish = True
        score = 0
        lost = 0

        for u in UFOs :
            u.kill()
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(5):
            UFO = Enemy("ufo.png",randint(80,620),-40,80,50,randint(1,5))
            UFOs.add(UFO)

        for i in range(3):
            asteroid = Asteroid("asteroid.png",randint(30,win_width-30),-40,80,50,randint(1,7))
            asteroids.add(asteroid)

    display.update()
    clock.tick(120)




#Create your own shooter


from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)

        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.speed
    def fire(self):
        bullet=Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-10)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y+=self.speed
        if self.rect.y>win_height:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=0
            lost+=1


class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()

win_width=700
win_height=500
clock=time.Clock()
FPS=40
ship=Player('rocket.png',5,390,80,100,4)
lost=0
monsters=sprite.Group()
for i in range(1,6):
    monster=Enemy('ufo.png',randint(70,win_width-80),-30,80,50,randint(1,3))
    monsters.add(monster)

asteroids=sprite.Group()
for i in range(1,3):
    asteroid=Enemy('asteroid.png',randint(30,win_width-30),-30,80,50,randint(1,5))
    asteroids.add(asteroid)
bullets=sprite.Group()

score=0
window = display.set_mode((win_width,win_height)) 
display.set_caption('Shooter game')
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
background=transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
finish =False
run=True
font.init()
style=font.SysFont('Arial',36)
rel_time=False
num_fire=0
fire_sound=mixer.Sound('fire.ogg')
life=3
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key== K_SPACE:
                if num_fire<5 and rel_time==False:
                    num_fire+=1
                    fire_sound.play()
                    ship.fire()
                if num_fire>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True
    if not finish:   
        window.blit(background,(0,0))
        ship.reset()
        ship.update()
        text_score=style.render('Score:'+str(score),1,(255,255,255))
        window.blit(text_score,(10,20))
        text_lose=style.render('Missed:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        monsters.draw(window)
        monsters.update()
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window)
        bullets.update()

        if rel_time==True:
            now_time=timer()

            if now_time-last_time<3:
                reload=style.render('Wait,reload...',1,(200,0,0))
                window.blit(reload,(250,450))
            else:
                num_fire=0
                rel_time=False
                


        lose=style.render('You lost!',1,(255,0,0))
        win=style.render('You win!',1,(0,255,0))
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life-=1
        if life==0 or lost>=3:
            finish=True
            window.blit(lose,(200,200))


            

        collides=sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score+=1
            monster=Enemy('ufo.png',randint(70,win_width-80),-30,80,50,randint(1,4))
            monsters.add(monster)

        if score >=10:
            finish=True
            window.blit(win,(100,100))

        if life ==3:
            life_color=(0,200,0)
        if life==2:
            life_color=(180,180,0)
        if life==1:
            life_color=(200,0,0)

        text_life=style.render(str(life),1,life_color)
        window.blit(text_life,(660,20))

        display.update()
    else:
        finish=False
        score=0
        lost=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1,6):
            monster=Enemy('ufo.png',randint(70,win_width-80),-30,80,50,randint(1,3))
            monsters.add(monster)

    
    clock.tick(FPS)

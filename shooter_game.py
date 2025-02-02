from pygame import *
from random import randint
from time import time as timer



mixer.init()
mixer.music.load('xor.mp3')
mixer.music.play()
fire_sound = mixer.Sound('ydar.mp3')
win_sound = mixer.Sound('pobg.mp3')
lose_sound = mixer.Sound('lose(2).mp3')









font.init()
font1 = font.SysFont('Arial',80)
win = font1.render('SUUUUUUUUU', True, (0, 255, 0))
lose = font1.render('YOU NO SUUUUUUU', True, (255, 0, 0))
font2 = font.SysFont('Arial', 36)



img_back = 'fottboll.jpg'
img_hero = 'ronaldik(1).png'
img_bullet = "mach(1).png"
img_enemy = 'mesi.png'


score = 0
goal = 10
lost = 0
life = 3
max_lost= 3


class GameSprite(sprite.Sprite):

    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):

        sprite.Sprite.__init__(self)



        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed



        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 35, 35, -15)
        bullets.add(bullet)


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()



win_width = 800
win_height = 1000
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 100, 137, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 118, randint(1, 6))
    monsters.add(monster)



finish = False


bullets = sprite.Group()



run = True


rel_time = False


num_fire = 0


while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10000 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()

                if num_fire > 10000 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:

        window.blit(background,(0,0))



        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)


        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Перезарядка...', 1, (255, 0 ,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:

            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 118, randint(1, 5))
            monsters.add(monster)
        




        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1
            
            
            
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (30, 450))
            lose_sound.play()




        if score >= goal:
            finish = True
            window.blit(win, (50, 450))
            win_sound.play()


        text = font2.render('Счёт: ' + str(score), 1, (0, 255, 0))
        window.blit(text, (10, 20))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 3:
            life_color = (150, 150, 0)
        if life == 3:
            life_color = (0, 150, 0)


        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 50))


        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        lfie = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()


        time.delay(3000)
        for i in range (1, 8):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 100, 118, randint(1, 8))
            monsters.add(monster)
        

    time.delay(35)



from pygame import *

# Gerekli sınıflar

# Spritelar için ana sınıf
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Oyuncu sprite için alt sınıf (oklarla kontrol edilir)
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

# Düşman sprite için alt sınıf (kendini hareket ettirir)
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, direction):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = direction
        self.initial_y = player_y  # İlk konumunu kaydediyoruz
        self.vertical_movement_range = 100  # Yukarıdan aşağıya hareket mesafesi

    def update(self):
        if self.direction == "down":
            if self.rect.y >= self.initial_y + self.vertical_movement_range:
                self.direction = "up"
            else:
                self.rect.y += self.speed
        elif self.direction == "up":
            if self.rect.y <= self.initial_y:
                self.direction = "down"
            else:
                self.rect.y -= self.speed
        elif self.direction == "left":
            if self.rect.x <= 5:
                self.direction = "right"
            else:
                self.rect.x -= self.speed
        elif self.direction == "right":
            if self.rect.x >= win_width - 85:
                self.direction = "left"
            else:
                self.rect.x += self.speed

# 3.Hafta
# Eng el sprite'ları için sınıf
class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
 
        # Duvar resmi - siyah bir dikdörtgen
        self.image = Surface([self.width, self.height])
        self.image.fill((0, 0, 0))
 
        # Her hareketli grafiğin bir rect özelliği saklaması gerekir - bir dikdörtgen
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
 
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Oyun açıklaması

# Oyun sahnesi
win_width = 800
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("Hero-Volcano.jpg"), (win_width, win_height))

# 3.Hafta
w1 = Wall(100, 20, 10, 380)
w2 = Wall(100, 480, 350, 10)
w3 = Wall(100, 20, 450, 10)
w4 = Wall(300, 130, 10, 350)
w5 = Wall(640, 130, 10, 360)

# Oyunun karakterleri
player = Player('hero.png', 5, win_height - 80, 4) 
monster1 = Enemy('indir.jpg', win_width - 450, 90, 3, "down")
monster2 = Enemy('indir.jpg', win_width - 450, 45, 3, "left")
final = GameSprite('treasure.png', win_width - 300, win_height - 80, 0)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
score_font = font.Font(None, 40)

score = 0

win = font.Font(None, 60).render('KAZANDINIZ!', True, (151, 255, 255))
lose = font.Font(None, 60).render('SALDIRAN KAZANDI!', True, (180, 0, 0))

mixer.init()
mixer.music.load('Volkan-Lav-Sesi.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

def render_score():
    score_text = score_font.render("Puan: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster1.update()
        monster2.update()
       
        player.reset()
        monster1.reset()
        monster2.reset()
        final.reset()
       
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        
        if sprite.collide_rect(player, monster1) or sprite.collide_rect(player, monster2) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5):
            # Oyuncu duvara veya düşmana çarptı
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
            score -= 10
            
        elif sprite.collide_rect(player, final):
            # Oyuncu hazineye dokundu, oyun kazanıldı
            finish = True
            window.blit(win, (200, 200))
            money.play()
            score += 20
      
    render_score()
    display.update()
    clock.tick(FPS)

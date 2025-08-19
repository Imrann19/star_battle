import pygame
import random
import math

class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def random(x_ma, y_ma):
        x = random.randint(0, x_ma)
        y = random.randint(0, y_ma)
        return Point2d(x, y)

class Boss:
    def __init__(self, x, y, surface):
        self.alive = True
        self.s = surface
        self.x = x
        self.final_y = y
        self.y = y - 100
        self.arriving = True
        self.lasers = []
        self.last_shot = 0
        self.countdown = 8000

    def update(self):
        if self.arriving:
            if self.y < self.final_y:
                self.y += 1
            else:
                self.arriving = False
        else:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.countdown:
                for i in range(4):
                    self.lasers.append(LaserB(self.x + 160+i*25, self.y+100+i*10, 5))
                for i in range(4):
                    self.lasers.append(LaserB(self.x +525-i*30, self.y+100+i*10, 5))
                laser_son2.play()
                self.last_shot = now
        for laser in self.lasers[:]:
            laser.move()
            if laser.out_screen():
                self.lasers.remove(laser)
            elif coli(xv, 500, laser.x, laser.y):
                self.lasers.remove(laser)
                global vj, ecg
                vj -= 1
                if vj <= 0:
                    gm.play()
                    pygame.mixer.music.stop()
                    ecg = 0

    def draw(self):
        if boss_hit:
            self.s.blit(boss_impact_image, (self.x, self.y))
        else:
            self.s.blit(boss, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(self.s)

def coli(x, y, x2, y2):
    if x - 45 < x2 < x + 70 and y < y2 < y + 70:
        return True
    return False

def coli_Boss(x, y, x2, y2):
    if x < x2 < x + 700 and y < y2 < y + 188:
        return True
    return False

class Starfield:
    def __init__(self, L, H, nb_stars, v_mi, v_ma):
        self.L = L
        self.H = H
        self.nb_stars = nb_stars
        self.v_mi = v_mi
        self.v_ma = v_ma
        self.p = []
        self.v = []
        self.c = []
        for _ in range(nb_stars):
            po = Point2d.random(L, H)
            vi = random.randint(v_mi, v_ma)
            co = 80 + (vi - v_mi) / (v_ma - v_mi) * 175
            self.p.append(po)
            self.v.append(vi)
            self.c.append(co)

    def move_draw(self, surface):
        for i in range(self.nb_stars):
            p = self.p[i]
            v = self.v[i]
            c = self.c[i]
            p.y += v
            if p.y > self.H:
                p.x = random.randint(0, self.L)
                p.y = 0
            surface.set_at((p.x, p.y), (int(c), int(c), int(c)))

class BAR:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, l, h, b, bm, s):
        pygame.draw.rect(s, G, (self.x, self.y, l, h))
        hl = int((b*l) / bm)
        if b / bm > 0.6:
            color = V
        elif b / bm > 0.3:
            color = J
        else:
            color = R
        pygame.draw.rect(s, color, (self.x, self.y, hl, h))
        pol = pygame.font.Font("fnt/Minecraftia-Regular.ttf", 23)
        t = pol.render("BOSS FINAL", True, (255, 0, 0))
        tr = t.get_rect(center=(400, 44))
        s.blit(t, tr)
        pourc = int(b*100)/bm
        tp = pol.render(f"{int(pourc)}%", True, (255, 0, 0))
        tpp = t.get_rect(center=(700, 44))
        s.blit(tp, tpp)

class Espace:
    def __init__(self, L, H):
        self.starfields = [
            Starfield(L, H, 40, 1, 2),
            Starfield(L, H, 60, 2, 3),
            Starfield(L, H, 80, 3, 4)
        ]
    def draws(self, surface):
        for s in self.starfields:
            s.move_draw(surface)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.played = False
    def animation(self, s, image, sound):
        s.blit(image, (self.x, self.y))
        if not self.played:
            sound.play()
            self.played = True

class Laser:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    def move(self):
        self.y += self.speed
    def draw(self, f, l):
        f.blit(l, (self.x, self.y))
        f.blit(l, (self.x + 53, self.y))
    def out_screen(self, T):
        return self.y < T

class LaserB:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        angle = math.radians(random.uniform(180, 0))
        self.l3 = pygame.transform.rotate(l3, -math.degrees(angle))
        self.vx = math.cos(angle)*speed
        self.vy = math.sin(angle)*speed
    def move(self):
        self.x += self.vx
        self.y += self.vy
    def draw(self, s):
        s.blit(self.l3, (self.x, self.y))
    def out_screen(self):
        return self.y > H or self.x > L or self.x < 0

class LaserE:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    def move(self):
        self.y += self.speed
    def draw(self, s):
        s.blit(l2, (self.x, self.y))
    def out_screen(self, H):
        return self.y > H

class ves:
    def __init__(self, lmi, lma):
        self.x = lma / 2
        self.y = 10
        self.speed = 1.5
        self.lmi = lmi
        self.lma = lma
        self.dir = 1
        self.stopped = False
        self.stop_time = 0
    def move(self):
        if self.stopped:
            if pygame.time.get_ticks() >= self.stop_time:
                self.stopped = False
            else:
                return
        if self.x <= self.lmi + 5:
            self.dir = 1
        elif self.x >= self.lma - 65:
            self.dir = -1
        self.x += self.speed * self.dir
    def draw(self, s):
        s.blit(ve, (self.x, self.y))
    def stop(self, ms):
        self.stopped = True
        self.stop_time = pygame.time.get_ticks() + ms

pygame.init()
pygame.mixer.init()
L, H = 800, 600
f = pygame.display.set_mode((L, H))
pygame.display.set_caption("Star Battle")
clock = pygame.time.Clock()

explo2 = pygame.image.load("img/e2.png")
victos = pygame.mixer.Sound("snd/victory-sound_130bpm_F_major.wav")
boss_impact_image = pygame.image.load("img/boss3-impact.png")
boss = pygame.image.load("img/boss3.png")
gam = pygame.image.load("img/game_over.png")
gam = pygame.transform.scale(gam, (L, H))
gam.set_alpha(0)
gm = pygame.mixer.Sound("snd/5-25. Game Over.mp3")
hi = pygame.image.load("img/pngegg.png")
hi = pygame.transform.scale(hi, (30, 30))
image = pygame.image.load("img/poi.png")
ve = pygame.image.load("img/Tie.PNG")
l2 = pygame.image.load("img/Laser2.png")
l3 = pygame.image.load("img/Laser3.png")
laser_image = pygame.image.load("img/laser.png")
explosion = pygame.image.load("img/explosion.png")
laser_son = pygame.mixer.Sound("snd/lego-star-wars-x-wing-fire-sound.mp3")
laser_son2 = pygame.mixer.Sound("snd/blast-101soundboards.mp3")
e_s = pygame.mixer.Sound("snd/mixkit-arcade-game-explosion-1699.wav")

pygame.mixer.music.load("snd/134270_Ultimate.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

boss_hit = False
boss_hit_time = 0
hit_duration = 100
boss_explosion = None
boss_explosion_start = 0
explosion_duration = 1000
victory_played = False

espace = Espace(L, H)
big_b = Boss(50, 55, f)
b_boss = BAR(100, 30)

xv = 350
lasers = []
lasersE = []

G = (60, 60, 60)
V = (0, 255, 0)
J = (255, 255, 0)
R = (255, 0, 0)

vie1, vie2 = 1, 1
vj = 3
ecg = 1
alpha = 0

boss_vie = 300
boss_vie_max = 300

ve1 = ves(0, L / 2)
ve2 = ves(L / 2, L)
last_shot1 = last_shot2 = 0
shot_interval = 3000

e1 = e2 = None
explosion_start1 = explosion_start2 = None

victory = False
victory_start = 0

ec = True
while ec:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ec = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and xv > 0:
        xv -= 5
    if keys[pygame.K_RIGHT] and xv < L - 70:
        xv += 5
    if keys[pygame.K_SPACE] and len(lasers) <= 2 and not victory:
        lasers.append(Laser(xv, 500, -10))
        laser_son.play()

    f.fill((0, 0, 0))
    if ecg == 1:
        espace.draws(f)
        now = pygame.time.get_ticks()
        for laser in lasers[:]:
            laser.move()
            laser.draw(f, laser_image)
            if laser.out_screen(0):
                lasers.remove(laser)
                continue
            if vie1 > 0 and coli(ve1.x, ve1.y, laser.x, laser.y):
                vie1 = 0
                lasers.remove(laser)
                e1 = Explosion(ve1.x, ve1.y)
                explosion_start1 = now
                continue
            if vie2 > 0 and coli(ve2.x, ve2.y, laser.x, laser.y):
                vie2 = 0
                lasers.remove(laser)
                e2 = Explosion(ve2.x, ve2.y)
                explosion_start2 = now
                continue
            if boss_vie > 0 and vie1 == 0 and vie2 == 0 and coli_Boss(big_b.x, big_b.y, laser.x, laser.y):
                boss_vie -= 1
                lasers.remove(laser)
                boss_hit = True
                boss_hit_time = pygame.time.get_ticks()
                if boss_vie <= 0:
                    big_b.alive = False
                    big_b.lasers = []
                    if not boss_explosion:
                        boss_explosion = Explosion(big_b.x, big_b.y)
                        boss_explosion_start = pygame.time.get_ticks()
        if vie1 > 0:
            ve1.move()
            ve1.draw(f)
            if now - last_shot1 > shot_interval:
                laser_son2.play()
                if not ve1.stopped:
                    ve1.stop(1000)
                lasersE.append(LaserE(int(ve1.x) + 20, int(ve1.y) + 40, 5))
                last_shot1 = now
        elif e1 and now - explosion_start1 < 1000:
            e1.animation(f, explosion, e_s)

        if vie2 > 0:
            ve2.move()
            ve2.draw(f)
            if now - last_shot2 > shot_interval:
                laser_son2.play()
                if not ve2.stopped:
                    ve2.stop(1000)
                lasersE.append(LaserE(int(ve2.x) + 20, int(ve2.y) + 40, 5))
                last_shot2 = now
        elif e2 and now - explosion_start2 < 1000:
            e2.animation(f, explosion, e_s)

        if vie1 == 0 and vie2 == 0:
            b_boss.draw(600, 25, boss_vie, boss_vie_max, f)
            if big_b.alive:
                big_b.update()
                big_b.draw()
            if boss_hit and pygame.time.get_ticks() - boss_hit_time > hit_duration:
                boss_hit = False
            if boss_explosion:
                if pygame.time.get_ticks() - boss_explosion_start < explosion_duration:
                    boss_explosion.animation(f, explo2, e_s)
                else:
                    boss_explosion = None
                    victory = True
                    victory_start = pygame.time.get_ticks()
                    if not victory_played:
                        pygame.mixer.music.stop()
                        victos.play()
                        victory_played = True
        for le in lasersE[:]:
            le.move()
            le.draw(f)
            if le.out_screen(H):
                lasersE.remove(le)
            if coli(xv, 500, le.x, le.y):
                lasersE.remove(le)
                vj -= 1
                if vj == 0:
                    gm.play()
                    pygame.mixer.music.stop()
                    ecg = 0

        if not victory:
            f.blit(image, (xv, 500))
        else:
            if xv >= 0 and xv <= L-70:
                f.blit(image, (xv, max(0, 500 - (pygame.time.get_ticks() - victory_start)//5)))
            if pygame.time.get_ticks() - victory_start > 3000:
                font = pygame.font.Font("fnt/Minecraftia-Regular.ttf", 60)
                victory_text = font.render("VICTORY", True, (255, 255, 0))
                rect = victory_text.get_rect(center=(L//2, H//2))
                f.blit(victory_text, rect)

        for i in range(vj):
            f.blit(hi, (10 + i * 35, 550))
    elif ecg == 0:
        if alpha < 255:
            alpha += 0.5
        gam.set_alpha(int(alpha))
        f.blit(gam, (0, 0))

    pygame.display.flip()
    clock.tick(60)

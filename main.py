import pgzrun
import math
import random
from pygame import Rect

# --- CONFIGURACAO ---
WIDTH = 800
HEIGHT = 600
TITLE = "Space Jumper Adventure"

# --- CORES ---
WHITE = (255, 255, 255)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLACK = (20, 20, 20)

# --- ESTADO GLOBAL ---
game_state = "MENU"
sound_enabled = True

# --- CLASSES ---

class Entity:
    # Classe base para personagens animados
    def __init__(self, x, y, images_idle, images_move):
        self.x = x
        self.y = y
        self.images_idle = images_idle
        self.images_move = images_move
        self.current_images = self.images_idle
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15
        self.facing_right = True
        # Cria rect de colisao
        self.rect = Rect(x, y, 50, 60) 

    def animate(self, dt, is_moving):
        self.anim_timer += dt
        
        if is_moving:
            self.current_images = self.images_move
        else:
            self.current_images = self.images_idle

        if self.anim_timer > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.current_images)
            self.anim_timer = 0

    def get_image(self):
        if self.frame_index >= len(self.current_images):
            self.frame_index = 0
        return self.current_images[self.frame_index]

class Hero(Entity):
    def __init__(self):
        # Imagens do heroi
        super().__init__(100, 450, 
                         ['hero_idle1', 'hero_idle2'], 
                         ['hero_run1', 'hero_run2'])
        self.vy = 0
        self.speed = 5
        
        # --- AJUSTE DE FISICA ---
        self.jump_power = -17
        self.gravity = 0.6
        
        self.on_ground = False

    def update(self, dt, platforms):
        is_moving = False
        
        # Movimento
        if keyboard.left:
            self.x -= self.speed
            self.facing_right = False
            is_moving = True
        elif keyboard.right:
            self.x += self.speed
            self.facing_right = True
            is_moving = True

        # Gravidade
        self.vy += self.gravity
        self.y += self.vy

        self.rect.topleft = (self.x, self.y)

        # Colisao com Plataformas
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat) and self.vy > 0:
                # Tolerancia de altura para pousar
                if self.rect.bottom - self.vy <= plat.bottom:
                    self.y = plat.top - self.rect.height
                    self.vy = 0
                    self.on_ground = True
                    self.rect.topleft = (self.x, self.y)

        # Morte por queda
        if self.y > HEIGHT + 100:
            return "DIED"
        
        self.animate(dt, is_moving)
        return "ALIVE"

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_power
            if sound_enabled:
                try: sounds.jump.play()
                except: pass

class Enemy(Entity):
    # Aceita as imagens como parametro
    def __init__(self, x, y, min_x, max_x, img_idle, img_run):
        super().__init__(x, y, img_idle, img_run)
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 2
        self.rect = Rect(x, y, 50, 50)

    def update(self, dt):
        self.x += self.speed
        self.rect.topleft = (self.x, self.y)
        
        if self.x > self.max_x:
            self.speed = -abs(self.speed)
            self.facing_right = False
        elif self.x < self.min_x:
            self.speed = abs(self.speed)
            self.facing_right = True
            
        self.animate(dt, True)

# --- CONFIGURACAO INICIAL ---
# Plataformas globais
platforms = [
    Rect(0, 550, 800, 50),    # Chao
    Rect(300, 400, 200, 20),  # Plat 1
    Rect(50, 250, 200, 20),   # Plat 2
    Rect(550, 200, 150, 20)   # Plat 3
]

# Botoes
btn_start = Rect(WIDTH//2 - 100, 200, 200, 50)
btn_sound = Rect(WIDTH//2 - 100, 280, 200, 50)
btn_exit = Rect(WIDTH//2 - 100, 360, 200, 50)

# Variaveis globais
hero = None
enemies = []

# --- FUNCOES DE JOGO ---

def reset_game():
    global hero, enemies
    hero = Hero()
    
    # Inimigo 1 (Animacao detalhada)
    imgs_set1_idle = ['enemy1', 'enemy_idle2']
    imgs_set1_run = ['enemy_run1', 'enemy_run2']
    
    # Inimigo 2 (Imagens simples)
    imgs_set2_idle = ['enemy2', 'enemy2_run1']
    imgs_set2_run = ['enemy2', 'enemy2_run2']

    enemies = [
        # Inimigo na plataforma do meio
        Enemy(350, 350, 300, 500, imgs_set1_idle, imgs_set1_run),
        
        # Inimigo na plataforma alta esquerda
        Enemy(100, 200, 50, 250, imgs_set2_idle, imgs_set2_run)
    ]

def draw():
    screen.fill(BLACK)

    if game_state == "MENU":
        screen.draw.text("PLATFORMER HERO", center=(WIDTH//2, 100), fontsize=60, color=BLUE)
        
        screen.draw.filled_rect(btn_start, GREEN)
        screen.draw.text("START GAME", center=btn_start.center, fontsize=30, color=BLACK)

        color_sound = GREEN if sound_enabled else RED
        txt_sound = "SOUND: ON" if sound_enabled else "SOUND: OFF"
        screen.draw.filled_rect(btn_sound, color_sound)
        screen.draw.text(txt_sound, center=btn_sound.center, fontsize=30, color=BLACK)

        screen.draw.filled_rect(btn_exit, RED)
        screen.draw.text("EXIT", center=btn_exit.center, fontsize=30, color=BLACK)

    elif game_state == "GAME":
        for plat in platforms:
            screen.draw.filled_rect(plat, BLUE)

        if hero:
            img_name = hero.get_image()
            screen.blit(img_name, (hero.x, hero.y))

        for en in enemies:
            screen.blit(en.get_image(), (en.x, en.y))

    elif game_state == "GAME_OVER":
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color=RED)
        screen.draw.text("Press SPACE to Menu", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30)

def update(dt):
    global game_state

    if game_state == "GAME" and hero:
        status = hero.update(dt, platforms)
        
        if status == "DIED":
            game_state = "GAME_OVER"
            try: music.stop()
            except: pass

        for en in enemies:
            en.update(dt)
            if hero.rect.colliderect(en.rect):
                game_state = "GAME_OVER"
                try: music.stop()
                except: pass

    elif game_state == "GAME_OVER":
        if keyboard.space:
            reset_game()
            game_state = "MENU"
            # REINICIA A MUSICA AO VOLTAR PARA O MENU
            if sound_enabled:
                try: music.play("music")
                except: pass

def on_key_down(key):
    if game_state == "GAME" and hero and key == keys.UP:
        hero.jump()

def on_mouse_down(pos):
    global game_state, sound_enabled
    
    if game_state == "MENU":
        if btn_start.collidepoint(pos):
            reset_game()
            game_state = "GAME"
            # Nao precisa dar play aqui porque ja esta tocando desde o inicio
            # ou foi reativada pelo botao de som
        
        elif btn_sound.collidepoint(pos):
            sound_enabled = not sound_enabled
            if sound_enabled:
                # SE LIGOU: Toca a musica (music.play usa o nome do arquivo sem extensao)
                try: sounds.music.play() 
                except: pass
            else:
                # SE DESLIGOU: Para a musica
                try: sounds.music.stop()
                except: pass

        elif btn_exit.collidepoint(pos):
            quit()

# Inicializa
reset_game()

# TOCA A MUSICA LOGO NA ABERTURA DO JOGO (FINAL DO ARQUIVO)
if sound_enabled:
    try: sounds.music.play()
    except: pass

pgzrun.go()
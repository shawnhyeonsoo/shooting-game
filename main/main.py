import pygame, sys
import random
from pygame.locals import *

pygame.init() # 화면 초기화하는 부분

FPS = 30
fpsClock = pygame.time.Clock()

DISPLAYNOTE = pygame.display.set_mode((350, 600))
pygame.display.set_caption("NotePlay")

# 이미지 변수들
enemy_img   = pygame.image.load("plane.png")
enemy_size  = enemy_img.get_rect().size
hero_img    = pygame.image.load("hero.png")
hero_size   = hero_img.get_rect().size

over_img    = pygame.image.load("gameover.png")
heart_img   = pygame.image.load("heart.png")

# 점수 변수
score = 0

# 적 전투기 리스트
# [speed, pos, img]
enemies = [[1, [150, 0], enemy_img],
           [2, [100, 0], enemy_img],
           [5, [200, 0], enemy_img]]

# 주인공 관련 변수들
hero_pos = [150, 550]
hero_move = [0, 0]
hero_speed = 5
hero_heart = 5

# 미사일 관련 변수들
missile = []
missile_speed = 5

# 적 비행기들 그려주는 함수
def draw_enemies(note, enemies):
    for p in enemies:
        note.blit(p[2], p[1])
        p[1][1] += p[0]

        if p[1][1] > 600:
            p[1][1] = 0
            p[1][0] = random.randrange(0, 300)
            p[0] = random.randrange(1, 5)

# 미사일 지우는 함수
def del_missile(mList):
    tempList = []
    for m in mList:
        if m[1] > 0:
            tempList.append(m)
    return tempList

# 점수 출력해주는 함수
def write_score(note, score):
    scoreFont = pygame.font.Font('freesansbold.ttf', 15)
    txt = scoreFont.render("SCORE:"+str(score), True, (0, 0, 0))
    note.blit(txt, (250, 15))

# 게임 MAIN PART
while True:

    # 배경 색 채우기
    DISPLAYNOTE.fill((210, 210, 200))

    # 적 비행기 그리기
    draw_enemies(DISPLAYNOTE, enemies)

    # 주인공 이동 및 그리기
    hero_pos[0] += hero_move[0]
    hero_pos[1] += hero_move[1]
    DISPLAYNOTE.blit(hero_img, hero_pos)

    # 미사일 이동 및 그리기
    for m in missile:
        pygame.draw.circle(DISPLAYNOTE, (0, 0, 0), m, 5, 0)
        m[1] -= missile_speed

    # 화면 밖으로 나간 미사일 지우기
    missile = del_missile(missile)

    # 적, 미사일 충돌 처리
    for m in missile:
        for e in enemies:
            if m[0] > e[1][0] \
                and m[0] < e[1][0] + enemy_size[0] \
                and m[1] > e[1][1] \
                and m[1] < e[1][1] + enemy_size[1]:
                # 적 비행기 초기화
                e[1][1] = 0
                e[1][0] = random.randrange(0, 300)
                e[0] = random.randrange(1, 5)
                # 충돌된 미사일 제거
                m[1] = -10
                # 점수 증가
                score += 10

    # 적, 주인공 충돌 처리
    for e in enemies:
        if hero_pos[0] < e[1][0] + enemy_size[0] \
            and hero_pos[0] + hero_size[0] > e[1][0] \
            and hero_pos[1] < e[1][1] + enemy_size[1] \
            and hero_pos[1] + hero_size[1] > e[1][1]:
            # 적 비행기 초기화
            e[1][1] = 0
            e[1][0] = random.randrange(0, 300)
            e[0] = random.randrange(1, 5)
            # heart 감소
            hero_heart -= 1

    # Heart 그리기
    for i in range(hero_heart):
        DISPLAYNOTE.blit(heart_img, (10 + i * 25, 10))

    # GAME OVER
    if hero_heart < 1:
        # GAME OVER
        DISPLAYNOTE.fill((210, 210, 200))
        DISPLAYNOTE.blit(over_img, (2, 200))

    # 점수 출력
    write_score(DISPLAYNOTE, score)

    # 컨트롤 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                hero_move[0] -= hero_speed
            elif event.key == K_RIGHT:
                hero_move[0] += hero_speed
            elif event.key == K_UP:
                hero_move[1] -= hero_speed
            elif event.key == K_DOWN:
                hero_move[1] += hero_speed
            elif event.key == K_SPACE:
                # 미사일 추가
                missile.append([int(hero_pos[0] + hero_size[0]/2), int(hero_pos[1])])

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                hero_move[0] = 0
            elif event.key == K_RIGHT:
                hero_move[0] = 0
            elif event.key == K_UP:
                hero_move[1] = 0
            elif event.key == K_DOWN:
                hero_move[1] = 0

    # 화면 update
    pygame.display.update()
    fpsClock.tick(FPS)

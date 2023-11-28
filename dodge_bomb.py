import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center= 900,400
    clock = pg.time.Clock()
    bomb_place = [random.randint(0,WIDTH),random.randint(0,HEIGHT)]
    # bomb_place = (10,10)
    bomb_harf = 10
    bomb = pg.Surface((bomb_harf*2,bomb_harf*2))
    pg.draw.circle(bomb,(255,0,0),(bomb_harf,bomb_harf),bomb_harf)
    bomb.set_colorkey((0,0,0))
    bomb_rect = bomb.get_rect()
    bomb_rect.center = bomb_place
    tmr = 0
    vx,vy = +5,+5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            move_sum = [0, 0]
            key_lst = pg.key.get_pressed()
            if key_lst[pg.K_UP]: move_sum[1] -= 5
            if key_lst[pg.K_DOWN]: move_sum[1] += 5
            if key_lst[pg.K_LEFT]: move_sum[0] -= 5
            if key_lst[pg.K_RIGHT]: move_sum[0] += 5
        screen.blit(bg_img, [0, 0])
        kk_side = inside(kk_rect)
        if not kk_side[0]:
            move_sum[1] = -move_sum[1]
        if not kk_side[1]:
            move_sum[0] = -move_sum[0]
        kk_rect.move_ip(move_sum)
        screen.blit(kk_img, kk_rect)
        bomb_side = inside(bomb_rect)
        if not bomb_side[0]:
            vy = vy * -1
        elif not bomb_side[1]:
            vx = vx * -1
        bomb_rect.move_ip(vx,vy)
        screen.blit(bomb,bomb_rect)
        pg.display.update()
        tmr += 1
        clock.tick(100)


def inside(img_rect):
    # 上下左右の順に画面内か調べる関数
    # 引数：各イメージのRect
    # 戻り値：画面内ならtrue,画面外ならfalse
    yoko,tate = True,True
    if (img_rect.top < 0.0)or(HEIGHT < img_rect.bottom):
        tate = False
    if (img_rect.left < 0.0)or(WIDTH < img_rect.right):
        yoko = False
    return [tate,yoko]


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
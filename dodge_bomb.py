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
    kk_img_ue = pg.transform.rotozoom(kk_img,-90,1.0)
    kk_img_sita = pg.transform.rotozoom(kk_img,90,1.0)
    kk_img_hidariue = pg.transform.rotozoom(kk_img,-45,1.0)
    kk_img_hidarisita = pg.transform.rotozoom(kk_img,45,1.0)
    kk_img_migi = pg.transform.flip(kk_img,True,False)
    kk_img_migiue = pg.transform.rotozoom(kk_img_migi,-45,1.0)
    kk_img_migisita = pg.transform.rotozoom(kk_img_migi,45,1.0)
    kk_imgs = [kk_img,kk_img_hidarisita,kk_img_sita,kk_img_migisita,kk_img_migi,kk_img_migiue,kk_img_ue,kk_img_hidariue]
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
    accs = [i for i in range(1,11)]
    tmr = 0
    vx,vy = +5,+5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            key_lst = pg.key.get_pressed()
            move_sum = [0, 0]
            if key_lst[pg.K_UP]: move_sum[1] -= 5
            if key_lst[pg.K_DOWN]: move_sum[1] += 5
            if key_lst[pg.K_LEFT]: move_sum[0] -= 5
            if key_lst[pg.K_RIGHT]: move_sum[0] += 5
        screen.blit(bg_img, [0, 0])

        bomb_side = inside(bomb_rect)
        if not bomb_side[0]:
            vy = vy * -1
        elif not bomb_side[1]:
            vx = vx * -1
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        vv = [avx,avy]
        kyori(bomb_rect,kk_rect,vv)
        screen.blit(bomb,bomb_rect)


        kk_side = inside(kk_rect)
        if not kk_side[0]:
            move_sum[1] = -move_sum[1]
        if not kk_side[1]:
            move_sum[0] = -move_sum[0]
        kk_rect.move_ip(move_sum)
        muki = koukakunn_muki(move_sum)
        screen.blit(kk_imgs[muki], kk_rect)

        if bomb_rect.colliderect(kk_rect):
            for i in range(8):
                screen.blit(kk_imgs[i],kk_rect)
                clock.tick(20)
                pg.display.update()
            print("GameOver")
            return
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


def kyori(moto_rect,saki_rect,muki):
    # 爆弾とこうかとんの距離を計算し、近づくためのベクトルを出す関数
    # 引数：爆弾のRectとこうかとんのRect、爆弾のベクトル
    # 戻り値：こうかとんへのベクトル、距離が500未満ならFalse
    moto_X = moto_rect.centerx
    moto_Y = moto_rect.centery
    saki_X = saki_rect.centerx
    saki_Y = saki_rect.centery
    X_v = saki_X - moto_X
    Y_v = saki_Y - moto_Y
    norum = X_v**2 + Y_v**2
    norum = norum**(1/2)
    n_X = X_v/norum
    n_Y = Y_v/norum
    n_X = n_X*(50**(1/2))
    n_Y = n_Y*(50**(1/2))
    if norum <= 500:
        moto_rect.move_ip(n_X,n_Y)
        return
    moto_rect.move_ip(n_X,n_Y)
    return



def koukakunn_muki(muki):
    # こうかくんの向きから画像選択する関数
    # 引数：移動方向のリスト
    # 戻り値：画像番号
    if muki[0] == -5:
        if muki[1] == -5:
            return 7
        elif muki[1] == 0:
            return 0
        elif muki[1] == 5:
            return 1
    elif muki[0] == 0:
        if muki[1] == -5:
            return 6
        elif muki[1] == 0:
            return 0
        elif muki[1] == 5:
            return 2
    else:
        if muki[1] == -5:
            return 5
        elif muki[1] == 0:
            return 4
        elif muki[1] == 5:
            return 3

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
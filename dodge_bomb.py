import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面外か画面内か判定する
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    GameOver時の画面の作成を行う
    背景画面とGameOverの文字、こうかとん画像を表示
    引数：screen
    戻り値：なし
    """
    # GameOver時の背景画面
    gameover_haikei = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gameover_haikei, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gameover_haikei.set_alpha(200)
    screen.blit(gameover_haikei, [0, 0])
    # GameOverの表示
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(txt, txt_rct)
    # こうかとんの表示
    kk_img = pg.image.load("fig/8.png")
    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH / 2, HEIGHT / 2
    screen.blit(kk_img, [kk_rct[0]-200, kk_rct[1]])
    screen.blit(kk_img, [kk_rct[0]+200, kk_rct[1]])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾の速度と大きさが加速、拡大する
    引数：なし
    戻り値：拡大爆弾のリストと加速度のリスト
    """
    accs = [a for a in range(1, 11)]  # 加速度のリスト
    bb_lst = []  # 拡大爆弾のリスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過
        bb_lst.append(bb_img)  # 拡大爆弾のリストに追加
    return bb_lst, accs


# def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
#     """
    
#     """    
#     kk_img = pg.image.load()
#     kk_img_dist = {(0, -5): pg.transform.rotozoom(),
#                    (+5, -5):,
#                    (+5, 0):,
#                    (+5, +5):,
#                    (0, +5):,
#                    (-5, 5):,
#                    (-5, 0):,
#                    (-5, -5):,
#                    }


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    vx, vy = +5, +5  # 爆弾速度ベクトル
    bb_img = pg.Surface((20, 20))  # 爆弾用の空surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():  # キーと値を取り出せる
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)  # 爆弾動く
        tate, yoko = check_bound(bb_rct)
        if not tate:
            vx *= -1
        if not yoko:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

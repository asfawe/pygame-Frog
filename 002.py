import pygame as pg

def 스프라이트_생성(이미지):
    스프라이트 = pg.sprite.Sprite()
    스프라이트.image = 이미지
    스프라이트.rect = 스프라이트.image.get_rect()
    return 스프라이트

pg.init()

# 게임 기본 설정
실행여부 = True
화면가로길이, 화면세로길이 = 800,450
화면 = pg.display.set_mode([화면가로길이, 화면세로길이])
pg.display.set_caption('동족을 노역장에서 구출하라!')

배경이미지 = pg.image.load('img/배경.png')
배경이미지 = pg.transform.scale(배경이미지, (화면가로길이, 화면세로길이))

개리점프이미지 = pg.image.load('img/개리-뛰는-모습5(점프).png')
개리점프이미지 = pg.transform.scale(개리점프이미지, (100, 100))
개리착지이미지 = pg.image.load('img/개리-뛰는-모습6(착지).png')
개리착지이미지 = pg.transform.scale(개리착지이미지, (100, 100))

개리뛰기이미지리스트 = [pg.image.load(f'img/개리-뛰는-모습{인덱스}.png') for 인덱스 in range(1,5)]
for 인덱스 in range(len(개리뛰기이미지리스트)):
    개리뛰기이미지리스트[인덱스] = pg.transform.scale(개리뛰기이미지리스트[인덱스], (100, 100))
개리스프라이트 = 스프라이트_생성(개리뛰기이미지리스트[0])

돌이미지 = pg.image.load('img/돌.png')
돌이미지 = pg.transform.scale(돌이미지, (100, 100))

# 게임 요소 초기화
개리시작높이 = 255

개리뛰기상태 = 0
개리뛰는흐름 = 1
개리동작업데이트시간 = 0
점프기본속도 = 0.1
점프속도 = 점프기본속도
점프상태 = False
개리위치 = [70, 개리시작높이]

시계 = pg.time.Clock()

while 실행여부:
    화면.blit(배경이미지, (0,0))

    # 게임 시간 계산
    경과시간 = 시계.tick(60) / 1000

    개리스프라이트.rect.x, 개리스프라이트.rect.y = 개리위치[0], 개리위치[1]
    화면.blit(개리스프라이트.image, 개리스프라이트.rect)

    화면.blit(돌이미지, (500,280))

    # 개리 점프
    if 점프상태:
        개리스프라이트.image = 점프속도 > 0 and 개리점프이미지 or 개리착지이미지
        개리위치[1] -= 점프속도 * 경과시간 * 1000
        점프속도 -= 점프기본속도 * 경과시간 * 2
        if 개리위치[1] >= 개리시작높이:
            개리위치[1] = 개리시작높이
            점프상태 = False
            점프속도 = 점프기본속도
    else:
        개리동작업데이트시간 += 경과시간
        if 개리동작업데이트시간 > 0.2:
            개리동작업데이트시간 = 0
            개리스프라이트.image = 개리뛰기이미지리스트[개리뛰기상태]
            개리뛰기상태 += 개리뛰는흐름
            if 개리뛰기상태 == len(개리뛰기이미지리스트) - 1 or 개리뛰기상태 == 0:
                개리뛰는흐름 *= -1

    for 이벤트 in pg.event.get():
        if 이벤트.type == pg.QUIT:
            실행여부 = False
        elif 이벤트.type == pg.KEYDOWN:
            if 이벤트.key == pg.K_SPACE and not 점프상태:
                점프상태 = True

    pg.display.update()

pg.display.quit()
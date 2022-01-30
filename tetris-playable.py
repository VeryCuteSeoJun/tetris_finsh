#초기 설정
import pygame
import random
import time

pygame.init()

font = pygame.font.SysFont("arial",30,True,True)

#색상설정
GRAY = (128,128,128) #테두리
WHITE = (255,255,255) #0
ORANGE = (255,128,0) #1 (─┘)
BLUE  = (0,0,255) #2 (ㄴ)
GREEN = (0,255,0) #3 (└┐)
RED   = (255,0,0) #4 (┌┘)
PURPLE = (127,0,255) #5 (ㅗ)
YELLOW = (255,255,0) #6 (ㅁ)
SKYBLUE = (102,255,255) #7 (ㅣ)
BLACK = (0,0,0)

#각종 변수
runcode = True #False가 되면 코드 종료
score=0 #점수
board = [] #테트리스판 상태 저장
'''호출 형식: board[x좌표][y좌표]'''
for i in range(0,10): #x좌표
    board.append([])
    for j in range(0,22): board[i].append(0)#y좌표

current_falling_block = 1 #현재 떨어지고 있는 블럭
current_rotation = 1 #현재 떨어지고 있는 블럭의 회전 상태
block_coordinate = [4,3] #떨어지고 있는 블럭 위치
fall_period = 50 #50이 될 때마다 y좌표 감소
hard_drop = False #하드 드랍 유무 (하드드랍은 블럭이 바닥에 닿았을 때 딜레이가 생기지 않고 바로 배치됨)
add_score = [0,100,300,700,1500] #점수 증가량
realblock = [[0,0],[0,0],[0,0],[0,0]] #실제 블럭 위치
block_log = [0,1,0,0,0,0,0,0] #각 블럭 등장 횟수 (블럭 고유 번호를 x라고 할 때 블럭이 나온 횟수는 block_log[x]로 호출하며, block_log[0]는 아무 의미 없는 칸으로 둠)
sameblock = 0 #동일한 블럭 연속으로 2회 등장 시 3회부터는 그 블럭이 나올 수 없게 하는 변수 

#블럭 클래스 생성
class Block():
    def __init__(self):
        self.blocklist = [[],[],[],[],[],[],[]]
        self.limitx = [[],[],[],[],[],[],[]]
        self.limity = [[],[],[],[],[],[],[]]
        
    def SetBlock(self,block_num,info,limitx,limity):
        self.blocklist[block_num-1].append(info)
        self.limitx[block_num-1].append(limitx)
        self.limity[block_num-1].append(limity)

#블럭 생성
tetris_block = Block()
tetris_block.SetBlock(1, [[1,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(1, [[-1,-1], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(1, [[-1,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(1, [[1,1], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(2, [[-1,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(2, [[-1,1], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(2, [[1,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(2, [[1,-1], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9], 1)
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(3, [[-1,-1], [-1,0], [0,0], [0,1]], [1,9], 1)
tetris_block.SetBlock(3, [[-1,1], [0,1], [0,0], [1,0]], [1,8], 0)

tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8], 1)
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8], 0)
tetris_block.SetBlock(4, [[1,-1], [0,0], [1,0], [0,1]], [0,8], 1)
tetris_block.SetBlock(4, [[-1,-1], [0,0], [0,-1], [1,0]], [1,8], 0)

tetris_block.SetBlock(5, [[0,-1], [-1,0], [0,0], [1,0]], [1,8], 0)
tetris_block.SetBlock(5, [[-1,0], [0,1], [0,0], [0,-1]], [1,9], 1)
tetris_block.SetBlock(5, [[0,1], [1,0], [0,0], [-1,0]], [1,8], 1)
tetris_block.SetBlock(5, [[1,0], [0,-1], [0,0], [0,1]], [0,8], 1)

tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)
tetris_block.SetBlock(6, [[0,-1], [1,-1], [0,0], [1,0]], [0,8], 0)

tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9], 1)
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,8], 0)
tetris_block.SetBlock(7, [[0,-2], [0,-1], [0,0], [0,1]], [0,9], 1)
tetris_block.SetBlock(7, [[-2,0], [-1,0], [0,0], [1,0]], [2,9], 0)

#함수 생성
def displayblock(): #블럭 불러오는 코드 (tetris_block.blocklist에서 기본 정보를 불러오고 중심점 (0,0)을 기준으로 블럭 좌표값 대입하여 블럭 위치 확정)
    for i in range(0,4):
        realblock[i][0]=tetris_block.blocklist[current_falling_block-1][current_rotation-1][i][0]
        realblock[i][1]=tetris_block.blocklist[current_falling_block-1][current_rotation-1][i][1]
    for i in range(0,4):
        realblock[i][0]+=block_coordinate[0]
        realblock[i][1]+=block_coordinate[1]

def checkbelow(): #y좌표 감소시키기 전 아래 체크하는 코드
    for i in range(0,4):
        if realblock[i][1]+1>=22: return False
        elif board[realblock[i][0]][realblock[i][1]+1]>0: return False
    return True

def checkleft(): #왼쪽 체크
    for i in range(0,4):
        if realblock[i][0]-1<0: return False
        elif board[realblock[i][0]-1][realblock[i][1]]>0: return False
    return True

def checkright(): #오른쪽 체크
    for i in range(0,4):
        if realblock[i][0]+1>9: return False
        elif board[realblock[i][0]+1][realblock[i][1]]>0: return False
    return True

def checkrotate(): #-90° 돌기 전 블럭이 있는지 없는지 체크
    global current_falling_block
    global current_rotation
    global block_coordinate
    global board
    x=block_coordinate[0]
    y=block_coordinate[1]

    if current_falling_block==1:
        if current_rotation==1:
            if board[x-1][y-1] + board[x][y-1] + board[x][y+1] > 0: return False
            else: return True
        elif current_rotation==2:
            if board[x-1][y] + board[x+1][y] + board[x-1][y+1] > 0: return False
            else: return True
        elif current_rotation==3:
            if board[x][y-1] + board[x][y-1] + board[x+1][y+1] > 0: return False
            else: return True
        elif current_rotation==4:
            if board[x-1][y] + board[x+1][y] + board[x+1][y-1] > 0: return False
            else: return True     

    elif current_falling_block==2:
        if current_rotation==1:
            if board[x][y-1] + board[x][y+1] + board[x-1][y-1] > 0: return False
            else: return True
        elif current_rotation==2:
            if board[x-1][y] + board[x+1][y] + board[x+1][y+1] > 0: return False
            else: return True
        elif current_rotation==3:
            if board[x][y+1] + board[x+1][y-1] + board[x][y+1] > 0: return False
            else: return True
        elif current_rotation==4:
            if board[x-1][y] + board[x-1][y-1] + board[x+1][y] > 0: return False
            else: return True
        
    elif current_falling_block==3:
        if current_rotation%2==1:
            if board[x+1][y] + board[x][y+1] + board[x-1][y+1] > 0: return False
            else: return True
        elif current_rotation%2==0:
            if board[x][y+1] + board[x-1][y] + board[x-1][y-1] > 0: return False
            else: return True
    
    elif current_falling_block==4:
        if current_rotation%2==1:
            if board[x][y-1] + board[x-1][y-1] + board[x+1][y] >0: return False
            else: return True
        elif current_rotation%2==0:
            if board[x+1][y] + board[x+1][y-1] + board[x][y+1] >0: return False
            else: return True
    
    elif current_falling_block==5:
        if current_rotation==1:
            if board[x][y-1] + board[x][y+1] + board[x-1][y] >0: return False
            else: return True
        elif current_rotation==2:
            if board[x-1][y] + board[x+1][y] + board[x][y+1] > 0: return False
            else: return True
        elif current_rotation==3:
            if board[x][y-1] + board[x][y+1] + board[x+1][y] > 0: return False
            else: return True
        elif current_rotation==4:
            if board[x-1][y] + board[x+1][y] + board[x][y-1] > 0: return False
            else: return True
    
    elif current_falling_block==7:
        if current_rotation%2==1:
            if board[x-2][y] + board[x-1][y] + board[x+1][y] > 0: return False
            else: return True
        elif current_rotation%2==0:
            if board[x][y-2] + board[x][y-1] + board[x][y+1] >0: return False
            else: return True
        
def downblock(fall): #1초에 한번씩 y좌표 1씩 줄이는 코드
    time.sleep(0.001)
    displayblock()
    if fall>=50:
        if checkbelow():
            for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=0
            block_coordinate[1]+=1
            for i in range(0,4): board[realblock[i][0]][realblock[i][1]+1]=current_falling_block*(-1)
            return True
        else: return False
    return True
    

def draw_square(COLOR,x,y): #(25 X 25) 사각형 그리기
    if y>=2: pygame.draw.rect(screen, COLOR, [25*x, 25*y-50, 25, 25],0)

def clean(a): #좌우&회전 이동 시 이동 이전의 블럭 흔적 지우기
    for i in range(0,10):
        if board[i][realblock[a][1]]<=0: board[i][realblock[a][1]]=0
        if realblock[a][1]-1>=0 and board[i][realblock[a][1]-1]<=0: board[i][realblock[a][1]-1]=0
        if realblock[a][1]+1<=21 and board[i][realblock[a][1]+1]<=0: board[i][realblock[a][1]+1]=0

#블럭 생성
def block_create():
    p = 0
    for j in range(0,block_log[1]+1): p += random.randint(2,10)*(-1) #random.randint(a,b): a<=x<=b 인 정수인 난수 x 리턴
    same_P = []
    same_P.append(1)
    new_P = p
    new = 1
        
    for i in range(2,8):
        P = 0
        for j in range(0,block_log[i]+1): P += random.randint(2,10)*(-1)
        if new_P < P:
            same_P = []
            same_P.append(i)
            new_P = P
            new = i
        elif new_P==P: same_P.append(i)
    if len(same_P) <= 1:
        block_log[new]+=1
        return new
    else:
        i=random.randrange(0,len(same_P))
        block_log[same_P[i]]+=1
        return same_P[i]
            

#초기설정
size = [10*25+25+10*25,20*25]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris N")
clock = pygame.time.Clock()

#본 코드
while runcode:
    clock.tick(100) #100fps
    #이벤트 감지 코드
    for event in pygame.event.get():
        if event.type == pygame.QUIT: runcode = False
            
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT and not hard_drop: # 왼쪽 키 입력
                if checkleft():
                    for i in range(0,4): clean(i)
                    block_coordinate[0]-=1
                    displayblock()
                    for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=current_falling_block*(-1)
                
            elif event.key == pygame.K_RIGHT and not hard_drop: # 오른쪽 키 입력
                if checkright():
                    for i in range(0,4): clean(i)
                    block_coordinate[0]+=1
                    displayblock()
                    for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=current_falling_block*(-1)
              
            elif event.key == pygame.K_SPACE: # 하드드롭
                for i in range(0,4): clean(i)
                endloop_aaaaa=False
                while True:
                    for i in range(0,4):
                        if realblock[i][1]+1>=22 or board[realblock[i][0]][realblock[i][1]+1]>0:
                            endloop_aaaaa=True
                            break
                    if endloop_aaaaa: break
                    block_coordinate[1]+=1
                    displayblock()
                for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=current_falling_block
                score+=10
                hard_drop=True
            
            elif event.key == pygame.K_UP: # 회전
                if checkrotate(): current_rotation+=1 # 회전해도 다른 블럭과 겹치지 않는지 확인
                if current_rotation==5: current_rotation=1
                for i in range(0,4): clean(i)
                before=current_rotation-1
                if before==0: before=4
                if block_coordinate[0]==tetris_block.limitx[current_falling_block-1][before-1][0]:
                    if(tetris_block.limitx[current_falling_block-1][before-1][0]<tetris_block.limitx[current_falling_block-1][current_rotation-1][0]): block_coordinate[0]+=tetris_block.limitx[current_falling_block-1][current_rotation-1][0]-tetris_block.limitx[current_falling_block-1][before-1][0]

                if block_coordinate[0]==tetris_block.limitx[current_falling_block-1][before-1][1]:
                    if(tetris_block.limitx[current_falling_block-1][before-1][1]>tetris_block.limitx[current_falling_block-1][current_rotation-1][1]): block_coordinate[0]+=tetris_block.limitx[current_falling_block-1][current_rotation-1][1]-tetris_block.limitx[current_falling_block-1][before-1][1]

                displayblock()
                for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=current_falling_block*(-1)

    #초기 설정
    screen.fill(WHITE)
            

    #블럭 드롭 or 생성
    if downblock(fall_period) and not hard_drop: #블럭 정착
      if fall_period>=50: fall_period=0
      fall_period+=1

    else: #새 블럭 생성
      for i in range(0,4): board[realblock[i][0]][realblock[i][1]]=current_falling_block
      current_falling_block=block_create()
      block_coordinate[0] = 4
      block_coordinate[1] = 3
      if current_falling_block == 3 or current_falling_block == 4 or current_falling_block == 7: block_coordinate[1]=2
      current_rotation = 1
      hard_drop=False
      fall_period=100

    #한 줄 차면 제거 & 게임오버 표시
    for x in range(0,10):
        if board[x][4]>0: runcode = False
    cleared_lines=0
    for y in range(6,22):
        filled=True
        while filled:
            for x in range(0,10):
                if board[x][y]<=0: filled=False
            if not filled: break
            for down in range(y-1,4,-1):
                for xx in range(0,10): board[xx][down+1]=board[xx][down]
            for xx in range(0,10): board[xx][4]=0
            cleared_lines+=1
    score += add_score[cleared_lines]
    #칸 정보 표시 (+디자인)
    for y in range(0,20):
        for x in range(0,10):
            if board[x][y+2] == 0: draw_square(WHITE,x,y)

    pygame.draw.rect(screen, GRAY, [0, 450, 250, 50],0)
    pygame.draw.rect(screen, GRAY, [0, 0, 250, 25],0)
    
    for y in range(0,20):
        for x in range(0,10):
            if board[x][y+2] == 1 or board[x][y+2] == -1: draw_square(ORANGE,x,y)#1번 블럭
            elif board[x][y+2] == 2 or board[x][y+2] == -2: draw_square(BLUE,x,y)#2번 블럭
            elif board[x][y+2] == 3 or board[x][y+2] == -3: draw_square(GREEN,x,y)#3번 블럭
            elif board[x][y+2] == 4 or board[x][y+2] == -4: draw_square(RED,x,y)#4번 블럭
            elif board[x][y+2] == 5 or board[x][y+2] == -5: draw_square(PURPLE,x,y)#5번 블럭
            elif board[x][y+2] == 6 or board[x][y+2] == -6: draw_square(YELLOW,x,y)#6번 블럭
            elif board[x][y+2] == 7 or board[x][y+2] == -7: draw_square(SKYBLUE,x,y)#7번 블럭

    pygame.draw.rect(screen, GRAY, [0, 0, 1, 500],0)
    pygame.draw.rect(screen, GRAY, [249, 0, 1, 500],0)
    for x in range(1,10): pygame.draw.rect(screen, GRAY, [25*x-1, 0, 2, 500],0)
    for y in range(1,20): pygame.draw.rect(screen, GRAY, [0, 25*y-1, 250, 2],0)
    pygame.draw.rect(screen, BLACK, [250, 0, 25, 500])
    
    #스코어 시스템
    score_text = font.render("Score : " + str(score), True, BLACK)
    screen.blit(score_text,(300,75))
    pygame.display.flip()
#종료

pygame.quit()

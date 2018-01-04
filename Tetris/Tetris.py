#URL https://www.cnblogs.com/lykyl/p/5946102.html
import rando,copy
import pygame as pg
from pygame.locals import *

'''
常量声明
'''
EMPTY_CELL=0  #空区标示，标示没有方块
FALLING_BLOCK=1  #下落的方块标示，也就是活动方块
STATIC_BLOCK=2   #固定方块标示

'''
全局变量声明
变量值以sysInit函数中初始化的结果为准
'''
defaultFont=None #默认字体
screen=None #屏幕输出对象
backSurface=None #图像输出缓冲画板
score=0 #玩家得分记录
clearLineScore=0  #玩家清除的方块行数
level=1 #关卡等级
clock=None #游戏时钟
nowBlock=None #当前下落的方块
nextBlock=None #下一个将出现的方块
fallSpeed=10  #当前方块下落的速度
beginFallSpeed=fallSpeed #游戏初始时方块下落的速度
speedBuff=0 #下落速度缓冲变量
keyBuff=None #上一次按键记录
maxBlockWidth=10 #舞台堆叠区X轴最大可容纳基础方块数
maxBlockHeight=18 #舞台堆叠区Y轴最大可容纳基础方块数
blockWidth=30 #以像素为单位的基础方块宽度
blockHeight=30 #以像素为单位的基础方块高度
block=[]  #方块形状矩阵四维列表，第一维为不同的方块形状，第二维为每个方块形状不同的方向(以0下表起始，一共四个方向)，第三维为Y轴方块形状占用情况，第四维为X轴方块形状占用情况，矩阵中0标识没有方块，1标识有方块
stage=[] #舞台堆叠区举证二维列表，第一维Y轴方块占用情况，第二维为X轴方块占用情况. 矩阵中0表示没有方块，1表示有固定方块，2标识有活动方块
gameOver=False #游戏结束标志
pause=False  #游戏暂停标志


def printTx(context, x, y, font, screen, color=(255, 255,255)):
    '''显示文本个
    args:
        content:待显示文本内容
        x,y:显示坐标
        font:字体
        screen:输出的screen
        color:颜色
    '''
    imgTxt=font.render(content, True, color)
    screen.blit(imgTxt, (x,y))

class point(object):
    '''平面坐标点类
    attributes:
    x,y:坐标值
    '''
    def __init__ (self, x, y):
        self.__x=x
        self.__y=y

    def getx(self):
        return self.__x

    def setx(x):
        self.__x=x

    x=property(getx, setx)

    def gety(self):
        return self.__y;

    def sety(y):
        self.__y=y

    y=property(gety, sety)

    def __str__(self)
        return "(x:"+"(:.0f".format(self.__x)+",y:"+"(:.0f)".format(self.__y)+")"

class blockSprite(object):
    '''
    方块形状精灵类
    下落方块的定义全靠它了
    atttibutes:
      shape:方块形状编号
      direction:方块方向编号
      xy:方块形状左上角方块坐标
      block:方块形状矩阵
    '''

def __init__(self, shape, direction, xy):
    self.shape=shape
    self.direction=direction
    self.xy=xy

def chaDirection(self, direction):
    '''
    改变方块的方向
    args:
        direction:1为向右转，0为向左转
    '''
    
    dirNumb=len(blocks[self.shape])-1
    if direction==1
        self.direction+=1
        if self.direction>dirNumb:
            self.direction=0
    else:
        self.direction-=1
        if self.direction<0:
            self.direction=dirNumb

def clone(self):
    '''
    克隆本体
    rerurnL
        返回自身的克隆
    '''
    return blockSprite(self.shape, self.direction, point(self.xy.x, self.xy.y))

def _getBlock(self):
    return blocks[self.shape][self.direction];

    block = property(_getBlock)

def getConf(fileName):
    '''
    从配置文件中读取方块形状数据
    每个方块以4*4矩阵标识形状，配置文件每行标示一个方块，用分号分割矩阵行，用逗号分割矩阵列，0表示没有方块，1表示有方块.
    因为此程序只针对俄罗斯方块的经典版，所以方块矩阵大小以编码的形式写死为4*4
    args:
        fileName:配置文件名
    '''
    global block #block记录方块形状
    with open(fileName,'rt') as fp:
        for temp in fp.readlines():
            block.append([])
            blocksNumb=len(blocks)-1
            blocks[blocksNumb]=[]
            #每种方块形状有四个方向，以0~3表示，配置文件中只记录一个方向形状，另外三个方向的矩阵排列在sysInit中通过调用transform计算出来
            blocks[blocksNumb].append([])
            row=temp.split(";")
            for r in range(len(row)):
                col=[]
                ct=row[r].split("'")
                #对矩阵列数据做规整，首先将非"1"的值全修正成"0"以 过滤空字符或回车符
                for c in range(len(ct)):
                    if ct[c]!="1":
                        col.append(0)
                    else:
                        col.append(1)
                #将不足四列的矩阵通过补0的方式，补足4列
                for c in range(len(ct)-1,3):
                    col.append(0)
                blocks[blocksNumb][0].append(col)
            #如果矩阵某行没有方块，则配置文件可以省略此行，程序会在末尾补上空行数据
        for r in range(len(row)-1,3):
            blocks[blocksNumb][0].append([0,0,0,])
        blocks[blockNumb][0]=formatBlock(blocks[blockNumb][0]

def sysInit():
    '''
    系统初始化
    包括pygame环境初始化，全局变量赋值，生成每个方块形状的四个方块矩阵
    '''
    global defaultFont,screen,backSurface,clock,blocks,stage,gameOver,fallSpeed,beginFallSpeed,nowBlock,nextBlock,score,level,clearLineScore,pause
    #pygame 运行环境初始化
    pg.init()
    screen=pg.display.set_mode((500,500))
    backSurface=pg.Surface((screen.get_rect().width, screen.get_rect().height))
    pg.display.set_caption("block")
    clock=pg.time.Clock()
    pg.mouse.set_vasible(False)

    #游戏全局变量初始化
    defaultFont=pg.font.Font("res/font/yh.ttf",16) #yh.tty这个字体文件请自行上网搜素下载，
    nowBlock=None
    nextBlock=None
    gameOver=False
    pause=False
    score=0
    level=1
    clearLineScore=0
    beginFallSpeed=20
    fallSpeed=beginFallSpeed-level*2

    #初始化游戏舞台
    stage=[]
    for y in range(maxBlockHeight):
        stage.append([])
        for x in range(maxBlockWidth):
            stage[y].append(EMPTY_CELL)

    #生成每个方块形状4个方向的矩阵数据
    for x in range(len(blocks)):
        if len(blocks[x]<2:
            t=blocks[x][0]
            for i in range(3):
                t=transform(t,1)
                blocks[x].append(formatBlock(t))

def transform(block,direction=0):
    result=[]
    for y in range(4)
        result.append([])
        for x in range(4)
            if direction==0:
                result[y].append(block[x][3-y])
            else:
                result[y].append(block[3-x][y])
    return result

def removeTopBlank(block):
    result=copy.deepcopy(block)
    blankNumb=0
    while sum(result[0])<1 and blankNumb<4:
        del result[0]
        result.append([0,0,0,0])
        blankNumb+=1

    return result

def formatBlock(block):
    result=transform(result, 1)
    result=removeTopBlank(result)
    result=transform(result, 0)
    return result

def checkDeany(sprite):
    topX=sprite.xy.x
    topY=sprite.xy.y
    for y in range(len(sprite.block)):
        for x in range(len(sprite.block[y])):
            if sprite.block[y][x]==1;
                yInStage=topY+y
                xInStage=topX+x
                if yInStage>maxBlockHeight-1 or yInStage<0:
                    return True

                if xInStage>maxBlockWidth-1 or xInStage<0:
                    return True

                if state[yInstage][xInstage]==STATIC_BLOCK;
                    return True

    return False

def checkLine():
    global stage
    clearCount=0
    tmpStage=[]

    for y in stage:
        if sum(y)>=maxBlockWidth*2:
            tmpStage.insert(0, maxBlockWidth*[0])
            clearCount+=1
        else:
            tmpStage.append(y)

    if clearCount>0:
        stage=tmpStage
        updateScore(clearCount)
        
    return clearCount


def updateStage(sprite, updateType=1):
    global stage
    topX=sprite.xy.x
    topY=sprite.xy.y
    for y in range(len(sprite.block)):
        if sprite.block[y][x]==1:
            if updateType==0:
                if stage[topY+y][topX+x]==FALLING_BLOCK:
                    stage[topY=y][topX+x]=EMPTY_CELL
                elif updateType==1:
                    if stage[topY+y][topX=x]==EMPTY_CELL;
                        stage[topY+y][topX+x]=FALLING_BLOCK
                else:
                    stage[topY+y][topX+x]=STATIC_BLOCK

def updateScore(clearCount):
    global score, fallspeed, level, clearLineScore

    prizePoint=0
    if clearCount>1:
        if clearCount<4:
            prizePoint=clearCount**clearCount
        else:
            prizePoint=clearCount*5
    score+=(clearCount+prizePoint)*level

    if score>999999999:
        score=0

    clearLineScore+=clearCount
    if clearLineScore>100:
        clearLineScore=0
        level+=1
        fallSpeed=beginFallSpeed
    fallSpeed=beginFallSpeed-level*2
    return score

def drawStage(drawScreen):
    staticColor=30,102,76
    activeColor=255,230,0
    fontColor=200,10,120
    baseRect=0,0,blockWidth*maxBlockWidth+1,blockHeight*maxBlockHeight+1

    drawScreen.fill((180,200,170))
    pg.draw.rect(drawscreen, staticColor,baseRect,1)

    for y in range(len(stage)):
        for x in range(len(stage[y])):
            baseRect= x*blockWidth,y*blockHeight,blockWidth,blockHeight
            if stage[y][x]==2:
                pg.draw.rect(drawSreen, staticColor, baseRect)
            elif stage [y][x]==1:
                pg.draw.rect(drawScreen, activeColor,baseRect)

    printTxt("Next:", 320,350,defaultFont,backSurface,fontColoe)
    if nextBlock!=None:
        for y in range(len(nextBlock.block)):
            for x in range(len(nextBlock.block[y])):
                baseRect=x*blockWidth,y*blockHeight,blockWidth,blockHeight
                if nextBlock.block[y][x]==1:
                    pg.draw.rect(drawScreen, activeColor, baseRect)

    printTxt("Level:%d" % lvevel, 320, 40, defaultFont, backSurface, fontColor)
    printTxt("Score:%d" % score, 320, 70, defaultFont, backSurface, fontColor)
    ptintTxt("Clear:%d" % clearLineScore, 320, 100, defaultFont, backDSurface, fontColor)

    if gameOver:
        printTxt("GAME OVER", 230, 200, defaultFont, back

import pygame as p
from math import cos,radians,sin,atan,degrees
import random
import time

p.init()

white=(255,255,255)
green=(0,255,0)
blue=(0,207,255)
red=(255,0,0)
black=(0,0,0)
display_width=1200
display_height=600
speed_plane=5
bullet_speed=7
fps=35
gravitational_acc=0.1


scn=p.display.set_mode((display_width,display_height))
p.display.set_caption('Blitzkrieg')

clock=p.time.Clock()
font=p.font.SysFont(None,50)
img1=p.image.load('jet.png')
p.display.set_icon(img1)
img_tank2=p.image.load('tank2.jpg')
img_tank3=p.image.load('tank3.jpg')
img_sky=p.image.load('sky.jpg')
img_blast=p.image.load('blast.png')
img_blast1=p.image.load('blast1.jpg')
img_blast3=p.image.load('blast3.jpg')
img_bomb=p.image.load('missile1.png')
img_missile=p.image.load('missile.png')
blast_sound=p.mixer.Sound('blast1.wav')
shortblast_sound=p.mixer.Sound('blast2.wav')
fire_sound=p.mixer.Sound('Swoosh.wav')
def message_to_scn(msg,colour,y):
    text=font.render(msg,True,colour)
    scn.blit(text,[600-7*len(msg),y])

def plane(x,y,img,angle):
    plane_img=p.transform.rotate(img,-angle)
    scn.blit(plane_img,[x,y])

def bullet(b):
    if b[2]==b[0]:
        shi=90
    else:
        shi=degrees(atan((b[2]-b[0])/(b[1]-b[3])))
    missile_img=p.transform.rotate(img_missile,-shi)
    scn.blit(missile_img,[b[0],b[1]])
    b[0]+=bullet_speed*sin(radians(shi))
    b[1]-=bullet_speed*cos(radians(shi))
    b[2]+=b[4]
    b[3]+=b[5]
def tank(tanklist):
    for tank_pos in tanklist:
        if tank_pos[1]>0:
            scn.blit(img_tank3,[tank_pos[0]+tank_pos[1],540])
        if tank_pos[1]<0:
            scn.blit(img_tank2,[tank_pos[0]+tank_pos[1],540])
        tank_pos[0]+=tank_pos[1]
        if tank_pos[0]>1200:
            tank_pos[0]=0
        if tank_pos[0]<0:
            tank_pos[0]=1200
def firebomb(bomblist):
    i=0
    for bomb_detail in bomblist:
        bomb_detail[3]=bomb_detail[3]+gravitational_acc
        bomb_detail[0]=bomb_detail[0]+bomb_detail[2]
        bomb_detail[1]=bomb_detail[1]+bomb_detail[3]
        i+=1
        phi=degrees(atan(bomb_detail[3]/bomb_detail[2]))
        if bomb_detail[2]>0:
            img=p.transform.rotate(img_bomb,-phi-90)
        if bomb_detail[2]<0:
            img=p.transform.rotate(img_bomb,-phi+90)
        scn.blit(img,[bomb_detail[0],bomb_detail[1]])
        if bomb_detail[1]>=560:
            scn.blit(img_blast1,[bomb_detail[0],bomb_detail[1]])
            p.mixer.Sound.play(shortblast_sound)
            del bomblist[i-1]

def gameloop():
    gexit=False
    mission_complete=False
    plane_x=100
    plane_y=100
    theta=0
    angular_v=0
    bombspeed=0
    bomblist=[]
    tanklist=[]
    bulletlist=[0,0,0,0,0,0]
    k=0
    count=0
    count2=0
    blast=[]
    bombcount=15
    for i in range(5):
        t=[]
        t.append(random.randrange(800*i/5,800*(i+1)/5))
        t.append(random.choice([2,-2]))
        tanklist.append(t)
    gameover=False
    while gexit==False:
        scn.blit(img_sky,[0,0])
        while gameover==True:
            message_to_scn('Press c to play again or q to quit',red,300)
            if mission_complete==True:
                message_to_scn('MISSION COMPLETE   ',red,350)
            else:
                message_to_scn('GAME OVER  ',red,350)
            p.display.update()
            for event in p.event.get():
                if event.type==p.QUIT:
                    p.quit()
                    quit()
                if event.type==p.KEYDOWN:
                    if event.key==p.K_c:
                        gameloop()
                    if event.key==p.K_q:
                        p.quit()
                        quit()
        p.draw.rect(scn,green,[0,560,1200,40])
        
        for event in p.event.get():
            if event.type==p.QUIT:
                    p.quit()
                    quit()
            if event.type==p.KEYDOWN:
                if event.key==p.K_UP:
                    angular_v=-3.5
                elif event.key==p.K_DOWN:
                    angular_v=3.5
                elif event.key==p.K_f:
                    bombcount-=1
                    bomb=[]
                    bomb.append(plane_x)
                    bomb.append(plane_y)
                    bomb.append(speed_x+bombspeed*cos(theta))
                    bomb.append(speed_y+bombspeed*sin(theta))
                    bomblist.append(bomb)
            if event.type==p.KEYUP:
                if event.key==p.K_UP:
                    angular_v=0
                elif event.key==p.K_DOWN:
                    angular_v=0
        for i in range(bombcount):
            scn.blit(img_bomb,[i*6,0])
        theta+=angular_v
        if plane_x>1200:
            plane_x=0
        if plane_x<0:
            plane_x=1200
        if plane_y<=0:
            theta=-theta
        if plane_y>=530:
            gameover=True
        speed_x=speed_plane*cos(radians(theta))
        speed_y=speed_plane*sin(radians(theta))
        
        plane_x+=speed_x
        plane_y+=speed_y
        plane(plane_x,plane_y,img1,theta)
        
        firebomb(bomblist)
        tank(tanklist)
        j=0
        for tank_pos in tanklist:
            for bomb in bomblist:
                if bomb[0]<=tank_pos[0]+60 and bomb[0]>=tank_pos[0]-10 and bomb[1]>=540:
                    blast.append(tank_pos[0])
                    p.mixer.Sound.play(blast_sound)
                    del tanklist[j]
                    count2=0
                    break
            j+=1
        for pos in blast:
            scn.blit(img_blast,[pos,520])
            count+=1
            if count>15:
                count=0
                blast=[]
        if bombcount==0 and len(tanklist)>0:
            gameover=True
        if len(tanklist)<5 and k<2:
            t=[]
            t.append(0)
            t.append(random.choice([2,-2]))
            tanklist.append(t)
            k+=1
        if count2==0 and len(tanklist)>=1:
            bulletlist[0]=(tanklist[0][0])
            bulletlist[1]=(540)
            bulletlist[2]=(plane_x)
            bulletlist[3]=(plane_y)
            count2=1
            p.mixer.Sound.play(fire_sound)
        
        bulletlist[4]=(speed_x)
        bulletlist[5]=(speed_y)
        
        
        if bulletlist[3]<bulletlist[1]:
            bullet(bulletlist)
            if bulletlist[0]>=plane_x-30 and bulletlist[0]<=plane_x+30 and bulletlist[1]>=plane_y-20 and bulletlist[1]<=plane_y+20:
                scn.blit(img_blast3,[plane_x,plane_y])
                p.mixer.Sound.play(blast_sound)
                p.display.update()
                gameover=True
                time.sleep(1)
        if len(tanklist)==0 and bombcount>=0:
            mission_complete=True
            gameover=True
        p.display.update()
        clock.tick(fps)
    p.quit()
    quit()
gameloop()

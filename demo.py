import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from mainLoader import *


def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(filename))


pygame.init()
viewport = (1000,800)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           

obj = OBJ('axum.obj', swapyz=False)

obj.generate()

clock = pygame.time.Clock()
glFrustum(-1, 1, -1, 1, 2, 10)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
gluLookAt(5, 2, 4, 0, 0, 0, 0, 2, 0)

rx, ry = (-2,16)
tx, ty = (-2,-16)
zpos = 29
soundtrac = load_sound('sound.wav')

rotate = move = False
while 1:
    soundtrac.play()
    clock.tick(30)
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
            print(rx,ry,zpos,rx,ry)
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
            print(rx,ry,zpos,rx,ry)
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
                print(rx,ry,zpos,rx,ry)
            if move:
                tx += i
                ty -= j
                print(rx,ry,zpos,rx,ry)
        elif keys[pygame.K_UP]:
            zpos -=2
            
        elif keys[pygame.K_DOWN]:
            zpos +=2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    obj.render()

    pygame.display.flip()
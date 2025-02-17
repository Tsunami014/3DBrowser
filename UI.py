import pygame
from OpenGL.GL import *  # noqa: F403
from OpenGL.GLU import gluPerspective, gluLookAt
from world import DefaultStage as DEFAULTSTAGE

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

glMatrixMode(GL_PROJECTION)
gluPerspective(45, display[0]/display[1], 0.1, 50.0)

glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# Center mouse
displayCenter = [screen.get_size()[i] // 2 for i in range(2)]
pygame.mouse.set_pos(displayCenter)
pygame.mouse.set_visible(False)

stage = DEFAULTSTAGE()
objs = stage.getObjs()

up_down_angle = 0.0
paused = False
run = True

# Main loop
while run:
    mouseMove = [0, 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_PAUSE, pygame.K_p]:
            paused = not paused
            pygame.mouse.set_pos(displayCenter)
            pygame.mouse.set_visible(paused)
        if not paused and event.type == pygame.MOUSEMOTION:
            mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)

    keypress = pygame.key.get_pressed()
    
    if not paused:
        glLoadIdentity()
        up_down_angle += mouseMove[1] * 0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        glPushMatrix()
        glLoadIdentity()

        # Movement controls
        move_speed = 0.3
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, move_speed)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -move_speed)
        if keypress[pygame.K_d]:
            glTranslatef(-move_speed, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(move_speed, 0, 0)
        if keypress[pygame.K_LSHIFT]:
            glTranslatef(0, 0.5, 0)
        if keypress[pygame.K_SPACE]:
            glTranslatef(0, -0.5, 0)

        # Apply rotation
        glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        
        # Render cubes
        for o in objs:
            o.render()
        
        glDisable(GL_TEXTURE_2D)

        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glVertex3f(-10, -10, -2)
        glVertex3f(10, -10, -2)
        glVertex3f(10, 10, -2)
        glVertex3f(-10, 10, -2)
        glEnd()

        glPopMatrix()
        
        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()

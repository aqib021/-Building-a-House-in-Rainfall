from OpenGL.GL import *
from OpenGL.GLUT import *
import random

window_width, window_height = 500, 500

def draw_house():
    # Defining house dimensions
    house_width = 300
    house_height = 120

    # Here calculating the scaling factors for width and height
    width_scale = window_width / 500
    height_scale = window_height / 500

    # Now calculating center of the window (Target to place at center)
    center_x = window_width / 2
    center_y = window_height / 2

    # Calculating house position based on the center
    house_x = center_x - (house_width * 0.5 * width_scale)
    house_y = center_y - (house_height * 0.5 * height_scale)

    # Drawing Roof using GL_TRIANGLES
    glColor3f(0.13, 0.55, 0.13)  # Forest Green color roof
    glBegin(GL_TRIANGLES)
    glVertex2f(center_x, house_y + house_height * height_scale)  # Top of the roof
    glVertex2f(center_x - (house_width * 0.5 * width_scale), house_y)  # and bottom-left corner of the roof
    glVertex2f(center_x + (house_width * 0.5 * width_scale), house_y)  # and bottom-right corner of the roof
    glEnd()

    # Here drawing the Walls using GL_LINES 
    glColor3f(1.0, 0.0, 0.0)  # Red color for the walls
    glBegin(GL_LINES)
    glVertex2f(center_x - (house_width * 0.5 * width_scale), house_y)  # Bottom-left corner of the walls
    glVertex2f(center_x - (house_width * 0.5 * width_scale), house_y - (house_height * height_scale))  # Top-left corner of the walls

    glVertex2f(center_x - (house_width * 0.5 * width_scale), house_y - (house_height * height_scale))  # Top-left corner of the walls
    glVertex2f(center_x + (house_width * 0.5 * width_scale), house_y - (house_height * height_scale))  # Top-right corner of the walls

    glVertex2f(center_x + (house_width * 0.5 * width_scale), house_y - (house_height * height_scale))  # Top-right corner of the walls
    glVertex2f(center_x + (house_width * 0.5 * width_scale), house_y)  # Bottom-right corner of the walls
    glEnd()

    # Drawing Door using GL_LINES
    door_width = 50
    door_height = house_height  # It adjust the door height to match the house height

    door_x = center_x - (door_width * 0.5 * width_scale)
    door_y = house_y  # Place the door at the bottom of the house

    glColor3f(0.4, 0.2, 0.0)  # Setting Brown color for the door
    glBegin(GL_LINES)
    glVertex2f(door_x, door_y)  # Bottom-left corner of the door
    glVertex2f(door_x + (door_width * width_scale), door_y)  # Bottom-right corner of the door

    glVertex2f(door_x + (door_width * width_scale), door_y)  # Bottom-right corner of the door
    glVertex2f(door_x + (door_width * width_scale), door_y - (door_height * height_scale))  # Top-right corner of the door

    glVertex2f(door_x + (door_width * width_scale), door_y - (door_height * height_scale))  # Top-right corner of the door
    glVertex2f(door_x, door_y - (door_height * height_scale))  # Top-left corner of the door

    glVertex2f(door_x, door_y - (door_height * height_scale))  # Top-left corner of the door
    glVertex2f(door_x, door_y)  # Bottom-left corner of the door
    glEnd()

    # Drawing doorknob using GL_TRIANGLES
    knob_x = door_x + (door_width * width_scale) - 5
    knob_y = door_y - (door_height * height_scale) * 0.5

    glColor3f(1.0, 0.0, 0.0)  # Red color for the doorknob
    glBegin(GL_TRIANGLES)
    glVertex2f(knob_x, knob_y + 5)  # Top vertex
    glVertex2f(knob_x, knob_y - 5)  # Bottom-right vertex
    glVertex2f(knob_x - 5, knob_y - 5)  # Bottom-left vertex
    glEnd()

raindrops = []
rain_angle = 0
rain_speed = 10

def create_raindrop(angle, speed):
    x = random.uniform(0, window_width)
    y = window_height
    speed = random.uniform(5, 20)
    length = random.uniform(10, 30)
    return {'x': x, 'y': y, 'speed': speed, 'length': length, 'angle': angle}

def draw_raindrop(x, y, length, angle):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angle, 0, 0, 1)
    glColor3f(0.0, 0.0, 1.0)  # Blue color for the raindrop
    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(0, -length)
    glEnd()
    glPopMatrix()

def draw_rain():
    for raindrop in raindrops:
        draw_raindrop(raindrop['x'], raindrop['y'], raindrop['length'], raindrop['angle'])

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(0.0, 0.0, 1.0)

    draw_house()

    for raindrop in raindrops:
        raindrop['y'] -= raindrop['speed']
        if raindrop['y'] < -raindrop['length']:
            raindrops.remove(raindrop)
            raindrops.append(create_raindrop(rain_angle, rain_speed))

    draw_rain()
    glutSwapBuffers()

def iterate():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def special_key_handler(key, x, y):
    global rain_angle, rain_speed
    if key == GLUT_KEY_RIGHT:
        if rain_angle < 45:
            rain_angle += 5
    elif key == GLUT_KEY_LEFT:
        if rain_angle > -45:
            rain_angle -= 5

def key_handler(key, x, y):
    if key == b'D' or key == b'd':
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Setting background color to white (day)
    elif key == b'N' or key == b'n':
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Setting background color to black (night)

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"House and Raindrops")
    glutDisplayFunc(show_screen)
    iterate()

if __name__ == "__main__":
    main()

    for _ in range(100):
        raindrops.append(create_raindrop(rain_angle, rain_speed))

    glutSpecialFunc(special_key_handler)
    glutKeyboardFunc(key_handler)
    glutIdleFunc(show_screen)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Setting initial background color to white (day)
    glutMainLoop()




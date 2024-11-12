import pyMeow
import time
from math import sqrt

def initialize_overlay(window_name="ShellShock Live"):
    pyMeow.overlay_init(target=window_name, title="Multi-Tool Overlay", fps=60, trackTarget=True)
    pyMeow.set_window_title("Multi-Tool Overlay")

def distance_between_points(point1, point2):
    return sqrt((point2['x'] - point1['x']) ** 2 + (point2['y'] - point1['y']) ** 2)

def find_closest_point(points, pos):
    closest_point = None
    min_distance = float('inf')
    for point in points:
        distance = distance_between_points(point, pos)
        if distance < min_distance:
            min_distance = distance
            closest_point = point
    return closest_point

def flip_y(y):
    return pyMeow.get_screen_height() - y

def main():
    initialize_overlay()
    
    point1, point2 = None, None
    toggle_drawing = False
    input_mode = "off"
    points_ready = False
    points = []
    timer_start = None
    timer_end = None
    timer_running = False

    margin_x, margin_y = 20, 70
    font_size = 16
    label_height = 25

    while pyMeow.overlay_loop():
        pyMeow.begin_drawing()
        pyMeow.gui_label(margin_x, margin_y, 300, label_height, f"Dibujo: {'ON' if toggle_drawing else 'OFF'} (Presiona 'T')")
        pyMeow.gui_label(margin_x, margin_y + label_height, 300, label_height, f"Modo de entrada: {input_mode} (Presiona 'M')")

        window_pos = pyMeow.get_window_position()

        if pyMeow.key_pressed(84):
            toggle_drawing = not toggle_drawing
            time.sleep(0.2)

        if pyMeow.key_pressed(77):
            input_mode = "distance" if input_mode == "off" else "points" if input_mode == "distance" else "cronometro" if input_mode == "points" else "off"
            time.sleep(0.2)

        if input_mode == "distance":
            if pyMeow.mouse_pressed("left"):
                pos = pyMeow.mouse_position()
                point1 = {'x': pos['x'] - window_pos['x'], 'y': pos['y'] - window_pos['y']}
                points_ready = False
                time.sleep(0.2)
            elif pyMeow.mouse_pressed("right"):
                pos = pyMeow.mouse_position()
                point2 = {'x': pos['x'] - window_pos['x'], 'y': pos['y'] - window_pos['y']}
                points_ready = False
                time.sleep(0.2)

        elif input_mode == "points":
            pos = pyMeow.mouse_position()
            pos = {'x': pos['x'] - window_pos['x'], 'y': pos['y'] - window_pos['y']}
            if pyMeow.mouse_pressed("left"):
                points.append(pos)
                time.sleep(0.2)
            elif pyMeow.mouse_pressed("right") and points:
                closest_point = find_closest_point(points, pos)
                if closest_point:
                    points.remove(closest_point)
                time.sleep(0.2)

        elif input_mode == "cronometro":
            if pyMeow.mouse_pressed("left") and not timer_running:
                timer_start = time.time()
                timer_running = True
                time.sleep(0.2)
            elif pyMeow.mouse_pressed("right") and timer_running:
                timer_end = time.time()
                timer_running = False
                time.sleep(0.2)

        if toggle_drawing:
            if point1 and point2:
                if not points_ready:
                    points_ready = True
                pyMeow.draw_line(point1['x'], point1['y'], point2['x'], point2['y'], pyMeow.get_color("red"))
                distance = distance_between_points(point1, point2)
                midpoint_x = (point1['x'] + point2['x']) / 2
                midpoint_y = (point1['y'] + point2['y']) / 2
                pyMeow.draw_text(f"Distancia: {distance:.2f}", midpoint_x, midpoint_y, font_size, pyMeow.get_color("white"))

            for point in points:
                pyMeow.draw_circle(point['x'], point['y'], 6, pyMeow.get_color("green"))
                flipped_y = flip_y(point['y'])
                pyMeow.draw_text(f"({int(point['x'])}, {int(flipped_y)})", point['x'] + 10, point['y'], font_size, pyMeow.get_color("white"))

            if timer_running:
                elapsed_time = time.time() - timer_start
                pyMeow.draw_text(f"Tiempo: {elapsed_time:.2f} s", margin_x, margin_y + 2 * label_height, font_size, pyMeow.get_color("yellow"))
            elif timer_start and timer_end:
                total_time = timer_end - timer_start
                pyMeow.draw_text(f"Tiempo total: {total_time:.2f} s", margin_x, margin_y + 2 * label_height, font_size, pyMeow.get_color("yellow"))

        pyMeow.end_drawing()


    pyMeow.overlay_close()

if __name__ == "__main__":
    main()

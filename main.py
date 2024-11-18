import pyMeow
import time
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import subprocess

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

def screen_to_physics(x, y):
    return x, pyMeow.get_screen_height() - y

def physics_to_screen(x, y):
    return x, pyMeow.get_screen_height() - y

def main():
    initialize_overlay()
    
    point1, point2 = None, None
    toggle_drawing = False
    input_mode = "off"
    modes = ['off', 'distance', 'points', 'cronometro', 'regression']
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
            current_index = modes.index(input_mode)
            input_mode = modes[(current_index + 1) % len(modes)]
            time.sleep(0.2)

        if pyMeow.key_pressed(80): 
            if point1 and point2:
                sx = point2['x'] - point1['x']
                sy = point2['y'] - point1['y']
                subprocess.Popen(["python3", "calculate.py", str(sx), str(sy)])
                time.sleep(0.2)            

       
        if input_mode == "distance":
            if pyMeow.mouse_pressed("left"):
                pos = pyMeow.mouse_position()
                x_screen = pos['x'] - window_pos['x']
                y_screen = pos['y'] - window_pos['y']
                x_phys, y_phys = screen_to_physics(x_screen, y_screen)
                point1 = {'x': x_phys, 'y': y_phys}
                points_ready = False
                time.sleep(0.2)
            elif pyMeow.mouse_pressed("right"):
                pos = pyMeow.mouse_position()
                x_screen = pos['x'] - window_pos['x']
                y_screen = pos['y'] - window_pos['y']
                x_phys, y_phys = screen_to_physics(x_screen, y_screen)
                point2 = {'x': x_phys, 'y': y_phys}
                points_ready = False
                time.sleep(0.2)

        elif input_mode == "points" or input_mode == "regression":
            pos = pyMeow.mouse_position()
            x_screen = pos['x'] - window_pos['x']
            y_screen = pos['y'] - window_pos['y']
            x_phys, y_phys = screen_to_physics(x_screen, y_screen)
            if pyMeow.mouse_pressed("left"):
                if input_mode == "regression":
                    point1 = {'x': x_phys, 'y': y_phys}
                else:
                    points.append({'x': x_phys, 'y': y_phys})
                time.sleep(0.2)
            elif pyMeow.mouse_pressed("right") and points:
                closest_point = find_closest_point(points, {'x': x_phys, 'y': y_phys})
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
                sx = point2['x'] - point1['x']
                sy = point2['y'] - point1['y']
                total_distance = sqrt(sx ** 2 + sy ** 2)
                
         
                x_screen1, y_screen1 = physics_to_screen(point1['x'], point1['y'])
                x_screen2, y_screen2 = physics_to_screen(point2['x'], point2['y'])
                
          
                pyMeow.draw_line(x_screen1, y_screen1, x_screen2, y_screen2, pyMeow.get_color("red"))
                
            
                midpoint_x = (x_screen1 + x_screen2) / 2
                midpoint_y = (y_screen1 + y_screen2) / 2
                
   
                pyMeow.draw_text(f"Distancia total: {total_distance:.2f} px", midpoint_x, midpoint_y - 20, font_size, pyMeow.get_color("white"))
                pyMeow.draw_text(f"sx: {sx:.2f} px", midpoint_x, midpoint_y, font_size, pyMeow.get_color("cyan"))
                pyMeow.draw_text(f"sy: {sy:.2f} px", midpoint_x, midpoint_y + 20, font_size, pyMeow.get_color("cyan"))
            
        
            if point1:
                x_screen1, y_screen1 = physics_to_screen(point1['x'], point1['y'])
                pyMeow.draw_circle(x_screen1, y_screen1, 6, pyMeow.get_color("green"))
                pyMeow.draw_text(f"({int(point1['x'])}, {int(point1['y'])})", x_screen1 + 10, y_screen1, font_size, pyMeow.get_color("white"))
            if point2:
                x_screen2, y_screen2 = physics_to_screen(point2['x'], point2['y'])
                pyMeow.draw_circle(x_screen2, y_screen2, 6, pyMeow.get_color("blue"))
                pyMeow.draw_text(f"({int(point2['x'])}, {int(point2['y'])})", x_screen2 + 10, y_screen2, font_size, pyMeow.get_color("white"))

      
            if timer_running:
                elapsed_time = time.time() - timer_start
                pyMeow.draw_text(f"Tiempo: {elapsed_time:.2f} s", margin_x, margin_y + 2 * label_height, font_size, pyMeow.get_color("yellow"))
            elif timer_start and timer_end:
                total_time = timer_end - timer_start
                pyMeow.draw_text(f"Tiempo total: {total_time:.2f} s", margin_x, margin_y + 2 * label_height, font_size, pyMeow.get_color("yellow"))

        
            if points:
                for point in points:
                    x_screen, y_screen = physics_to_screen(point['x'], point['y'])
                    pyMeow.draw_circle(x_screen, y_screen, 4, pyMeow.get_color("white"))
                    if point1:
                      
                        sx = point['x'] - point1['x']
                        sy = point['y'] - point1['y']
                    
                        pyMeow.draw_text(f"({sx:.2f}, {sy:.2f})", x_screen + 5, y_screen - 15, font_size, pyMeow.get_color("white"))

         
            if point1 and len(points) >= 3:
                sx_list = []
                sy_list = []
                for point in points:
                    sx = point['x'] - point1['x']
                    sy = point['y'] - point1['y']
                    sx_list.append(sx)
                    sy_list.append(sy)
              
                coefficients = np.polyfit(sx_list, sy_list, 2)
                a, b, c = coefficients
    
                sx_range = np.linspace(min(sx_list), max(sx_list), 100)
                sy_fit = a * sx_range**2 + b * sx_range + c
      
                x_curve_screen = [physics_to_screen(sx + point1['x'], 0)[0] for sx in sx_range]
                y_curve_screen = [physics_to_screen(0, sy + point1['y'])[1] for sy in sy_fit]
        
                for i in range(len(x_curve_screen) - 1):
                    pyMeow.draw_line(
                        x_curve_screen[i], y_curve_screen[i],
                        x_curve_screen[i + 1], y_curve_screen[i + 1],
                        pyMeow.get_color("red")
                    )
          
                pyMeow.draw_text(f"sy = {a:.4f}*sx^2 + {b:.4f}*sx + {c:.4f}", margin_x, margin_y + 3 * label_height, font_size, pyMeow.get_color("yellow"))

     
        if pyMeow.key_pressed(83):  
            if point1 and len(points) >= 3:
                sx_array = np.array([p['x'] - point1['x'] for p in points])
                sy_array = np.array([p['y'] - point1['y'] for p in points])
                coefficients = np.polyfit(sx_array, sy_array, 2)
                a, b, c = coefficients
                plt.figure()
                plt.scatter(sx_array, sy_array, color='blue', label='Datos')
                sx_fit = np.linspace(min(sx_array), max(sx_array), 500)
                sy_fit = a * sx_fit**2 + b * sx_fit + c
                plt.plot(sx_fit, sy_fit, color='red', label='Regresión Cuadrática')
                plt.xlabel('sx')
                plt.ylabel('sy')
                plt.title('Regresión Cuadrática')
                plt.legend()
                plt.savefig('regression_plot.png')
                plt.close()
                pyMeow.draw_text("Imagen de regresión guardada.", margin_x, margin_y + 4 * label_height, font_size, pyMeow.get_color("green"))
            else:
                pyMeow.draw_text("No hay suficientes datos para guardar la imagen.", margin_x, margin_y + 4 * label_height, font_size, pyMeow.get_color("red"))
            time.sleep(0.2)

        pyMeow.end_drawing()

    pyMeow.overlay_close()

if __name__ == "__main__":
    main()

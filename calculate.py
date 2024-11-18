import dearpygui.dearpygui as dpg
import math
import sys


def calcular_potencia(theta_deg, sx, sy):
    g = 223.75
    k = 0.1628
    theta_rad = math.radians(theta_deg)

    numerator = g * sx**2
    denominator = 2 * math.cos(theta_rad)**2 * (sx * math.tan(theta_rad) - sy)
    if denominator == 0 or numerator / denominator < 0:
        return None

    u_squared = numerator / denominator
    u = math.sqrt(u_squared)
    return k * u


def calculate_power(sender, app_data, user_data):
    try:
        theta = float(dpg.get_value("Angle Input"))
        sx = float(user_data["sx"])
        sy = float(user_data["sy"])

        power = calcular_potencia(theta, sx, sy)
        if power is not None:
            dpg.set_value("Result Label", f"Potencia: {power:.2f}")
        else:
            dpg.set_value("Result Label", "Cálculo no válido")
    except ValueError:
        dpg.set_value("Result Label", "Error: Entrada no válida")


def open_gui(sx, sy):
    dpg.create_context()
    dpg.create_viewport(title="Cálculo de Potencia", width=400, height=300)

    with dpg.window(label="Cálculo de Potencia", width=400, height=300):
        dpg.add_text(f"sx: {sx}")
        dpg.add_text(f"sy: {sy}")

        dpg.add_input_text(tag="Angle Input", label="Ángulo (grados)", default_value="45.0", width=150)
        dpg.add_button(label="Calcular", callback=calculate_power, user_data={"sx": sx, "sy": sy})
        dpg.add_text("", tag="Result Label")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 script.py <sx> <sy>")
        sys.exit(1)

    try:
        sx = float(sys.argv[1])
        sy = float(sys.argv[2])
        open_gui(sx, sy)
    except ValueError:
        print("Error: sx y sy deben ser números.")
        sys.exit(1)

import math

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
    potencia = k * u

    return potencia


try:
    theta = float(input("Ingresa el ángulo de disparo en grados: "))
    sx = float(input("Ingresa la distancia horizontal (s_x) en píxeles: "))
    sy = float(input("Ingresa la diferencia de altura (s_y) en píxeles: "))

    potencia_necesaria = calcular_potencia(theta, sx, sy)

    if potencia_necesaria is not None:
        print(f"La potencia necesaria es: {potencia_necesaria:.2f}")
    else:
        print("No es posible calcular la potencia para los valores dados. Revisa los valores ingresados.")
except ValueError:
    print("Por favor, ingresa valores numéricos válidos.")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Motor:
    def __init__(self, rpm_maxima=3000, torque_maximo=5, tiempo_final=10, n_puntos=1000, pendiente_rpm_ref=300):
        self.rpm_maxima = rpm_maxima
        self.torque_maximo = torque_maximo
        self.tiempo_final = tiempo_final
        self.n_puntos = n_puntos
        self.pendiente_rpm_ref = pendiente_rpm_ref

    def simular(self, archivo_csv="resultados_motor.csv"):

        tiempo = np.linspace(0, self.tiempo_final, self.n_puntos)


        rpm_referencia = self.pendiente_rpm_ref * tiempo


        torque = self.torque_maximo * (1 - rpm_referencia / self.rpm_maxima)


        velocidad_angular = rpm_referencia * 2 * np.pi / 60


        potencia = torque * velocidad_angular


        plt.figure(figsize=(10,4))
        plt.plot(tiempo, rpm_referencia, label="Referencia de RPM", color="blue")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("RPM")
        plt.title("Evolución de la referencia de RPM del motor")
        plt.legend()
        plt.grid(True)
        plt.show()


        plt.figure(figsize=(10,4))
        plt.plot(rpm_referencia, potencia, label="Potencia vs Velocidad", color="red")
        plt.xlabel("Velocidad (RPM)")
        plt.ylabel("Potencia (W)")
        plt.title("Curva de Potencia del motor")
        plt.legend()
        plt.grid(True)
        plt.show()


        datos = {
            "Tiempo (s)": tiempo,
            "RPM referencia": rpm_referencia,
            "Torque (N·m)": torque,
            "Velocidad angular (rad/s)": velocidad_angular,
            "Potencia (W)": potencia
        }
        df = pd.DataFrame(datos)
        df.to_csv(archivo_csv, index=False)
        print(f"Resultados guardados en {archivo_csv}")


motor = Motor(rpm_maxima=3000, torque_maximo=5, tiempo_final=10, n_puntos=1000, pendiente_rpm_ref=300)
motor.simular("resultados_motor.csv")


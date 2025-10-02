import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Usar backend compatible con Tkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk
import time
import pandas as pd


def motor_step(rpm_prev, u, K, tau, Ts):
    return rpm_prev + (Ts/tau) * (-rpm_prev + K * u)

class MotorSimulator:
    def __init__(self, K=100, tau=0.5, Ts=0.05):
        self.K = K
        self.tau = tau
        self.Ts = Ts
        self.rpm = 0
        self.running = False
        self.time = [0]
        self.rpm_history = [0]
        self.u_history = [0]
        self.start_time = time.time()

    def step(self):
        u = 1.0 if self.running else 0.0
        self.rpm = motor_step(self.rpm, u, self.K, self.tau, self.Ts)
        t = time.time() - self.start_time
        self.time.append(t)
        self.rpm_history.append(self.rpm)
        self.u_history.append(u)


def animate(i, sim, ax1, ax2):
    sim.step()
    ax1.clear()
    ax2.clear()

    ax1.plot(sim.time, sim.rpm_history, label="Motor (RPM)", color="blue")
    ax1.set_ylabel("RPM")
    ax1.set_title("Motor con Control ON/OFF")
    ax1.grid(True)
    ax1.legend()

    ax2.plot(sim.time, sim.u_history, label="Entrada (u)", color="green")
    ax2.set_xlabel("Tiempo [s]")
    ax2.set_ylabel("Potencia Normalizada")
    ax2.grid(True)
    ax2.legend()


class MotorTeorico:
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

        # Exportar CSV
        datos = {
            "Tiempo (s)": tiempo,
            "RPM referencia": rpm_referencia,
            "Torque (N·m)": torque,
            "Velocidad angular (rad/s)": velocidad_angular,
            "Potencia (W)": potencia
        }
        df = pd.DataFrame(datos)
        df.to_csv(archivo_csv, index=False)
        print(f"✅ Resultados guardados en {archivo_csv}")

        # Mostrar gráficas
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


def start_app():
    sim = MotorSimulator()

    # Crear ventana principal
    root = tk.Tk()
    root.title("Control del Motor + Gráfica")

    # Frame de botones
    frame_controls = ttk.Frame(root)
    frame_controls.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    def turn_on():
        sim.running = True
        print("✅ Motor encendido")

    def turn_off():
        sim.running = False
        print("🛑 Motor apagado")

    btn_on = tk.Button(frame_controls, text="Encender Motor", command=turn_on, bg="lightgreen", width=20)
    btn_on.pack(pady=10)

    btn_off = tk.Button(frame_controls, text="Apagar Motor", command=turn_off, bg="lightcoral", width=20)
    btn_off.pack(pady=10)


    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ani = animation.FuncAnimation(fig, animate, fargs=(sim, ax1, ax2), interval=50, cache_frame_data=False)

    # Al cerrar ventana → correr modelo teórico
    def on_closing():
        root.destroy()
        motor_teorico = MotorTeorico()
        motor_teorico.simular("resultados_motor.csv")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    start_app()

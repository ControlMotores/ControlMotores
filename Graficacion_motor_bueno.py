import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


t = np.linspace(0, 10, 1000)
rpm_ref = 300 * t


torque = 5 * (1 - rpm_ref / 3000)
omega = rpm_ref * 2 * np.pi / 60
potencia = torque * omega


plt.figure(figsize=(10,4))
plt.plot(t, rpm_ref, label="Referencia de RPM", color="blue")
plt.xlabel("Tiempo (s)")
plt.ylabel("RPM")
plt.title("Evolución de la referencia de RPM del motor")
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10,4))
plt.plot(rpm_ref, potencia, label="Potencia vs Velocidad", color="red")
plt.xlabel("Velocidad (RPM)")
plt.ylabel("Potencia (W)")
plt.title("Curva de Potencia del motor")
plt.legend()
plt.grid(True)
plt.show()


data = {
    "Tiempo (s)": t,
    "RPM referencia": rpm_ref,
    "Torque (N·m)": torque,
    "Velocidad angular (rad/s)": omega,
    "Potencia (W)": potencia
}

df = pd.DataFrame(data)


df.to_csv("resultados_motor.csv", index=False)
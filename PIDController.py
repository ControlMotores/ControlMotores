class PIDController:
    def __init__(self, Kp, Ki, Kd, dt):
        # Valores de ganancias (proporcional(P),integral(I),derivativa(D))
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt

        self.integral = 0.0
        self.error_anterior = 0.0
        self.salida_control = 0.0

    def calcular_salida(self, referencia, salida_actual):

        # 1. Calcular el Error
        error = referencia - salida_actual

        # 2. Acción Proporcional (P): Responde a la magnitud del error.
        ter_p = self.Kp * error

        # 3. Acción Integral (I): Acumula el error para eliminar el error de estado estacionario.
        self.integral += error * self.dt
        ter_i = self.Ki * self.integral

        # 4. Acción Derivativa (D): Responde a la tasa de cambio del error (para amortiguar).
        if self.dt > 0:
            derivada = (error - self.error_anterior) / self.dt
        else:
            derivada = 0.0
        ter_d = self.Kd * derivada

        # 5. Salida de Control: Suma de las tres acciones.
        self.salida_control = ter_p + ter_i + ter_d

        # 6. Actualizar el Error Anterior para el próximo ciclo
        self.error_anterior = error

        # 7. Retornar la salida de control
        return self.salida_control
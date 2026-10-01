"""
Práctica 1: Diseño de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Mildred Angel Torales
Número de control: 23212731
Correo institucional: L23212731@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo
Correo: paul.valle@tectijuana.edu.mx
"""


# ============================================================
# INSTALAR LIBRERÍAS EN CONSOLA SI ES NECESARIO
# ============================================================
# pip install numpy control matplotlib


# ============================================================
# LIBRERÍAS
# ============================================================

import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt
import os


# ============================================================
# DATOS GENERALES DE LA SIMULACIÓN
# ============================================================

x0 = 0
t0 = 0
tend = 10
dt = 1E-3
w = 7
h = 3.5

N = round(tend / dt) + 1

t = np.linspace(t0, tend, N)

# Entrada escalón
u1 = np.ones(N)

# Entrada impulso
u2 = np.zeros(N)
u2[round(1 / dt):round(2 / dt)] = 1

# Entrada rampa
u3 = t / tend

# Entrada senoidal
u4 = np.sin(m.pi / 2 * t)

# Matriz con las cuatro señales
u = np.column_stack((u1, u2, u3, u4))

# Nombres de los archivos
signals = [
    "step",
    "impulse",
    "ramp",
    "sinusoidal"
]


# ============================================================
# COMPONENTES DEL CIRCUITO RLC
# ============================================================

R = 100
L = 680E-6
C = 100E-6

num = [
    C * L * R**2 + L,
    R
]

den = [
    3 * C * L * R,
    5 * C * R**2 + L,
    2 * R
]

sys = ctrl.tf(num, den)

print("\n==========================================")
print("FUNCIÓN DE TRANSFERENCIA")
print("==========================================")

print(sys)


# ============================================================
# POLOS DEL SISTEMA
# ============================================================

polos = np.roots(den)

print("\n==========================================")
print("POLOS DEL SISTEMA")
print("==========================================")

print(
    f"Polos del sistema: "
    f"L1 = {polos[0]:.3e}, "
    f"L2 = {polos[1]:.3e}\n"
)


# ============================================================
# COMPONENTES DEL CONTROLADOR INTEGRAL
# ============================================================

kI = 39465549479.4982

Cr = 1E-6

Re = 1 / (Cr * kI)

numPID = [1]

denPID = [
    Re * Cr,
    0
]

PID = ctrl.tf(numPID, denPID)

print("==========================================")
print("CONTROLADOR INTEGRAL")
print("==========================================")

print(f"Ganancia kI: {kI}")
print(f"Resistencia Re: {Re} Ohms")
print(f"Capacitancia Cr: {Cr} Faradios")
print(f"Función de transferencia del controlador:")
print(PID)


# ============================================================
# SISTEMA DE CONTROL EN LAZO CERRADO
# ============================================================

sysPID = ctrl.feedback(
    ctrl.series(PID, sys),
    1,
    sign=-1
)

print("\n==========================================")
print("SISTEMA EN LAZO CERRADO")
print("==========================================")

print(
    f"Función de transferencia en lazo cerrado:"
)
print(sysPID)


# ============================================================
# COLORES
# ============================================================

clr1 = np.array([247, 214, 208]) / 255
clr2 = np.array([226, 180, 189]) / 255
clr3 = np.array([62, 88, 121]) / 255


# ============================================================
# FUNCIONES DEL SISTEMA EN LAZO ABIERTO
# Y LAZO CERRADO
# ============================================================

def openloop(t, sys, u):

    _, PAu = ctrl.forced_response(
        sys,
        t,
        u,
        x0
    )

    return PAu


def closedloop(t, sysPID, u):

    _, PIDu = ctrl.forced_response(
        sysPID,
        t,
        u,
        x0
    )

    return PIDu


# ============================================================
# CARPETA PARA GUARDAR LOS ARCHIVOS PDF
# ============================================================

carpeta = os.path.expanduser(
    "~/Documents/DisenoControladores"
)

# Crear carpeta si no existe
os.makedirs(
    carpeta,
    exist_ok=True
)

print("\n==========================================")
print("CARPETA DE GUARDADO")
print("==========================================")

print(carpeta)


# ============================================================
# CONFIGURACIÓN DE LAS GRÁFICAS
# ============================================================

plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']


# ============================================================
# RESPUESTAS: SIMULACIONES NUMÉRICAS
# ============================================================

for i in range(4):

    # Respuesta del sistema en lazo abierto
    PAu = openloop(
        t,
        sys,
        u[:, i]
    )

    # Respuesta del sistema en lazo cerrado
    PIDu = closedloop(
        t,
        sysPID,
        u[:, i]
    )

    # Crear figura
    fg = plt.figure(
        i + 1,
        figsize=(w, h)
    )

    # Señal de entrada
    plt.plot(
        t,
        u[:, i],
        '-',
        color=clr1,
        label='Ve(t)'
    )

    # Respuesta en lazo abierto
    plt.plot(
        t,
        PAu,
        '--',
        color=clr2,
        label='PA(t)'
    )

    # Respuesta en lazo cerrado
    plt.plot(
        t,
        PIDu,
        ':',
        linewidth=2.5,
        color=clr3,
        label='PID(t)'
    )

    # Configuración del eje X
    plt.xlim(0, 10)

    plt.xticks(
        np.arange(0, 11, 1)
    )

    # Configuración del eje Y
    if i == 0 or i == 1 or i == 2:

        plt.ylim(-0.1, 1.2)

        plt.yticks(
            np.arange(-0.1, 1.3, 0.1)
        )

    elif i == 3:

        plt.ylim(-1.2, 1.2)

        plt.yticks(
            np.arange(-1.2, 1.4, 0.2)
        )

    # Etiquetas de los ejes
    plt.xlabel(
        't [s]'
    )

    plt.ylabel(
        'Vi(t) [V]'
    )

    # Leyenda
    plt.legend(
        bbox_to_anchor=(0.5, -0.25),
        loc='center',
        ncol=3,
        frameon=False
    )

    # Cuadrícula
    plt.grid(
        True,
        alpha=0.3
    )

    # Ajustar automáticamente los espacios
    plt.tight_layout()


    # ========================================================
    # GUARDAR LA GRÁFICA
    # ========================================================

    nombre_archivo = signals[i] + '_python.pdf'

    ruta_archivo = os.path.join(
        carpeta,
        nombre_archivo
    )

    fg.savefig(
        ruta_archivo,
        bbox_inches='tight'
    )

    print(
        f"Gráfica guardada: {nombre_archivo}"
    )

    # Mostrar gráfica
    plt.show()

    # Cerrar la figura
    plt.close(fg)


# ============================================================
# FINAL
# ============================================================

print("\n==========================================")
print("SIMULACIÓN TERMINADA")
print("==========================================")

print("Las cuatro gráficas fueron guardadas correctamente.")

print("\nArchivos generados:")

print("1. step_python.pdf")
print("2. impulse_python.pdf")
print("3. ramp_python.pdf")
print("4. sinusoidal_python.pdf")

print("\nUbicación de los archivos:")
print(carpeta)
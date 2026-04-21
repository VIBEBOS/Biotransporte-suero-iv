"""
================================================================================
 Análisis del caudal en un sistema de administración de suero intravenoso
 por gravedad
--------------------------------------------------------------------------------
 Proyecto Final - Biotransporte (64-005)
 Universidad Latinoamericana de Ciencia y Tecnología (ULACIT)
 Ingeniería Biomédica - I Cuatrimestre 2026
--------------------------------------------------------------------------------
 Autores:
   - Luis Fernández Zamora
   - Kendall Hernández Lara
   - Angelo Huertas Rosales
   - Jose Ramirez Villalobos
--------------------------------------------------------------------------------
 Descripción:
   Este script ejecuta los cálculos del modelo matemático del sistema de
   infusión intravenosa por gravedad, basado en la ecuación unificada de
   Hagen-Poiseuille con presión hidrostática:

                       π · r⁴ · ρ · g · h
                Q  =  ─────────────────────
                            8 · μ · L

   Genera:
     1. Cálculo de la presión hidrostática (ΔP).
     2. Cálculo del caudal volumétrico (Q).
     3. Validación del régimen de flujo mediante el número de Reynolds.
     4. Análisis de resistencias hidráulicas (tubo vs. pinza reguladora).
     5. Análisis de sensibilidad: Q vs h, Q vs r, Q vs L.
     6. Cuatro gráficas en formato PNG.

 Requisitos:
   - Python 3.8+
   - matplotlib
   - numpy (opcional)

 Uso:
   $ python analisis_caudal_iv.py
================================================================================
"""

import math
import matplotlib.pyplot as plt


# ==============================================================================
# 1. PARÁMETROS DEL MODELO
# ==============================================================================
# Propiedades del fluido (suero fisiológico 0.9% NaCl)
RHO = 1000.0          # Densidad del fluido [kg/m³]
MU  = 1.0e-3          # Viscosidad dinámica [Pa·s]

# Constantes físicas
G = 9.81              # Aceleración gravitacional [m/s²]

# Geometría del sistema
H     = 1.0           # Diferencia de altura bolsa-vena [m]
L     = 1.5           # Longitud total del conducto [m]
R_EF  = 2.838e-4      # Radio efectivo impuesto por la pinza reguladora [m]
R_TUBO = 1.5e-3       # Radio físico del tubo de perfusión [m]

# Parámetros clínicos de referencia
Q_CLINICO_ML_H = 60.0       # Caudal clínico típico [mL/h]
FACTOR_GOTEO   = 20.0       # Factor de goteo estándar [gotas/mL]


# ==============================================================================
# 2. FUNCIONES DEL MODELO
# ==============================================================================

def presion_hidrostatica(rho, g, h):
    """
    Calcula la presión hidrostática generada por una columna de fluido.

        ΔP = ρ · g · h

    Parámetros
    ----------
    rho : float   Densidad del fluido [kg/m³]
    g   : float   Aceleración gravitacional [m/s²]
    h   : float   Altura de la columna de fluido [m]

    Retorna
    -------
    float   Presión hidrostática [Pa]
    """
    return rho * g * h


def caudal_poiseuille(r, delta_P, mu, L):
    """
    Calcula el caudal volumétrico mediante la ecuación de Hagen-Poiseuille
    para flujo laminar de un fluido newtoniano en un conducto cilíndrico.

        Q = (π · r⁴ · ΔP) / (8 · μ · L)

    Parámetros
    ----------
    r       : float   Radio interno del conducto [m]
    delta_P : float   Diferencia de presión entre los extremos [Pa]
    mu      : float   Viscosidad dinámica del fluido [Pa·s]
    L       : float   Longitud del conducto [m]

    Retorna
    -------
    float   Caudal volumétrico [m³/s]
    """
    return (math.pi * r**4 * delta_P) / (8.0 * mu * L)


def caudal_modelo_unificado(r, rho, g, h, mu, L):
    """
    Modelo matemático final del sistema - ecuación unificada:

                π · r⁴ · ρ · g · h
        Q  =  ─────────────────────
                     8 · μ · L

    Combina la estática de fluidos (ΔP = ρgh) con la ecuación de
    Hagen-Poiseuille en una sola expresión.

    Retorna
    -------
    float   Caudal volumétrico [m³/s]
    """
    return (math.pi * r**4 * rho * g * h) / (8.0 * mu * L)


def numero_reynolds(rho, V, D, mu):
    """
    Calcula el número de Reynolds para evaluar el régimen de flujo.

        Re = ρ · V · D / μ

    - Re < 2000    →  Flujo laminar
    - Re > 4000    →  Flujo turbulento
    - 2000 < Re < 4000  →  Zona de transición

    Retorna
    -------
    float   Número de Reynolds [adimensional]
    """
    return (rho * V * D) / mu


def resistencia_hidraulica(mu, L, r):
    """
    Calcula la resistencia hidráulica de un conducto cilíndrico bajo el
    modelo de Hagen-Poiseuille.

        R = (8 · μ · L) / (π · r⁴)

    Retorna
    -------
    float   Resistencia hidráulica [Pa·s/m³]
    """
    return (8.0 * mu * L) / (math.pi * r**4)


def mL_por_hora(Q_m3_s):
    """Convierte un caudal de m³/s a mL/h."""
    return Q_m3_s * 1e6 * 3600.0


def gotas_por_minuto(Q_mL_h, factor=FACTOR_GOTEO):
    """Convierte un caudal en mL/h al ritmo de goteo clínico estándar."""
    return (Q_mL_h / 60.0) * factor


# ==============================================================================
# 3. EJECUCIÓN PRINCIPAL - CÁLCULOS BASE
# ==============================================================================

def calculos_base():
    """Ejecuta los cálculos principales del modelo en el punto nominal."""

    print("=" * 78)
    print(" CÁLCULOS DEL MODELO - PUNTO DE OPERACIÓN NOMINAL")
    print("=" * 78)

    # -------- 1. Presión hidrostática --------
    delta_P = presion_hidrostatica(RHO, G, H)
    delta_P_mmHg = delta_P / 133.322

    print("\n[1] Presión hidrostática")
    print(f"    ΔP = ρ · g · h = {RHO} × {G} × {H}")
    print(f"    ΔP = {delta_P:.2f} Pa")
    print(f"    ΔP = {delta_P_mmHg:.2f} mmHg")

    # -------- 2. Caudal volumétrico --------
    Q = caudal_modelo_unificado(R_EF, RHO, G, H, MU, L)
    Q_mL_h   = mL_por_hora(Q)
    Q_mL_min = Q * 1e6 * 60
    gotas_min = gotas_por_minuto(Q_mL_h)

    print("\n[2] Caudal volumétrico (modelo unificado)")
    print(f"    Q = (π × r⁴ × ρgh) / (8μL)")
    print(f"    r_efectivo = {R_EF*1000:.4f} mm")
    print(f"    Q = {Q:.4e} m³/s")
    print(f"    Q = {Q_mL_h:.2f} mL/h")
    print(f"    Q = {Q_mL_min:.4f} mL/min")
    print(f"    Ritmo de goteo = {gotas_min:.1f} gotas/min")

    # -------- 3. Número de Reynolds --------
    D_ef = 2 * R_EF
    A_ef = math.pi * R_EF**2
    V_media = Q / A_ef
    Re = numero_reynolds(RHO, V_media, D_ef, MU)

    print("\n[3] Validación del régimen de flujo")
    print(f"    A_efectiva = {A_ef:.4e} m²")
    print(f"    V_media = Q/A = {V_media:.4f} m/s")
    print(f"    Re = ρVD/μ = {Re:.2f}")
    print(f"    → Re << 2000 : FLUJO LAMINAR CONFIRMADO ✓")

    # -------- 4. Resistencias hidráulicas --------
    R_total = resistencia_hidraulica(MU, L, R_EF)
    R_tubo  = resistencia_hidraulica(MU, L, R_TUBO)
    R_pinza = R_total - R_tubo

    print("\n[4] Análisis de resistencias hidráulicas")
    print(f"    R_tubo  (r=1.5 mm)    = {R_tubo:.4e} Pa·s/m³  ({R_tubo/R_total*100:.2f} %)")
    print(f"    R_pinza (r_ef=0.284 mm) = {R_pinza:.4e} Pa·s/m³  ({R_pinza/R_total*100:.2f} %)")
    print(f"    R_total                 = {R_total:.4e} Pa·s/m³  (100.00 %)")
    print(f"    → La pinza aporta el {R_pinza/R_total*100:.2f}% de la resistencia total.")

    return {
        "delta_P": delta_P, "Q": Q, "Q_mL_h": Q_mL_h, "Re": Re,
        "R_total": R_total, "R_tubo": R_tubo, "R_pinza": R_pinza
    }


# ==============================================================================
# 4. ANÁLISIS DE SENSIBILIDAD
# ==============================================================================

def sensibilidad_altura():
    """Analiza cómo varía Q con h (manteniendo r, L, μ, ρ constantes)."""
    print("\n" + "=" * 78)
    print(" ANÁLISIS DE SENSIBILIDAD: Q vs h (altura de la bolsa)")
    print("=" * 78)
    print(f"{'h (m)':<10} {'ΔP (Pa)':<14} {'Q (m³/s)':<16} {'Q (mL/h)':<12} {'Gotas/min':<10}")
    print("-" * 68)

    alturas = [0.50, 0.75, 1.00, 1.25, 1.50, 2.00]
    datos = []
    for h in alturas:
        dP = presion_hidrostatica(RHO, G, h)
        Q  = caudal_poiseuille(R_EF, dP, MU, L)
        Q_mLh = mL_por_hora(Q)
        gotas = gotas_por_minuto(Q_mLh)
        datos.append((h, dP, Q, Q_mLh, gotas))
        print(f"{h:<10.2f} {dP:<14.2f} {Q:<16.4e} {Q_mLh:<12.2f} {gotas:<10.1f}")
    return datos


def sensibilidad_radio():
    """Analiza cómo varía Q con el radio efectivo (h, L, μ, ρ constantes)."""
    print("\n" + "=" * 78)
    print(" ANÁLISIS DE SENSIBILIDAD: Q vs r (radio efectivo)")
    print("=" * 78)
    print(f"{'r (mm)':<10} {'r (m)':<14} {'Q (m³/s)':<16} {'Q (mL/h)':<12}")
    print("-" * 58)

    radios_mm = [0.150, 0.200, 0.250, 0.284, 0.300, 0.350, 0.400]
    dP = presion_hidrostatica(RHO, G, H)
    datos = []
    for rm in radios_mm:
        r = rm / 1000
        Q = caudal_poiseuille(r, dP, MU, L)
        Q_mLh = mL_por_hora(Q)
        datos.append((rm, r, Q, Q_mLh))
        print(f"{rm:<10.3f} {r:<14.5f} {Q:<16.4e} {Q_mLh:<12.4f}")
    return datos


def sensibilidad_longitud():
    """Analiza cómo varía Q con la longitud del tubo (h, r, μ, ρ constantes)."""
    print("\n" + "=" * 78)
    print(" ANÁLISIS DE SENSIBILIDAD: Q vs L (longitud del tubo)")
    print("=" * 78)
    print(f"{'L (m)':<10} {'Q (m³/s)':<16} {'Q (mL/h)':<12}")
    print("-" * 44)

    longitudes = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    dP = presion_hidrostatica(RHO, G, H)
    datos = []
    for Lv in longitudes:
        Q = caudal_poiseuille(R_EF, dP, MU, Lv)
        Q_mLh = mL_por_hora(Q)
        datos.append((Lv, Q, Q_mLh))
        print(f"{Lv:<10.2f} {Q:<16.4e} {Q_mLh:<12.4f}")
    return datos


# ==============================================================================
# 5. GENERACIÓN DE GRÁFICAS
# ==============================================================================

# Paleta consistente con el documento del proyecto
COLOR_MAIN = "#2E4057"
COLOR_ACC  = "#1B998B"
COLOR_WARN = "#E84855"
COLOR_GRID = "#E8EAF0"


def configurar_estilo_grafica():
    """Aplica el estilo visual consistente a todas las gráficas."""
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 10,
        'axes.titlesize': 11,
        'axes.labelsize': 10,
        'axes.titleweight': 'bold',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'figure.dpi': 180,
    })


def graficar_sensibilidad(x_vals, y_vals, x_label, y_label, titulo,
                          x_nominal, y_nominal, nombre_nominal,
                          filename, nota, x_lim=None, y_lim=None,
                          offset=(0.1, -10)):
    """Función genérica para graficar una curva de sensibilidad."""
    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.plot(x_vals, y_vals, color=COLOR_MAIN, linewidth=2.2, marker='o',
            markersize=6, markerfacecolor='white', markeredgewidth=2,
            markeredgecolor=COLOR_MAIN, zorder=3)

    ax.axvline(x=x_nominal, color=COLOR_ACC, linestyle='--',
               linewidth=1.4, alpha=0.8, label=f'{nombre_nominal}')
    ax.axhline(y=y_nominal, color=COLOR_WARN, linestyle='--',
               linewidth=1.4, alpha=0.8, label='Q objetivo clínico (60 mL/h)')
    ax.scatter([x_nominal], [y_nominal], color=COLOR_WARN, s=80, zorder=5)

    ax.annotate(f'Punto de\noperación',
                xy=(x_nominal, y_nominal),
                xytext=(x_nominal + offset[0], y_nominal + offset[1]),
                fontsize=8.5, color=COLOR_WARN,
                arrowprops=dict(arrowstyle='->', color=COLOR_WARN, lw=1.3))

    ax.set_xlabel(x_label, labelpad=8)
    ax.set_ylabel(y_label, labelpad=8)
    ax.set_title(titulo)
    if x_lim: ax.set_xlim(x_lim)
    if y_lim: ax.set_ylim(y_lim)
    ax.grid(True, color=COLOR_GRID, linewidth=0.8, zorder=0)
    ax.legend(fontsize=8.5, framealpha=0.9)
    ax.tick_params(axis='both', which='major', labelsize=9)

    fig.text(0.12, 0.01, f'Nota. {nota}',
             fontsize=7.5, color='#555555', style='italic')
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(filename, bbox_inches='tight', dpi=180)
    plt.close()
    print(f"   ✓ Gráfica generada: {filename}")


def graficar_resistencias(R_tubo, R_pinza, R_total):
    """Grafica la distribución porcentual de las resistencias hidráulicas."""
    fig, ax = plt.subplots(figsize=(6, 4))

    labels = ['R_tubo\n(tubo completo)', 'R_pinza\n(regulador)', 'R_total\n(sistema)']
    values = [R_tubo / R_total * 100, R_pinza / R_total * 100, 100]
    colors = [COLOR_ACC, COLOR_WARN, COLOR_MAIN]

    bars = ax.bar(labels, values, color=colors, width=0.5,
                  edgecolor='white', linewidth=1.2)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{val:.2f}%', ha='center', va='bottom',
                fontsize=9.5, fontweight='bold')

    ax.set_ylabel('Porcentaje de resistencia total (%)', labelpad=8)
    ax.set_title('Distribución de la resistencia hidráulica en el sistema de infusión')
    ax.set_ylim(0, 115)
    ax.grid(True, axis='y', color=COLOR_GRID, linewidth=0.8, zorder=0)
    ax.tick_params(axis='both', which='major', labelsize=9)
    ax.set_axisbelow(True)

    fig.text(0.12, 0.01,
             'Nota. La pinza reguladora aporta el 99.87% de la resistencia hidráulica total del sistema.',
             fontsize=7.5, color='#555555', style='italic')
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig("fig_resistencias.png", bbox_inches='tight', dpi=180)
    plt.close()
    print(f"   ✓ Gráfica generada: fig_resistencias.png")


def generar_todas_las_graficas(sens_h, sens_r, sens_L, base):
    """Ejecuta la generación de las 4 figuras del análisis."""
    print("\n" + "=" * 78)
    print(" GENERACIÓN DE GRÁFICAS")
    print("=" * 78)
    configurar_estilo_grafica()

    # Figura 2: Q vs h
    graficar_sensibilidad(
        x_vals=[x[0] for x in sens_h],
        y_vals=[x[3] for x in sens_h],
        x_label='Diferencia de altura h (m)',
        y_label='Caudal volumétrico Q (mL/h)',
        titulo='Figura 2. Caudal volumétrico en función de la altura de la bolsa de suero',
        x_nominal=1.0, y_nominal=60.0,
        nombre_nominal='Altura nominal (h = 1 m)',
        filename="fig_Q_vs_h.png",
        nota='Relación lineal Q ∝ h, con r_ef = 0.284 mm, L = 1.5 m, μ = 1×10⁻³ Pa·s, ρ = 1000 kg/m³.',
        x_lim=(0.35, 2.15), y_lim=(0, 140), offset=(0.25, -10)
    )

    # Figura 3: Q vs r
    graficar_sensibilidad(
        x_vals=[x[0] for x in sens_r],
        y_vals=[x[3] for x in sens_r],
        x_label='Radio efectivo r (mm)',
        y_label='Caudal volumétrico Q (mL/h)',
        titulo='Figura 3. Caudal volumétrico en función del radio efectivo del conducto (Q ∝ r⁴)',
        x_nominal=0.284, y_nominal=60.15,
        nombre_nominal='r efectivo nominal (0.284 mm)',
        filename="fig_Q_vs_r.png",
        nota='Relación Q ∝ r⁴. Pequeñas variaciones en r producen cambios muy amplificados en Q. h = 1 m, L = 1.5 m.',
        x_lim=(0.12, 0.43), y_lim=(0, 260), offset=(0.03, 40)
    )

    # Figura 4: Q vs L
    graficar_sensibilidad(
        x_vals=[x[0] for x in sens_L],
        y_vals=[x[2] for x in sens_L],
        x_label='Longitud del tubo L (m)',
        y_label='Caudal volumétrico Q (mL/h)',
        titulo='Figura 4. Caudal volumétrico en función de la longitud del tubo de infusión',
        x_nominal=1.5, y_nominal=60.0,
        nombre_nominal='Longitud nominal (L = 1.5 m)',
        filename="fig_Q_vs_L.png",
        nota='Relación inversamente proporcional Q ∝ 1/L. h = 1 m, r_ef = 0.284 mm, μ = 1×10⁻³ Pa·s.',
        x_lim=(0.3, 3.2), y_lim=(0, 200), offset=(0.5, 20)
    )

    # Figura 5: Resistencias hidráulicas
    graficar_resistencias(base["R_tubo"], base["R_pinza"], base["R_total"])


# ==============================================================================
# 6. PROGRAMA PRINCIPAL
# ==============================================================================

def main():
    """Ejecuta el análisis completo del modelo."""

    print("\n" + "#" * 78)
    print("#  ANÁLISIS DEL CAUDAL EN UN SISTEMA DE INFUSIÓN IV POR GRAVEDAD")
    print("#  Proyecto Final - Biotransporte (64-005) - ULACIT")
    print("#" * 78)

    # Cálculos base en el punto nominal
    base = calculos_base()

    # Análisis de sensibilidad
    sens_h = sensibilidad_altura()
    sens_r = sensibilidad_radio()
    sens_L = sensibilidad_longitud()

    # Generación de gráficas
    generar_todas_las_graficas(sens_h, sens_r, sens_L, base)

    print("\n" + "=" * 78)
    print(" ANÁLISIS COMPLETADO CORRECTAMENTE ✓")
    print("=" * 78)
    print(" Archivos generados:")
    print("   - fig_Q_vs_h.png")
    print("   - fig_Q_vs_r.png")
    print("   - fig_Q_vs_L.png")
    print("   - fig_resistencias.png")
    print()


if __name__ == "__main__":
    main()

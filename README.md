# Biotransporte-suero-iv

Análisis del caudal en un sistema de administración de suero intravenoso por gravedad.  
Proyecto final del curso **Biotransporte (64-005)**, Ingeniería Biomédica, ULACIT.  
Modelo matemático basado en **Hagen-Poiseuille** con presión hidrostática, implementado en Python 3.

---

## Autores

- Luis Fernández Zamora
- Kendall Hernández Lara
- Angelo Huertas Rosales
- Jose Ramírez Villalobos

**Profesor:** Jorge Sánchez Castro  
**Universidad:** Universidad Latinoamericana de Ciencia y Tecnología (ULACIT)  
**Cuatrimestre:** I Cuatrimestre 2026

---

## Descripción

Este script implementa el modelo matemático unificado del sistema de infusión intravenosa por gravedad, combinando la ecuación de la presión hidrostática (ΔP = ρgh) con la ecuación de Hagen-Poiseuille para flujo laminar en conductos cilíndricos:

π · r⁴ · ρ · g · h

Q  =  ─────────────────────
8 · μ · L

El programa ejecuta:

1. Cálculo de la presión hidrostática (ΔP)
2. Cálculo del caudal volumétrico (Q)
3. Validación del régimen de flujo mediante el número de Reynolds
4. Análisis de resistencias hidráulicas (tubo físico vs. pinza reguladora)
5. Análisis de sensibilidad: Q vs h, Q vs r, Q vs L
6. Generación de 4 gráficas en formato PNG

---

## Requisitos

- **Python 3.8** o superior
- **matplotlib** (librería externa)

> La librería `math` viene incluida en Python por defecto y no requiere instalación.

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/VIBEBOS/Biotransporte-suero-iv.git
cd Biotransporte-suero-iv
```

Instalar la dependencia necesaria:

```bash
pip install matplotlib
```

---

## Uso

Ejecutar el script desde la terminal:

```bash
python analisis_caudal_iv.py
```

El script imprimirá en consola todos los cálculos paso a paso y generará los siguientes archivos:

- `fig_Q_vs_h.png` — Caudal vs. altura de la bolsa
- `fig_Q_vs_r.png` — Caudal vs. radio efectivo del conducto
- `fig_Q_vs_L.png` — Caudal vs. longitud del tubo
- `fig_resistencias.png` — Distribución de resistencias hidráulicas

---

## Parámetros del modelo

| Parámetro | Símbolo | Valor |
|---|---|---|
| Densidad del fluido | ρ | 1000 kg/m³ |
| Viscosidad dinámica | μ | 1.0 × 10⁻³ Pa·s |
| Aceleración gravitacional | g | 9.81 m/s² |
| Altura bolsa–vena | h | 1.0 m |
| Longitud del tubo | L | 1.5 m |
| Radio efectivo (pinza) | r_ef | 2.838 × 10⁻⁴ m |
| Radio físico del tubo | r_tubo | 1.5 × 10⁻³ m |

---

## Resultado esperado

Bajo las condiciones nominales del modelo:

- **ΔP** = 9 810 Pa (73.58 mmHg)
- **Q** = 60 mL/h (1.666 × 10⁻⁸ m³/s)
- **Re** = 37.37 → Flujo laminar confirmado
- La pinza reguladora concentra el **99.87 %** de la resistencia hidráulica total

---

## Licencia

Proyecto académico desarrollado con fines educativos.

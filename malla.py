# =============================================================================
# malla.py — Datos de la malla curricular
# Ingeniería de Sistemas y Computación — UTP
# =============================================================================
# ESTRUCTURA DE CADA ASIGNATURA:
#   "CODIGO": {
#       "nombre":    nombre legible,
#       "creditos":  número de créditos,
#       "semestre":  semestre sugerido por el plan oficial,
#       "pre":       lista de códigos que son PRERREQUISITO,
#       "co":        lista de códigos que son CORREQUISITO,
#   }
#
# NOTA SOBRE PRERREQUISITOS:
#   Los prerrequisitos se infieren de la secuencia lógica del plan.
#   Ajusta la lista "pre" con los datos exactos del sistema académico UTP
#   (https://app4.utp.edu.co/MatAcad/...) cuando tengas acceso.
# =============================================================================

ASIGNATURAS = {
    # ── SEMESTRE 1 ────────────────────────────────────────────────────────────
    "BA170": {
        "nombre":   "Humanidades I",
        "creditos": 2,
        "semestre": 1,
        "pre": [],
        "co":  [],
    },
    "BU101": {
        "nombre":   "Deportes I",
        "creditos": 1,
        "semestre": 1,
        "pre": [],
        "co":  [],
    },
    "CB1B3": {
        "nombre":   "Matemáticas Fundamentales",
        "creditos": 3,
        "semestre": 1,
        "pre": [],
        "co":  [],
    },
    "IS142": {
        "nombre":   "Desarrollo del Pensamiento Lógico",
        "creditos": 2,
        "semestre": 1,
        "pre": [],
        "co":  [],
    },

    # ── SEMESTRE 2 ────────────────────────────────────────────────────────────
    "IS105": {
        "nombre":   "Programación I",
        "creditos": 5,
        "semestre": 2,
        "pre": ["IS142"],
        "co":  [],
    },
    "CB2A3": {
        "nombre":   "Cálculo Diferencial",
        "creditos": 3,
        "semestre": 2,
        "pre": ["CB1B3"],
        "co":  [],
    },
    "CB234": {
        "nombre":   "Física I",
        "creditos": 4,
        "semestre": 2,
        "pre": ["CB1B3"],
        "co":  ["CB242"],
    },
    "CB242": {
        "nombre":   "Laboratorio de Física I",
        "creditos": 2,
        "semestre": 2,
        "pre": ["CB1B3"],
        "co":  ["CB234"],
    },
    "IS193": {
        "nombre":   "Introducción a la Informática",
        "creditos": 3,
        "semestre": 2,
        "pre": [],
        "co":  [],
    },
    "BA372": {
        "nombre":   "Humanidades II",
        "creditos": 2,
        "semestre": 2,
        "pre": ["BA170"],
        "co":  [],
    },

    # ── SEMESTRE 3 ────────────────────────────────────────────────────────────
    "CB223": {
        "nombre":   "Álgebra Lineal",
        "creditos": 3,
        "semestre": 3,
        "pre": ["CB1B3"],
        "co":  [],
    },
    "CB334": {
        "nombre":   "Física II",
        "creditos": 4,
        "semestre": 3,
        "pre": ["CB234"],
        "co":  ["CB342"],
    },
    "CB342": {
        "nombre":   "Laboratorio de Física II",
        "creditos": 2,
        "semestre": 3,
        "pre": ["CB242"],
        "co":  ["CB334"],
    },
    "IS284": {
        "nombre":   "Programación II",
        "creditos": 4,
        "semestre": 3,
        "pre": ["IS105"],
        "co":  [],
    },
    "CB3A4": {
        "nombre":   "Cálculo Integral",
        "creditos": 4,
        "semestre": 3,
        "pre": ["CB2A3"],
        "co":  [],
    },

    # ── SEMESTRE 4 ────────────────────────────────────────────────────────────
    "CB4A4": {
        "nombre":   "Cálculo Multivariado",
        "creditos": 4,
        "semestre": 4,
        "pre": ["CB3A4"],
        "co":  [],
    },
    "IS304": {
        "nombre":   "Estructura de Datos",
        "creditos": 4,
        "semestre": 4,
        "pre": ["IS284"],
        "co":  [],
    },
    "IS474": {
        "nombre":   "Fundamentos de Electrónica",
        "creditos": 3,
        "semestre": 4,
        "pre": ["CB334"],
        "co":  ["IS543"],
    },
    "IS482": {
        "nombre":   "Teoría de Sistemas",
        "creditos": 2,
        "semestre": 4,
        "pre": ["IS193"],
        "co":  [],
    },
    "IS543": {
        "nombre":   "Laboratorio de Electrónica",
        "creditos": 2,
        "semestre": 4,
        "pre": ["CB342"],
        "co":  ["IS474"],
    },

    # ── SEMESTRE 5 ────────────────────────────────────────────────────────────
    "CB4A3": {
        "nombre":   "Ecuaciones Diferenciales Ordinarias",
        "creditos": 3,
        "semestre": 5,
        "pre": ["CB4A4"],
        "co":  [],
    },
    "IS323": {
        "nombre":   "Lógica",
        "creditos": 3,
        "semestre": 5,
        "pre": ["IS142"],
        "co":  [],
    },
    "IS453": {
        "nombre":   "Programación III",
        "creditos": 3,
        "semestre": 5,
        "pre": ["IS304"],
        "co":  [],
    },

    # ── SEMESTRE 6 ────────────────────────────────────────────────────────────
    "CB434": {
        "nombre":   "Física III",
        "creditos": 4,
        "semestre": 6,
        "pre": ["CB334", "CB4A4"],
        "co":  ["CB442"],
    },
    "CB442": {
        "nombre":   "Laboratorio de Física III",
        "creditos": 2,
        "semestre": 6,
        "pre": ["CB342"],
        "co":  ["CB434"],
    },
    "IS405": {
        "nombre":   "Gramáticas y Lenguajes Formales",
        "creditos": 4,
        "semestre": 6,
        "pre": ["IS323", "IS453"],
        "co":  [],
    },
    "IS503": {
        "nombre":   "Administración de Empresas",
        "creditos": 3,
        "semestre": 6,
        "pre": [],
        "co":  [],
    },
    "IS634": {
        "nombre":   "Electrónica Digital",
        "creditos": 3,
        "semestre": 6,
        "pre": ["IS474"],
        "co":  ["IS773"],
    },
    "IS773": {
        "nombre":   "Laboratorio de Electrónica Digital",
        "creditos": 2,
        "semestre": 6,
        "pre": ["IS543"],
        "co":  ["IS634"],
    },
    "IS512": {
        "nombre":   "Estadística",
        "creditos": 2,
        "semestre": 6,
        "pre": ["CB3A4"],
        "co":  [],
    },
    "IS553": {
        "nombre":   "Programación IV",
        "creditos": 3,
        "semestre": 6,
        "pre": ["IS453"],
        "co":  [],
    },

    # ── SEMESTRE 7 ────────────────────────────────────────────────────────────
    "IS184": {
        "nombre":   "Técnicas de la Comunicación",
        "creditos": 2,
        "semestre": 7,
        "pre": [],
        "co":  [],
    },
    "IS614": {
        "nombre":   "Arquitectura de Computadores",
        "creditos": 4,
        "semestre": 7,
        "pre": ["IS634"],
        "co":  [],
    },
    "IS623": {
        "nombre":   "Computación Gráfica",
        "creditos": 3,
        "semestre": 7,
        "pre": ["IS553", "CB223"],
        "co":  [],
    },
    "IS644": {
        "nombre":   "Base de Datos I",
        "creditos": 4,
        "semestre": 7,
        "pre": ["IS304"],
        "co":  [],
    },
    "IS692": {
        "nombre":   "Estadística Especial",
        "creditos": 2,
        "semestre": 7,
        "pre": ["IS512"],
        "co":  [],
    },

    # ── SEMESTRE 8 ────────────────────────────────────────────────────────────
    "IS653": {
        "nombre":   "Investigación de Operaciones",
        "creditos": 3,
        "semestre": 8,
        "pre": ["CB4A3", "IS512"],
        "co":  [],
    },
    "IS714": {
        "nombre":   "Ingeniería de Software I",
        "creditos": 4,
        "semestre": 8,
        "pre": ["IS553"],
        "co":  [],
    },
    "IS723": {
        "nombre":   "Comunicaciones I",
        "creditos": 3,
        "semestre": 8,
        "pre": ["CB4A3", "IS614"],
        "co":  [],
    },
    "IS734": {
        "nombre":   "Sistemas Operativos I",
        "creditos": 4,
        "semestre": 8,
        "pre": ["IS614"],
        "co":  [],
    },

    # ── SEMESTRE 9 ────────────────────────────────────────────────────────────
    "IS753": {
        "nombre":   "Compiladores",
        "creditos": 3,
        "semestre": 9,
        "pre": ["IS405", "IS734"],
        "co":  [],
    },
    "IS784": {
        "nombre":   "Inteligencia Artificial",
        "creditos": 3,
        "semestre": 9,
        "pre": ["IS692", "IS453"],
        "co":  [],
    },
    "IS884": {
        "nombre":   "Ingeniería de Software II",
        "creditos": 4,
        "semestre": 9,
        "pre": ["IS714"],
        "co":  [],
    },
    "IS842": {
        "nombre":   "Legislación, Ética y Contratación",
        "creditos": 2,
        "semestre": 9,
        "pre": [],
        "co":  [],
    },
    "IS053": {
        "nombre":   "Gerencia de Proyectos",
        "creditos": 3,
        "semestre": 9,
        "pre": ["IS503"],
        "co":  [],
    },

    # ── SEMESTRE 10 ───────────────────────────────────────────────────────────
    "IS823": {
        "nombre":   "Comunicaciones II",
        "creditos": 3,
        "semestre": 10,
        "pre": ["IS723"],
        "co":  [],
    },
    "IS845": {
        "nombre":   "Computación Blanda",
        "creditos": 4,
        "semestre": 10,
        "pre": ["IS784"],
        "co":  [],
    },
    "IS873": {
        "nombre":   "Laboratorio del Software",
        "creditos": 3,
        "semestre": 10,
        "pre": ["IS884"],
        "co":  [],
    },
    "IS893": {
        "nombre":   "Sistemas Distribuidos",
        "creditos": 3,
        "semestre": 10,
        "pre": ["IS734", "IS723"],
        "co":  [],
    },
    "IS953": {
        "nombre":   "Administración de Proyectos de Software",
        "creditos": 3,
        "semestre": 10,
        "pre": ["IS053"],
        "co":  [],
    },

    # ── SEMESTRE 11 ───────────────────────────────────────────────────────────
    "IS924": {
        "nombre":   "Arquitectura Cliente-Servidor",
        "creditos": 4,
        "semestre": 11,
        "pre": ["IS893"],
        "co":  [],
    },
    "IS962": {
        "nombre":   "Proyecto de Grado I",
        "creditos": 2,
        "semestre": 11,
        "pre": ["IS884", "IS953"],
        "co":  [],
    },
    "IS023": {
        "nombre":   "Auditoría de Sistemas",
        "creditos": 3,
        "semestre": 11,
        "pre": ["IS644"],
        "co":  [],
    },
    "IS9A0": {
        "nombre":   "Electiva A1",
        "creditos": 6,
        "semestre": 11,
        "pre": [],
        "co":  [],
    },

    # ── SEMESTRE 12 ───────────────────────────────────────────────────────────
    "IS031": {
        "nombre":   "Constitución Política",
        "creditos": 1,
        "semestre": 12,
        "pre": [],
        "co":  [],
    },
    "IS066": {
        "nombre":   "Proyecto de Grado II",
        "creditos": 6,
        "semestre": 12,
        "pre": ["IS962"],
        "co":  [],
    },
    "IS024": {
        "nombre":   "Emprendimiento",
        "creditos": 3,
        "semestre": 12,
        "pre": ["IS503"],
        "co":  [],
    },
    "IS0A0": {
        "nombre":   "Electiva A2",
        "creditos": 6,
        "semestre": 12,
        "pre": ["IS9A0"],
        "co":  [],
    },
}

# Parámetros del problema
MAX_SEMESTRES   = 12
MIN_CREDITOS    = 9   # mínimo de créditos por semestre (evitar semestres vacíos)
MAX_CREDITOS    = 21  # máximo de créditos por semestre según reglamento UTP

CODIGOS = list(ASIGNATURAS.keys())
N       = len(CODIGOS)
IDX     = {c: i for i, c in enumerate(CODIGOS)}   # código → índice numérico


def resumen():
    total = sum(a["creditos"] for a in ASIGNATURAS.values())
    print(f"Total asignaturas : {N}")
    print(f"Total créditos    : {total}")
    por_sem = {}
    for a in ASIGNATURAS.values():
        s = a["semestre"]
        por_sem[s] = por_sem.get(s, 0) + a["creditos"]
    for s in sorted(por_sem):
        print(f"  Semestre {s:2d}: {por_sem[s]:3d} créditos")


if __name__ == "__main__":
    resumen()

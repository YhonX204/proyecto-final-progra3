#!/usr/bin/env python3
"""
main.py — Ejecutor principal del proyecto
Proyecto Final Programación III — UTP
"""

from malla import resumen
from parte1_restricciones import analizar_malla, generar_dzn, resolver_parte1
from parte2_agentes import comparar_agentes


def main():
    print("\n" + "╔" + "═"*61 + "╗")
    print("║   PROYECTO FINAL — PROGRAMACIÓN III                        ║")
    print("║   Malla Curricular Ingeniería de Sistemas — UTP            ║")
    print("╚" + "═"*61 + "╝\n")

    print("── RESUMEN DE LA MALLA ──────────────────────────────────────")
    resumen()

    analizar_malla()
    generar_dzn("datos.dzn")

    print("\n")
    resolver_parte1()

    print("\n\n")
    comparar_agentes()

    print("\n\n" + "═"*63)
    print("  Ejecución finalizada.")
    print("  Para ejecutar con MiniZinc:")
    print("  → minizinc --solver Gecode plan_estudios.mzn datos.dzn")
    print("═"*63 + "\n")


if __name__ == "__main__":
    main()

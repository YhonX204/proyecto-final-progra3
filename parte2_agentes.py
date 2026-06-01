#!/usr/bin/env python3
"""
parte2_agentes.py — Parte II: Sistema de agentes
Proyecto Final Programación III — UTP

Implementa:
  1. Agente "Alumno Esforzado"  — prioriza materias con más créditos
  2. Agente "Alumno Ocupado"   — toma materias hasta 15 créditos sin orden
  3. Sociedad de Agentes       — dos sub-agentes negocian cada semestre
"""

from malla import ASIGNATURAS, CODIGOS, MAX_SEMESTRES, MAX_CREDITOS


# ─── Utilidades compartidas ───────────────────────────────────────────────────

def materias_disponibles(cursadas: set, en_curso: set = None) -> list:
    """
    Retorna códigos de materias que el estudiante puede cursar:
    - Todos sus prerrequisitos ya fueron cursados.
    - No ha sido cursada aún.
    - Si tiene correquisito, ese correquisito también debe estar disponible
      (o ya cursado).
    """
    if en_curso is None:
        en_curso = set()
    disponibles = []
    for cod in CODIGOS:
        if cod in cursadas or cod in en_curso:
            continue
        datos = ASIGNATURAS[cod]
        # Prerrequisitos cumplidos
        if not all(p in cursadas for p in datos["pre"]):
            continue
        disponibles.append(cod)
    return disponibles


def verificar_corequisitos(seleccion: list) -> bool:
    """Verifica que los correquisitos de las materias seleccionadas estén
    todos dentro de la misma selección."""
    seleccion_set = set(seleccion)
    for cod in seleccion:
        for co in ASIGNATURAS[cod]["co"]:
            if co not in seleccion_set and co not in {
                c for c in CODIGOS if ASIGNATURAS[c]["semestre"] < ASIGNATURAS[cod]["semestre"]
            }:
                return False
    return True


def creditos_de(lista: list) -> int:
    return sum(ASIGNATURAS[c]["creditos"] for c in lista)


def imprimir_plan(nombre_agente: str, plan: dict):
    """Imprime el plan de estudios generado por un agente."""
    print(f"\n{'='*65}")
    print(f"  AGENTE: {nombre_agente}")
    print(f"{'='*65}")
    total_cred = 0
    for sem in sorted(plan.keys()):
        materias = plan[sem]
        creds    = creditos_de(materias)
        total_cred += creds
        print(f"\n  ── Semestre {sem:2d}  ({creds} créditos) {'─'*35}")
        for cod in materias:
            a = ASIGNATURAS[cod]
            print(f"     [{cod}] {a['nombre']:<42} {a['creditos']} cr")
    print(f"\n  Semestres totales : {max(plan.keys())}")
    print(f"  Créditos totales  : {total_cred}")
    pendientes = set(CODIGOS) - {c for lst in plan.values() for c in lst}
    if pendientes:
        print(f"  ⚠️  Materias no asignadas: {len(pendientes)}")
        for p in pendientes:
            print(f"     - {ASIGNATURAS[p]['nombre']}")
    else:
        print("  ✅ Todas las materias asignadas correctamente.")


# ─── AGENTE 1: Alumno Esforzado ───────────────────────────────────────────────

class AgenteEsforzado:
    """
    Estrategia: En cada semestre selecciona las materias disponibles
    ordenadas de MAYOR a MENOR número de créditos, respetando el límite.
    Objetivo: avanzar lo más posible en créditos cada semestre.
    """
    nombre = "Alumno Esforzado (max créditos)"

    def ejecutar(self, max_creditos: int = MAX_CREDITOS) -> dict:
        cursadas = set()
        plan     = {}

        for semestre in range(1, MAX_SEMESTRES + 1):
            disponibles = materias_disponibles(cursadas)
            if not disponibles:
                break

            # Ordenar de mayor a menor créditos
            disponibles.sort(key=lambda c: -ASIGNATURAS[c]["creditos"])

            seleccion  = []
            cred_total = 0

            for cod in disponibles:
                cred = ASIGNATURAS[cod]["creditos"]
                if cred_total + cred <= max_creditos:
                    # Verificar que los correquisitos de cod también quepan
                    coreqs_cod = [co for co in ASIGNATURAS[cod]["co"]
                                  if co not in cursadas]
                    cred_co = sum(ASIGNATURAS[co]["creditos"]
                                  for co in coreqs_cod
                                  if co not in seleccion)
                    if cred_total + cred + cred_co <= max_creditos:
                        seleccion.append(cod)
                        for co in coreqs_cod:
                            if co not in seleccion:
                                seleccion.append(co)
                        cred_total = creditos_de(seleccion)

            if not seleccion:
                break

            # Deduplicar preservando orden
            seen = set()
            seleccion = [c for c in seleccion if not (c in seen or seen.add(c))]
            plan[semestre] = seleccion
            cursadas.update(seleccion)

            if cursadas >= set(CODIGOS):
                break

        return plan


# ─── AGENTE 2: Alumno Ocupado ─────────────────────────────────────────────────

class AgenteOcupado:
    """
    Estrategia: En cada semestre agrega materias disponibles en el orden
    en que aparecen (sin priorizar créditos) hasta completar 15 créditos.
    Objetivo: no sobrecargarse, completar el mínimo viable.
    """
    nombre = "Alumno Ocupado (max 15 créditos)"
    LIMITE = 15

    def ejecutar(self) -> dict:
        cursadas = set()
        plan     = {}

        for semestre in range(1, MAX_SEMESTRES + 1):
            disponibles = materias_disponibles(cursadas)
            if not disponibles:
                break

            seleccion  = []
            cred_total = 0

            for cod in disponibles:
                cred = ASIGNATURAS[cod]["creditos"]
                if cred_total + cred <= self.LIMITE:
                    coreqs_cod = [co for co in ASIGNATURAS[cod]["co"]
                                  if co not in cursadas]
                    cred_co = sum(ASIGNATURAS[co]["creditos"]
                                  for co in coreqs_cod
                                  if co not in seleccion)
                    if cred_total + cred + cred_co <= self.LIMITE:
                        seleccion.append(cod)
                        for co in coreqs_cod:
                            if co not in seleccion:
                                seleccion.append(co)
                        cred_total = creditos_de(seleccion)

            if not seleccion:
                break

            seen = set()
            seleccion = [c for c in seleccion if not (c in seen or seen.add(c))]
            plan[semestre] = seleccion
            cursadas.update(seleccion)

            if cursadas >= set(CODIGOS):
                break

        return plan


# ─── AGENTE 3: Sociedad de Agentes ────────────────────────────────────────────
#
# DISEÑO DE LA SOCIEDAD:
#   Sub-agente A — "Estratega de Créditos":
#       Propone materias ordenadas por mayor número de créditos.
#       Meta: maximizar créditos por semestre.
#
#   Sub-agente B — "Estratega de Desbloqueo":
#       Propone materias que desbloquean el mayor número de futuras materias.
#       Meta: abrir el camino para semestres siguientes.
#
#   Mecanismo de negociación:
#       1. Cada sub-agente construye su propuesta individual.
#       2. Se forma la UNIÓN de ambas propuestas (sin superar MAX_CREDITOS).
#       3. Si hay conflicto por límite de créditos, se prioriza por votación:
#          la materia con mayor "puntaje combinado" (créditos + desbloqueos) gana.
#       4. El árbitro (coordinador) valida correquisitos y emite el plan final.

class SubAgenteCreditos:
    """Propone materias priorizando mayor número de créditos."""

    def proponer(self, disponibles: list, cursadas: set, presupuesto: int) -> list:
        ordenadas = sorted(disponibles, key=lambda c: -ASIGNATURAS[c]["creditos"])
        return self._seleccionar(ordenadas, cursadas, presupuesto)

    def _seleccionar(self, ordenadas, cursadas, presupuesto):
        seleccion  = []
        cred_total = 0
        for cod in ordenadas:
            cred = ASIGNATURAS[cod]["creditos"]
            if cred_total + cred <= presupuesto and cod not in seleccion:
                seleccion.append(cod)
                cred_total += cred
        return seleccion


class SubAgenteDesbloqueo:
    """Propone materias priorizando las que desbloquean más materias futuras."""

    def _cuantas_desbloquea(self, cod: str, cursadas: set) -> int:
        """Cuenta cuántas materias quedarian disponibles si se cursa 'cod'."""
        hipoteticas = cursadas | {cod}
        count = 0
        for c in CODIGOS:
            if c not in hipoteticas:
                if all(p in hipoteticas for p in ASIGNATURAS[c]["pre"]):
                    count += 1
        return count

    def proponer(self, disponibles: list, cursadas: set, presupuesto: int) -> list:
        puntuadas  = sorted(
            disponibles,
            key=lambda c: -self._cuantas_desbloquea(c, cursadas)
        )
        seleccion  = []
        cred_total = 0
        for cod in puntuadas:
            cred = ASIGNATURAS[cod]["creditos"]
            if cred_total + cred <= presupuesto and cod not in seleccion:
                seleccion.append(cod)
                cred_total += cred
        return seleccion


class CoordinadorSociedad:
    """
    Árbitro que recibe las propuestas de ambos sub-agentes,
    las negocia y emite una selección final válida.
    """

    def negociar(self,
                 propuesta_a: list,
                 propuesta_b: list,
                 cursadas: set,
                 presupuesto: int) -> list:
        """
        Construye la selección final votando por cada materia candidata.
        Puntaje = (créditos × votos) donde votos = 1 si la propuso solo un agente,
                                                    2 si la propusieron ambos.
        """
        set_a     = set(propuesta_a)
        set_b     = set(propuesta_b)
        todos     = list(set_a | set_b)

        def puntaje(cod):
            votos = (1 if cod in set_a else 0) + (1 if cod in set_b else 0)
            return votos * 10 + ASIGNATURAS[cod]["creditos"]

        candidatos = sorted(todos, key=puntaje, reverse=True)

        seleccion  = []
        cred_total = 0
        for cod in candidatos:
            cred = ASIGNATURAS[cod]["creditos"]
            # Incluir correquisitos obligatorios
            coreqs_necesarios = [co for co in ASIGNATURAS[cod]["co"]
                                  if co not in cursadas and co not in seleccion]
            extra_cred = sum(ASIGNATURAS[co]["creditos"] for co in coreqs_necesarios)

            if cred_total + cred + extra_cred <= presupuesto:
                seleccion.append(cod)
                seleccion.extend(coreqs_necesarios)
                cred_total += cred + extra_cred

        return seleccion


class SociedadAgentes:
    """
    Sociedad de agentes que construye el plan semestre a semestre
    mediante negociación entre SubAgenteCreditos y SubAgenteDesbloqueo.
    """
    nombre = "Sociedad de Agentes (Créditos ↔ Desbloqueo)"

    def __init__(self):
        self.agente_a     = SubAgenteCreditos()
        self.agente_b     = SubAgenteDesbloqueo()
        self.coordinador  = CoordinadorSociedad()

    def ejecutar(self, max_creditos: int = MAX_CREDITOS) -> dict:
        cursadas  = set()
        plan      = {}
        log_neg   = []  # registro de negociaciones

        for semestre in range(1, MAX_SEMESTRES + 1):
            disponibles = materias_disponibles(cursadas)
            if not disponibles:
                break

            # Cada sub-agente hace su propuesta con la mitad del presupuesto
            # para que ambos tengan espacio de negociación
            presupuesto_parcial = max_creditos // 2 + 3

            prop_a = self.agente_a.proponer(disponibles, cursadas, presupuesto_parcial)
            prop_b = self.agente_b.proponer(disponibles, cursadas, presupuesto_parcial)

            # El coordinador negocia y elige la selección final
            seleccion = self.coordinador.negociar(prop_a, prop_b, cursadas, max_creditos)

            if not seleccion:
                # Fallback: tomar al menos una materia disponible
                seleccion = [disponibles[0]]

            log_neg.append({
                "semestre": semestre,
                "prop_a":   prop_a,
                "prop_b":   prop_b,
                "final":    seleccion,
            })

            plan[semestre] = seleccion
            cursadas.update(seleccion)

            if cursadas >= set(CODIGOS):
                break

        self._imprimir_log(log_neg)
        return plan

    def _imprimir_log(self, log):
        print("\n  ── Registro de negociaciones ──────────────────────────────")
        for entrada in log:
            s   = entrada["semestre"]
            a   = [ASIGNATURAS[c]["nombre"] for c in entrada["prop_a"]]
            b   = [ASIGNATURAS[c]["nombre"] for c in entrada["prop_b"]]
            fin = [ASIGNATURAS[c]["nombre"] for c in entrada["final"]]
            print(f"\n  Semestre {s}:")
            print(f"    Agente Créditos propone   : {a}")
            print(f"    Agente Desbloqueo propone : {b}")
            print(f"    → Decisión final          : {fin}")


# ─── Comparación de agentes ───────────────────────────────────────────────────

def comparar_agentes():
    print("\n" + "=" * 65)
    print("  COMPARACIÓN DE AGENTES")
    print("=" * 65)

    resultados = []

    for AgenteCls, kwargs in [
        (AgenteEsforzado, {}),
        (AgenteOcupado,   {}),
        (SociedadAgentes, {}),
    ]:
        agente = AgenteCls()
        plan   = agente.ejecutar(**kwargs)
        imprimir_plan(agente.nombre, plan)

        asignadas = {c for lst in plan.values() for c in lst}
        resultados.append({
            "nombre":     agente.nombre,
            "semestres":  max(plan.keys()) if plan else 99,
            "completo":   asignadas >= set(CODIGOS),
            "cred_prom":  sum(creditos_de(v) for v in plan.values()) / len(plan) if plan else 0,
        })

    print("\n\n" + "=" * 65)
    print("  RESUMEN COMPARATIVO")
    print("=" * 65)
    print(f"\n  {'Agente':<40} {'Sems':>5} {'Completo':>9} {'Cr/Sem':>8}")
    print("  " + "-" * 62)
    for r in resultados:
        comp = "✅" if r["completo"] else "❌"
        print(f"  {r['nombre']:<40} {r['semestres']:>5} {comp:>9} {r['cred_prom']:>7.1f}")


if __name__ == "__main__":
    comparar_agentes()

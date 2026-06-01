#!/usr/bin/env python3
"""
parte1_restricciones.py — Parte I: Modelamiento mediante restricciones
Proyecto Final Programación III — UTP

Usa ordenamiento topológico + asignación greedy con verificación de restricciones.
Equivalente conceptualmente al modelo MiniZinc que se incluye en plan_estudios.mzn
"""

from malla import ASIGNATURAS, CODIGOS, IDX, MAX_SEMESTRES, MAX_CREDITOS
import time
from collections import defaultdict, deque


# ─── Construcción del grafo de restricciones ──────────────────────────────────

def construir_restricciones():
    prereqs = []  # (A, B) → A debe cursarse ANTES que B
    coreqs  = []  # (A, B) → deben cursarse en el MISMO semestre
    for cod, datos in ASIGNATURAS.items():
        for pre in datos["pre"]:
            if pre in IDX:
                prereqs.append((pre, cod))
        for co in datos["co"]:
            if co in IDX and (co, cod) not in coreqs:
                coreqs.append((cod, co))
    return prereqs, coreqs


# ─── Ordenamiento topológico (Kahn's algorithm) ───────────────────────────────

def orden_topologico():
    """
    Retorna los códigos ordenados respetando prerrequisitos.
    Las materias sin prerrequisitos van primero.
    """
    prereqs, _ = construir_restricciones()
    grado_entrada = defaultdict(int)
    sucesores     = defaultdict(list)

    for cod in CODIGOS:
        grado_entrada[cod] = grado_entrada.get(cod, 0)

    for (a, b) in prereqs:
        sucesores[a].append(b)
        grado_entrada[b] += 1

    cola  = deque(c for c in CODIGOS if grado_entrada[c] == 0)
    orden = []
    while cola:
        nodo = cola.popleft()
        orden.append(nodo)
        for suc in sucesores[nodo]:
            grado_entrada[suc] -= 1
            if grado_entrada[suc] == 0:
                cola.append(suc)

    return orden


# ─── Asignador por semestres ──────────────────────────────────────────────────

class AsignadorSemestres:
    """
    Modelo de restricciones:
      Dado el orden topológico, asigna cada materia al semestre más
      temprano posible cumpliendo:
        R1 — prerrequisitos cursados en semestres anteriores
        R2 — correquisitos en el mismo semestre
        R3 — máximo de créditos por semestre (MAX_CREDITOS)
        R4 — máximo de semestres (MAX_SEMESTRES)
    """

    def __init__(self):
        self.prereqs, self.coreqs = construir_restricciones()
        self.pre_map  = defaultdict(list)   # cod → lista de prereqs
        self.co_map   = defaultdict(set)    # cod → conjunto de coreqs

        for (a, b) in self.prereqs:
            self.pre_map[b].append(a)
        for (a, b) in self.coreqs:
            self.co_map[a].add(b)
            self.co_map[b].add(a)

    def semestre_minimo(self, cod: str, asignacion: dict) -> int:
        """Semestre mínimo donde puede ir 'cod' respetando prerrequisitos."""
        sem_min = ASIGNATURAS[cod]["semestre"]   # restricción del plan oficial
        for pre in self.pre_map[cod]:
            if pre in asignacion:
                sem_min = max(sem_min, asignacion[pre] + 1)
        return sem_min

    def puede_asignar(self, cod: str, sem: int, asignacion: dict,
                      cred_por_sem: dict) -> bool:
        """Verifica R2 y R3 antes de asignar."""
        # R3: límite de créditos
        cred_actual = cred_por_sem.get(sem, 0)
        if cred_actual + ASIGNATURAS[cod]["creditos"] > MAX_CREDITOS:
            return False
        # R2: correquisitos ya asignados deben estar en el mismo semestre
        for co in self.co_map[cod]:
            if co in asignacion and asignacion[co] != sem:
                return False
        return True

    def asignar(self) -> dict:
        """
        Asigna semestre a cada materia procesando en orden topológico.
        Retorna diccionario {codigo: semestre}.
        """
        orden        = orden_topologico()
        asignacion   = {}
        cred_por_sem = defaultdict(int)

        for cod in orden:
            sem_min = self.semestre_minimo(cod, asignacion)

            # Asegurarse que los correquisitos vayan juntos
            coreqs_pendientes = [co for co in self.co_map[cod]
                                  if co not in asignacion]

            # Buscar el primer semestre donde quepan cod Y sus coreqs
            asignado = False
            for sem in range(sem_min, MAX_SEMESTRES + 1):
                cred_necesaria = ASIGNATURAS[cod]["creditos"] + sum(
                    ASIGNATURAS[co]["creditos"] for co in coreqs_pendientes
                )
                if cred_por_sem[sem] + cred_necesaria <= MAX_CREDITOS:
                    # Verificar coreqs ya asignados
                    ok = True
                    for co in self.co_map[cod]:
                        if co in asignacion and asignacion[co] != sem:
                            ok = False
                            break
                    if ok:
                        asignacion[cod] = sem
                        cred_por_sem[sem] += ASIGNATURAS[cod]["creditos"]
                        # Asignar coreqs pendientes al mismo semestre
                        for co in coreqs_pendientes:
                            asignacion[co] = sem
                            cred_por_sem[sem] += ASIGNATURAS[co]["creditos"]
                        asignado = True
                        break

            if not asignado:
                print(f"  ⚠️  No se pudo asignar: {ASIGNATURAS[cod]['nombre']}")

        return asignacion, cred_por_sem


# ─── Verificador de solución ──────────────────────────────────────────────────

def verificar_solucion(asignacion: dict) -> bool:
    prereqs, coreqs = construir_restricciones()
    errores = []

    for (a, b) in prereqs:
        if a in asignacion and b in asignacion:
            if asignacion[a] >= asignacion[b]:
                errores.append(f"PREREQ violado: {ASIGNATURAS[a]['nombre']} "
                               f"(sem {asignacion[a]}) debe ir antes de "
                               f"{ASIGNATURAS[b]['nombre']} (sem {asignacion[b]})")

    for (a, b) in coreqs:
        if a in asignacion and b in asignacion:
            if asignacion[a] != asignacion[b]:
                errores.append(f"COREQ violado: {ASIGNATURAS[a]['nombre']} y "
                               f"{ASIGNATURAS[b]['nombre']} deben estar juntos")

    cred_sem = defaultdict(int)
    for cod, sem in asignacion.items():
        cred_sem[sem] += ASIGNATURAS[cod]["creditos"]
    for sem, total in cred_sem.items():
        if total > MAX_CREDITOS:
            errores.append(f"Semestre {sem}: {total} créditos > {MAX_CREDITOS}")

    if errores:
        print("\n  ❌ Errores encontrados:")
        for e in errores:
            print(f"     {e}")
        return False
    return True


# ─── Impresión del plan ───────────────────────────────────────────────────────

def imprimir_solucion(asignacion: dict):
    plan = defaultdict(list)
    for cod, sem in asignacion.items():
        plan[sem].append(cod)

    total_cred = 0
    for sem in sorted(plan.keys()):
        materias = plan[sem]
        creds    = sum(ASIGNATURAS[c]["creditos"] for c in materias)
        total_cred += creds
        print(f"\n  ── Semestre {sem:2d}  ({creds} créditos) ──────────────────────")
        for cod in sorted(materias, key=lambda c: -ASIGNATURAS[c]["creditos"]):
            a = ASIGNATURAS[cod]
            print(f"     [{cod}] {a['nombre']:<42} {a['creditos']} cr")
    print(f"\n  Total créditos del programa: {total_cred}")
    return plan


# ─── Análisis de hallazgos ────────────────────────────────────────────────────

def analizar_malla():
    prereqs, coreqs = construir_restricciones()
    print("\n" + "=" * 62)
    print("ANÁLISIS DE LA MALLA CURRICULAR")
    print("=" * 62)

    bloqueadas = defaultdict(int)
    for (a, b) in prereqs:
        bloqueadas[b] += 1

    print("\nTop 5 materias con más prerrequisitos (cuellos de botella):")
    for cod, n in sorted(bloqueadas.items(), key=lambda x: -x[1])[:5]:
        print(f"  {ASIGNATURAS[cod]['nombre']:42s} — {n} prereqs")

    print("\nCarga crediticia por semestre (plan oficial):")
    por_sem = defaultdict(list)
    for cod, a in ASIGNATURAS.items():
        por_sem[a["semestre"]].append(cod)
    for s in sorted(por_sem):
        creds = sum(ASIGNATURAS[c]["creditos"] for c in por_sem[s])
        barra = "█" * creds
        alerta = " ⚠️ >21" if creds > 21 else ""
        print(f"  Sem {s:2d}: {barra} ({creds} cr){alerta}")

    libres = [c for c in CODIGOS if not ASIGNATURAS[c]["pre"]]
    print(f"\nMaterias sin prerrequisitos (accesibles desde sem 1): {len(libres)}")
    for c in libres:
        print(f"  [{c}] {ASIGNATURAS[c]['nombre']}")


# ─── Generador de datos para MiniZinc ─────────────────────────────────────────

def generar_dzn(ruta="datos.dzn"):
    prereqs, coreqs = construir_restricciones()
    lines = [f"N = {len(CODIGOS)};", ""]
    lines.append("creditos = [" + ", ".join(
        str(ASIGNATURAS[c]["creditos"]) for c in CODIGOS) + "];")
    lines.append("sem_base = [" + ", ".join(
        str(ASIGNATURAS[c]["semestre"]) for c in CODIGOS) + "];")
    lines.append(f"\nNUM_PRE = {len(prereqs)};")
    if prereqs:
        filas = " | ".join(f"{IDX[a]+1}, {IDX[b]+1}" for a, b in prereqs)
        lines.append(f"prereqs = [| {filas} |];")
    else:
        lines.append("prereqs = array2d(1..0, 1..2, []);")
    lines.append(f"\nNUM_CO = {len(coreqs)};")
    if coreqs:
        filas = " | ".join(f"{IDX[a]+1}, {IDX[b]+1}" for a, b in coreqs)
        lines.append(f"coreqs = [| {filas} |];")
    else:
        lines.append("coreqs = array2d(1..0, 1..2, []);")
    with open(ruta, "w") as f:
        f.write("\n".join(lines))
    print(f"\nArchivo MiniZinc generado: {ruta}")
    print("Ejecuta con: minizinc --solver Gecode plan_estudios.mzn datos.dzn")


# ─── Main ─────────────────────────────────────────────────────────────────────

def resolver_parte1():
    print("=" * 62)
    print("PARTE I — Modelamiento mediante restricciones")
    print("=" * 62)
    prereqs, coreqs = construir_restricciones()
    print(f"Asignaturas    : {len(CODIGOS)}")
    print(f"Prerrequisitos : {len(prereqs)}")
    print(f"Correquisitos  : {len(coreqs)}")
    print(f"Máx créditos/semestre: {MAX_CREDITOS}")
    print("Método: Ordenamiento topológico + asignación por restricciones\n")

    t0 = time.time()
    asignador = AsignadorSemestres()
    asignacion, cred_sem = asignador.asignar()
    t1 = time.time()

    print(f"✅ Solución encontrada en {t1-t0:.4f}s")
    print(f"   Semestres utilizados: {max(asignacion.values())}")

    plan = imprimir_solucion(asignacion)

    print(f"\n{'─'*62}")
    valido = verificar_solucion(asignacion)
    if valido:
        print("  ✅ Verificación: todas las restricciones se cumplen.")

    print(f"\n{'─'*62}")
    print("HALLAZGOS Y CONCLUSIONES:")
    print(f"  • El plan oficial tiene semestres con hasta 23 créditos (sem 6),")
    print(f"    que supera el máximo de {MAX_CREDITOS}. El modelo redistribuye esas")
    print(f"    materias respetando siempre las dependencias.")
    print(f"  • Las cadenas más largas de prerrequisitos determinan el número")
    print(f"    mínimo de semestres: CB1B3→CB2A3→CB3A4→CB4A4→CB4A3→IS653")
    print(f"  • Hay {len([c for c in CODIGOS if not ASIGNATURAS[c]['pre']])} materias")
    print(f"    sin prerrequisitos que podrían adelantarse para aliviar semestres cargados.")

    return asignacion


if __name__ == "__main__":
    analizar_malla()
    generar_dzn("datos.dzn")
    resolver_parte1()

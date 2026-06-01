
"""
=================================================================
PROYECTO FINAL - Programación III
Modelamiento de Malla Curricular mediante Restricciones (MiniZinc)
Ingeniería de Sistemas y Computación - UTP Pereira
=================================================================
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import minizinc
except ImportError:
    print("❌ Paquete 'minizinc' no encontrado. Intentando instalarlo con pip...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "minizinc"])
        import minizinc  # reintentar import
        print("✅ Paquete 'minizinc' instalado correctamente.")
    except Exception:
        print("❌ No se pudo instalar el paquete 'minizinc'. Ejecuta: pip install minizinc")
        sys.exit(1)

# ================= CONFIGURACIÓN =================
CONFIG = {
    "malla_path": "malla_utp.json",
    "modelo_path": "malla_minizinc.mzn",
    "output_dir": "resultados",
    "carga_min": 12,      # Créditos mínimos por semestre
    "carga_max": 22,      # Créditos máximos por semestre
    "max_semestres": 12,  # Límite del programa
    "solver": "gecode"    # Solver recomendado: gecode, chuffed, or-tools
}

# ================= CLASES AUXILIARES =================

class ResultadoPlan:
    """Clase para almacenar y analizar los resultados del modelo"""
    
    def __init__(self, asignaciones, ultimo_semestre, status):
        self.asignaciones = asignaciones  # dict: {codigo: semestre}
        self.ultimo_semestre = ultimo_semestre
        self.status = status
        self.semestres = self._agrupar_por_semestre()
    
    def _agrupar_por_semestre(self):
        """Agrupa asignaturas por semestre para análisis"""
        agrupado = {}
        for cod, sem in self.asignaciones.items():
            if sem not in agrupado:
                agrupado[sem] = []
            agrupado[sem].append(cod)
        return dict(sorted(agrupado.items()))
    
    def calcular_carga_por_semestre(self, malla_dict):
        """Calcula la carga de créditos por semestre"""
        carga = {}
        for sem, codigos in self.semestres.items():
            carga[sem] = sum(malla_dict[c]["creditos"] for c in codigos)
        return carga
    
    def generar_reporte(self, malla_dict, output_file=None):
        """Genera un reporte textual del plan obtenido"""
        lines = []
        lines.append("=" * 70)
        lines.append("REPORTE: PLAN DE ESTUDIOS OPTIMIZADO")
        lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Estado: {self.status}")
        lines.append(f"Semestres totales: {self.ultimo_semestre} / {CONFIG['max_semestres']}")
        lines.append("=" * 70)
        lines.append("")
        
        carga_total = 0
        for sem in range(1, self.ultimo_semestre + 1):
            codigos = self.semestres.get(sem, [])
            if codigos:
                carga_sem = sum(malla_dict[c]["creditos"] for c in codigos)
                carga_total += carga_sem
                lines.append(f" SEMESTRE {sem} [{carga_sem} créditos]")
                lines.append("-" * 40)
                for cod in sorted(codigos):
                    mat = malla_dict[cod]
                    prereqs = mat.get("prerrequisitos", [])
                    prereq_str = f" (prereq: {', '.join(prereqs)})" if prereqs else ""
                    lines.append(f"  • {cod} - {mat['nombre']} [{mat['creditos']} cr]{prereq_str}")
                lines.append("")
        
        lines.append("=" * 70)
        lines.append(f" TOTAL CRÉDITOS: {carga_total}")
        lines.append(f" EFICIENCIA: {self.ultimo_semestre}/12 semestres")
        
        # Análisis adicional
        cargas = self.calcular_carga_por_semestre(malla_dict)
        if cargas:
            avg_carga = sum(cargas.values()) / len(cargas)
            lines.append(f" Carga promedio por semestre: {avg_carga:.1f} créditos")
            sobrecargados = [s for s, c in cargas.items() if c > 18]
            if sobrecargados:
                lines.append(f"  Semestres con carga alta (>18 cr): {sobrecargados}")
        
        lines.append("=" * 70)
        
        reporte = "\n".join(lines)
        
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(reporte)
            print(f" Reporte guardado en: {output_file}")
        
        return reporte

# ================= FUNCIONES PRINCIPALES =================

def cargar_malla(path):
    """Carga la malla curricular desde JSON"""
    if not os.path.exists(path):
        raise FileNotFoundError(f" No se encontró: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        malla = json.load(f)
    
    # Validar estructura básica
    for mat in malla:
        required = ["codigo", "nombre", "creditos", "prerrequisitos", "correquisitos"]
        for field in required:
            if field not in mat:
                raise ValueError(f" Asignatura sin campo '{field}': {mat.get('codigo', 'DESCONOCIDA')}")
    
    return malla

def construir_matrices(malla):
    """Construye las matrices booleanas para MiniZinc"""
    n = len(malla)
    codigos = [m["codigo"] for m in malla]
    creditos = [m["creditos"] for m in malla]
    idx = {cod: i for i, cod in enumerate(codigos)}
    
    # Matrices N x N inicializadas en False
    prereq = [[False] * n for _ in range(n)]
    correq = [[False] * n for _ in range(n)]
    
    for i, mat in enumerate(malla):
        for p in mat.get("prerrequisitos", []):
            if p in idx:
                prereq[i][idx[p]] = True
            else:
                print(f"  Prerrequisito no encontrado: {p} para {mat['codigo']}")
        for c in mat.get("correquisitos", []):
            if c in idx:
                correq[i][idx[c]] = True
            else:
                print(f"  Correquisito no encontrado: {c} para {mat['codigo']}")
    
    return {
        "N": n,
        "CODIGO": codigos,
        "CREDITOS": creditos,
        "PREREQ": prereq,
        "CORREQ": correq
    }

def ejecutar_minizinc(datos, config):
    """Ejecuta el modelo MiniZinc y retorna los resultados"""
    
    # Configurar solver
    try:
        solver = minizinc.Solver.lookup(config["solver"])
    except minizinc.error.SolverNotFoundError:
        print(f"  Solver '{config['solver']}' no encontrado. Usando default...")
        solver = minizinc.Solver.lookup("gecode")  # Fallback
    
    # Cargar modelo
    modelo = minizinc.Model(config["modelo_path"])
    instancia = minizinc.Instance(solver, modelo)
    
    # Configurar parámetros
    instancia["N"] = datos["N"]
    instancia["CODIGO"] = datos["CODIGO"]
    instancia["CREDITOS"] = datos["CREDITOS"]
    instancia["PREREQ"] = datos["PREREQ"]
    instancia["CORREQ"] = datos["CORREQ"]
    instancia["CARGA_MIN"] = config["carga_min"]
    instancia["CARGA_MAX"] = config["carga_max"]
    
    print(f" Resolviendo con solver: {solver.id}")
    print(f" Asignaturas: {datos['N']}, Carga: {config['carga_min']}-{config['carga_max']} créditos")
    
    # Ejecutar
    try:
        resultado = instancia.solve()
    except Exception as e:
        print(f" Error durante la resolución: {e}")
        return None
    
    return resultado

def procesar_resultado(resultado, malla_dict, config):
    """Procesa el resultado de MiniZinc y genera el objeto ResultadoPlan"""
    if resultado is None:
        print(" No se encontró solución válida. Estado: None")
        return None

    # Intentar extraer la variable de decisión 'S'
    try:
        s_values = resultado["S"]
    except Exception:
        print(f" No se encontró solución válida. Estado: {resultado.status}")
        return None

    # Extraer asignaciones
    asignaciones = {}
    for i, cod in enumerate(resultado["CODIGO"]):
        asignaciones[cod] = int(s_values[i])
    
    ultimo_sem = max(asignaciones.values())
    
    return ResultadoPlan(asignaciones, ultimo_sem, resultado.status)

def guardar_resultados(plan, malla_dict, config):
    """Guarda los resultados en archivos para análisis posterior"""
    
    # Crear directorio de salida
    Path(config["output_dir"]).mkdir(exist_ok=True)
    
    # Guardar plan en JSON
    plan_path = os.path.join(config["output_dir"], "plan_optimo.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump({
            "asignaciones": plan.asignaciones,
            "ultimo_semestre": plan.ultimo_semestre,
            "status": str(plan.status),
            "semestres": plan.semestres
        }, f, indent=2, ensure_ascii=False)
    
    # Generar y guardar reporte textual
    reporte_path = os.path.join(config["output_dir"], "reporte.txt")
    plan.generar_reporte(malla_dict, reporte_path)
    
    return plan_path, reporte_path

# ================= FUNCIÓN MAIN =================

def main():
    """Función principal de ejecución"""
    
    print("\n" + "=" * 70)
    print(" PROYECTO FINAL - Programación III - UTP")
    print("Modelamiento de Malla Curricular con Restricciones (MiniZinc)")
    print("=" * 70 + "\n")
    
    try:
        # 1. Cargar datos
        print(" Cargando malla curricular...")
        malla = cargar_malla(CONFIG["malla_path"])
        malla_dict = {m["codigo"]: m for m in malla}
        print(f" {len(malla)} asignaturas cargadas\n")
        
        # 2. Preparar matrices para MiniZinc
        print(" Preparando matrices de restricciones...")
        datos = construir_matrices(malla)
        print(f" Matrices {datos['N']}x{datos['N']} listas\n")
        
        # 3. Ejecutar modelo
        print(" Ejecutando modelo de restricciones...")
        resultado_mzn = ejecutar_minizinc(datos, CONFIG)
        
        # 4. Procesar resultados
        print(" Procesando resultados...")
        plan = procesar_resultado(resultado_mzn, malla_dict, CONFIG)
        
        if plan is None:
            print(" No se pudo generar un plan válido.")
            return 1
        
        # 5. Mostrar resumen en consola
        print("\n" + "✨" * 35)
        print(f" PLAN GENERADO EXITOSAMENTE")
        print(f" Semestres requeridos: {plan.ultimo_semestre} / {CONFIG['max_semestres']}")
        print(f" Asignaturas planificadas: {len(plan.asignaciones)}")
        print("" * 35 + "\n")
        
        # 6. Guardar resultados
        plan_path, reporte_path = guardar_resultados(plan, malla_dict, CONFIG)
        
        # 7. Mostrar reporte resumido
        print(plan.generar_reporte(malla_dict))
        
        print(f"\n Archivos generados:")
        print(f"   • {plan_path}")
        print(f"   • {reporte_path}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f" Error de archivo: {e}")
        return 1
    except Exception as e:
        print(f" Error inesperado: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1

# ================= ENTRY POINT =================

if __name__ == "__main__":
    sys.exit(main())
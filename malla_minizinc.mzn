% =====================================================
% MODELO DE PLAN DE ESTUDIOS - Ingeniería de Sistemas UTP
% Parte I: Modelamiento mediante restricciones
% =====================================================

include "globals.mzn";

% --- PARÁMETROS DE ENTRADA ---
int: N;                           % Número total de asignaturas
int: MAX_SEMESTRES = 12;          % Límite máximo de semestres
array[1..N] of string: CODIGO;    % Códigos de asignaturas
array[1..N] of int: CREDITOS;     % Créditos por asignatura
array[1..N, 1..N] of bool: PREREQ;% Matriz de prerrequisitos
array[1..N, 1..N] of bool: CORREQ;% Matriz de correquisitos
int: CARGA_MIN;                   % Carga mínima por semestre
int: CARGA_MAX;                   % Carga máxima por semestre

% --- VARIABLES DE DECISIÓN ---
% S[i] = semestre en el que se cursa la asignatura i
array[1..N] of var 1..MAX_SEMESTRES: S;

% --- RESTRICCIONES ---

% 1. Prerrequisitos estrictos: si j es prereq de i, entonces i debe cursarse después
constraint forall(i, j in 1..N where PREREQ[i,j]) (
    S[i] > S[j]
);

% 2. Correquisitos: si j es correquisito de i, pueden cursarse en mismo semestre o j antes
constraint forall(i, j in 1..N where CORREQ[i,j]) (
    S[i] >= S[j]
);

% 3. Carga académica por semestre dentro del rango permitido
constraint forall(s in 1..MAX_SEMESTRES) (
    let {
        var int: carga_s = sum(i in 1..N) (if S[i] == s then CREDITOS[i] else 0 endif)
    } in
        carga_s >= CARGA_MIN /\ carga_s <= CARGA_MAX
);

% 4. Todas las asignaturas deben asignarse a algún semestre (implícito por el dominio)

% --- FUNCIÓN OBJETIVO: Minimizar el último semestre usado ---
var 1..MAX_SEMESTRES: ultimo_sem = max(i in 1..N)(S[i]);
solve minimize ultimo_sem;

% --- OUTPUT PARA ANÁLISIS ---
output [
    "=== PLAN DE ESTUDIOS OPTIMIZADO ===\n",
    "Semestres totales: \(ultimo_sem)\n\n",
    "S = ", show(S), "\n"
];
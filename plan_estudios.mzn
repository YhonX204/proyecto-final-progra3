% =============================================================================
% plan_estudios.mzn  —  Parte I: Modelamiento mediante restricciones
% Proyecto Final Programación III — UTP
%
% Para ejecutar:
%   minizinc --solver Gecode plan_estudios.mzn datos.dzn
% =============================================================================

% ── Parámetros recibidos desde datos.dzn ─────────────────────────────────────
int: N;                          % número de asignaturas
int: MAX_SEM  = 12;              % semestres máximos
int: MAX_CRED = 21;              % créditos máximos por semestre
int: MIN_CRED = 1;               % créditos mínimos por semestre (si hay materias)

array[1..N] of int: creditos;    % créditos de cada asignatura
array[1..N] of int: sem_base;    % semestre sugerido por el plan oficial

% Prerrequisitos: lista de pares (i,j) => asignatura i debe cursarse ANTES que j
int: NUM_PRE;
array[1..NUM_PRE, 1..2] of int: prereqs;

% Correquisitos: lista de pares (i,j) => deben cursarse en el MISMO semestre
int: NUM_CO;
array[1..NUM_CO, 1..2] of int: coreqs;

% ── Variables de decisión ────────────────────────────────────────────────────
% semestre[i] = semestre en que se cursa la asignatura i
array[1..N] of var 1..MAX_SEM: semestre;

% ── Restricciones ────────────────────────────────────────────────────────────

% R1: Prerrequisitos — si A es prereq de B, A debe cursarse ANTES
constraint forall(k in 1..NUM_PRE)(
    semestre[prereqs[k,1]] < semestre[prereqs[k,2]]
);

% R2: Correquisitos — ambas materias en el mismo semestre
constraint forall(k in 1..NUM_CO)(
    semestre[coreqs[k,1]] == semestre[coreqs[k,2]]
);

% R3: Límite máximo de créditos por semestre
constraint forall(s in 1..MAX_SEM)(
    sum(i in 1..N where semestre[i] == s)(creditos[i]) <= MAX_CRED
);

% R4: Respetar semestre mínimo del plan oficial (no adelantar más de 1 sem)
constraint forall(i in 1..N)(
    semestre[i] >= sem_base[i]
);

% ── Función objetivo ─────────────────────────────────────────────────────────
% Minimizar el semestre máximo usado (terminar lo antes posible)
var 1..MAX_SEM: ultimo_semestre = max(semestre);
solve minimize ultimo_semestre;

% ── Salida ───────────────────────────────────────────────────────────────────
output [
    "Último semestre: \(ultimo_semestre)\n",
    concat([
        "Semestre \(semestre[i]): asignatura \(i)\n"
        | i in 1..N
    ])
];

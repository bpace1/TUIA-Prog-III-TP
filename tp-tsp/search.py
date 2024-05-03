"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem, TSP
from random import choice
from time import time

class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)

class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""
    def solve(self, problem: TSP) -> None:
        start: int = time()

        cnt: int = 0
        iterations: int = 100

        # Arrancamos del estado inicial
        actual: list[int] = problem.init
        value = problem.obj_val(problem.init)

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff: dict[tuple[int, int], float] = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts: list[tuple[int, int]] = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act: tuple[int, int] = choice(max_acts)

            all_states_results: list[list[int]] = [actual]

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                actual = problem.random_reset()

                all_states_results.append(actual)
                
                cnt += 1
                
                if cnt == iterations:
                    values: list[float] = [problem.obj_val(state) for state in all_states_results]
                    final_val: int = max(values)
                    final_state: list[int] = all_states_results[values.index(final_val)]

                    end = time()
                    self.time = end-start
                    self.tour = final_state
                    self.value = final_val

                    return 
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""
    def solve(self, problem: TSP) -> None:
        # Inicio del reloj
        start: int = time()

        iterations: int = 1000

        # Arrancamos del estado inicial
        actual: list[int] = problem.init
        state_mejor: list[int] = actual
        value_mejor: float = problem.obj_val(problem.init)
        lista_tabu: list[int] = []

        while self.niters < iterations:
            # y las diferencias en valor objetivo que resultan
            diff: dict[tuple[int, int], float] = problem.val_diff(actual)

            no_tabues: dict = {}

            for i,j in diff.items():
                if i not in lista_tabu:
                    no_tabues[i] = j

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts: list[int] = [act for act, val in no_tabues.items() if val ==
                        max(no_tabues.values())]

            # Elegir una accion aleatoria
            act: int = choice(max_acts)

            # Nos movemos al sucesor
            actual: list[int] = problem.result(actual, act)
            value: float = problem.obj_val(actual)
            
            # La cantidad de valores lo decidimos comparando diversos numeros
            if len(lista_tabu) > 40:
                lista_tabu.pop(0)
            
            lista_tabu.append(act)
            self.niters += 1
            if value_mejor < value:
                state_mejor = actual
                value_mejor = value
            
        self.tour = state_mejor
        self.value = value_mejor
        end = time()
        self.time = end-start
        return state_mejor

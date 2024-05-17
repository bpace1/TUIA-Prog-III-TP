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
        # Inicio del reloj para medir el tiempo de ejecución del algoritmo
        start = time()

        # Arrancamos desde el estado inicial definido en el problema
        actual = problem.init
        # Evaluamos el valor objetivo del estado inicial
        value = problem.obj_val(problem.init)

        while True:
            # Determinamos las acciones posibles desde el estado actual
            # y calculamos las diferencias en valor objetivo que resultan de aplicar cada acción
            diff = problem.val_diff(actual)

            # Identificamos las acciones que generan el mayor incremento en el valor objetivo
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegimos aleatoriamente una de las mejores acciones
            act = choice(max_acts)

            # Si la diferencia de valor objetivo para la mejor acción no es positiva
            # significa que hemos alcanzado un óptimo local
            if diff[act] <= 0:
                # Guardamos el estado y el valor objetivo final
                self.tour = actual
                self.value = value
                # Medimos el tiempo total de ejecución
                end = time()
                self.time = end - start
                # Terminamos la ejecución del algoritmo
                return

            # Si no estamos en un óptimo local, nos movemos al estado sucesor
            else:
                # Actualizamos el estado actual aplicando la acción elegida
                actual = problem.result(actual, act)
                # Actualizamos el valor objetivo sumando la diferencia producida por la acción
                value = value + diff[act]
                # Incrementamos el contador de iteraciones
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: TSP) -> None:
        start: int = time()

        cnt: int = 0
        iterations: int = 100

        # Arrancamos del estado inicial
        actual: list[int] = problem.init
        value: float = problem.obj_val(problem.init)

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff: dict[tuple[int, int], float] = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts: list[tuple[int, int]] = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una acción aleatoria entre las que generan el mayor incremento en el valor objetivo
            act: tuple[int, int] = choice(max_acts)

            # Lista para almacenar todos los estados generados durante el reinicio
            all_states_results: list[list[int]] = [actual]

            # Retornar si estamos en un óptimo local (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                # Reiniciamos aleatoriamente el estado y agregamos el nuevo estado a la lista de resultados
                actual = problem.random_reset()
                all_states_results.append(actual)
                
                # Incrementamos el contador de reinicios
                cnt += 1
                
                # Si alcanzamos el número máximo de reinicios, seleccionamos el mejor estado encontrado
                if cnt == iterations:
                    # Evaluamos el valor objetivo de todos los estados generados durante el reinicio
                    values: list[float] = [problem.obj_val(state) for state in all_states_results]
                    # Seleccionamos el estado con el mayor valor objetivo
                    final_val: int = max(values)
                    final_state: list[int] = all_states_results[values.index(final_val)]

                    # Registro del tiempo y resultados finales
                    end = time()
                    self.time = end - start
                    self.tour = final_state
                    self.value = final_val

                    # Terminamos la ejecución del algoritmo
                    return 
            else:
                # Si no estamos en un óptimo local, nos movemos al estado sucesor
                actual = problem.result(actual, act)
                # Actualizamos el valor objetivo sumando la diferencia producida por la acción
                value = value + diff[act]
                # Incrementamos el contador de iteraciones
                self.niters += 1


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def solve(self, problem: TSP) -> None:
        # Inicio del reloj para medir el tiempo de ejecución del algoritmo
        start: int = time()

        iterations: int = 1000

        # Arrancamos del estado inicial
        actual: list[int] = problem.init
        state_mejor: list[int] = actual
        value_mejor: float = problem.obj_val(problem.init)
        lista_tabu: list[int] = []

        while self.niters < iterations:
            # Calculamos las diferencias en valor objetivo que resultan de aplicar cada acción
            diff: dict[tuple[int, int], float] = problem.val_diff(actual)

            # Filtramos las acciones que no están en la lista tabú
            no_tabues: dict = {}

            for i, j in diff.items():
                if i not in lista_tabu:
                    no_tabues[i] = j

            # Buscamos las acciones que generan el mayor incremento de valor objetivo
            max_acts: list[int] = [act for act, val in no_tabues.items() if val ==
                        max(no_tabues.values())]

            # Elegimos aleatoriamente una de las mejores acciones
            act: int = choice(max_acts)

            # Nos movemos al estado sucesor aplicando la acción seleccionada
            actual: list[int] = problem.result(actual, act)
            value: float = problem.obj_val(actual)
            
            # Actualizamos la lista tabú con la nueva acción
            if len(lista_tabu) > 40:
                lista_tabu.pop(0)
            
            lista_tabu.append(act)
            
            # Incrementamos el contador de iteraciones
            self.niters += 1
            
            # Actualizamos el mejor estado y valor objetivo si encontramos una solución mejor
            if value_mejor < value:
                state_mejor = actual
                value_mejor = value
            
        # Guardamos el mejor estado y valor objetivo encontrado
        self.tour = state_mejor
        self.value = value_mejor
        
        # Registro del tiempo de ejecución
        end = time()
        self.time = end - start
        
        # Retornamos el mejor estado encontrado
        return state_mejor

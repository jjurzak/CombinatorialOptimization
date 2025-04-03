'''
Czy graf przedstawiający ruch skoczka na szachownicy o wymiarach
8 x 8, z której usunięto pole a1 ma cykl Hamiltona?

JJurzak 59099
'''

import sys
import threading
import os
from ortools.linear_solver import pywraplp

def to_chess_notation(i, j):
    return chr(ord("a") + j) + str(i + 1)

def build_board(board_size):
    squares = []
    for i in range(board_size):
        for j in range(board_size):
            if not (i == 0 and j == 0):
                squares.append((i, j))
    if len(squares) != board_size**2 - 1:
        print("Niepoprawny rozmiar szachownicy")
        sys.exit()
    return squares

def build_edges(board_size, squares):
    square_to_index = {square: idx for idx, square in enumerate(squares)}
    knight_moves = [
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
    ]
    edges = {}
    for idx, (i, j) in enumerate(squares):
        edges[idx] = []
        for di, dj in knight_moves:
            ni, nj = i + di, j + dj
            if (0 <= ni < board_size and 0 <= nj < board_size and not (ni == 0 and nj == 0)):
                neighbor = square_to_index.get((ni, nj))
                if neighbor is not None:
                    edges[idx].append(neighbor)
    return edges

solution_found_event = threading.Event()
solution_lock = threading.Lock()
global_solution = {
    "found": False,
    "cycle": None,
    "moves_map": None,
    "starting_index": None,
}

def solve_for_start(start_index, board_size, squares, edges):
    if solution_found_event.is_set():
        return

    n = len(squares)
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise Exception("Solver nie został poprawnie zainicjowany!")
    
    
    x = {} 
    for i in range(n):
        for j in edges[i]:
            x[(i, j)] = solver.BoolVar(f"x[{i},{j}]")

    for i in range(n):
        solver.Add(sum(x[(i, j)] for j in edges[i]) == 1)
    
    for j in range(n):
        incoming = []
        for i in range(n):
            if (i, j) in x:
                incoming.append(x[(i, j)])
        solver.Add(sum(incoming) == 1)
    
   
    u = {}  # zmienna pomocnicza -> miller-tucker-zemlin - usuwanie podcykli.
    for i in range(n):
        u[i] = solver.NumVar(0, n - 1, f"u[{i}]")
    solver.Add(u[start_index] == 0)
    
    for i in range(n):
        if i == start_index:
            continue
        for j in edges[i]:
            if j != start_index:
                solver.Add(u[i] - u[j] + n * x[(i, j)] <= n - 1)
    
    solver.Minimize(solver.Sum(x[(i, j)] for (i, j) in x))
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        with solution_lock:
            if not solution_found_event.is_set():
                solution_found_event.set()
                cycle = []
                current = start_index
                for _ in range(n):
                    cycle.append(current)
                    for j in edges[current]:
                        if x[(current, j)].solution_value() > 0.5:
                            current = j
                            break
                
                moves_map = {}
                for idx in range(len(cycle)):
                    current_node = cycle[idx]
                    next_node = cycle[(idx + 1) % len(cycle)]
                    current_square = squares[current_node]
                    next_square = squares[next_node]
                    moves_map[to_chess_notation(*current_square)] = to_chess_notation(*next_square)
                
                global_solution["found"] = True
                global_solution["cycle"] = cycle
                global_solution["moves_map"] = moves_map
                global_solution["starting_index"] = start_index
                
                print(f"Rozwiązanie znalezione przez wątek dla indeksu startowego: {start_index}, ")  
                print("Indeks startowy w notacji szachowej:", to_chess_notation(*squares[start_index]))
                print("Cykl (indeksy):", cycle)
                with open("ruchy_skoczka.txt", "w", encoding="utf-8") as file:
                    file.write("Mapa ruchów skoczka:\n")
                    for source, dest in moves_map.items():
                        file.write(f"{source} -> {dest}\n")
                os._exit(0)
    else:
        print(f"Wątek dla start_index {start_index} nie znalazł rozwiązania optymalnego.")

def main():
    if len(sys.argv) > 1:
        board_size_input = sys.argv[1]
    else:
        board_size_input = input("Podaj rozmiar szachownicy: ") or "8"
    board_size = int(board_size_input)

    squares = build_board(board_size)
    print(f"Szachownica o wymiarach {board_size}x{board_size} została poprawnie zainicjowana.")
    edges = build_edges(board_size, squares)
    n = len(squares)


    threads = []
    for start_index in range(n):
        thread = threading.Thread(
            target=solve_for_start, args=(start_index, board_size, squares, edges)
        )
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    if not global_solution["found"]:
        print("Nie znaleziono cyklu Hamiltona lub problem nie został optymalnie rozwiązany.")

if __name__ == "__main__":
    main()

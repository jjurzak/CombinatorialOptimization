from ortools.linear_solver import pywraplp
import sys

def to_chess_notation(i, j):
    return chr(ord('a') + j) + str(i + 1)

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise Exception("Solver nie został poprawnie zainicjowany!")

board_size_input = input("Podaj rozmiar szachownicy: ")
board_size = int(board_size_input)

squares = []
for i in range(board_size):
    for j in range(board_size):
        if not (i == 0 and j == 0):
            squares.append((i, j))

n = len(squares)

if not (n != board_size**2 - 1): 
    print("Szachownica o wymiarach", board_size, "x", board_size, "została poprawnie zainicjowana.")
else:
    print("Niepoprawny rozmiar szachownicy")
    sys.exit()

square_to_index = {square: idx for idx, square in enumerate(squares)}


knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                (1, 2), (1, -2), (-1, 2), (-1, -2)]
edges = {}
for idx, (i, j) in enumerate(squares):
    edges[idx] = []
    for di, dj in knight_moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < board_size and 0 <= nj < board_size and not (ni == 0 and nj == 0):
            neighbor = square_to_index[(ni, nj)]
            edges[idx].append(neighbor)



x = {}
for i in range(n):
    for j in edges[i]:
        x[(i, j)] = solver.BoolVar(f'x[{i},{j}]')



for i in range(n):
    solver.Add(sum(x[(i, j)] for j in edges[i]) == 1)

for j in range(n):
    incoming = []
    for i in range(n):
        if (i, j) in x:
            incoming.append(x[(i, j)])
    solver.Add(sum(incoming) == 1)

# Dodanie ograniczeń MTZ eliminujących podcykle
u = {}
for i in range(n):
    u[i] = solver.NumVar(0, n - 1, f'u[{i}]')
solver.Add(u[0] == 0)  

for i in range(1, n):
    for j in edges[i]:
        if j != 0:  
            solver.Add(u[i] - u[j] + n * x[(i, j)] <= n - 1)

solver.Minimize(solver.Sum(x[(i, j)] for (i, j) in x))
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Znaleziono cykl Hamiltona:")
    
    
    cycle = []
    current = 0
    for _ in range(n):
        cycle.append(current)
        for j in edges[current]:
            if x[(current, j)].solution_value() > 0.5:
                current = j
                break

    
    print("Cykl (indeksy):", cycle)
    print("Mapa ruchów skoczka znajduje się w pliku ruchy_skoczka.txt")
    
    
    moves_map = {}
    for idx in range(len(cycle)):
        current_node = cycle[idx]
        next_node = cycle[(idx + 1) % len(cycle)]
        current_square = squares[current_node]  # współrzędne (i, j)
        next_square = squares[next_node]
        moves_map[to_chess_notation(*current_square)] = to_chess_notation(*next_square)

   
    with open("ruchy_skoczka.txt", "w", encoding="utf-8") as file:
        file.write("Mapa ruchów skoczka:\n")
        for source, destination in moves_map.items():
            file.write(f"{source} -> {destination}\n")

else:
    print("Nie znaleziono cyklu Hamiltona lub problem nie został optymalnie rozwiązany.")

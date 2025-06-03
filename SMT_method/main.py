from z3 import *
'''
Znajdź liczby rzeczywiste dodatnie 𝑥 i 𝑦 spełniające warunki:
 𝑦 − 𝑥 < 2,
 2𝑥 + 3𝑦 < 1 
(0.2 − 𝑦)/(1.3 − 𝑥) − sin(𝑥)/𝑥 < −1.1008.

Wykorzystałem przybliżenie szeregiem Taylora dla sin(x)/x.

Jakub Jurzak 59099
'''

x = Real('x')
y = Real('y')

s = Solver()

s.add(y - x < 2)
s.add(2 * x + 3 * y < 1)

s.add(x > 0)
s.add(y > 0)


sin_x_over_x_approx = 1 - x**2 / 6 + x**4 / 120 # Przybliżenie szeregiem Taylora dla sin(x)/x
s.add((0.2 - y) / (1.3 - x) - sin_x_over_x_approx < -1.1008)


if s.check() == sat:
    m = s.model()
    print("Znaleziono rozwiązanie:")
    print(f"x = {m[x]}")
    print(f"y = {m[y]}")

    x_val = float(m[x].as_decimal(10).replace('?', ''))
    y_val = float(m[y].as_decimal(10).replace('?', ''))
    expr_rat = (0.2 - m[y]) / (1.3 - m[x])
    sin_x_over_x_approx_val = 1 - x_val**2 / 6 + x_val**4 / 120 # tą zmienna i tą u dołu zapisałem dla czytelności printu.
    expr_val = (0.2 - y_val) / (1.3 - x_val) - sin_x_over_x_approx_val


    print("Sprawdzenie warunków:")
    if {m[y] - m[x] < 2} and {2 * m[x] + 3 * m[y] < 1} and {(0.2 - m[y]) / (1.3 - m[x]) - sin_x_over_x_approx < -1.1008}:
        print("Wszystkie warunki są spełnione.")
        print(f'1. warunek: {m[y] - m[x] < 2} -> {y_val - x_val < 2} ({y_val - x_val} < 2)')
        print(f'2. warunek: {2 * m[x] + 3 * m[y] < 1} -> {2 * x_val + 3 * y_val < 1} ({2 * x_val + 3 * y_val} < 1)')
        print(f'3. warunek: (0.2 - {m[y]})/(1.3 - {m[x]}) - sin({m[x]})/{m[x]} < -1.1008 -> {expr_val < -1.1008} (wynik {expr_val} < -1.1008)')
    else:
        print("Nie znaleziono rozwiązania.")



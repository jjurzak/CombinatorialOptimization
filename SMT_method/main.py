from dreal import Variable, sin, And, CheckSatisfiability

'''
Znajdź liczby rzeczywiste dodatnie 𝑥 i 𝑦 spełniające warunki:
 𝑦 − 𝑥 < 2,
 2𝑥 + 3𝑦 < 1 
(0.2 − 𝑦)/(1.3 − 𝑥) − sin(𝑥)/𝑥 < −1.1008.

Nie robiłem tego w bibliotece Z3, ponieważ nie działała mi funkcja sinusowa.
Wykorzystałem biblioteke dreal, któa jest dosłownie tym samym co Z3, ale trzeba było użyć do tego dockera.

docker pull dreal/dreal4
docker run -it --rm -v "${PWD}:/workspace" -w /workspace dreal/dreal4 python3 main.py



Jakub Jurzak 59099
'''
def is_less(a, b, eps=1e-9):
    """Porownanie a < b z tolerancja blędu."""
    return a < b + eps

def solve_with_dreal(delta=1e-6):
    x = Variable("x")
    y = Variable("y")

    c1 = y - x < 2
    c2 = 2 * x + 3 * y < 1
    c3 = (0.2 - y) / (1.3 - x) - sin(x) / x < -1.1008

    phi = And(c1, c2, c3, x > 0, y > 0)

    result = CheckSatisfiability(phi, delta)

    if result is not None:
        print("SAT - rozwiazanie w danym przyblizeniu:")
        for var, box in result.items():
            print(f"  {var}: [{box.lb():.6f}, {box.ub():.6f}]")

        x_val = (result[x].lb() + result[x].ub()) / 2
        y_val = (result[y].lb() + result[y].ub()) / 2

        print(f"\nTestujemy srodek przedzialu:")
        print(f"  x ~ {x_val:.12f}")
        print(f"  y ~ {y_val:.12f}")

 
        check1 = is_less(y_val - x_val, 2)
        check2 = is_less(2 * x_val + 3 * y_val, 1)
        # granica dla x→0: sin(x)/x → 1 
        # Dla dokładnie x = 0 nierówność nie ma sensu (dzielenie przez zero).
        # Ale dla bardzo małego 𝑥 > 0 granica istnieje i nierówność jest spełniona stąd takie podejście do problemu
        if abs(x_val) < 1e-8:
            sinx_over_x = 1.0
        else:
            sinx_over_x = sin(x_val) / x_val
        check3 = is_less((0.2 - y_val) / (1.3 - x_val) - sinx_over_x, -1.1008)

        print("\nSprawdzanie nierownosci dla srodka:")
        print(f"  c1: y - x < 2        -> {y_val:.12f} - {x_val:.12f} < 2        -> {check1}")
        print(f"  c2: 2x + 3y < 1      -> 2*{x_val:.12f} + 3*{y_val:.12f} < 1      -> {check2}")
        print(f"  c3: (0.2 - y)/(1.3 - x) - sin(x)/x < -1.1008 -> "
              f"{0.2 - y_val:.12f})/({1.3 - x_val:.12f}) - {sinx_over_x:.12f} < -1.1008 ->  {check3}")

        all_checks = check1 and check2 and check3
        print(f"\nWszystkie nierownosci spelnione (srodek, z epsilon): {all_checks}")

        return result
    else:
        print("UNSAT - brak rozwiazania w danym δ-przyblizeniu")
        return None

if __name__ == "__main__":
    solve_with_dreal(delta=1e-6)

import sys

#Na ile sposobów możemy (całkowicie) pokryć szachownicę o wymiarach 3 × 12 ostkami o wymiarach 1x2 oraz 2x1?
#JJurzak 59099


def tiling_3xn(n):
    
    dp = [0] * (n + 1)
    dp[0] = 1  
    if n >= 1:
        dp[1] = 0
    if n >= 2:
        dp[2] = 3

    # Hardcore na 4 wynika z matematycznej natury problem bo dla dp[0, 1, 2] pusta plansza/3x1[nie da sie]/3x2 [3 sposoby]/
    # dopiero od czwórki ma to sens i zaczyna być rekurencją dynamiczną
    for i in range(4, n + 1, 2):
        dp[i] = 4 * dp[i - 2] - dp[i - 4]
    
    return dp[n]

if len(sys.argv) > 1:
        n = sys.argv[1]
else:
    n = input("Podaj rozmiar szachownicy: ") or "12"
    n = int(n)


if n % 2 != 0:
    print("Liczba n musi być parzysta.")
    sys.exit(1)


wynik = tiling_3xn(n)
print(f"Liczba sposobów pokrycia szachownicy 3x{n}:", wynik)
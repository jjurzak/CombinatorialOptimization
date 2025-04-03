import sys
sys.set_int_max_str_digits(10**6) # dla n => 4300 value error


def tiling_3xn(n):
    
    dp = [0] * (n + 1)
    dp[0] = 1  
    if n >= 1:
        dp[1] = 0
    if n >= 2:
        dp[2] = 3

    # Hardcore na 4 wynika z matematycznej natury problem bo dla dp[0, 1, 2] pusta plansza/3x1/3x2/
    # dopiero od czwórki ma to sens i zaczyna być rekurencją
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

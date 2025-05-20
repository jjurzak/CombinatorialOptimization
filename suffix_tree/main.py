import sys, os, time, random, string

def generate_random_string(length, alphabet=string.ascii_lowercase):
    return ''.join(random.choices(alphabet, k=length))

def find_lexicographically_smallest_rotation():
    user_input = input("Podaj własny ciąg znaków (zaczynający się od litery) lub liczbę (aby wygenerować losowy ciąg o tej długości) lub domyślny ciągów znaków (zostaw puste pole): ").strip()
    start = time.time()
    if not user_input:
        s = "aabaaabaa"
        print(f"Domyślny ciąg: \n{s}")
    elif user_input[0].isdigit():
        length = int(user_input)
        s = generate_random_string(length)
        if length > 50000:
            print("Uwaga: Wygenerowany ciąg jest długi (> 50000 znaków) i zostanie zapisany w pliku tekstowym.")
        else:
            print(f"Losowy ciąg: \n{s}")
    else:
        s = user_input
    n = len(s)

    if n == 0:
        print("")
        return
    i, j, k = 0, 1, 0

    while i < n and j < n and k < n:
        char_from_rot_i = s[(i + k) % n]
        char_from_rot_j = s[(j + k) % n]
        if char_from_rot_i == char_from_rot_j:
            k += 1  
        else:
            if char_from_rot_i > char_from_rot_j:
                i = i + k + 1
            else: 
                j = j + k + 1
            k = 0  
            if i == j:
                i += 1
    
    start_index = min(i, j)
    
    result_rotation = s[start_index:] + s[:start_index]
    if n <= 50000:
        print(result_rotation)

    if n > 50000:
        with open("generated_string_chain", "w", encoding="utf-8") as f:
            f.write(s)
        with open("lexicographically_ordered_chain", "w", encoding="utf-8") as f:
            f.write(result_rotation)
        print("Ciągi zapisano do plików: 'generated_string_chain' i 'lexicographically_ordered_chain'.")

    end = time.time()
    print(f"Czas wykonania: {round(end - start, 4)} s")

if __name__ == '__main__':
    find_lexicographically_smallest_rotation()
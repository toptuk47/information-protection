def linear_congruential_generator(seed, A, C, M, n):
    sequence = []
    current = seed
    for _ in range(n):
        current = (A * current + C) % M
        sequence.append(current)
    return sequence

def text_to_bits(text, b):
    bits = []
    for char in text:
        binary = format(ord(char), f'0{b}b')
        bits.append(binary)
    return bits

def bits_to_text(bits):
    chars = []
    for binary in bits:
        char_code = int(binary, 2)
        chars.append(chr(char_code))
    return ''.join(chars)

def xor_encrypt_decrypt(text_bits, gamma_bits):
    result_bits = []
    for t_bit, g_bit in zip(text_bits, gamma_bits):
        t_int = int(t_bit, 2)
        g_int = int(g_bit, 2)
        xor_result = t_int ^ g_int
        result_bits.append(format(xor_result, f'0{len(t_bit)}b'))
    return result_bits

def main():
    # Параметры
    A = 5
    C = 3
    T0 = 7
    b = 7
    M = 2 ** b

    original_text = "Hello!"

    print("--- Линейный конгруэнтный генератор ПСЧ (Вариант 5) ---")
    print(f"Исходный текст: '{original_text}'")
    print(f"Параметры: A={A}, C={C}, T(0)={T0}, b={b}, M={M}")

    # 1. Преобразуем текст в биты
    text_bits = text_to_bits(original_text, b)
    print(f"\n1. Исходный текст в {b}-битном представлении:")
    for i, bit_str in enumerate(text_bits):
        print(f"\tСимвол '{original_text[i]}': {bit_str}")

    # 2. Генерируем гамму
    num_chars = len(original_text)
    gamma_numbers = linear_congruential_generator(T0, A, C, M, num_chars)

    gamma_bits = [format(num, f'0{b}b') for num in gamma_numbers]
    print(f"\n2. Сгенерированная гамма (ПСЧ):")
    for i, (num, bit_str) in enumerate(zip(gamma_numbers, gamma_bits)):
        print(f"\tT({i+1}) = {num} -> {bit_str}")

    # 3. Шифрование (XOR текста и гаммы)
    encrypted_bits = xor_encrypt_decrypt(text_bits, gamma_bits)
    encrypted_text = bits_to_text(encrypted_bits)
    print(f"\n3. Зашифрованный текст (криптограмма): '{encrypted_text}'")
    print("\tКриптограмма в битах:")
    for bit_str in encrypted_bits:
        print(f"\t{bit_str}")

    # 4. Дешифрование (XOR криптограммы и той же гаммы)
    decryption_gamma_numbers = linear_congruential_generator(T0, A, C, M, num_chars)
    decryption_gamma_bits = [format(num, f'0{b}b') for num in decryption_gamma_numbers]

    decrypted_bits = xor_encrypt_decrypt(encrypted_bits, decryption_gamma_bits)
    decrypted_text = bits_to_text(decrypted_bits)

    print(f"\n4. Дешифрованный текст: '{decrypted_text}'")

    # 5. Проверка
    if original_text == decrypted_text:
        print("\nУспех! Дешифрованный текст совпадает с исходным.")
    else:
        print("\nОшибка! Дешифрованный текст не совпадает с исходным.")

    # Изменение параметра и сравнение
    print("\n" + "="*50)
    print("Изменение параметра T(0) на 8")
    T0_modified = 8
    print(f"Новый T(0) = {T0_modified}")

    # Генерируем новую гамму с измененным параметром
    new_gamma_numbers = linear_congruential_generator(T0_modified, A, C, M, num_chars)
    new_gamma_bits = [format(num, f'0{b}b') for num in new_gamma_numbers]
    new_encrypted_bits = xor_encrypt_decrypt(text_bits, new_gamma_bits)
    new_encrypted_text = bits_to_text(new_encrypted_bits)
    print(f"Новая криптограмма с T(0)={T0_modified}: '{new_encrypted_text}'")
    print("(Отличается от предыдущей криптограммы, т.к. гамма изменилась)")

if __name__ == "__main__":
    main()

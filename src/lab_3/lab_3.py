class FeistelCipher:
    def __init__(self, key, rounds=10, block_size=64):
        self.rounds = rounds
        self.half = block_size // 2
        self.mask = 0xFFFFFFFF
        self.params = [(key >> (i * 6)) & 0x3F or 1 for i in range(rounds)]

    def _shift_right(self, val, shift):
        sign = (val >> (self.half - 1)) & 1
        result = val >> shift
        if sign:
            result |= self.mask ^ ((1 << (self.half - shift)) - 1)
        return result & self.mask

    def _round(self, L, R, param):
        F = self._shift_right(R, param)
        return R, L ^ F

    def encrypt(self, text):
        data = text.encode('utf-8')
        block_len = self.half // 4
        pad = block_len - (len(data) % block_len)
        data += bytes([pad] * pad)

        result = []
        for i in range(0, len(data), block_len):
            block = data[i:i + block_len]
            val = int.from_bytes(block, 'big')
            L, R = (val >> self.half) & self.mask, val & self.mask

            for p in self.params:
                L, R = self._round(L, R, p)

            result.append((L << self.half) | R)
        return result

    def decrypt(self, blocks):
        block_len = self.half // 4
        result = b''

        for val in blocks:
            L, R = (val >> self.half) & self.mask, val & self.mask

            for p in reversed(self.params):
                R, L = self._round(R, L, p)

            result += ((L << self.half) | R).to_bytes(block_len, 'big')

        return result[:-result[-1]].decode('utf-8', errors='ignore')


if __name__ == "__main__":
    KEY = 0x1234567890ABCDEF
    TEXT = "Hello!"

    cipher = FeistelCipher(key=KEY, rounds=10)

    print(f"\nИсходный текст: '{TEXT}'")
    print(f"Параметры раундов: {cipher.params}")

    # Шифрование
    encrypted = cipher.encrypt(TEXT)

    # Преобразуем зашифрованные блоки в байты
    encrypted_bytes = b''
    for block in encrypted:
        encrypted_bytes += block.to_bytes(8, 'big')

    # Создаем строковое представление (видимые символы + точки для невидимых)
    encrypted_string = ''
    for b in encrypted_bytes:
        if 32 <= b <= 126:  # Печатаемые ASCII символы
            encrypted_string += chr(b)
        else:
            encrypted_string += '.'  # Заменяем непечатаемые на точки

    print(f"Зашифрованный текст (string): {encrypted_string}")
    print(f"Зашифрованный текст (hex): {encrypted_bytes.hex()}")

    # Дешифрование
    decrypted = cipher.decrypt(encrypted)

    print(f"Расшифрованный текст: '{decrypted}'")

    # Проверка
    if decrypted == TEXT:
        print("Тексты совпадают!")
    else:
        print("Тексты не совпадают!")

    print("\nТрассировка первого блока:")
    test = TEXT[:8].encode().ljust(8, b'\x00')
    val = int.from_bytes(test, 'big')
    L, R = (val >> 32) & 0xFFFFFFFF, val & 0xFFFFFFFF
    print(f"  L(0) = 0x{L:08X}, R(0) = 0x{R:08X}")
    F = cipher._shift_right(R, cipher.params[0])
    print(f"  F(R, V1) = 0x{F:08X} (сдвиг на {cipher.params[0]})")
    print(f"  L(1) = 0x{R:08X}, R(1) = 0x{L ^ F:08X}")

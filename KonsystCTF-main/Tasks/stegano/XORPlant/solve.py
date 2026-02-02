import zlib
import hashlib

def main():
    # Шаг 1: Извлекаем CRC32 из plant.jpg
    with open("plant.jpg", "rb") as f:
        crc_key = zlib.crc32(f.read()) & 0xFFFFFFFF
    print(f"[+] CRC32 ключ: {hex(crc_key)}")

    # Шаг 2: Расшифровываем data.bin
    with open("data.bin", "rb") as f:
        encrypted = f.read()
    
    key_bytes = crc_key.to_bytes(4, "big")
    decrypted = bytes([b ^ key_bytes[i % 4] for i, b in enumerate(encrypted)])
    coordinates = decrypted.decode()
    print(f"[+] Координаты: {coordinates}")

    # Шаг 3: Получаем пароль архива
    password = hashlib.sha256(coordinates.encode()).hexdigest()
    print(f"[+] Пароль: {password}")

    # Шаг 4: Открываем архив (вручную)
    print(f"Выполните: unzip -P '{password}' vault.zip")

if __name__ == "__main__":
    main()

import re
import sys
from collections import Counter
'''
def cleaning(raw_text):
    text = raw_text.lower()
    text = text.replace("ё", "е")
    cleaned_text = re.sub(r"[^а-я]", "", text)
    return cleaned_text

input = "crypto_lab2.txt"
cleaned_text = "crypto_lab2_cleaned.txt"
with open(input, 'r', encoding='utf-8') as input_file:
    raw_text = input_file.read()
    cleanedtext = cleaning(raw_text)
    with open(cleaned_text, 'w', encoding='utf-8') as cleaned_file:
        cleaned_file.write(cleanedtext)
'''

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
mod32 = len(alphabet)
char_to_num = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27, 'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
num_to_char = {0: 'а', 1: 'б', 2: 'в', 3: 'г', 4: 'д', 5: 'е', 6: 'ж', 7: 'з', 8: 'и', 9: 'й', 10: 'к', 11: 'л', 12: 'м', 13: 'н', 14: 'о', 15: 'п', 16: 'р', 17: 'с', 18: 'т', 19: 'у', 20: 'ф', 21: 'х', 22: 'ц', 23: 'ч', 24: 'ш', 25: 'щ', 26: 'ъ', 27: 'ы', 28: 'ь', 29: 'э', 30: 'ю', 31: 'я'}



def encrypt(plaintext, key):
    """Шифрує текст шифром Віженера."""
    ciphertext = []
    key_len = len(key) # ex r = 2

    for i, char in enumerate(plaintext):
        text_num = char_to_num[char]
        # (i % key_len) дозволяє циклічно повторювати ключ
        key_char = key[i % key_len]
        key_num = char_to_num[key_char]

        #Формула шифрування  yi(xi + ki mod r)mod32 :
        cipher_num = (text_num + key_num) % mod32
        ciphertext.append(num_to_char[cipher_num])
    return "".join(ciphertext)

def decrypt(ciphertext,key):
    """Розшифровує текст шифром Віженера."""
    plaintext = []
    key_len = len(key)

    for i, char in enumerate(ciphertext):
        cipher_num = char_to_num[char]
        key_char = key[i % key_len]
        key_num = char_to_num[key_char]
        # 3. Формула розшифрування: P = (C - K + M) mod M
        #(додаємо M, щоб уникнути від'ємних чисел)
        text_num = (cipher_num - key_num + mod32) % mod32
        plaintext.append(num_to_char[text_num])
    return "".join(plaintext)

clean_text = "crypto_lab2_cleaned.txt"
with open(clean_text, 'r', encoding='utf-8') as f:
    plaintext = f.read()
#    (r = 2, 3, 4, 5 та 10-20 символів)
keys = {
    "r2": "да",
    "r3": "три",
    "r4": "сила",
    "r5": "атака",
    "r10": "безопасность",
    "r11": "секретность",
    "r12": "криптография",
    "r13": "полиалфавитный",
    "r14": "статистический",
    "r15": "автокорреляция",
    "r16": "частотныйанализ",
    "r17": "расшифровывание",
    "r18": "криптографический",
    "r19": "вероятностнаямодель",
    "r20": "методстатистического"
}
for name, key in keys.items():
    ciphertext = encrypt(plaintext, key)
    output_file = f"encrypted_{name}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(ciphertext)

def calculate_theoretical_ic(probabilities):
    ic_sum = 0.0
    for char in alphabet:
        p_i = probabilities.get(char, 0.0)
        # Формула: Σ(p_i^2)
        ic_sum += p_i * p_i
    return ic_sum
lab1_freqs = {'о': 0.1070699374,'е': 0.08844015904,'и': 0.08184988717,'а': 0.07004874808,'т': 0.06974981194,'н': 0.06765530514,'с': 0.05534421617,'в': 0.04840420855,'р': 0.0428690054,'л': 0.03897306644,'м': 0.03513183474,'д': 0.02860994695,'к': 0.02667760812,'п': 0.02635717984,'у': 0.02372341569,'я': 0.02304152868,'ы': 0.02209978215,'ь': 0.01992321444,'б': 0.01607416742,'з': 0.01585533835,'ч': 0.01560134033,'г': 0.01502691402,'й': 0.01085157723,'ж': 0.01042564208,'х': 0.008901653918,'ю': 0.007991168684,'ш': 0.007438234518,'ц': 0.00515420611,'э': 0.00457977803,'щ': 0.003774801442,'ф': 0.002356320155}
theoretical_ic = calculate_theoretical_ic(lab1_freqs)
print(theoretical_ic)
random_ic = 0.3125  # 1/32 чим довший шифртекст тим ближчим до цього рендомного значення буде наше практичне Ic.
print(random_ic)
def calculate_ic(text):
    """
    Обчислює індекс відповідності (IC)
    Формула: I(Y) = (1 / (N * (N-1))) * sum(n_i t * (n_i t - 1))
    де n_i - кількість входжень i-ї літери,
    N - загальна довжина тексту.
    """
    N = len(text)

    if N < 2:
        return 0.0
    frequencies = Counter(text)
    ic_sum = 0
    for char in alphabet:
        n_i = frequencies.get(char, 0)
        ic_sum += n_i * (n_i - 1)
    ic_value = ic_sum / (N * (N - 1))
    return ic_value

files = [
        "crypto_lab2_cleaned.txt", #ВТ
        "encrypted_r2.txt", # Шифртексти
        "encrypted_r3.txt",
        "encrypted_r4.txt",
        "encrypted_r5.txt",
        "encrypted_r10.txt",
        "encrypted_r11.txt",
        "encrypted_r12.txt",
        "encrypted_r13.txt",
        "encrypted_r14.txt",
        "encrypted_r15.txt",
        "encrypted_r16.txt",
        "encrypted_r17.txt",
        "encrypted_r18.txt",
        "encrypted_r19.txt",
        "encrypted_r20.txt"
    ]
for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    ic = calculate_ic(text)
    print(f"{filename}: {ic:.6f}")

def key_len(encryptedtext, maximum_r):
    """
    Знаходить найбільш імовірну довжину ключа,
    обчислюючи середній індекс відповідності для r від 2 до max_r.
    """
    results = {}
    for r in range(2, maximum_r + 1):
        blocks = [""] * r
        for i, char in enumerate(encryptedtext):
            blocks[i % r] += char
        block_ics = []
        for block in blocks:
            block_ics.append(calculate_ic(block))
        avg_ic = sum(block_ics) / len(block_ics)
        results[r] = avg_ic
        print(f"{r}\t| {avg_ic:.5f}")
    return results

def dr_statistics(encryptedtext, maximum_r):
    """
    Обчислює статистику співпадінь D_r для r від 2 до max_r.
    D_r = sum(delta(y_i, y_i+r))
    """
    n = len(encryptedtext)
    results = {}
    for r in range(2, maximum_r + 1):
        sum = 0
        # Проходимо по тексту, порівнюючи y_i та y_i+r
        for i in range(n - r):
            if encryptedtext[i] == encryptedtext[i + r]:
                sum += 1

        results[r] = sum
        print(f"{r} : {sum}")
    return results

var22 = "lab2_var2.txt"
with open(var22, 'r', encoding='utf-8') as f:
    ciphertext = f.read().strip()

maximum_key = 32

dr_results = dr_statistics(ciphertext, maximum_key)

key_len = 14
freq_letter_1 = 'о'
freq_letter_2 = 'е'

blocks = [""] * key_len
for i, char in enumerate(ciphertext):
    blocks[i % key_len] += char

key_1_o = ""
key_2_e = ""

for i in range(key_len):
    block_text = blocks[i]

    # Знаходимо найчастішу літеру 'y*' в блоці
    y_star = Counter(block_text).most_common(1)[0][0]
    y_star_num = char_to_num[y_star]

    # Припущення 1: y* = 'о'
    x_star_1_num = char_to_num[freq_letter_1]
    key_i_num_1 = (y_star_num - x_star_1_num + mod32) % mod32
    key_i_char_1 = num_to_char[key_i_num_1]
    key_1_o += key_i_char_1

    # Припущення 2: y* = 'е'
    x_star_2_num = char_to_num[freq_letter_2]
    key_i_num_2 = (y_star_num - x_star_2_num + mod32) % mod32
    key_i_char_2 = num_to_char[key_i_num_2]
    key_2_e += key_i_char_2

    #print(f"{i:<4} | {y_star}  | {key_i_char_1:<10} | {key_i_char_2}")

print(f"Ключ1 ('о') : {key_1_o}")
print(f"Ключ2 ('е') : {key_2_e}")

key = "последнийдозор"
print(f"Ключ: {key} (довжина {len(key)})")

decrypted_text = decrypt(ciphertext, key)

result = "lab2_var2_solved.txt"
with open(result, 'w', encoding='utf-8') as file:
       file.write(decrypted_text)
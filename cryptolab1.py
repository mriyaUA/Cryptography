import re
import math
from collections import Counter


def cleaning(text):
    text = text.lower()
    text = text.replace("ё", "е").replace("ъ", "ь")
    text = re.sub(r"[^а-я ]", " ", text)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def cleanspaces(text):
    text = cleaning(text).replace(" ", "")
    return text


book = open("lab1crypto.txt", 'r', encoding='utf-8')
cleanedbook = book.read()
withspaces = cleaning(cleanedbook)
nospaces = cleanspaces(cleanedbook)
book.close()

with open("lab1crypto_spaces.txt", 'w', encoding='utf-8') as writebook1:
    writebook1.write(withspaces)
    writebook1.close()

with open("lab1crypto_nospaces.txt", 'w', encoding='utf-8') as writebook2:
    writebook2.write(nospaces)
    writebook2.close()


def letter_counter(text):
    letters = set(text)
    count = {}
    for letter in letters:
        count[letter] = text.count(letter)
    #print(letters)
    return count


withspaces_count = letter_counter(withspaces)
nospaces_count = letter_counter(nospaces)

print(f"Кількість букв (з пробілами)#####: {withspaces_count}\n")
print(f"Кількість букв (без пробілів)#####: {nospaces_count}\n")


def bigram_count(text, step):
    if step == 1:
        bigram = [text[i:i+2] for i in range(len(text) - 1)]
    elif step == 2:
        bigram = [text[i:i+2] for i in range(0, len(text) - 1, 2)]
    else:
        return

    return dict(Counter(bigram))


b_withspaces = bigram_count(withspaces, 1)
b_nospaces = bigram_count(nospaces, 1)
b2_withspaces = bigram_count(withspaces, 2)
b2_nospaces = bigram_count(nospaces, 2)

print(f"Кількість букв біграм (з пробілами)#####: {b_withspaces}\n")
print(f"Кількість букв біграм (без пробілів)#####: {b_nospaces}\n")

print(f"Кількість букв біграм з кроком 2 (з пробілами)#####: {b2_withspaces}\n")
print(f"Кількість букв біграм з кроком 2 (без пробілів)#####: {b2_nospaces}\n")


def frequent_count(el_count, text, step=0):
    freq = {}
    text_length = len(text)

    if step == 0:
        text_length = len(text)
    elif step == 1:
        text_length -= 1
    elif step == 2:
        text_length //= 2
    else:
        return

    for el, val in el_count.items():
        p = val / text_length
        freq[el] = p

    return freq


#H1 with, w/o spaces
freq_h1_spaces = frequent_count(withspaces_count, withspaces)
print(f"Частота монограм (з пробілами)#####: {freq_h1_spaces}\n")

freq_h1_nospaces = frequent_count(withspaces_count, nospaces)
print(f"Частота монограм (без пробілів)#####: {freq_h1_nospaces}\n")

#H2 with, w/o spaces 1 step
freq_h2b1_spaces = frequent_count(b_withspaces, withspaces, 1)
print(f"Частота біграм (з пробілами)#####: {freq_h2b1_spaces}\n")

freq_h2b1_nospaces = frequent_count(b_nospaces, nospaces, 1)
print(f"Частота біграм (без пробілів)#####: {freq_h2b1_nospaces}\n")

#H2 with, w/o spaces 2 step
freq_h2b2_spaces = frequent_count(b2_withspaces, withspaces, 2)
print(f"Частота біграм (з пробілами, крок 2)#####: {freq_h2b2_spaces}\n")

freq_h2b2_nospaces = frequent_count(b2_nospaces, nospaces, 2)
print(f"Частота біграм (без пробілів, крок 2)#####: {freq_h2b2_nospaces}\n")


def entropy(el_count, text, step=0):
    H = 0
    text_length = len(text)

    if step == 0:
        text_length = len(text)
    elif step == 1:
        text_length -= 1
    elif step == 2:
        text_length //= 2
    else:
        return

    for val in el_count.values():
        p = val / text_length
        H -= p * math.log2(p)

    return H


#H1 with, w/o spaces
H_withspaces = entropy(withspaces_count, withspaces)

H_nospaces = entropy(nospaces_count, nospaces)

#H2 with, w/o spaces 1 step
H2_withspaces = entropy(b_withspaces, withspaces, 1)
H2_withspaces /= 2

H2_nospaces = entropy(b_nospaces, nospaces, 1)
H2_nospaces /= 2

#H2 with, w/o spaces 2 step
H2_step2_withspaces = entropy(b2_withspaces, withspaces, 2)
H2_step2_withspaces /= 2

H2_step2_nospaces = entropy(b2_nospaces, nospaces, 2)
H2_step2_nospaces /= 2


def surplus_count(text, entropy_spaces):
    elements_range = set("".join(text.keys()))
    length_elements = len(elements_range)
    print(elements_range, length_elements)
    h0 = math.log2(length_elements)
    surplus = 1 - (entropy_spaces / h0)
    print(f"Максимальна ентропія: {h0}")
    print(f"Надлишковість: {surplus}\n")


print(f"Ентропія (з пробілами)#####: {H_withspaces}")
surplus_count(withspaces_count, H_withspaces)
print(f"Ентропія (без пробілів)#####: {H_nospaces}")
surplus_count(nospaces_count, H_nospaces)

print(f"Ентропія біграм (з пробілами): {H2_withspaces}")
surplus_count(b_withspaces, H2_withspaces)
print(f"Ентропія біграм (без пробілів): {H2_nospaces}")
surplus_count(b_nospaces, H2_nospaces)

print(f"Ентропія біграм з кроком 2 (з пробілами): {H2_step2_withspaces}")
surplus_count(b2_withspaces, H2_step2_withspaces)
print(f"Ентропія біграм з кроком 2 (без пробілів): {H2_step2_nospaces}")
surplus_count(b2_nospaces, H2_step2_nospaces)



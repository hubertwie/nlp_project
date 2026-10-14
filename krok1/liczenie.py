import re
import csv
from collections import Counter


def process_swedish_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    text = text.lower()
    words = re.findall(r"[a-zåäö]+", text)

    return words


file_name = "pg57052.txt"
try:
    print("Przetwarzanie tekstu...")
    clean_words = process_swedish_text(file_name)
    word_frequencies = Counter(clean_words)

    print(
        f"Znaleziono {len(clean_words)} słów (w tym {len(word_frequencies)} unikalnych)."
    )

    with open("slowa_czestotliwosc.csv", "w", encoding="utf-8", newline="") as file1:
        writer = csv.writer(file1)
        writer.writerow(["Slowo", "Liczba_wystapien"])
        for word, count in word_frequencies.most_common():
            writer.writerow([word, count])

    print("Zapisano plik: slowa_czestotliwosc.csv")

    with open("slowa_alfabetycznie.csv", "w", encoding="utf-8", newline="") as file2:
        writer = csv.writer(file2)
        writer.writerow(["Slowo", "Liczba_wystapien"])
        words_alphabetical = sorted(word_frequencies.items(), key=lambda x: x[0])

        for word, count in words_alphabetical:
            writer.writerow([word, count])

    print("Zapisano plik: slowa_alfabetycznie.csv")

except FileNotFoundError:
    print(f"Błąd: Nie znaleziono pliku '{file_name}'.")

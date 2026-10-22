import csv
import re
from collections import Counter
from pathlib import Path


class WordCounter:
    def __init__(self, input_file: str | Path | None = None):
        self.input_file = (
            Path(input_file)
            if input_file is not None
            else Path(__file__).resolve().parent / "pg57052.txt"
        )
        self.words = []
        self.word_frequencies = Counter()

    @staticmethod
    def tokenize(text: str):
        text = text.lower()
        return re.findall(r"[a-zåäö]+", text)

    def process_text(self):
        with open(self.input_file, "r", encoding="utf-8") as file:
            text = file.read()

        self.words = self.tokenize(text)
        self.word_frequencies = Counter(self.words)
        return self.words

    def save_frequency_csvs(
        self,
        frequency_file="slowa_czestotliwosc.csv",
        alphabetical_file="slowa_alfabetycznie.csv",
    ):
        with open(frequency_file, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Slowo", "Liczba_wystapien"])
            writer.writerows(self.word_frequencies.most_common())

        with open(alphabetical_file, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Slowo", "Liczba_wystapien"])
            writer.writerows(sorted(self.word_frequencies.items()))

    def save_nodes_csv(self, output_file="slowa_nody.csv"):
        with open(output_file, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Pozycja", "Slowo"])
            writer.writerows(
                (position, word) for position, word in enumerate(self.words, start=1)
            )

    def run(self):
        print("Przetwarzanie tekstu...")
        self.process_text()
        print(
            f"Znaleziono {len(self.words)} słów "
            f"(w tym {len(self.word_frequencies)} unikalnych)."
        )

        self.save_frequency_csvs()
        self.save_nodes_csv()
        print("Zapisano plik: slowa_czestotliwosc.csv")
        print("Zapisano plik: slowa_alfabetycznie.csv")
        print("Zapisano plik: slowa_nody.csv")


if __name__ == "__main__":
    try:
        WordCounter().run()
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku 'pg57052.txt'.")

import re
import csv as sc
import pandas as pd


class FrequencyCounter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.all_letters_count = 0
        self.letter_counts = {}
        self.letter_frequencies = {}

    def process_text(self):
        df = pd.read_csv(self.file_path, encoding="utf-8")
        for row in df.itertuples():
            word = getattr(row, "Slowo", "")
            count = getattr(row, "Liczba_wystapien", 1)
            for letter in word:
                if self.letter_counts.get(letter) is None:
                    self.letter_counts[letter] = 0
                self.letter_counts[letter] += count
                self.all_letters_count += count
        for letter, count in self.letter_counts.items():
            self.letter_frequencies[letter] = count / self.all_letters_count

    def save_to_csv(self, output_file):
        with open(output_file, "w", encoding="utf-8", newline="") as file:
            writer = sc.writer(file)
            writer.writerow(["Litera", "Liczba_wystapien", "Frekwencja"])
            for letter in self.letter_frequencies:
                writer.writerow(
                    [
                        letter,
                        self.letter_counts[letter],
                        self.letter_frequencies[letter],
                    ]
                )

    def get_attributes(self):
        return self.all_letters_count, self.letter_counts, self.letter_frequencies

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ZipfLawChecker:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.ranks = np.arange(1, len(self.df) + 1)
        self.word_counts = self.df["Liczba_wystapien"].values
        self.frequencies = self.word_counts / np.sum(self.word_counts)
        self.log_ranks = np.log(self.ranks)
        self.log_frequencies = np.log(self.frequencies)

    def plot(self):
        plt.scatter(self.log_ranks, self.log_frequencies)
        plt.xlabel("log(rank)")
        plt.ylabel("log(frequency)")
        plt.savefig("zipf_law_plot.png")
        plt.close()
        print(
            "Wykres zależności log(rank) od log(frequency) został zapisany jako zipf_law_plot.png."
        )

    def check(self):
        coefficients = np.polyfit(self.log_ranks, self.log_frequencies, 1)
        slope = coefficients[0]
        intercept = coefficients[1]
        return slope, intercept

    def score(self, slope, intercept):
        return np.mean((self.log_frequencies - slope * self.log_ranks - intercept) ** 2)

    def is_zipf_law_satisfied(self, slope, score):
        return -1.2 <= slope <= -0.8 and score <= 0.1

    def print_zipf_assessment(self, slope, score):
        if self.is_zipf_law_satisfied(slope, score):
            print("Wniosek: prawo Zipfa jest spełnione dla badanego tekstu.")
        else:
            print("Wniosek: prawo Zipfa nie jest spełnione dla badanego tekstu.")

    def cumulative_frequencies(self):
        sorted_counts = np.sort(self.word_counts)[::-1]
        return np.cumsum(sorted_counts) / np.sum(sorted_counts)

    def words_for_coverage(self, coverage=0.9):
        if not 0 < coverage <= 1:
            raise ValueError("Pokrycie musi być większe od 0 i nie większe niż 1.")

        sorted_data = (
            self.df.groupby("Slowo", as_index=False)["Liczba_wystapien"]
            .sum()
            .sort_values(by="Liczba_wystapien", ascending=False)
        )
        total_count = sorted_data["Liczba_wystapien"].sum()
        cumulative_count = 0
        words = []

        for _, row in sorted_data.iterrows():
            words.append(row["Slowo"])
            cumulative_count += row["Liczba_wystapien"]
            if cumulative_count / total_count >= coverage:
                break

        return words

    def print_words_for_coverage(self, coverage=0.9):
        words = self.words_for_coverage(coverage)
        print(
            f"Słowa pokrywające {coverage:.0%} tekstu ({len(words)} unikalnych słów):"
        )
        print(", ".join(words))
        with open("words_for_coverage.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(words))
        print("Słowa zostały zapisane do pliku 'words_for_coverage.txt'.")
        return words

    def plot_fit(self, slope, intercept):
        plt.scatter(self.log_ranks, self.log_frequencies)
        plt.plot(self.log_ranks, slope * self.log_ranks + intercept, color="red")
        plt.xlabel("log(rank)")
        plt.ylabel("log(frequency)")
        plt.savefig("zipf_law_fit.png")
        plt.close()
        print("Wykres dopasowania został zapisany jako zipf_law_fit.png.")

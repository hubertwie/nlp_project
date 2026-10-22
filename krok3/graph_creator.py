import csv
import json
from collections import Counter


class GraphCreator:
    def __init__(self, nodes_file):
        self.nodes_file = nodes_file
        self.words = []
        self.graph = {}

    def read_nodes(self):
        with open(self.nodes_file, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != ["Pozycja", "Slowo"]:
                raise ValueError("Plik węzłów musi zawierać kolumny: Pozycja, Slowo")
            return [row["Slowo"] for row in reader]

    def create_graph(self):
        self.words = self.read_nodes()

        word_counts = Counter(self.words)

        self.graph = {
            word: {"prevs": {}, "nexts": {}} for word, _ in word_counts.most_common()
        }

        for i in range(len(self.words) - 1):
            current_word = self.words[i]
            next_word = self.words[i + 1]

            if next_word not in self.graph[current_word]["nexts"]:
                self.graph[current_word]["nexts"][next_word] = 0
            self.graph[current_word]["nexts"][next_word] += 1

            if current_word not in self.graph[next_word]["prevs"]:
                self.graph[next_word]["prevs"][current_word] = 0
            self.graph[next_word]["prevs"][current_word] += 1

        for _, data in self.graph.items():
            data["prevs"] = dict(
                sorted(data["prevs"].items(), key=lambda item: item[1], reverse=True)
            )
            data["nexts"] = dict(
                sorted(data["nexts"].items(), key=lambda item: item[1], reverse=True)
            )

    def save_to_json(self, output_file="slowa_sasiedztwo.json"):
        if not self.graph:
            self.create_graph()

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(self.graph, file, ensure_ascii=False, indent=4)

    def get_language_core(self, size=100):
        if not self.graph:
            self.create_graph()
        if size <= 0:
            raise ValueError("Rozmiar rdzenia musi być większy od zera.")
        if len(self.graph) < size:
            raise ValueError(
                f"Graf zawiera mniej niż {size} węzłów i nie można utworzyć rdzenia."
            )

        return [
            word
            for word, _ in sorted(
                self.graph.items(),
                key=lambda item: len(item[1]["nexts"]),
                reverse=True,
            )[:size]
        ]

    def save_language_core(self, output_file="rdzen_jezyka.json", size=100):
        language_core = self.get_language_core(size)
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(language_core, file, ensure_ascii=False, indent=4)
        print(f"Rdzeń języka został zapisany do pliku '{output_file}'.")
        return language_core

    def print_language_core(self, size=100):
        language_core = self.get_language_core(size)
        print(f"Rdzeń języka ({len(language_core)} węzłów):")
        print(", ".join(language_core))
        return language_core

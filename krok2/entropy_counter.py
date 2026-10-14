import math
import heapq
from itertools import count


class EntropyHuffmanCounter:
    def __init__(self, letter_frequencies, all_letters_count):
        self.letter_frequencies = {
            letter: frequency
            for letter, frequency in letter_frequencies.items()
            if frequency > 0
        }
        self.all_letters_count = all_letters_count

    def calculate_entropy(self):
        if not self.letter_frequencies:
            return 0

        return -sum(
            frequency * math.log2(frequency)
            for frequency in self.letter_frequencies.values()
        )

    def calculate_codes(self):
        """Return a binary Huffman code for every symbol."""
        if not self.letter_frequencies:
            return {}

        sequence = count()
        heap = [
            (frequency, next(sequence), letter)
            for letter, frequency in self.letter_frequencies.items()
        ]
        heapq.heapify(heap)

        if len(heap) == 1:
            return {heap[0][2]: "0"}

        while len(heap) > 1:
            left_frequency, _, left = heapq.heappop(heap)
            right_frequency, _, right = heapq.heappop(heap)
            heapq.heappush(
                heap,
                (
                    left_frequency + right_frequency,
                    next(sequence),
                    (left, right),
                ),
            )

        codes = {}

        def walk(node, prefix):
            if isinstance(node, str):
                codes[node] = prefix
                return
            left, right = node
            walk(left, prefix + "0")
            walk(right, prefix + "1")

        walk(heap[0][2], "")
        return codes

    def calculate_code_average_length(self):
        codes = self.calculate_codes()
        return sum(
            self.letter_frequencies[letter] * len(code)
            for letter, code in codes.items()
        )

    def calculate_efficiency(self):
        average_length = self.calculate_code_average_length()
        if average_length == 0:
            return 0
        return self.calculate_entropy() / average_length * 100
from entropy_huffman_counter import EntropyHuffmanCounter
from frequency_counter import FrequencyCounter

def main():
    input_file = "../krok1/slowa_czestotliwosc.csv"
    output_file = "litery_frekwencja.csv"

    frequency_counter = FrequencyCounter(input_file)
    frequency_counter.process_text()
    frequency_counter.save_to_csv(output_file)

    all_letters_count, letter_counts, letter_frequencies = frequency_counter.get_attributes()

    entropy_huffman_counter = EntropyHuffmanCounter(letter_frequencies, all_letters_count)
    entropy = entropy_huffman_counter.calculate_entropy()
    codes = entropy_huffman_counter.calculate_codes()

    print(f"Entropy: {entropy}")
    print("Huffman Codes:")
    for letter, code in codes.items():
        print(f"{letter}: {code}")
    print(f"Average Code Length: {entropy_huffman_counter.calculate_code_average_length()}")
    print(f"Efficiency: {entropy_huffman_counter.calculate_efficiency():.2f}%")

if __name__ == "__main__":
    main()
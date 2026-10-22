from graph_creator import GraphCreator
from zipf_law_checker import ZipfLawChecker


def main():
    zipf_checker = ZipfLawChecker("../krok1/slowa_czestotliwosc.csv")
    zipf_checker.plot()
    slope, intercept = zipf_checker.check()
    print(f"Współczynnik kierunkowy: {slope}, wyraz wolny: {intercept}")
    score = zipf_checker.score(slope, intercept)
    print(f"Średni błąd kwadratowy dopasowania: {score}")
    zipf_checker.print_zipf_assessment(slope, score)
    zipf_checker.print_words_for_coverage()
    zipf_checker.plot_fit(slope, intercept)
    graph_creator = GraphCreator("../krok1/slowa_nody.csv")
    graph_creator.create_graph()
    graph_creator.save_to_json()
    graph_creator.save_language_core()
    graph_creator.print_language_core()
    print("Zapisano graf: slowa_sasiedztwo.json")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("Błąd: Najpierw uruchom krok 1, aby utworzyć plik slowa_nody.csv.")

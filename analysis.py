"""
Driver Risk by Age & Gender — Heatmap
=====================================

Wizualizacja statystyczna wskaznika smiertelnosci (Fatal %) w podziale
na grupe wiekowa oraz plec kierowcy. Wykres stanowi czesc projektu
analizy bezpieczenstwa ruchu drogowego w Wielkiej Brytanii (2010-2017).

Skrypt powstal pierwotnie jako wizual Python wewnatrz Power BI (gdzie
ramka danych jest automatycznie dostarczana jako `dataset`). Ponizsza
wersja jest samodzielna i wczytuje dane z pliku CSV, dzieki czemu mozna
ja uruchomic poza Power BI.

Wymagane kolumny w danych wejsciowych:
    - Age_Band_of_Driver : przedzial wiekowy kierowcy (np. "26 - 35")
    - Sex_of_Driver : plec kierowcy (np. "Male", "Female")
    - Fatal % : wskaznik smiertelnosci dla danego rekordu

Autor: Igor Kozak
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def plot_risk_heatmap(dataset: pd.DataFrame):
    """Rysuje heatmape wskaznika smiertelnosci wg wieku i plci kierowcy."""

    # Tabela przestawna: srednia Fatal % dla kazdej kombinacji wiek x plec
    pivot = dataset.pivot_table(
        values="Fatal %",
        index="Age_Band_of_Driver",
        columns="Sex_of_Driver",
        aggfunc="mean",
    )

    fig = plt.figure(figsize=(6, 4), facecolor="none")
    ax = sns.heatmap(
        data=pivot.sort_index(),
        annot=True,
        fmt=".1%",
        cmap="Blues",
        linewidths=0.5,
        linecolor="white",
    )

    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    plt.title("Driver Risk by Age & Gender", fontsize=12)
    plt.xlabel("Gender")
    plt.ylabel("Age Group")
    plt.tight_layout()

    return fig


if __name__ == "__main__":
    # Podmien sciezke na swoj plik z danymi
    # (eksport z modelu lub przygotowany CSV z kolumnami wymienionymi powyzej)
    dataset = pd.read_csv("data/driver_risk.csv")

    plot_risk_heatmap(dataset)
    plt.show()

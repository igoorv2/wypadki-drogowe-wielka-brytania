# wypadki-drogowe-wielka-brytania
# 🚗 UK Road Accidents — Hurtownia Danych & Dashboard Analityczny

> Kompleksowa hurtownia danych oraz interaktywny dashboard w Power BI, analizujący czynniki wpływające na śmiertelność w wypadkach drogowych w Wielkiej Brytanii w latach **2010–2017**.

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat&logo=latex&logoColor=white)
![Status](https://img.shields.io/badge/status-completed-success)

---

## 📋 Spis treści

- [Cel projektu](#-cel-projektu)
- [Pytania analityczne](#-pytania-analityczne)
- [Stack technologiczny](#-stack-technologiczny)
- [Dane i proces ETL](#-dane-i-proces-etl)
- [Architektura i model danych](#-architektura-i-model-danych)
- [Miary DAX](#-miary-dax)
- [Dashboard](#-dashboard)
- [Kluczowe wnioski](#-kluczowe-wnioski)
- [Struktura repozytorium](#-struktura-repozytorium)
- [Autor](#-autor)

---

## 🎯 Cel projektu

Głównym celem było zaprojektowanie i wdrożenie kompleksowej hurtowni danych oraz interaktywnego dashboardu w środowisku **Power BI**. Analiza skupia się na identyfikacji kluczowych czynników wpływających na śmiertelność w wypadkach drogowych w Wielkiej Brytanii.

Finalny zbiór danych obejmuje:

| Metryka | Wartość |
|---|---|
| 🚦 Zdarzenia drogowe | **1,10 mln** |
| 🤕 Poszkodowani | **1,48 mln** |
| 🚙 Pojazdy | **2,03 mln** |
| 📅 Zakres czasowy | **2010–2017** |

---

## ❓ Pytania analityczne

1. Jak zmieniała się liczba wypadków drogowych w latach 2010–2017?
2. Jakie warunki pogodowe i drogowe najbardziej zwiększają ryzyko śmiertelnych wypadków?
3. Czy jazda nocą wpływa na wzrost wskaźnika śmiertelności?
4. Które grupy kierowców są najbardziej narażone na śmiertelne wypadki?
5. Jakie typy pojazdów charakteryzują się najwyższym poziomem ryzyka?
6. Czy Londyn jest bezpieczniejszy pod względem śmiertelności niż pozostałe regiony?

---

## 🛠 Stack technologiczny

- **Power BI** (Power Query, DAX) — główny silnik raportowy, procesy ETL oraz modelowanie danych
- **Python** (Seaborn, Matplotlib) — wizualizacja statystyczna korelacji między wiekiem a ryzykiem wypadku
- **LaTeX** — dokumentacja techniczna projektu

---

## 🔄 Dane i proces ETL

**Źródło danych:** [UK Road Safety: Traffic Accidents and Vehicles (Kaggle)](https://www.kaggle.com/datasets/tsiaras/uk-road-safety-accidents-and-vehicles)

Oryginalny zbiór (lata 2005–2017) zawężono do okresu **2010–2017** w celu skupienia się na najbardziej aktualnych trendach i zapewnienia spójności czasowej.

Proces **ETL (Extract, Transform, Load)** obejmował:

- **Zarządzanie brakami** — eliminacja rekordów `Unknown` i `Data missing` (znikomy odsetek całości)
- **Transformacja** — ujednolicenie typów danych (daty, liczby, tekst)
- **Selekcja kolumn** — usunięcie nieprzydatnych atrybutów (np. technicznych identyfikatorów) w celu redukcji rozmiaru modelu i poprawy wydajności zapytań
- **Inżynieria cech** — stworzenie flag logicznych (np. *czy weekend*) oraz scalanie zapytań

> ⚠️ **Uwaga:** surowe dane z Kaggle nie są dołączone do repozytorium ze względu na licencję oraz rozmiar. Aby odtworzyć projekt, pobierz je z linku powyżej.

---

## 🏗 Architektura i model danych

Projekt oparto na **Schemacie Gwiazdy (Star Schema)**, zapewniającym wysoką wydajność obliczeniową i klarowność raportowania. Ze względu na relację wiele-do-wielu (jeden wypadek może obejmować wiele pojazdów i kierowców), zastosowano **tabelę mostu (Bridge Table)**.

![Star Schema](docs/star_schema.png)

**Struktura tabel:**

| Tabela | Typ | Opis |
|---|---|---|
| `Fact_Accident` | Fakt | Centralna tabela; granularność = pojedyncze zdarzenie drogowe (`Accident_ID`) |
| `DimDate` | Wymiar | Data, rok, kwartał, miesiąc, dzień tygodnia |
| `DimLocation` | Wymiar | Dane przestrzenne miejsca wypadku |
| `DimWeather` | Wymiar | Warunki pogodowe |
| `DimLight` | Wymiar | Warunki oświetleniowe |
| `DimRoadSurface` | Wymiar | Stan i rodzaj nawierzchni |
| `DimSeverity` | Wymiar | Powaga zdarzenia: *Slight / Serious / Fatal* |
| `DimDriver` | Wymiar | Profil kierowcy (wiek, płeć) |
| `DimVehicle` | Wymiar | Charakterystyka pojazdu |
| `Bridge_VehicleDriver` | Most | Relacja M:N między zdarzeniem a profilami pojazdów/kierowców |

---

## 📐 Miary DAX

Przykładowe wskaźniki efektywności (KPI) zaimplementowane w języku DAX:

```dax
Total Accidents =
COUNT ( Fact_Accident[Accident_ID] )
```

```dax
Fatal Accidents =
CALCULATE (
    [Total Accidents],
    DimSeverity[Accident_Severity] = "Fatal"
)
```

```dax
Fatal % =
DIVIDE ( [Fatal Accidents], [Total Accidents] )
```

```dax
Fatal Night =
CALCULATE (
    [Fatal %],
    DimLight[Light_Group] = "Night"
)
```

---

## 📊 Dashboard

Interaktywny raport podzielono na **cztery sekcje**:

### 1️⃣ Overview
Ogólna analiza bezpieczeństwa ruchu. KPI umożliwiają szybką ocenę liczby wypadków, pojazdów i poziomu śmiertelności. Trend czasowy wskazuje na stopniowy spadek liczby wypadków.

![Overview](images/overview.png)

### 2️⃣ Conditions Analysis
Wpływ warunków pogodowych, nawierzchni i oświetlenia na śmiertelność. Najwyższy wskaźnik występuje podczas mgły oraz jazdy nocnej.

![Conditions Analysis](images/conditions.png)

### 3️⃣ Driver & Vehicle
Zależności między profilem kierowcy, typem pojazdu a ryzykiem. Najbardziej narażeni są mężczyźni 75+, a najwyższe ryzyko wśród pojazdów mają pojazdy typu *Goods*.

![Driver & Vehicle](images/driver_vehicle.png)

### 4️⃣ Location Analysis
Przestrzenny rozkład wypadków. Londyn generuje znaczną część zdarzeń, ale przy niższym wskaźniku śmiertelności niż reszta kraju.

![Location Analysis](images/location.png)

---

## 💡 Kluczowe wnioski

- **🧓 Spadek bezpieczeństwa u seniorów** — mężczyźni 75+ mają najwyższy wskaźnik śmiertelności (**2,6%**). *Rekomendacja: cykliczne badania psychomotoryczne dla kierowców po 70. roku życia.*
- **🌆 Paradoks Londynu** — stolica generuje **17,4%** zdarzeń, lecz śmiertelność jest tam niższa o **0,81%**. *Rekomendacja: adaptacja londyńskich rozwiązań infrastrukturalnych na obszary wiejskie.*
- **🌫 Mgła jako główny winowajca** — mimo że najwięcej wypadków dzieje się przy dobrej pogodzie, mgła niesie najwyższe ryzyko zgonu (**2,08%**). *Rekomendacja: systemy ostrzegania na drogach wysokiego ryzyka.*
- **🚚 Niebezpieczny transport** — pojazdy *Goods* mają najwyższy wskaźnik śmiertelności (**4,58%**). *Rekomendacja: zaostrzenie wymogów technicznych i kontroli.*
- **📉 Skuteczność długofalowa** — w latach 2010–2017 liczba wypadków spadła o **19%**. *Rekomendacja: kontynuacja programów bezpieczeństwa, szczególnie na obszarach wiejskich i w nocy.*

> Analiza potwierdza, że bezpieczeństwo ruchu drogowego jest zjawiskiem wieloczynnikowym. Najskuteczniejsze działania prewencyjne powinny koncentrować się na grupach wysokiego ryzyka: seniorach, kierowcach pojazdów ciężkich oraz osobach prowadzących nocą w warunkach ograniczonej widoczności.

---

## 👤 Autor

**Igor Kozak**
Projekt zrealizowany w ramach przedmiotu *Hurtownie danych i systemy analizy danych*
Czerwiec 2026


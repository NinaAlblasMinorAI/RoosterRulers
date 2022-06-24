# Mijn Project

In deze case moet een weekrooster gemaakt worden voor een vakkenlijst op Science Park.
- Vakken bestaan uit hoorcolleges en/of werkcolleges en/of practica. Er zijn maximumaantallen per werkcollege en practica.
- Er zijn zeven zalen van verschillende groottes, alle zalen zijn voor alle drie collegetypes geschikt.
- Een college duurt van 9:00-11:00, 11:00-13:00, 13:00-15:00 of 15:00-17:00 op een werkdag. Voor de grootste zaal is er een extra avondslot.
- Een geldig weekrooster is een weekrooster waarvoor aan alle roosterbare activiteiten van ieder vak een tijdsslot met een zaal hebben. 
- Een zaalslot kan enkel gebruikt worden voor één activiteit.
- Studenten hebben allemaal een individueel rooster.
Het doel is om een rooster te maken waarin de studenten zo veel mogelijk in de lokalen passen, en met zo min mogelijk avondlessen, roosterconflicten voor studenten en tussenuren.

## Aan de slag (Getting Started)

### Vereisten (Prerequisites)

Deze codebase is volledig geschreven in [Python3.8.10](https://www.python.org/downloads/). In requirements.txt staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip dmv. de volgende instructie:

```
pip install -r requirements.txt
```

### Structuur (Structure)

De files zijn onderverdeeld met de volgende mappen.
- code: alle Python scripts, met subfolders.
    - algorithms
    - classes
    - trash
    - visualization
    
- doc: documenten, zoals presentaties. 
- input_data: de input voor de case.
- output_data: de output die door de code wordt gegenereerd.

### Test (Testing)

Gebruik onderstaande commando om de code te draaien. Als algoritme voor het verdelen van de lessen kan gekozen worden voor random, hillclimber of simulated_annealing. Voor het verdelen van de studenten wordt altijd een hillclimber gebruikt, dus dat hoeft niet gespecificeerd te worden.

```
python main.py <algoritme>
```
Onderstaande opties zijn mogelijk:
- -n -> het aantal runs voor het totale algoritme
- -r -> het aantal repeats voor het algoritme voor het verdelen van de vakken. Voor hillclimber gaat het om het aantal iteraties dat de waarde niet verandert voordat het algoritme stopt, voor simulated annealing gaat het om het totaal aantal iteraties.
- -o -> het aantal repeats voor het verdelen van studenten voor het kiezen van twee lessen dat de score niet verbetert, voordat het algoritme stopt
- -i -> het aantal repeats voor het verdelen van studenten voor het kiezen van twee studenten dat de score niet verbetert, voordat het algoritme stopt
- -t -> de start temperatuur voor simulated annealing
- -v -> verbose -> het printen van extra logging op de command prompt
## Auteurs (Authors)

* Nina Alblas
* Dennis Vlegels
* Marc Jurriens

## Dankwoord (Acknowledgments)

* 
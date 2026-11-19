# Adapter Pattern — Reporting System

[Diagramme de classes UML](uml.md)

`LegacyReportAdapter` implémente `ReportGeneratorInterface.generate(data)`. Il appelle le générateur historique de l’énoncé, analyse le XML obtenu, puis renvoie une chaîne JSON que le tableau de bord peut lire.

```python
from report_adapter import AnalyticsDashboard, LegacyReportAdapter, LegacyReportGenerator

generator = LegacyReportAdapter(LegacyReportGenerator())
AnalyticsDashboard().display(generator.generate({"total_sales": 150000, "orders": 1234}))
```

Le format de l’énoncé est un élément `<report>` avec un champ par enfant direct. Comme le XML ne contient aucune information de type, les valeurs qui représentent des nombres JSON deviennent des nombres, et les autres restent du texte. Un XML mal formé déclenche une erreur de parsing.

Depuis ce dossier, lancer la démonstration des rapports de ventes et de stocks, puis les tests.

```sh
python3 -B report_adapter.py
python3 -B -m unittest -v
```

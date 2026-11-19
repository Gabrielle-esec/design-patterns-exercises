# Builder Pattern — HR Employee Onboarding System

[Diagramme de classes UML](uml.md)

`Employee` est une dataclass qui reprend les 17 champs de l’énoncé. Les méthodes `with_…` configurent un brouillon et retournent le builder pour permettre le chaînage. `build()` vérifie que les deux noms sont renseignés, que l’adresse e-mail a une forme valide et que le salaire est un nombre fini, positif ou nul. Chaque appel retourne une fiche indépendante.

```python
from employee_builder import DeveloperBuilder, EmployeeBuilder

employee = (
    EmployeeBuilder()
    .with_name("John", "Doe")
    .with_email("john.doe@company.com")
    .with_job("Engineering", "Senior Developer", 75_000)
    .with_equipment(laptop=True, parking=False)
    .with_access(vpn=True, admin=True)
    .build()
)

developer = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
```

Le preset reprend le poste, le salaire, le bureau et les accès du développeur de l’énoncé. Les méthodes héritées permettent de personnaliser ces valeurs. La date de début vaut `None` jusqu’à un appel à `with_start_date()`.

Depuis ce dossier, lancer la démonstration et les tests avec Python 3.11 ou plus récent. La démonstration affiche les fiches d’un développeur et d’une stagiaire.

```sh
python3 employee_builder.py
python3 -B -m unittest -v
```

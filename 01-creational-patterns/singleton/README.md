# Singleton Pattern — Basic Configuration Manager

[Diagramme de classes UML](uml.md)

Au premier appel, `ConfigManager.get_instance()` charge le fichier `config.json` situé à côté du module Python. Les appels suivants récupèrent la même instance pendant la durée du processus. Le verrou garantit une initialisation unique lorsque plusieurs threads démarrent en même temps.

```python
from config_manager import ConfigManager

config = ConfigManager.get_instance()
print(config.get("database.host"))  # localhost
print(config.get("app.debug"))      # True
```

`get()` accepte les clés imbriquées séparées par des points et lève `KeyError` si le chemin est introuvable. Les sections renvoyées sont des copies pour protéger la configuration partagée.

Depuis ce dossier, avec Python 3.11 ou plus récent, exécuter la démonstration des quatre services simulés, puis les tests.

```sh
python3 -B demo.py
python3 -B -m unittest -v
```

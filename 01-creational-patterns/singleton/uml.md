# Singleton Pattern — Basic Configuration Manager

```mermaid
classDiagram
    class ConfigManager {
        <<singleton>>
        -_instance$ ConfigManager
        -_lock$ Lock
        -_config dict
        +get_instance()$ ConfigManager
        +get(key: str) object
    }

    class Demo {
        <<module>>
        +start_application()
        +connect_database()
        +send_email(to: str, subject: str)
        +process_payment(amount: float)
    }

    Demo ..> ConfigManager : consulte la configuration partagée
```

Le premier accès charge `config.json`. Le verrou empêche deux appels simultanés de créer chacun leur instance. Les quatre fonctions de la démonstration consultent cette même instance.

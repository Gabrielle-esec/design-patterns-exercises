# Builder Pattern — HR Employee Onboarding System

```mermaid
classDiagram
    class Employee {
        <<dataclass>>
        +str first_name
        +str last_name
        +str email
        +str department
        +str position
        +float salary
        +str start_date
        +int manager_id
        +str phone
        +str address
        +str emergency_contact
        +bool has_parking
        +bool has_laptop
        +bool has_vpn_access
        +bool has_admin_rights
        +str office_location
        +str contract_type
    }

    class EmployeeBuilder {
        -Employee _draft
        +with_name(first_name, last_name) Self
        +with_email(email) Self
        +with_job(department, position, salary) Self
        +with_start_date(start_date) Self
        +with_manager(manager_id) Self
        +with_phone(phone) Self
        +with_address(address) Self
        +with_emergency_contact(emergency_contact) Self
        +with_equipment(laptop, parking) Self
        +with_access(vpn, admin) Self
        +with_office_location(office_location) Self
        +with_contract_type(contract_type) Self
        +build() Employee
    }

    class DeveloperBuilder {
        +DeveloperBuilder(first_name, last_name, email)
    }

    EmployeeBuilder <|-- DeveloperBuilder
    EmployeeBuilder *-- Employee : brouillon
    EmployeeBuilder ..> Employee : retourne une copie validée
    note for Employee "Champs facultatifs à None\nstart_date, manager_id, phone, address, emergency_contact, office_location"
```

`EmployeeBuilder` configure un brouillon, puis `build()` valide ses données et retourne une copie indépendante. `DeveloperBuilder` reprend les mêmes méthodes avec une configuration initiale pour le poste de développeur.

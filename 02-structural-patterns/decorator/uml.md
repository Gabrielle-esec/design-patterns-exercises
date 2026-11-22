# Decorator Pattern — Order Pricing System

```mermaid
classDiagram
    class OrderComponent {
        <<abstract>>
        +get_cost() float
        +get_description() str
        +base_price float
    }
    class BaseOrder
    class OrderDecorator {
        <<abstract>>
        #OrderComponent _order
    }
    class ExpressShippingDecorator
    class InsuranceDecorator
    class GiftWrapDecorator
    class DiscountDecorator {
        -float _percent
    }
    class PremiumMemberDecorator

    OrderComponent <|-- BaseOrder
    OrderComponent <|-- OrderDecorator
    OrderDecorator o-- OrderComponent : enveloppe
    OrderDecorator <|-- ExpressShippingDecorator
    OrderDecorator <|-- InsuranceDecorator
    OrderDecorator <|-- GiftWrapDecorator
    OrderDecorator <|-- DiscountDecorator
    DiscountDecorator <|-- PremiumMemberDecorator
```

Chaque décorateur enveloppe une commande et ajoute une ligne au détail du prix. Le prix de base reste accessible à travers la chaîne pour calculer l’assurance.

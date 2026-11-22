# Decorator Pattern — Order Pricing System

[Diagramme de classes UML](uml.md)

`BaseOrder` fournit le prix initial. Chaque décorateur enveloppe un `OrderComponent`, ajuste son prix et ajoute une ligne à sa description. Une même commande de base peut servir à composer plusieurs variantes.

```python
from order_decorators import (
    BaseOrder,
    DiscountDecorator,
    ExpressShippingDecorator,
    GiftWrapDecorator,
    InsuranceDecorator,
    PremiumMemberDecorator,
)

order = BaseOrder(100.00)
order = ExpressShippingDecorator(order)
order = InsuranceDecorator(order)
order = GiftWrapDecorator(order)
order = DiscountDecorator(order, percent=15)
order = PremiumMemberDecorator(order)
print(order.get_description())
print(f"Total: {order.get_cost():.2f}€")
```

La livraison express coûte 15 €, l’assurance vaut 5 % du prix de base et l’emballage cadeau coûte 5 €. Chaque remise s’applique au sous-total de la commande qu’elle enveloppe. La remise personnalisée accepte de 0 à 100 %, et la remise premium vaut 10 %. Les calculs gardent leur précision jusqu’à l’affichage à deux décimales.

Depuis ce dossier, lancer la démonstration et les tests.

```sh
python3 -B order_decorators.py
python3 -B -m unittest -v
```

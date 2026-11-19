"""Fluent construction of HR onboarding records."""

import math
import re
from dataclasses import dataclass, replace
from typing import Self


@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str | None = None
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self) -> None:
        self._draft = Employee(
            first_name="", last_name="", email="",
            department="", position="", salary=0.0,
        )

    def with_name(self, first_name: str, last_name: str) -> Self:
        self._draft.first_name = first_name
        self._draft.last_name = last_name
        return self

    def with_email(self, email: str) -> Self:
        self._draft.email = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> Self:
        self._draft.department = department
        self._draft.position = position
        self._draft.salary = salary
        return self

    def with_start_date(self, start_date: str | None) -> Self:
        self._draft.start_date = start_date
        return self

    def with_manager(self, manager_id: int | None) -> Self:
        self._draft.manager_id = manager_id
        return self

    def with_phone(self, phone: str | None) -> Self:
        self._draft.phone = phone
        return self

    def with_address(self, address: str | None) -> Self:
        self._draft.address = address
        return self

    def with_emergency_contact(self, emergency_contact: str | None) -> Self:
        self._draft.emergency_contact = emergency_contact
        return self

    def with_equipment(
        self, *, laptop: bool | None = None, parking: bool | None = None
    ) -> Self:
        if laptop is not None:
            self._draft.has_laptop = laptop
        if parking is not None:
            self._draft.has_parking = parking
        return self

    def with_access(
        self, *, vpn: bool | None = None, admin: bool | None = None
    ) -> Self:
        if vpn is not None:
            self._draft.has_vpn_access = vpn
        if admin is not None:
            self._draft.has_admin_rights = admin
        return self

    def with_office_location(self, office_location: str | None) -> Self:
        self._draft.office_location = office_location
        return self

    def with_contract_type(self, contract_type: str) -> Self:
        self._draft.contract_type = contract_type
        return self

    def build(self) -> Employee:
        draft = self._draft
        if any(
            not isinstance(name, str) or not name.strip()
            for name in (draft.first_name, draft.last_name)
        ):
            raise ValueError("First and last names are required")

        if not isinstance(draft.email, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", draft.email
        ):
            raise ValueError("A valid email address is required")

        salary = draft.salary
        if (
            isinstance(salary, bool)
            or not isinstance(salary, (int, float))
            or salary < 0
            or (isinstance(salary, float) and not math.isfinite(salary))
        ):
            raise ValueError("Salary must be a finite, non-negative number")

        return replace(draft)


class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        super().__init__()
        self.with_name(first_name, last_name).with_email(email)
        self.with_job("Engineering", "Senior Developer", 75_000)
        self.with_equipment(laptop=True, parking=False)
        self.with_access(vpn=True, admin=True)
        self.with_office_location("Paris HQ")


def main() -> None:
    developer = (
        DeveloperBuilder("John", "Doe", "john.doe@company.com")
        .with_start_date("2024-01-15")
        .with_phone("+33612345678")
        .build()
    )
    intern = (
        EmployeeBuilder()
        .with_name("Jane", "Smith")
        .with_email("jane.smith@company.com")
        .with_job("Marketing", "Intern", 15_000)
        .with_start_date("2024-02-01")
        .with_manager(42)
        .with_equipment(laptop=True)
        .with_office_location("Paris HQ")
        .with_contract_type("internship")
        .build()
    )
    print(developer)
    print(intern)


if __name__ == "__main__":
    main()

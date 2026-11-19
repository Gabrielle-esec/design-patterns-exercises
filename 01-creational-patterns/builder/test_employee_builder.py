import unittest
from dataclasses import asdict

from employee_builder import DeveloperBuilder, Employee, EmployeeBuilder


class EmployeeBuilderTests(unittest.TestCase):
    def make_builder(self):
        return (
            EmployeeBuilder()
            .with_name("Jane", "Smith")
            .with_email("jane.smith@company.com")
            .with_job("Marketing", "Intern", 15_000)
        )

    def test_all_fields_and_fluent_methods(self):
        builder = self.make_builder()
        configured = (
            builder.with_start_date("2024-02-01")
            .with_manager(42)
            .with_phone("+33600000000")
            .with_address("10 rue Exemple")
            .with_emergency_contact("Alex Smith")
            .with_equipment(laptop=True, parking=True)
            .with_access(vpn=True, admin=False)
            .with_office_location("Paris HQ")
            .with_contract_type("internship")
        )
        self.assertIs(configured, builder)
        employee = builder.build()
        self.assertIsInstance(employee, Employee)
        self.assertEqual(asdict(employee), {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@company.com",
            "department": "Marketing",
            "position": "Intern",
            "salary": 15_000,
            "start_date": "2024-02-01",
            "manager_id": 42,
            "phone": "+33600000000",
            "address": "10 rue Exemple",
            "emergency_contact": "Alex Smith",
            "has_parking": True,
            "has_laptop": True,
            "has_vpn_access": True,
            "has_admin_rights": False,
            "office_location": "Paris HQ",
            "contract_type": "internship",
        })

    def test_optional_defaults_and_zero_salary(self):
        employee = self.make_builder().with_job("Marketing", "Intern", 0).build()
        self.assertEqual(employee.salary, 0)
        self.assertEqual(employee.contract_type, "permanent")
        for field in (
            "start_date", "manager_id", "phone", "address",
            "emergency_contact", "office_location",
        ):
            with self.subTest(field=field):
                self.assertIsNone(getattr(employee, field))
        for field in ("has_parking", "has_laptop", "has_vpn_access", "has_admin_rights"):
            with self.subTest(field=field):
                self.assertIs(getattr(employee, field), False)

    def test_validates_both_names(self):
        for first, last in [("", "Smith"), ("Jane", ""), ("Jane", "  "), (None, "Smith")]:
            with self.subTest(first=first, last=last):
                with self.assertRaisesRegex(ValueError, "names"):
                    self.make_builder().with_name(first, last).build()

    def test_validates_email(self):
        for email in ("", "jane", "@company.com", "jane@", "jane smith@company.com"):
            with self.subTest(email=email):
                with self.assertRaisesRegex(ValueError, "email"):
                    self.make_builder().with_email(email).build()

    def test_validates_salary(self):
        for salary in (-1, float("nan"), float("inf"), "15000", True):
            with self.subTest(salary=salary):
                with self.assertRaisesRegex(ValueError, "Salary"):
                    self.make_builder().with_job("Marketing", "Intern", salary).build()

    def test_builds_independent_records(self):
        builder = self.make_builder()
        first = builder.build()
        second = builder.with_phone("+33600000000").build()
        self.assertIsNot(first, second)
        self.assertIsNone(first.phone)
        second.first_name = "Changed"
        self.assertEqual(builder.build().first_name, "Jane")

    def test_developer_preset_can_build_and_be_customized(self):
        builder = DeveloperBuilder("John", "Doe", "john.doe@company.com")
        employee = builder.build()
        self.assertEqual(employee.department, "Engineering")
        self.assertEqual(employee.position, "Senior Developer")
        self.assertEqual(employee.salary, 75_000)
        self.assertEqual(employee.office_location, "Paris HQ")
        self.assertEqual(employee.contract_type, "permanent")
        self.assertTrue(employee.has_laptop)
        self.assertFalse(employee.has_parking)
        self.assertTrue(employee.has_vpn_access)
        self.assertTrue(employee.has_admin_rights)

        customized = builder.with_access(admin=False).with_equipment(parking=True).build()
        self.assertFalse(customized.has_admin_rights)
        self.assertTrue(customized.has_vpn_access)
        self.assertTrue(customized.has_parking)
        self.assertTrue(customized.has_laptop)


if __name__ == "__main__":
    unittest.main()

"""Contact Management System"""

from typing import List, Dict, Optional


class ContactManager:
    def __init__(self):
        self.contacts: List[Dict[str, str]] = []

    def _is_valid_phone(self, phone: str) -> bool:
        """Check that phone contains only digits, hyphens, and an optional leading +."""
        return bool(phone) and all(char.isdigit() or char == '-' or char == '+' for char in phone) and phone.replace('-', '').replace('+', '').isdigit()

    def _is_valid_email(self, email: str) -> bool:
        """Check that email contains both '@' and '.' characters."""
        return '@' in email and '.' in email and email.count('@') == 1

    def _find_contact(self, name: str) -> Optional[Dict[str, str]]:
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                return contact
        return None

    def add_contact(self, name: str, phone: str, email: str = ""):
        if not name.strip():
            print("Error: Name cannot be empty.")
            return

        if not self._is_valid_phone(phone):
            print("Error: Phone number must contain only digits, hyphens, and an optional leading '+'.")
            return

        if email.strip() and not self._is_valid_email(email):
            print("Error: Email must contain '@' and a period (.).")
            return

        if self._find_contact(name):
            print(f"Error: Contact '{name}' already exists.")
            return

        self.contacts.append({
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip()
        })
        print(f"Contact '{name}' added successfully.")

    def view_contact(self, name: str):
        contact = self._find_contact(name)
        if contact is None:
            print(f"Contact '{name}' not found.")
            return
        print(self._format_contact(contact))

    def update_contact(self, name: str, new_name: str = "", new_phone: str = "", new_email: str = ""):
        contact = self._find_contact(name)
        if contact is None:
            print(f"Contact '{name}' not found.")
            return

        if new_name.strip():
            if self._find_contact(new_name) and new_name.lower() != name.lower():
                print(f"Error: Contact '{new_name}' already exists.")
                return
            contact["name"] = new_name.strip()

        if new_phone.strip():
            if not self._is_valid_phone(new_phone):
                print("Error: Phone number must contain only digits, hyphens, and an optional leading '+'.")
                return
            contact["phone"] = new_phone.strip()

        if new_email.strip() or contact.get("email"):
            if new_email.strip() and not self._is_valid_email(new_email):
                print("Error: Email must contain '@' and a period (.).")
                return
            if new_email.strip():
                contact["email"] = new_email.strip()

        print(f"Contact '{name}' updated successfully.")

    def delete_contact(self, name: str):
        contact = self._find_contact(name)
        if contact is None:
            print(f"Contact '{name}' not found.")
            return
        self.contacts.remove(contact)
        print(f"Contact '{name}' deleted successfully.")

    def search_contacts(self, keyword: str):
        keyword = keyword.lower().strip()
        if not keyword:
            print("Please enter a keyword to search.")
            return

        matches = [
            contact for contact in self.contacts
            if keyword in contact["name"].lower()
            or keyword in contact["phone"].lower()
            or keyword in contact["email"].lower()
        ]

        if not matches:
            print(f"No contacts found for '{keyword}'.")
            return

        print("Search results:")
        for contact in matches:
            print(self._format_contact(contact))

    def list_contacts(self):
        if not self.contacts:
            print("No contacts saved.")
            return
        print("All contacts:")
        for contact in self.contacts:
            print(self._format_contact(contact))

    @staticmethod
    def _format_contact(contact: Dict[str, str]) -> str:
        email = contact.get("email", "")
        return f"Name: {contact['name']} | Phone: {contact['phone']} | Email: {email if email else 'Not provided'}"


def main():
    manager = ContactManager()

    while True:
        print("\n=== Contact Manager Menu ===")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone number: ").strip()
            email = input("Enter email (optional): ").strip()
            manager.add_contact(name, phone, email)

        elif choice == "2":
            name = input("Enter the contact name to view: ").strip()
            manager.view_contact(name)

        elif choice == "3":
            name = input("Enter the contact name to update: ").strip()
            new_name = input("Enter new name (leave blank to keep): ").strip()
            new_phone = input("Enter new phone number (leave blank to keep): ").strip()
            new_email = input("Enter new email (leave blank to keep): ").strip()
            manager.update_contact(name, new_name, new_phone, new_email)

        elif choice == "4":
            name = input("Enter the contact name to delete: ").strip()
            manager.delete_contact(name)

        elif choice == "5":
            keyword = input("Enter a name, phone, or email to search: ").strip()
            manager.search_contacts(keyword)

        elif choice == "6":
            manager.list_contacts()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 7.")


if __name__ == "__main__":
    main()

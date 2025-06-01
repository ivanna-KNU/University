from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Generic, TypeVar, Optional
import uuid

# Static polymorphism with generics
T = TypeVar('T')

class Collection(Generic[T]):
    def __init__(self):
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        self._items.append(item)
    
    def remove(self, item: T) -> bool:
        if item in self._items:
            self._items.remove(item)
            return True
        return False
    
    def get_all(self) -> List[T]:
        return self._items.copy()
    
    def count(self) -> int:
        return len(self._items)


class Person:
    def __init__(self, name: str, email: str, phone: str):
        self._id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._registration_date = datetime.now()
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if '@' in value:  # Simple validation
            self._email = value
        else:
            raise ValueError("Invalid email format")
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value
    
    def get_contact_info(self) -> str:
        return f"Name: {self._name}, Email: {self._email}, Phone: {self._phone}"
    
    def update_contact_info(self, email: str = None, phone: str = None) -> None:
        if email:
            self.email = email
        if phone:
            self.phone = phone


class Student(Person):
    def __init__(self, name: str, email: str, phone: str, student_id: str, major: str):
        super().__init__(name, email, phone)
        self._student_id = student_id
        self._major = major
        self._borrowed_items: List[LibraryItem] = []
        self._max_items = 5
        self._fine_balance = 0.0
    
    @property
    def student_id(self) -> str:
        return self._student_id
    
    @property 
    def major(self) -> str:
        return self._major
    
    @property
    def borrowed_items(self) -> List['LibraryItem']:
        return self._borrowed_items.copy()
    
    @property
    def fine_balance(self) -> float:
        return self._fine_balance
    
    def can_borrow(self) -> bool:
        return len(self._borrowed_items) < self._max_items and self._fine_balance <= 10.0
    
    def borrow_item(self, item: 'LibraryItem') -> bool:
        if not self.can_borrow():
            return False
        if item.is_available():
            self._borrowed_items.append(item)
            return True
        return False
    
    def return_item(self, item: 'LibraryItem') -> float:
        if item in self._borrowed_items:
            self._borrowed_items.remove(item)
            fine = item.calculate_fine()
            self._fine_balance += fine
            return fine
        return 0.0
    
    def pay_fine(self, amount: float) -> float:
        if amount > self._fine_balance:
            payment = self._fine_balance
            self._fine_balance = 0.0
            return payment
        else:
            self._fine_balance -= amount
            return amount
    
    def get_student_details(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "student_id": self._student_id,
            "major": self._major,
            "borrowed_items": len(self._borrowed_items),
            "fine_balance": self._fine_balance
        }


class Librarian(Person):
    def __init__(self, name: str, email: str, phone: str, employee_id: str, department: str):
        super().__init__(name, email, phone)
        self._employee_id = employee_id
        self._department = department
        self._admin_level = 1
    
    @property
    def employee_id(self) -> str:
        return self._employee_id
    
    @property
    def department(self) -> str:
        return self._department
    
    @property
    def admin_level(self) -> int:
        return self._admin_level
    
    def promote(self) -> bool:
        if self._admin_level < 3:
            self._admin_level += 1
            return True
        return False
    
    def can_manage_item(self, item: 'LibraryItem') -> bool:
        # Different departments handle different types of items
        if self._department == "Books" and isinstance(item, Book):
            return True
        elif self._department == "Media" and isinstance(item, (DVD, Magazine)):
            return True
        elif self._department == "General":
            return True
        return False
    
    def process_return(self, student: Student, item: 'LibraryItem') -> float:
        fine = student.return_item(item)
        item.return_to_library()
        if fine > 0:
            notification = Notification(
                student.id, 
                f"Fine of ${fine:.2f} charged for late return of {item.title}"
            )
            return fine
        return 0.0
    
    def issue_item(self, student: Student, item: 'LibraryItem') -> bool:
        if not student.can_borrow() or not item.is_available():
            return False
        
        if student.borrow_item(item):
            item.check_out()
            return True
        return False


class LibraryItem(ABC):
    def __init__(self, title: str, item_id: str, location: str):
        self._title = title
        self._item_id = item_id
        self._location = location
        self._checked_out = False
        self._due_date = None
        self._daily_fine = 1.0  # Default fine per day
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def item_id(self) -> str:
        return self._item_id
    
    @property
    def location(self) -> str:
        return self._location
    
    @location.setter
    def location(self, value: str) -> None:
        self._location = value
    
    @property
    def is_checked_out(self) -> bool:
        return self._checked_out
    
    @property
    def due_date(self) -> Optional[datetime]:
        return self._due_date
    
    def is_available(self) -> bool:
        return not self._checked_out
    
    def check_out(self) -> None:
        if not self._checked_out:
            self._checked_out = True
            self._due_date = datetime.now() + self.get_loan_period()
    
    def return_to_library(self) -> None:
        self._checked_out = False
        self._due_date = None
    
    @abstractmethod
    def get_loan_period(self) -> timedelta:
        pass
    
    @abstractmethod
    def get_item_details(self) -> Dict:
        pass
    
    def calculate_fine(self) -> float:
        if not self._checked_out or not self._due_date:
            return 0.0
        
        days_overdue = (datetime.now() - self._due_date).days
        if days_overdue > 0:
            return days_overdue * self._daily_fine
        return 0.0
    
    def __str__(self) -> str:
        status = "Checked Out" if self._checked_out else "Available"
        return f"{self._title} ({self._item_id}) - {status}"


class Book(LibraryItem):
    def __init__(self, title: str, item_id: str, location: str, author: str, isbn: str, publisher: str, pages: int):
        super().__init__(title, item_id, location)
        self._author = author
        self._isbn = isbn
        self._publisher = publisher
        self._pages = pages
        self._daily_fine = 0.5  # Lower fine for books
    
    @property
    def author(self) -> str:
        return self._author
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @property
    def publisher(self) -> str:
        return self._publisher
    
    @property
    def pages(self) -> int:
        return self._pages
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=21)  # 3 weeks for books
    
    def get_item_details(self) -> Dict:
        return {
            "type": "Book",
            "title": self._title,
            "item_id": self._item_id,
            "location": self._location,
            "author": self._author,
            "isbn": self._isbn,
            "publisher": self._publisher,
            "pages": self._pages,
            "checked_out": self._checked_out,
            "due_date": self._due_date.strftime("%Y-%m-%d") if self._due_date else None
        }


class Magazine(LibraryItem):
    def __init__(self, title: str, item_id: str, location: str, publisher: str, issue_number: str, publication_date: datetime):
        super().__init__(title, item_id, location)
        self._publisher = publisher
        self._issue_number = issue_number
        self._publication_date = publication_date
        self._daily_fine = 1.0
    
    @property
    def publisher(self) -> str:
        return self._publisher
    
    @property
    def issue_number(self) -> str:
        return self._issue_number
    
    @property
    def publication_date(self) -> datetime:
        return self._publication_date
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=7)  # 1 week for magazines
    
    def get_item_details(self) -> Dict:
        return {
            "type": "Magazine",
            "title": self._title,
            "item_id": self._item_id,
            "location": self._location,
            "publisher": self._publisher,
            "issue_number": self._issue_number,
            "publication_date": self._publication_date.strftime("%Y-%m-%d"),
            "checked_out": self._checked_out,
            "due_date": self._due_date.strftime("%Y-%m-%d") if self._due_date else None
        }


class DVD(LibraryItem):
    def __init__(self, title: str, item_id: str, location: str, director: str, runtime: int, genre: str, release_year: int):
        super().__init__(title, item_id, location)
        self._director = director
        self._runtime = runtime
        self._genre = genre
        self._release_year = release_year
        self._daily_fine = 2.0  # Higher fine for DVDs
    
    @property
    def director(self) -> str:
        return self._director
    
    @property
    def runtime(self) -> int:
        return self._runtime
    
    @property
    def genre(self) -> str:
        return self._genre
    
    @property
    def release_year(self) -> int:
        return self._release_year
    
    def get_loan_period(self) -> timedelta:
        return timedelta(days=3)  # 3 days for DVDs
    
    def get_item_details(self) -> Dict:
        return {
            "type": "DVD",
            "title": self._title,
            "item_id": self._item_id,
            "location": self._location,
            "director": self._director,
            "runtime": self._runtime,
            "genre": self._genre,
            "release_year": self._release_year,
            "checked_out": self._checked_out,
            "due_date": self._due_date.strftime("%Y-%m-%d") if self._due_date else None
        }


class Catalog:
    def __init__(self):
        self._items: Dict[str, LibraryItem] = {}
    
    def add_item(self, item: LibraryItem) -> None:
        self._items[item.item_id] = item
    
    def remove_item(self, item_id: str) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False
    
    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        return self._items.get(item_id)
    
    def search_by_title(self, title: str) -> List[LibraryItem]:
        return [item for item in self._items.values() if title.lower() in item.title.lower()]
    
    def get_available_items(self) -> List[LibraryItem]:
        return [item for item in self._items.values() if item.is_available()]
    
    def get_checked_out_items(self) -> List[LibraryItem]:
        return [item for item in self._items.values() if item.is_checked_out]
    
    def count_items_by_type(self) -> Dict[str, int]:
        result = {"Book": 0, "Magazine": 0, "DVD": 0}
        for item in self._items.values():
            if isinstance(item, Book):
                result["Book"] += 1
            elif isinstance(item, Magazine):
                result["Magazine"] += 1
            elif isinstance(item, DVD):
                result["DVD"] += 1
        return result


class Reservation:
    def __init__(self, student: Student, item: LibraryItem, reservation_date: datetime = None):
        self._id = str(uuid.uuid4())
        self._student = student
        self._item = item
        self._reservation_date = reservation_date or datetime.now()
        self._status = "Active"
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def student(self) -> Student:
        return self._student
    
    @property
    def item(self) -> LibraryItem:
        return self._item
    
    @property
    def reservation_date(self) -> datetime:
        return self._reservation_date
    
    @property
    def status(self) -> str:
        return self._status
    
    def cancel(self) -> bool:
        if self._status == "Active":
            self._status = "Cancelled"
            return True
        return False
    
    def fulfill(self) -> bool:
        if self._status == "Active" and self._item.is_available():
            self._status = "Fulfilled"
            return True
        return False
    
    def is_expired(self) -> bool:
        # Reservations expire after 3 days
        return (datetime.now() - self._reservation_date).days > 3
    
    def get_reservation_details(self) -> Dict:
        return {
            "id": self._id,
            "student_id": self._student.id,
            "student_name": self._student.name,
            "item_id": self._item.item_id,
            "item_title": self._item.title,
            "reservation_date": self._reservation_date.strftime("%Y-%m-%d %H:%M"),
            "status": self._status,
            "is_expired": self.is_expired()
        }


class Notification:
    def __init__(self, recipient_id: str, message: str, created_at: datetime = None):
        self._id = str(uuid.uuid4())
        self._recipient_id = recipient_id
        self._message = message
        self._created_at = created_at or datetime.now()
        self._read = False
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def recipient_id(self) -> str:
        return self._recipient_id
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def is_read(self) -> bool:
        return self._read
    
    def mark_as_read(self) -> None:
        self._read = True
    
    def mark_as_unread(self) -> None:
        self._read = False
    
    def format_notification(self) -> str:
        status = "Read" if self._read else "Unread"
        return f"[{status}] [{self._created_at.strftime('%Y-%m-%d %H:%M')}] {self._message}"


class Library:
    def __init__(self, name: str, address: str):
        self._name = name
        self._address = address
        self._catalog = Catalog()
        self._students: Dict[str, Student] = {}
        self._librarians: Dict[str, Librarian] = {}
        self._reservations: Collection[Reservation] = Collection[Reservation]()
        self._notifications: List[Notification] = []
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def address(self) -> str:
        return self._address
    
    def register_student(self, student: Student) -> None:
        self._students[student.id] = student
    
    def register_librarian(self, librarian: Librarian) -> None:
        self._librarians[librarian.id] = librarian
    
    def add_item_to_catalog(self, item: LibraryItem) -> None:
        self._catalog.add_item(item)
    
    def get_student(self, student_id: str) -> Optional[Student]:
        return self._students.get(student_id)
    
    def get_librarian(self, librarian_id: str) -> Optional[Librarian]:
        return self._librarians.get(librarian_id)
    
    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        return self._catalog.get_item(item_id)
    
    def make_reservation(self, student_id: str, item_id: str) -> Optional[Reservation]:
        student = self.get_student(student_id)
        item = self.get_item(item_id)
        
        if not student or not item:
            return None
        
        reservation = Reservation(student, item)
        self._reservations.add(reservation)
        
        # Create notification
        notification = Notification(
            student_id, 
            f"Reservation created for {item.title}. It will be held for 3 days."
        )
        self._notifications.append(notification)
        
        return reservation
    
    def process_checkout(self, librarian_id: str, student_id: str, item_id: str) -> bool:
        librarian = self.get_librarian(librarian_id)
        student = self.get_student(student_id)
        item = self.get_item(item_id)
        
        if not librarian or not student or not item:
            return False
        
        if librarian.issue_item(student, item):
            notification = Notification(
                student_id,
                f"You have checked out {item.title}. Due date: {item.due_date.strftime('%Y-%m-%d')}"
            )
            self._notifications.append(notification)
            return True
        return False
    
    def process_return(self, librarian_id: str, student_id: str, item_id: str) -> float:
        librarian = self.get_librarian(librarian_id)
        student = self.get_student(student_id)
        item = self.get_item(item_id)
        
        if not librarian or not student or not item:
            return 0.0
        
        return librarian.process_return(student, item)
    
    def send_overdue_notifications(self) -> int:
        count = 0
        current_date = datetime.now()
        
        for student in self._students.values():
            for item in student.borrowed_items:
                if item.due_date and current_date > item.due_date:
                    days_overdue = (current_date - item.due_date).days
                    notification = Notification(
                        student.id,
                        f"OVERDUE: {item.title} was due {days_overdue} days ago. Current fine: ${item.calculate_fine():.2f}"
                    )
                    self._notifications.append(notification)
                    count += 1
        
        return count
    
    def get_library_statistics(self) -> Dict:
        return {
            "total_students": len(self._students),
            "total_librarians": len(self._librarians),
            "items_by_type": self._catalog.count_items_by_type(),
            "available_items": len(self._catalog.get_available_items()),
            "checked_out_items": len(self._catalog.get_checked_out_items()),
            "active_reservations": len([r for r in self._reservations.get_all() if r.status == "Active"]),
            "total_notifications": len(self._notifications)
        }


if __name__ == "__main__":
    central_library = Library("Central City Library", "123 Main St, City")
    
    # Create librarians
    john = Librarian("John Smith", "john@library.com", "555-1234", "EMP001", "Books")
    mary = Librarian("Mary Johnson", "mary@library.com", "555-5678", "EMP002", "Media")
    
    central_library.register_librarian(john)
    central_library.register_librarian(mary)
    
    # Create students
    alice = Student("Alice Brown", "alice@university.edu", "555-9012", "STU001", "Computer Science")
    bob = Student("Bob Wilson", "bob@university.edu", "555-3456", "STU002", "Literature")
    
    central_library.register_student(alice)
    central_library.register_student(bob)
    
    # Add items to the catalog
    book1 = Book("Python Programming", "B001", "Floor 2, Shelf A", "John Doe", "978-1234567890", "Tech Press", 350)
    book2 = Book("Database Systems", "B002", "Floor 1, Shelf C", "Jane Smith", "978-0987654321", "CS Publications", 420)
    
    magazine1 = Magazine("Science Today", "M001", "Floor 1, Shelf D", "Science Press", "Issue 42", datetime(2023, 5, 15))
    
    dvd1 = DVD("Introduction to Algorithms", "D001", "Floor 3, Shelf B", "Prof. X", 120, "Educational", 2023)
    
    central_library.add_item_to_catalog(book1)
    central_library.add_item_to_catalog(book2)
    central_library.add_item_to_catalog(magazine1)
    central_library.add_item_to_catalog(dvd1)
    
    # Example of checkout process
    checkout_success = central_library.process_checkout(john.id, alice.id, book1.item_id)
    print(f"Checkout successful: {checkout_success}")
    print(f"Book status: {'Checked Out' if book1.is_checked_out else 'Available'}")
    print(f"Due date: {book1.due_date.strftime('%Y-%m-%d')}")
    
    # Example of reservation
    reservation = central_library.make_reservation(bob.id, book1.item_id)
    print(f"Reservation created: {reservation.id}")
    print(f"Reservation status: {reservation.status}")
    
    # Display library statistics
    print("\nLibrary Statistics:")
    stats = central_library.get_library_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}") 
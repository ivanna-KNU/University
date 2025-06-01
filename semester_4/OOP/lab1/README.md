# Library Management System

A Python-based object-oriented library management system that demonstrates OOP principles including inheritance, polymorphism, and encapsulation.

## Features

- **User Management**: Track students and librarians with different access rights
- **Item Management**: Handle different types of library items (books, magazines, DVDs)
- **Loan System**: Check out items, track due dates, calculate fines
- **Reservation System**: Allow students to reserve items
- **Notification System**: Generate and track notifications for users

## Requirements

- Python 3.11+
- No external dependencies required

## Running the Application

Simply run the main file:

```bash
python library_system.py
```

This will execute the demo example code at the bottom of the file, which demonstrates creating a library, registering users, adding items, and performing operations.

## Project Structure

The system is organized around several main classes:

1. **Person Hierarchy**:
   - `Person`: Base class with common user properties
   - `Student`: Users who can borrow items
   - `Librarian`: Staff who manage the library

2. **LibraryItem Hierarchy**:
   - `LibraryItem`: Abstract base class for all borrowable items
   - `Book`: Book-specific implementation
   - `Magazine`: Magazine-specific implementation
   - `DVD`: DVD-specific implementation

3. **Support Classes**:
   - `Catalog`: Manages the collection of items
   - `Reservation`: Tracks item reservations
   - `Notification`: Handles user notifications
   - `Library`: Central class that coordinates all operations
   - `Collection`: Generic collection class

## Example Usage

```python
# Create library
library = Library("Central Library", "123 Main St")

# Register users
student = Student("Alice Brown", "alice@university.edu", "555-9012", "STU001", "Computer Science")
librarian = Librarian("John Smith", "john@library.com", "555-1234", "EMP001", "Books")

library.register_student(student)
library.register_librarian(librarian)

# Add items
book = Book("Python Programming", "B001", "Floor 2, Shelf A", 
            "John Doe", "978-1234567890", "Tech Press", 350)
library.add_item_to_catalog(book)

# Checkout process
success = library.process_checkout(librarian.id, student.id, book.item_id)
print(f"Checkout successful: {success}")

# Return process
fine = library.process_return(librarian.id, student.id, book.item_id)
print(f"Fine charged: ${fine:.2f}")
```

## OOP Requirements

This project was designed to demonstrate specific OOP principles. For a detailed breakdown of how the implementation meets those requirements, please see the [requirements.md](requirements.md) file. 
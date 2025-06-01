# Library Management System - OOP Requirements Summary

This project demonstrates object-oriented programming concepts by implementing a Library Management System. Below is a summary of how the implementation meets the requirements:

## Classes (9 required, 9 implemented)
1. `Person` (base class)
2. `Student` (extends Person)
3. `Librarian` (extends Person)
4. `LibraryItem` (abstract base class)
5. `Book` (extends LibraryItem)
6. `Magazine` (extends LibraryItem)
7. `DVD` (extends LibraryItem)
8. `Catalog`
9. `Reservation`
10. `Notification`
11. `Library`
12. `Collection` (generic class)

## Fields (15 required, 46+ implemented)
1. Person: `_id`, `_name`, `_email`, `_phone`, `_registration_date`
2. Student: `_student_id`, `_major`, `_borrowed_items`, `_max_items`, `_fine_balance`
3. Librarian: `_employee_id`, `_department`, `_admin_level`
4. LibraryItem: `_title`, `_item_id`, `_location`, `_checked_out`, `_due_date`, `_daily_fine`
5. Book: `_author`, `_isbn`, `_publisher`, `_pages`
6. Magazine: `_publisher`, `_issue_number`, `_publication_date`
7. DVD: `_director`, `_runtime`, `_genre`, `_release_year`
8. Catalog: `_items`
9. Reservation: `_id`, `_student`, `_item`, `_reservation_date`, `_status`
10. Notification: `_id`, `_recipient_id`, `_message`, `_created_at`, `_read`
11. Library: `_name`, `_address`, `_catalog`, `_students`, `_librarians`, `_reservations`, `_notifications`
12. Collection: `_items`

## Non-trivial Methods (25 required, 40+ implemented)
1. Person: `get_contact_info()`, `update_contact_info()`
2. Student: `can_borrow()`, `borrow_item()`, `return_item()`, `pay_fine()`, `get_student_details()`
3. Librarian: `promote()`, `can_manage_item()`, `process_return()`, `issue_item()`
4. LibraryItem: `is_available()`, `check_out()`, `return_to_library()`, `calculate_fine()`, `__str__()`
5. Book, Magazine, DVD: `get_loan_period()`, `get_item_details()`
6. Catalog: `add_item()`, `remove_item()`, `search_by_title()`, `get_available_items()`, `get_checked_out_items()`, `count_items_by_type()`
7. Reservation: `cancel()`, `fulfill()`, `is_expired()`, `get_reservation_details()`
8. Notification: `mark_as_read()`, `mark_as_unread()`, `format_notification()`
9. Library: `register_student()`, `register_librarian()`, `add_item_to_catalog()`, `make_reservation()`, `process_checkout()`, `process_return()`, `send_overdue_notifications()`, `get_library_statistics()`
10. Collection: `add()`, `remove()`, `get_all()`, `count()`

## Inheritance Hierarchies (2 required, 2 implemented)
1. Person hierarchy:
   - Person (base)
   - Student (extends Person)
   - Librarian (extends Person)

2. LibraryItem hierarchy:
   - LibraryItem (abstract base)
   - Book (extends LibraryItem)
   - Magazine (extends LibraryItem)
   - DVD (extends LibraryItem)

## Polymorphism (3 required, 3+ implemented)
1. Static polymorphism:
   - Generic Collection<T> class with type parameter
   - Type-parameterized methods working with generic types

2. Dynamic polymorphism (overriding):
   - LibraryItem's abstract methods `get_loan_period()` and `get_item_details()` implemented differently in Book, Magazine, and DVD
   - Different calculation of fines in different LibraryItem subclasses

3. Dynamic polymorphism (interface):
   - Librarian's `can_manage_item()` using instanceof checks

## Encapsulation
- All class fields are private (with `_` prefix)
- Public access provided through properties and methods
- Appropriate validation in setters (e.g., email validation)

## Client Code
The main demo demonstrates client code using polymorphism by:
1. Working with different Person types through common operations
2. Using LibraryItem subclasses through the common interface
3. Using Collection<T> with different types

This implementation thoroughly satisfies the requirements for OOP principles through a practical library management system example. 
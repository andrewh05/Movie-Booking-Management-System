# 🎬 Movie Booking Management System

A Python-based desktop application that allows users to manage movies and their bookings in different theaters using a graphical user interface (GUI) built with `Tkinter` and a backend powered by `MySQL`.

---

## 📁 Project Structure

|-- create_mv.py
|
|-- movie.py
|
|-- booking.py


---

## 🧠 Features

### 🎥 Movie Management (`movie.py`)
- Add new movies with ID, name, theater, and activation status.
- Update existing movie data.
- View all or single movie records.
- Delete movies from the database.

### 🪑 Booking System (`booking.py`)
- Visual seat selection for a movie across time slots and theater rooms.
- Automatically disables already booked seats.
- Allows unbooking of selected seats.
- Reset all bookings for a specific movie and time.

### 🗃️ Database Schema (`create_mv.py`)
- Creates the `mv_managment` database with:
  - `movie` table: Stores movie metadata.
  - `booking` table: Stores booking details with foreign key relationships.

---

## 🧰 Tech Stack

- **Language:** Python 3.x
- **GUI Library:** Tkinter
- **Database:** MySQL
- **Connector:** `mysql-connector-python`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/andrewh05/Movie-Booking-Managment-System.git
cd Movie-Booking-Managment-System
```

### 2. Install Requirements

```bash
pip install mysql-connector-python
```
### 3. Set Up the Database

```bash
python create_mv.py
```
Note: Ensure MySQL server is running and accessible with `root` user (adjust credentials in the script if needed).



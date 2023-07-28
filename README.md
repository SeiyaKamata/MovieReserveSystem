# documantation

# Movie Reservation Website

## General Description

The proposed web application allows the user to book tickets to a movie theater. The user can:

1. Select the movie from the predefined list.
2. Choose the desired date in the calendar.
3. Choose the place in the cinema hall.
4. Type own name and confirm own choice with OK button. (The system should notify whether the reservation is completed successfully.)
5. Additionally, the user can register in the system, so that the app will not have to ask the user name during the next booking.
6. The system can show the history of movies booked by the currently logged user.

Notes:

1. There are N (≈10) different movies in the system.
2. There are M (≈5) movies shown daily in the theater.
3. Reservation can be done for the next 14 days.
4. The number of seats in the hall is limited, and they are different.

Suggestions for the user interface:

1. If the user selects the desired movie first, he/she can only select dates when this movie is shown.
2. If there are no available seats for a certain day/film, the app should inform the user about it.
3. The user should be able to select the seat using the movie hall map. (Available seats should be highlighted).
4. Registration requires entering a unique combination of login/password.
5. If a certain user is logged in, there is no need to ask for a user name

## Database Structure

---

### User

| Column   | Type      | Comment                            |
| -------- | --------- | ---------------------------------- |
| name     | char(128) | User name (such as “Seiya Kamata”) |
| password | char(128) | password (such as “****\*\*****”)  |

### Movies

| Column      | Type      | Comment                                 |
| ----------- | --------- | --------------------------------------- |
| id          | int       | Unique movie ID                         |
| name        | char(128) | Movie name (such as “Frozen”)           |
| screen time | integer   | screen time of the movie                |
| thumbnail   | image     | thumbnail of the movie                  |
| is_deleted  | boolean   | True if the screening period has passed |

### Hole

| Column | Type      | Comment                      |
| ------ | --------- | ---------------------------- |
| id     | int       | Unique Hole ID               |
| name   | Char(128) | Hole name (such as “Hole 1”) |
| row    | integer   | Number of low                |
| col    | integer   | Number of col                |

## Seat

| Column | Type    | Comment        |
| ------ | ------- | -------------- |
| id     | int     | Unique Seat ID |
| hole   | Hole    | Hole           |
| row    | integer | row index      |
| col    | integer | col index      |

## Schedule

| Column      | Type        | Comment                       |
| ----------- | ----------- | ----------------------------- |
| id          | int         | Unique user ID                |
| movie       | Movie       | Associated with a foreign key |
| hole        | Hole        | Associated with a foreign key |
| start_at    | DateAndTime | Screening start time          |
| is_sold_out | boolean     | True if fully reserved        |
| is_deleted  | boolean     | True if playing is cancel     |

### Reservation

| Column     | Type        | Comment                       |
| ---------- | ----------- | ----------------------------- |
| id         | int         | Unique reservation ID         |
| schedule   | Schedule    | Associated with a foreign key |
| user       | User        | Associated with a foreign key |
| seat       | Char        | Associated with a foreign key |
| created_at | DateAndTime | reserved time                 |
| is_deleted | boolean     | true if reservation is cancel |

## Project Plan

1. Setup the system (all required software tools).
2. Create the database and design its structure.
3. Create the business logic. Make sure it works without user interface.
4. Create the prototype of the user interface in plain HTML.

# Hoop & Go (NCI-AMNI-Team-Project-2026)

**Live site:** [https://hoop-and-go.onrender.com/](https://hoop-and-go.onrender.com/)

run " docker compose up --build " to compose image and then use link http://localhost:8080/ to view website locally

## Introduction

This project is a sports gathering platform built to help basketball players find and join 2,3,4,5,6-a-side games nearby. The website is for users who want to easily discover, join, and manage basketball event bookings without the hassle of organising games manually.

The website is built using the Django framework, containerised with Docker, hosted on a free-tier PostgreSQL database (Neon), and follows an agile methodology approach for development using Jira for sprint tracking.

## Table of Contents

- [Introduction](#introduction)
- [User Experience](#user-experience)
    - [Project Goal](#project-goal)
    - [User Stories](#user-stories)
    - [Scope](#scope)
    - [Agile Methodology](#agile-methodology)
- [Design](#design)
    - [Use Case Diagram](#use-case-diagram)
    - [Database Schema](#database-schema)
- [Features](#features)
- [Future Features](#future-features)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Python Packages](#python-packages)
- [Deployment](#deployment)
    - [Docker Setup](#docker-setup)
    - [Database Hosting (Neon)](#database-hosting-neon)
    - [Fork Repository](#to-fork-this-repository)
    - [Cloning](#cloning-this-project)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

<br>

## User Experience
<br>

### Project Goal

* The goal of Hoop and Go is to make it simple for basketball players to find, join, and manage 5-a-side games in their area, while also solving the everyday problem of finding parking near the courts.
<br><br>

### User Stories

|  | As a non-logged in user |
| --- | --- |
| 1. | I want to browse available basketball events without needing to create an account. |
| 2. | I want to view event details such as location, date, and time before deciding to join. |
| 3. | I want to easily navigate the website and find relevant information. |
| 4. | I want to register on the website so I can join events and manage bookings. |
| 5. | I want to log in once I've registered. |

<br>

|  | As a logged in user (Player) |
| --- | --- |
| 1. | I want to select and join a basketball event of my choice. |
| 2. | I want to register my vehicle so I get free reserved parking at the event. |
| 3. | I want to view and manage my bookings, including cancelling if I can no longer attend. |
| 4. | I want to view and edit my account details, including my password. |
| 5. | I want to log out of the website. |

<br>

|  | As an event organiser |
| --- | --- |
| 1. | I want to create a new basketball event with location, date, time, and capacity. |
| 2. | I want to delete an event I created if it's no longer happening. |
| 3. | I want my create/delete actions to be protected by my password so no other user can alter my events. |
| 4. | I want to see confirmation once my event is successfully created or deleted. |
| 5. | I want to pick from a fixed list of tournament formats and Dublin locations so listings stay consistent and accurate. |

<br>

### Scope

User Registration and Authentication
- Users can create an account and log in to the website.
- Users can reset their passwords if forgotten.
- Login accepts either email or username.

Event Discovery and Booking
- Users can browse available basketball events without logging in.
- Users can select and join an event, subject to availability.
- Users can register their vehicle to reserve parking for a specific event.

Booking Management
- Users can view all their current bookings.
- Users can cancel one or multiple bookings, with confirmation prompts.

Event Management (Organisers Only)
- Organisers can create new events by entering event details.
- Organisers can delete existing events, protected by password confirmation.
- Deleted events are immediately removed from the public event list.

User Profile
- Users can view and edit their personal details, including changing their password.
- Users receive validation feedback if entered details are incorrect.

<br>

### Agile Methodology

The development of Hoop and Go follows an agile methodology approach using weekly sprint cycles. Each sprint focuses on delivering specific features drawn from the Requirements Specification, tracked through Jira with a rotating Scrum Master each sprint. All user stories, sprint backlogs, and progress can be accessed via our Jira board [here](https://aidaskibas17.atlassian.net/jira/software/projects/SCRUM/summary).

Our GitHub repository is linked to Jira so that branches, commits, and pull requests are tracked directly against their corresponding Jira issue.

<br>

## Design

### Use Case Diagram

The core functional requirements are represented by 8 use cases: Login, Register New User, Register Vehicle, Select Event, Manage Booking, Change Details, Create Event, and Delete Event, as detailed in our Requirements Specification.

### Database Schema

The core entities are User, Event, Booking, and Payment, linked as follows: a User can organise many Events, a User can make many Bookings, an Event can have many Bookings, and a Booking generates one Payment once checkout is completed via Stripe. Events also store a price, which is used directly when creating the Stripe checkout session.

<br>

## Features

- User registration and login (email or username)
- Password reset flow
- Browse and search available basketball events
- Join an event with real-time capacity checks
- Register a vehicle for free event parking
- View and manage (cancel) bookings
- Edit personal account details
- Organiser-only event creation and deletion, password-protected
- **Stripe payment integration** for paid events, allowing organisers to charge entry fees and users to pay securely at checkout.
- **Search events by location**, with results paginated 6 per page.
- **Create Event page**, restricted to logged-in users, with a fixed list of tournament formats (1v1–6v6) and 15 preset Dublin locations to choose from.
- **Delete Event page**, only visible to the event's organiser, protected by password confirmation.
- Event capacity capped between 2 and 12 players, and event date cannot be set in the past.
- **Refund attempt on booking cancellation** if the booking was already paid via Stripe.
- Editable event price per event, used directly in the Stripe checkout amount.
- Profile page to view/edit first and last name, and see your registered vehicle.
- Custom 404 and 500 error pages.


<br>

## Future Features

- Support additional sports beyond basketball.
- Add email notifications for booking confirmations and cancellations.
- Add an admin dashboard for organisers to see booking stats per event.
- "Every 10th event free" loyalty feature.

<br>

## Known Limitations

- Sport type is currently locked to Basketball only; the field exists in the model for future expansion to other sports.
- Refunds on cancellation are attempted automatically via Stripe, but if the Stripe API call fails, the booking is still cancelled and a warning message is shown asking the user to follow up manually.

<br>

## Testing 


Automated unit tests cover:
- Event listing (past events are correctly hidden)
- Booking flow (capacity limits, duplicate booking prevention)
- Manage events (viewing and removing bookings)
- Vehicle registration (model, form, and view access control)

Run all tests with:
```bash
docker compose exec web python manage.py test --keepdb
```
<br>

## Technologies Used

- Python
- Django
- PostgreSQL (hosted on Neon)
- Docker & Docker Compose
- django-allauth (authentication)
- Bootstrap 5 (via django-crispy-forms)
- GitHub (version control)
- Jira (sprint planning and issue tracking)
- Stripe (payment processing for paid events)
- Render (live deployment and hosting)

<br>

## Python Packages

- Django
- django-allauth
- django-crispy-forms
- dj-database-url
- psycopg2-binary
- python-decouple
- gunicorn
- whitenoise
- stripe

<br>

## Deployment

### Docker Setup

This project runs inside Docker for consistent environments across all team members' machines.

1. Clone the repository (see below).
2. Create a `.env` file at the project root using `.env.example` as a template.
3. Run `docker compose build` followed by `docker compose up`.
4. Run migrations: `docker compose exec web python manage.py migrate`.
5. Create a superuser: `docker compose exec web python manage.py createsuperuser`.
6. Visit `http://localhost:8080` to view the running application.

### Database Hosting (Neon)

The project's PostgreSQL database is hosted for free on [Neon](https://neon.com). All team members connect to the same shared database via a `DATABASE_URL` environment variable, kept out of version control via `.gitignore`.

### To Fork This Repository

1. Log in to GitHub.
2. Navigate to the repository page.
3. Click the "Fork" button in the top right.

### Cloning This Project

1. Log in to GitHub.
2. Navigate to the repository page.
3. Click "Code" and copy the HTTPS URL.
4. Open a terminal and run `git clone <copied-url>`.

<br>

## Credits

- Aidas Kibas
- Michal Pokojny
- Nerijus Kmitas
- Ionut Ciobanu

<br>

## Acknowledgements

- National College of Ireland, Team Project module, lectured by Sumit Tripathi.

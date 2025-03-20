# Laundry Tracker MVP

This is a simple web application built as an MVP for laundry owners to track orders and manage laundry inventory. The project uses Flask, Python, MySQL (via SQLAlchemy), and optionally an API for extended functionality.

## Features

- **Order Form:** Log new orders with customer name, fabric type, quantity, order status, and date received.
- **Order Report:** View a summary of all orders in a table format.
- **Dashboard:** See quick statistics on total orders, orders in progress, completed orders, and pending orders.

## Technology Stack

- Flask (Web Framework)
- Python
- MySQL (via SQLAlchemy)
- Flask-WTF (Form handling)
- Flask-Migrate (Database migrations)
- python-dotenv (Environment variable management)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd laundry-tracker


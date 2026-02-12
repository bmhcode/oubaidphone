<<<<<<< HEAD
Web site ecommerce
=======
# Oubaidphone Zay Shop

A professional Django e-commerce application for Oubaidphone Zay.

## Features

*   **Product Catalog**: Browse products by category and brand.
*   **Store Information**: Dynamic store details management.
*   **Product Details**: Comprehensive product views.
*   **Contact & About**: Informational pages.

## Prerequisites

*   Python 3.10+
*   pip

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd oubaidphone-zay
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv env
    # Windows
    .\env\Scripts\activate
    # Linux/Mac
    source env/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**:
    *   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Update `.env` with your settings (Secret Key, Database URL, etc.).

5.  **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Create Superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

## Deployment

This project is configured for deployment on platforms like Render.com. ensure you set the environment variables in your deployment dashboard.
>>>>>>> 4a62d62 (new version)

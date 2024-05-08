# VMS
The Vendor Management System developed using Django and Django REST Framework is a robust solution designed to streamline and optimize vendor-related processes within an organization. This system facilitates efficient management of vendor information, purchase orders, and vendor performance tracking.

# Overview
This Vendor Management System is designed to streamline vendor-related processes and enhance efficiency in vendor management, purchase order handling, and performance tracking. Below are the key functionalities and setup instructions for using the system.

# Vendor Management System

## Overview
This Vendor Management System is designed to streamline vendor-related processes and enhance efficiency in vendor management, purchase order handling, and performance tracking.

## Functionalities

### Vendor Creation
- Endpoint: `/api/vendors/`
- Description: Create a new vendor profile with details such as name, contact information, address, vendor code, etc.

### Vendor Modification
- Endpoint: `/api/vendors/<str:pk>/`
- Description: Modify an existing vendor's information, including contact details, address, and vendor code.

### Purchase Order Creation
- Endpoint: `/api/purchaseorders/`
- Description: Create a new purchase order with details like order date, delivery date, items, quantity, and vendor information.

### Purchase Order Modification
- Endpoint: `/api/purchaseorders/<str:pk>/`
- Description: Modify an existing purchase order, including updating order details, items, and quantities.

### Vendor Performance Calculation (Delivery Rating)
- Endpoint: `/api/vendors/<str:pk>/performance/`
- Description: Calculate and view the delivery rating performance of a particular vendor based on on-time delivery rates.

### Delivery Tracking
- Description: Track delivery status and dates for purchase orders, including acknowledgment of delivery.

### Acknowledging
- Endpoint: `/api/purchaseorders/<str:pk>/acknowledge/`
- Description: Acknowledge delivery of a purchase order, updating the acknowledgment date.

## Setup Instructions

1. **Install Requirements:**
   Install the required packages by running:

2. **Open Project in VS Code:**
Open the project directory in Visual Studio Code or any preferred IDE.

3. **Run Migrations:**
Create and apply database migrations:

4. **Start Server:**
Start the Django development server:
   
Specify a port number if needed (e.g., `python manage.py runserver 8000`).

5. **Access APIs:**
Use the provided APIs to perform vendor management, purchase order creation/modification, and performance tracking.
Example: `http://localhost:8000/api/vendors/`, `http://localhost:8000/api/purchaseorders/`, etc.



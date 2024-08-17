# Invoice Generation Web App

## Overview

This Django-based web application allows companies to generate, manage, and send invoice bills efficiently. It provides an intuitive interface for adding clients, creating detailed invoices, viewing them as PDFs, and sending them directly via email. The application also includes a dashboard for tracking all invoices sent by the company.

## Features

- **Client Management**: Add and manage client information including name, address, and contact details.
  
- **Invoice Creation**: Create invoices by adding products, specifying quantities, and setting prices. The system automatically calculates the total amount.
  
- **Invoice Viewing and Exporting**: View invoices in a user-friendly format and export them as PDF files for easy sharing and record-keeping.
  
- **Email Invoices**: Send invoices directly to clients via email with a single click, ensuring prompt delivery and communication.

- **Dashboard**: Access a centralized dashboard that lists all invoices sent by the company, with details like client name, date, and invoice status.

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/Mohamed-Javeed/Invoice-Project.git
   ```

2. **Navigate to the Project Directory**
   ```
   cd Invoice-Project
   ```

3. **Install Dependencies**
   Make sure you have `pip` and `virtualenv` installed. Then, create a virtual environment and install the required dependencies:
   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   Set up the database by running the migrations:
   ```
   python manage.py migrate
   ```

5. **Run the Server**
   Start the development server:
   ```
   python manage.py runserver
   ```

6. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

1. **Adding Clients**:
   - Navigate to the "Add Client" section.
   - Fill in the client's details and save.

2. **Creating Invoices**:
   - Go to the "Create Invoice" section.
   - Select the client, add the necessary products with quantities and prices, and generate the invoice.

3. **Viewing and Exporting Invoices**:
   - Invoices can be viewed on the dashboard or by searching the invoice number.
   - Click on "View as PDF" to export the invoice.

4. **Sending Invoices via Email**:
   - After generating an invoice, click the "Send via Email" button.
   - The invoice will be sent to the client's registered email address.

5. **Dashboard**:
   - The dashboard provides a summary of all invoices, including their status and associated client information.

## Project Structure

- **clients/**: Contains the app logic for managing client information.
- **invoices/**: Manages invoice creation, viewing, and exporting.
- **dashboard/**: Handles the overview and management of all invoices.
- **templates/**: HTML templates for rendering the web pages.
- **static/**: Static files like CSS and JavaScript.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact

For any queries or issues, please reach out via [GitHub Issues](https://github.com/Mohamed-Javeed/Invoice-Project/issues).

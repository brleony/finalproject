# Nummi

Nummi is a web based expense tracker application.
It is my final project for the course Web Programming with Python and JavaScript.
You can use the site to track your expenses and view the history of your expenses to give you more insight in your financial habits.

The website is easy to use on a mobile phone or tablet.
To use the website, you have to create an account first.
After doing that, you can add your first **wallet**. Every wallet is a seperate collection of expenses.
It is possible to have one wallet for all your expenses, but you can also create multiple ones.
For example, you could start a new wallet for a trip, or for a special event like a birthday party or wedding.
When creating a wallet, you choose the name and the currency.

You can also group your expenses in **categories**, like rent, car, groceries, clothing, etc.
Every category has a color associated with it, to provide some visual clarity.
You do not have to use categories if you do not want to.
When adding a new **expense**, you specify the amount, the date, the payment method, the wallet and the category. You can also add a comment.
There are different ways to view your expense history. You can browse all your expenses on the **history** page.
On this page, all the expenses are displayed in a table.

## Components

`currency.csv` is a file containing currency codes, their names and their symbols.
This file is loaded into the database using `import.py`.
The data is needed so users can choose from every currently used currency when creating a wallet.

### Expensetracker
Main Django application.

### Tracker
Application for the expense tracking functionality, like viewing the dashboard, and adding and viewing wallets, categories and expenses.
It contains six templates that extend `base.html`.

### Users
Application for creating an account, logging in, and logging out.
Based on Django functionality, like `authenticate`, `login`, and `logout`.
Folder `templates` contains the templates for the login page and the register page.

### Static
Contains css, scss, JavaScript, fonts and images.

### Templates
Contains only the `base.html` template and the template for messages that it uses: `messages.html`.

## Made with
* Django https://www.djangoproject.com/
* Bootstrap 4 https://getbootstrap.com/
* Sufee Admin Dashboard Template https://github.com/puikinsh/sufee-admin-dashboard
* Bootstrap Datepicker https://github.com/uxsolutions/bootstrap-datepicker
* Datatables https://datatables.net/
* World currencies csv https://gist.github.com/Chintan7027/fc4708d8b5c8d1639a7c

##### Leony Brok

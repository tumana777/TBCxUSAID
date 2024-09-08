import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QComboBox  # Add QComboBox
from PyQt5 import uic
from PyQt5.QtGui import QDoubleValidator

# Conversion rates for the currency converter
conversion_rates = {
    ("USD", "GEL"): 2.69,
    ("EUR", "GEL"): 2.97,
    ("TRY", "GEL"): 0.08,
    ("CNY", "GEL"): 0.38,
    ("GEL", "USD"): 1 / 2.69,
    ("GEL", "EUR"): 1 / 2.97,
    ("GEL", "TRY"): 1 / 0.08,
    ("GEL", "CNY"): 1 / 0.38,
    ("USD", "EUR"): 2.69 / 2.97,
    ("USD", "TRY"): 2.69 / 0.08,
    ("USD", "CNY"): 2.69 / 0.38,
    ("EUR", "USD"): 2.97 / 2.69,
    ("EUR", "TRY"): 2.97 / 0.08,
    ("EUR", "CNY"): 2.97 / 0.38,
    ("TRY", "USD"): 0.08 / 2.69,
    ("TRY", "EUR"): 0.08 / 2.97,
    ("TRY", "CNY"): 0.08 / 0.38,
    ("CNY", "USD"): 0.38 / 2.69,
    ("CNY", "EUR"): 0.38 / 2.97,
    ("CNY", "TRY"): 0.38 / 0.08,
}

currencies = ["USD", "EUR", "GEL", "TRY", "CNY"]

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi('app.ui', self)  # Load the UI file dynamically

        # Populate the currency combo boxes
        self.from_currency.addItems(currencies)  # Add currency options to the "from_currency"
        self.update_to_currency_options()

        # Set up connections and validators
        self.login_button.clicked.connect(self.handle_login)
        self.convert_button.clicked.connect(self.convert_currency)
        self.clear_button.clicked.connect(self.clear_inputs)
        self.logout_button.clicked.connect(self.logout)

        # Ensure password input is masked
        self.password_input.setEchoMode(QLineEdit.Password)

        # Set validator for amount input
        self.amount_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2))

        # Handle currency selection
        self.from_currency.currentIndexChanged.connect(self.update_to_currency_options)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "admin":
            self.stackedWidget.setCurrentIndex(1)  # Switch to currency converter page
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            self.clear_inputs()

    def convert_currency(self):
        try:
            amount = float(self.amount_input.text())
            from_currency = self.from_currency.currentText()
            to_currency = self.to_currency.currentText()
            result = amount * conversion_rates[(from_currency, to_currency)]
            self.result_label.setText(f"Result: {result:.2f} {to_currency}")
        except KeyError:
            QMessageBox.warning(self, "Conversion Error", "Invalid currency conversion selected.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")

    def update_to_currency_options(self):
        from_currency = self.from_currency.currentText()
        self.to_currency.clear()
        filtered_currencies = [currency for currency in currencies if currency != from_currency]
        self.to_currency.addItems(filtered_currencies)

    def clear_inputs(self):
        self.amount_input.clear()
        self.result_label.setText("Result: ")
        self.from_currency.setCurrentIndex(0)
        self.update_to_currency_options()

    def logout(self):
        self.stackedWidget.setCurrentIndex(0)  # Switch back to login page
        self.username_input.clear()  # Clear username input
        self.password_input.clear()  # Clear password input


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

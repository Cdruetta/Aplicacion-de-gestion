from PySide6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QDialog, QFormLayout, QMessageBox, QLabel, QDateEdit
from PySide6.QtCore import Qt
from datetime import datetime
import sqlite3

class AgregarArticulo(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()  
        self.setWindowTitle("INSUX6 - V1.5.0")
        self.resize(900, 400)

        self.title = QLabel("Agregar Articulo")
        self.title.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.title.setStyleSheet("font-size: 24px; color: #fc0303; font-weight: bold;")  # Cambia el color del texto a blanco
        layout.addWidget(self.title)
    
        self.nombre = QLineEdit()
        self.precio = QLineEdit()
        self.cantidad = QLineEdit()
        self.tipo = QLineEdit()
        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setDisplayFormat("dd-MM-yyyy")
        self.observaciones = QLineEdit()
        self.button = QPushButton("Agregar")
        self.button.clicked.connect(self.agregarArticulos)
        form.addRow("Nombre:", self.nombre)  
        form.addRow("Precio:", self.precio)
        form.addRow("Cantidad:", self.cantidad)
        form.addRow("Tipo:", self.tipo)
        form.addRow("Fecha:", self.fecha_ingreso)
        form.addRow("Observaciones:", self.observaciones)
        layout.addLayout(form)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def agregarArticulos(self):
        nombre = self.nombre.text()
        precio = self.precio.text()
        cantidad = self.cantidad.text()
        tipo = self.tipo.text()
        fecha_ingreso = self.fecha_ingreso.date().toString("dd-MM-yyyy")
        observaciones = self.observaciones.text()

        # Validación de entrada para cada campo
        try:
            precio = float(precio)
        except ValueError:
            QMessageBox.critical(self, "Error de entrada", "Por favor, ingrese un precio válido.")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            QMessageBox.critical(self, "Error de entrada", "Por favor, ingrese una cantidad válida.")
            return

        try:
            datetime.strptime(fecha_ingreso, '%d-%m-%Y')
        except ValueError:
            QMessageBox.critical(self, "Error de entrada", "Por favor, ingrese una fecha válida en el formato 'dd-MM-yyyy'.")
            return

        try:
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articulos WHERE nombre=?", (nombre,))
            if cursor.fetchone() is not None:
                QMessageBox.critical(self, "Error de entrada", "El nombre del artículo ya existe. Por favor, ingrese un nombre diferente.")
                return
            cursor.execute("INSERT INTO articulos (nombre, precio, cantidad, tipo, fecha_ingreso, observaciones) VALUES (?, ?, ?, ?, ?, ?)", 
                (nombre, precio, cantidad, tipo, fecha_ingreso, observaciones))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error de base de datos", f"Ocurrió un error al insertar en la base de datos: {e}")
        else:
            conn.close()
            self.nombre.clear()
            self.precio.clear()
            self.cantidad.clear()
            self.tipo.clear()
            self.fecha_ingreso.clear()
            self.observaciones.clear()

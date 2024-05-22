from PySide6.QtWidgets import QLabel, QDateEdit, QVBoxLayout, QLineEdit, QPushButton, QDialog, QFormLayout, QMessageBox, QCompleter
from PySide6.QtCore import Qt, QStringListModel, QDate
import sqlite3

class Modificar(QDialog):
    def __init__(self): 
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()   
        self.setWindowTitle("INSUX6 - V1.5.0")
        self.resize(900, 400)

        # Agrega un título con estilo personalizado
        self.title = QLabel("Modificar")
        self.title.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.title.setStyleSheet("font-size: 24px; color: #fc0303; font-weight: bold;")  # Cambia el color del texto a blanco
        layout.addWidget(self.title)
    
        # Buscador de artículo (Por nombre)
        self.articulo_nombre = QLineEdit()
        self.completer = QCompleter()

        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM articulos WHERE deleted=0")
        articulos = cursor.fetchall()
        conn.close()

        model = QStringListModel()
        model.setStringList([articulo[0] for articulo in articulos])
        self.completer.setModel(model)
        self.articulo_nombre.setCompleter(self.completer)
        self.articulo_nombre.textChanged.connect(self.updateCompleter)

        # Botón para limpiar el campo de búsqueda
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: #000000;")
        self.clear_button.clicked.connect(self.limpiarBusqueda)

        # Campo para ingresar el ID del artículo a modificar
        self.articulo_id = QLineEdit()
        self.load_button = QPushButton("Cargar Artículo")
        self.load_button.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: #000000;")
        self.load_button.clicked.connect(self.cargarArticulo)
        form.addRow("Buscar Artículo:", self.articulo_nombre)
        form.addRow(self.load_button)
        form.addRow(self.clear_button)  # Agregar el botón "Limpiar" al formulario

        # Campos para mostrar/editar el artículo
        self.nombre = QLineEdit()
        self.precio = QLineEdit()
        self.cantidad = QLineEdit()
        self.tipo = QLineEdit()
        self.fecha_ingreso = QDateEdit()
        self.observaciones = QLineEdit()
        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: black;")
        self.save_button.clicked.connect(self.guardarCambios)
        form.addRow("Nombre:", self.nombre)  
        form.addRow("Precio:", self.precio)
        form.addRow("Cantidad:", self.cantidad)
        form.addRow("Tipo:", self.tipo)
        form.addRow("Fecha:", self.fecha_ingreso)
        form.addRow("Observaciones:", self.observaciones)
        form.addRow(self.save_button)

        layout.addLayout(form)   
        self.setLayout(layout)
    
    def limpiarBusqueda(self):
        self.articulo_nombre.clear()

    def updateCompleter(self):
        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM articulos WHERE nombre LIKE ? AND deleted=0", (self.articulo_nombre.text() + '%',))
        articulos = cursor.fetchall()
        conn.close()
    def cargarArticulo(self):
        articulo_nombre = self.articulo_nombre.text().strip()

        try:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            # Ejecutar la consulta SQL para obtener los detalles del artículo
            cursor.execute("SELECT * FROM articulos WHERE nombre=? AND deleted=0", (articulo_nombre,))
            articulo = cursor.fetchone()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return

        if articulo:
            # Llenar los campos de entrada de texto con los detalles del artículo
            self.articulo_id.setText(str(articulo[0]))  # Asumiendo que el ID es el primer campo de la tupla
            self.nombre.setText(articulo[1])
            self.precio.setText(str(articulo[2]))
            self.cantidad.setText(str(articulo[3]))
            self.tipo.setText(articulo[4])
            fecha_ingreso = QDate.fromString(articulo[5], 'yyyy-MM-dd')  # Asumiendo que la fecha está en formato 'yyyy-MM-dd'
            self.fecha_ingreso.setDate(fecha_ingreso)
            self.observaciones.setText(articulo[6])
            print("Articulo cargado exitosamente")
        else:
            print("Articulo no encontrado")

    def guardarCambios(self):
        articulo_id = self.articulo_id.text().strip()
        nombre = self.nombre.text().strip()
        try:
            precio = float(self.precio.text())
            cantidad = int(self.cantidad.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un precio y una cantidad válidos.")
            return
        
        tipo = self.tipo.text().strip()
        fecha_ingreso = self.fecha_ingreso.text().strip()  # Considera validar el formato de fecha
        observaciones = self.observaciones.text().strip()

        try:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            # Ejecutar la consulta SQL para actualizar los detalles del artículo
            cursor.execute("UPDATE articulos SET nombre=?, precio=?, cantidad=?, tipo=?, fecha_ingreso=?, observaciones=? WHERE id=?", 
                        (nombre, precio, cantidad, tipo, fecha_ingreso, observaciones, articulo_id))
            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Cambios guardados exitosamente")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error",f"Error al guardar los cambios: {e}")
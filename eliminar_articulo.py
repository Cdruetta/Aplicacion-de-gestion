from PySide6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QFormLayout, QMessageBox, QLabel, QTextEdit, QCompleter
from PySide6.QtCore import Qt, QStringListModel
import sqlite3

class Eliminar(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        form = QFormLayout()
        self.setWindowTitle('INSUX6 - V1.5.0')
        self.setStyleSheet('Background-color: #c4b78b;')
        self.resize(900, 400)

        # Agrega un título con estilo personalizado
        self.title = QLabel("Eliminar")
        self.title.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.title.setStyleSheet("font-size: 24px; color: #fc0303; font-weight: bold;")  # Cambia el color del texto a blanco
        layout.addWidget(self.title)  # Añade el título al diseño

        # Buscador de articulo (Por nombre)
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

        # Connect the textChanged signal to the updateCompleter slot
        self.articulo_nombre.textChanged.connect(self.updateCompleter)

        self.load_button = QPushButton('Buscar Articulo')
        self.load_button.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: #000000;")
        self.load_button.clicked.connect(self.buscarArt)
        form.addRow('Nombre Articulo:', self.articulo_nombre)
        form.addRow(self.load_button)

        # Datos
        self.nombre = QTextEdit()
        self.precio = QTextEdit()
        self.cantidad = QTextEdit()
        self.tipo = QTextEdit()
        self.fecha_ingreso = QTextEdit()
        self.observaciones = QTextEdit()

        # Boton eliminar
        self.save_button = QPushButton("Eliminar Articulo")
        self.save_button.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: black;")
        self.save_button.clicked.connect(self.eliminarArt)

        # Muestra Datos
        form.addRow("Nombre:", self.nombre) 
        form.addRow("Precio:", self.precio)
        form.addRow("Unidades:", self.cantidad)
        form.addRow("Tipo:", self.tipo)
        form.addRow("Fecha:", self.fecha_ingreso)
        form.addRow("Observaciones:", self.observaciones)
        form.addRow(self.save_button)

        layout.addLayout(form)
        self.setLayout(layout)

    def updateCompleter(self):
        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM articulos WHERE nombre LIKE ? AND deleted=0", (self.articulo_nombre.text() + '%',))
        articulos = cursor.fetchall()
        conn.close()

        model = QStringListModel()
        model.setStringList([articulo[0] for articulo in articulos])

        self.completer.setModel(model)

            
    def buscarArt(self):
        articulo_nombre = self.articulo_nombre.text()
        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articulos WHERE nombre=? AND deleted=0", (articulo_nombre,))
        articulo = cursor.fetchone()
        conn.close()

        if articulo:
            self.nombre.setText(articulo[1])
            self.precio.setText(str(articulo[2]))
            self.cantidad.setText(str(articulo[3]))
            self.tipo.setText(articulo[4])
            self.fecha_ingreso.setText(articulo[5])
            self.observaciones.setText(articulo[6])
        else:
            QMessageBox.information(self, "Error", "Articulo No Encontrado")
    def eliminarArt(self):
        articulo_nombre = self.articulo_nombre.text()

        conn = sqlite3.connect('mydb.db')
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE articulos SET deleted = 1 WHERE nombre = ?", (articulo_nombre,))
            conn.commit()
            QMessageBox.information(self, "Articulo Eliminado", "El articulo ha sido eliminado con éxito.")

            # Actualiza los datos del modelo
            #self.model.select()

            self.nombre.clear()
            self.precio.clear()
            self.cantidad.clear()
            self.tipo.clear()
            self.fecha_ingreso.clear()
            self.observaciones.clear()            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error al Eliminar Articulo', f'Error: {str(e)}')
        finally:
            conn.close()

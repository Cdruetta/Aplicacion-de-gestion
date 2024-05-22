from PySide6.QtWidgets import QLabel,QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import sqlite3

class ActualizarPrecio(QDialog):
    def __init__(self): 
        super().__init__()
        layout = QFormLayout()
        self.setWindowTitle("INSUX6 - V1.5.0")
        self.resize(400, 200)

        self.title = QLabel("Actualizar Precios")
        self.title.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.title.setStyleSheet("font-size: 24px; color: #fc0303; font-weight: bold;")  # Cambia el color del texto a blanco
        layout.addWidget(self.title)

        # Campo para ingresar el aumento fijo
        self.aumento_fijo = QLineEdit()
        layout.addRow("Aumento Fijo ($):", self.aumento_fijo)

        # Campo para ingresar el porcentaje de aumento
        self.porcentaje_aumento = QLineEdit()
        layout.addRow("Porcentaje de Aumento (%):", self.porcentaje_aumento)

        # Botón para aplicar el aumento
        self.btActualizar = QPushButton("Actualizar")
        self.btActualizar.clicked.connect(self.actualizarPrecios)
        layout.addRow(self.btActualizar)

        self.setLayout(layout)
    
    # Método para actualizar los precios
    def actualizarPrecios(self):
        aumento_fijo = self.aumento_fijo.text()
        porcentaje_aumento = self.porcentaje_aumento.text()

        if aumento_fijo and porcentaje_aumento:
            QMessageBox.warning(self, "Error", "Por favor, ingrese solo un tipo de aumento: fijo o porcentaje.")
            return

        if aumento_fijo:
            aumento = float(aumento_fijo)
            self.actualizarPreciosFijo(aumento)
        elif porcentaje_aumento:
            porcentaje = float(porcentaje_aumento) / 100 + 1
            self.actualizarPreciosPorcentaje(porcentaje)
        else:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un aumento.")

    def actualizarPreciosFijo(self, aumento):
        try:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            # Ejecutar la consulta SQL para obtener todos los artículos
            cursor.execute("SELECT * FROM articulos")
            articulos = cursor.fetchall()
            
            for articulo in articulos:
                id_articulo = articulo[0]
                precio_actual = articulo[2]
                nuevo_precio = precio_actual + aumento
                # Ejecutar la consulta SQL para actualizar el precio del artículo
                cursor.execute("UPDATE articulos SET precio=? WHERE id=?", (nuevo_precio, id_articulo))
            
            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Precios actualizados exitosamente")
            self.close()  # Cerrar la ventana
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar los precios: {e}")

    def actualizarPreciosPorcentaje(self, porcentaje):
        try:
            # Conectar a la base de datos SQLite
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            # Ejecutar la consulta SQL para obtener todos los artículos
            cursor.execute("SELECT * FROM articulos")
            articulos = cursor.fetchall()
            
            for articulo in articulos:
                id_articulo = articulo[0]
                precio_actual = articulo[2]
                nuevo_precio = precio_actual * porcentaje
                # Ejecutar la consulta SQL para actualizar el precio del artículo
                cursor.execute("UPDATE articulos SET precio=? WHERE id=?", (nuevo_precio, id_articulo))
            
            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Éxito", "Precios actualizados exitosamente")
            self.close()  # Cerrar la ventana
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar los precios: {e}")

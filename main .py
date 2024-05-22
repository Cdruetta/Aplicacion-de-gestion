from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox, QPushButton
from PySide6.QtCore import Qt
from agregar_articulo import AgregarArticulo
from modificar_articulo import Modificar
from ver_articulo import VerArticulo
from eliminar_articulo import Eliminar
from actualizar_precio import ActualizarPrecio
import sqlite3
import sys

def initialize_db():
    con = sqlite3.connect("mydb.db")
    cursor = con.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS articulos (
           id INTEGER PRIMARY KEY,
           nombre TEXT,
           precio REAL,
           cantidad INTEGER,
           tipo TEXT,
           Fecha_ingreso DATE,
           observaciones TEXT,  
           deleted INTEGER DEFAULT 0
       )
    ''')

    con.commit()
    con.close()
   

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        initialize_db()
        layout = QVBoxLayout()
        self.texto = QLabel()
        self.texto.setFont("Roboto, 25, Bold")
        self.texto.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.texto)
        titulos = ["Agregar Articulo", "Ver Articulo",
                   "Modificar Articulo", "Actualizar Precio","Eliminar Articulo"]

        for i in range(5):
            boton = QPushButton(titulos[i])
            boton.setDefault(True)
            if titulos[i] == "Agregar Articulo":
                boton.clicked.connect(self.abrirVentanaAgregar)
            elif titulos[i] == "Ver Articulo":
                boton.clicked.connect(self.abrirVentanaVer)
            elif titulos[i] == "Modificar Articulo":
                boton.clicked.connect(self.modificar)
            elif titulos[i] == "Actualizar Precio":
                boton.clicked.connect(self.actualizar)
            elif titulos[i] == "Eliminar Articulo":
                boton.clicked.connect(self.eliminar)

            layout.addWidget(boton)

        centralWidget = QWidget()
        centralWidget.setObjectName("centralWidget")
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.setGeometry(100, 100, 600, 600)


        centralWidget.setStyleSheet("""
            QWidget {
                background-image: url("fondocopado.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton {
                background: #c4b78b;
            }
        """)
    def abrirVentanaAgregar(self):
        try:
            self.ventana_agregar = AgregarArticulo()
            self.ventana_agregar.show()
        except Exception as e:
            QMessageBox.critical(self, f"Ocurrió un error al abrir la ventana de agregar articulo {e}")
            
    def abrirVentanaVer(self):
        try:
            self.ventana_ver = VerArticulo()
            self.ventana_ver.show()
        except Exception as e:
            QMessageBox.critical(self, "Error al abrir la ventana de ver articulo", str(e))
            

    def modificar(self):
        try:
            self.ventana_modificar = Modificar()
            self.ventana_modificar.show()
        except Exception as e:
             QMessageBox.critical(self, f"Ocurrió un error al abrir la ventana de modificar articulo {e}")

    def actualizar(self):
        try:
            self.ventana_actualizar = ActualizarPrecio()
            self.ventana_actualizar.show()
        except Exception as e:
            QMessageBox.critical(f"Error al abrir la ventana de actualizar precios: {e}")

            
    def eliminar(self):
        try:
            self.ventana_eliminar = Eliminar()
            self.ventana_eliminar.show()
        except Exception as e:
            QMessageBox.critical(f"Error al abrir la ventana de eliminar artículo: {e}") 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    css = '*{font-size: 30px; background-color: #c4b78b; color: #0f0f0f;}'
    app.setStyleSheet(css)
    window = MainWindow()
    window.show()
    app.setStyle("Fusion")
    app.exec()

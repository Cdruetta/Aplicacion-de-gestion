from PySide6.QtWidgets import QTableView, QVBoxLayout, QDialog, QMessageBox, QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication
from PySide6.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PySide6.QtCore import Qt, QSortFilterProxyModel

class ModeloDeTabla(QSqlTableModel):
    def rowCount(self, parent=1):
        if parent and parent.isValid():
            return 0
        db = QSqlDatabase.database()
        query = QSqlQuery(db)
        query.exec_("SELECT COUNT(*) FROM articulos WHERE deleted = 0")
        query.next()
        return query.value(0)


    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 1:
                return "Nombre"
            elif section == 2:
                return "Precio"
            elif section == 3:
                return "Cantidad"
            elif section == 4:
                return "Tipo"
            elif section == 5:
                return "Fecha de Ingreso"
            elif section == 6:
                return "Observaciones"
        return super().headerData(section, orientation, role)
    

    def flags(self, index):
        flags = super().flags(index)
        if index.column() in [1, 2, 3, 4, 5, ]:  # Ajusta este valor según tus necesidades
            return Qt.ItemIsSelectable
        return flags
    

class VerArticulo(QDialog):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Ver Articulo")
        self.resize(1500, 600)
        self.title = QLabel("INVENTARIO")
        self.setWindowTitle("INSUX6 - V1.5.0")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; color: #fc0303; font-weight: bold")
        layout.addWidget(self.title)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydb.db')
        if not db.open():
            QMessageBox.critical(self, "Error de base de datos", db.lastError().text())
            return

        self.model = ModeloDeTabla(self)
        self.model.setTable("articulos")
        self.model.setFilter("deleted = 0")  # Filtra los artículos no eliminados

        if not self.model.select():
            QMessageBox.critical(self, "Error de selección", self.model.lastError().text())
            return

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(1)

        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Buscar...")
        self.search_field.textChanged.connect(self.proxy.setFilterRegularExpression)

        hbox = QHBoxLayout()
        hbox.addWidget(self.search_field)

        self.clear_button = QPushButton("Limpiar")
        self.clear_button.setFixedSize(100, 30)
        self.clear_button.clicked.connect(self.search_field.clear)
        hbox.addWidget(self.clear_button)

        layout.addLayout(hbox)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setStyleSheet("""
            QTableView {
        border: 2px solid #c4b78b;
        background-color: #c4b78b;
        font-size: 10px;
        font-family: Calibri;  # Cambia la fuente a Calibri
        
     }
    QTableView::item {
        font-weight: bold;  # Hace que la fuente esté en negrita
    }
""")
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setWordWrap(True)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(7, True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionMode(QTableView.SingleSelection)

        layout.addWidget(self.table)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = VerArticulo()
    window.show()
    app.exec_()


B0 = '#000000'                      # '#000000'
B150 = '#FFFFFF'                    # '#FFFFFF'

Background = '#19232D'              # '#19232D' Color de fondo general
B30 = '#37414F'                     # '#37414F' Hover tabla, background menu, hover boton
Border = '#455364'                  # '#455364' Bordes, borde interior cmb, separador
B50 = '#54687A'                     # '#54687A' Background hover default de botton, background selected tab
B60 = '#60798B'                     # '#60798B' No hover slidebar, Menu Separator, Background button checked, pressed y selected
DeactivatedTextColor = '#9DA9B5'    # '#9DA9B5' Desactived text color general
TextColor = '#E0E1E3'               # '#E0E1E3' Actived text color general
DarkBackground = '#0F1A25'          # '#0F1A25'


C20 = '#26486B'  # '#26486B' TabBar, Slider, ProgressBar
C70 = '#259AE9'  # '#259AE9' TabBar y otros

TableSelect = '#83716B'  # FF7F3F '#F0651F' F0651F
ColorStrong = '#F0651F'  # '#F0651F' F0651F
Hover_and_SelectTable = '#FFA375'  # '#346792' Hover de componentes y select de tabla
Hover_Combo = '#844426'
Focus_and_HoverMenus = '#FD884C'   # '#1A72BB' Focus de componentes y hover menus

ColorSelectedWeak = '#D66100'

custom_css = '''
QToolBar {
    border: 1px solid ''' + Background + '''; 
    background-color: ''' + Background + '''; 
    padding: 4px;
}

QToolTip {
    border: 1px solid ''' + ColorStrong + '''; 
    background-color: ''' + DarkBackground + ''';
} 

QToolButton {
    border: 1px solid ''' + ColorStrong + '''; 
    background-color: ''' + DarkBackground + ''';
} 

QToolButton:hover {
    border: 1px solid ''' + Focus_and_HoverMenus + '''; 
    background-color: ''' + B30 + ''';
}

QToolButton:pressed {
    border: 1px solid ''' + Focus_and_HoverMenus + '''; 
    background-color: ''' + Border + ''';
}

QToolButton:disabled {
    border: 1px solid ''' + Border + '''; 
    background-color: ''' + DarkBackground + ''';
    color: ''' + Border + ''';
}

QPushButton {
    border: 1px solid ''' + ColorStrong + '''; 
    background-color: ''' + DarkBackground + ''';
} 

QPushButton:hover {
    border: 1px solid ''' + Focus_and_HoverMenus + '''; 
    background-color: ''' + B30 + ''';
}

QPushButton:pressed {
    border: 1px solid ''' + Focus_and_HoverMenus + '''; 
    background-color: ''' + Border + ''';
}

QPushButton:disabled {
    border: 1px solid ''' + Border + '''; 
    background-color: ''' + DarkBackground + ''';
    color: ''' + Border + ''';
}

QMenuBar {
    background-color: ''' + DarkBackground + ''';
    border-color: ''' + DarkBackground + ''';
    border-bottom-color: ''' + ColorStrong + ''';
}

QStatusBar {
    background-color: ''' + DarkBackground + ''';
    border-color: ''' + DarkBackground + ''';
    border-top-color: ''' + ColorStrong + ''';
}

QProgressBar {
    border: 1px solid ''' + ColorStrong + '''; 
    background-color: ''' + DarkBackground + ''';
} 

QTableWidget:focus {
    border-color: ''' + Border + ''';
}

QProgressBar:disabled {
    border: 1px solid ''' + Border + '''; 
    color: ''' + Border + ''';
}

QTableWidget::item:hover:!selected{
    background-color: ''' + Background + ''';
}

QTableWidget::item {
    border: 2px solid transparent;
}

QTableWidget::item:hover:selected, 
QTableWidget::item:!hover:selected {
    background-color: ''' + TableSelect + ''';
    border-top: 2px solid ''' + ColorStrong + ''';
    border-bottom: 2px solid ''' + ColorStrong + ''';
}




'''




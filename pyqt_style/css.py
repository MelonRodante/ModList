from pyqt_style import colors, style_rc

style = '''
/* Light Style - QDarkStyleSheet ------------------------------------------ */
/*

See Qt documentation:

  - https://doc.qt.io/qt-5/stylesheet.html
  - https://doc.qt.io/qt-5/stylesheet-reference.html
  - https://doc.qt.io/qt-5/stylesheet-examples.html

--------------------------------------------------------------------------- */
/* Reset elements ------------------------------------------------------------

Resetting everything helps to unify styles across different operating systems

--------------------------------------------------------------------------- */
* {
  padding: 0px;
  margin: 0px;
  border: 0px;
  border-style: none;
  border-image: none;
  outline: 0;
}

/* specific reset for elements inside QToolBar */
QToolBar * {
  margin: 0px;
  padding: 0px;
}

/* QWidget ----------------------------------------------------------------

--------------------------------------------------------------------------- */
QWidget {
  background-color: ''' + colors.Background + ''';
  border: 0px solid ''' + colors.Border + ''';
  padding: 0px;
  color: ''' + colors.TextColor + ''';
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
  selection-color: ''' + colors.TextColor + ''';
}

QWidget:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  selection-background-color: ''' + colors.C20 + ''';
  selection-color: ''' + colors.DeactivatedTextColor + ''';
}

QWidget::item:selected {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QWidget::item:hover:!selected {
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

/* QMainWindow ------------------------------------------------------------

This adjusts the splitter in the dock widget, not qsplitter
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmainwindow

--------------------------------------------------------------------------- */
QMainWindow::separator {
  background-color: ''' + colors.Border + ''';
  border: 0px solid ''' + colors.Background + ''';
  spacing: 0px;
  padding: 2px;
}

QMainWindow::separator:hover {
  background-color: ''' + colors.B60 + ''';
  border: 0px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QMainWindow::separator:horizontal {
  width: 5px;
  margin-top: 2px;
  margin-bottom: 2px;
  image: url(":/qss_icons/dark/rc/toolbar_separator_vertical.png");
}

QMainWindow::separator:vertical {
  height: 5px;
  margin-left: 2px;
  margin-right: 2px;
  image: url(":/qss_icons/dark/rc/toolbar_separator_horizontal.png");
}

/* QToolTip ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtooltip

--------------------------------------------------------------------------- */
QToolTip {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.TextColor + ''';
  /* If you remove the border property, background stops working on Windows */
  border: none;
  /* Remove padding, for fix combo box tooltip */
  padding: 0px;
  /* Remove opacity, fix #174 - may need to use RGBA */
}

/* QStatusBar -------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qstatusbar

--------------------------------------------------------------------------- */
QStatusBar {
  border: 1px solid ''' + colors.Border + ''';
  /* Fixes Spyder #9120, #9121 */
  background: ''' + colors.Border + ''';
  /* Fixes #205, white vertical borders separating items */
}

QStatusBar::item {
  border: none;
}

QStatusBar QToolTip {
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
  border: 1px solid ''' + colors.Background + ''';
  color: ''' + colors.Background + ''';
  /* Remove padding, for fix combo box tooltip */
  padding: 0px;
  /* Reducing transparency to read better */
  opacity: 230;
}

QStatusBar QLabel {
  /* Fixes Spyder #9120, #9121 */
  background: transparent;
}

/* QCheckBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcheckbox

--------------------------------------------------------------------------- */
QCheckBox {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  spacing: 4px;
  outline: none;
  padding-top: 4px;
  padding-bottom: 4px;
}

QCheckBox:focus {
  border: none;
}

QCheckBox QWidget:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

QCheckBox::indicator {
  margin-left: 2px;
  height: 14px;
  width: 14px;
}

QCheckBox::indicator:unchecked {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked.png");
}

QCheckBox::indicator:unchecked:hover, QCheckBox::indicator:unchecked:focus, QCheckBox::indicator:unchecked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_focus.png");
}

QCheckBox::indicator:unchecked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_disabled.png");
}

QCheckBox::indicator:checked {
  image: url(":/qss_icons/dark/rc/checkbox_checked.png");
}

QCheckBox::indicator:checked:hover, QCheckBox::indicator:checked:focus, QCheckBox::indicator:checked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_checked_focus.png");
}

QCheckBox::indicator:checked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_checked_disabled.png");
}

QCheckBox::indicator:indeterminate {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate.png");
}

QCheckBox::indicator:indeterminate:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate_disabled.png");
}

QCheckBox::indicator:indeterminate:focus, QCheckBox::indicator:indeterminate:hover, QCheckBox::indicator:indeterminate:pressed {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate_focus.png");
}

/* QGroupBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qgroupbox

--------------------------------------------------------------------------- */
QGroupBox {
  font-weight: bold;
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  padding: 2px;
  margin-top: 6px;
  margin-bottom: 4px;
}

QGroupBox::title {
  subcontrol-origin: margin;
  subcontrol-position: top left;
  left: 4px;
  padding-left: 2px;
  padding-right: 4px;
  padding-top: -4px;
}

QGroupBox::indicator {
  margin-left: 2px;
  margin-top: 2px;
  padding: 0;
  height: 14px;
  width: 14px;
}

QGroupBox::indicator:unchecked {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_unchecked.png");
}

QGroupBox::indicator:unchecked:hover, QGroupBox::indicator:unchecked:focus, QGroupBox::indicator:unchecked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_focus.png");
}

QGroupBox::indicator:unchecked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_disabled.png");
}

QGroupBox::indicator:checked {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_checked.png");
}

QGroupBox::indicator:checked:hover, QGroupBox::indicator:checked:focus, QGroupBox::indicator:checked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_checked_focus.png");
}

QGroupBox::indicator:checked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_checked_disabled.png");
}

/* QRadioButton -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qradiobutton

--------------------------------------------------------------------------- */
QRadioButton {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  spacing: 4px;
  padding-top: 4px;
  padding-bottom: 4px;
  border: none;
  outline: none;
}

QRadioButton:focus {
  border: none;
}

QRadioButton:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border: none;
  outline: none;
}

QRadioButton QWidget {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  spacing: 0px;
  padding: 0px;
  outline: none;
  border: none;
}

QRadioButton::indicator {
  border: none;
  outline: none;
  margin-left: 2px;
  height: 14px;
  width: 14px;
}

QRadioButton::indicator:unchecked {
  image: url(":/qss_icons/dark/rc/radio_unchecked.png");
}

QRadioButton::indicator:unchecked:hover, QRadioButton::indicator:unchecked:focus, QRadioButton::indicator:unchecked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_unchecked_focus.png");
}

QRadioButton::indicator:unchecked:disabled {
  image: url(":/qss_icons/dark/rc/radio_unchecked_disabled.png");
}

QRadioButton::indicator:checked {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked.png");
}

QRadioButton::indicator:checked:hover, QRadioButton::indicator:checked:focus, QRadioButton::indicator:checked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked_focus.png");
}

QRadioButton::indicator:checked:disabled {
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked_disabled.png");
}

/* QMenuBar ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenubar

--------------------------------------------------------------------------- */
QMenuBar {
  background-color: ''' + colors.Border + ''';
  padding: 2px;
  border: 1px solid ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  selection-background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

QMenuBar:focus {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QMenuBar::item {
  background: transparent;
  padding: 4px;
}

QMenuBar::item:selected {
  padding: 4px;
  background: transparent;
  border: 0px solid ''' + colors.Border + ''';
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

QMenuBar::item:pressed {
  padding: 4px;
  border: 0px solid ''' + colors.Border + ''';
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
  color: ''' + colors.TextColor + ''';
  margin-bottom: 0px;
  padding-bottom: 0px;
}

/* QMenu ------------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qmenu

--------------------------------------------------------------------------- */
QMenu {
  border: 0px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  margin: 0px;
  background-color: ''' + colors.B30 + ''';
  selection-background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

QMenu::separator {
  height: 1px;
  background-color: ''' + colors.B60 + ''';
  color: ''' + colors.TextColor + ''';
}

QMenu::item {
  background-color: ''' + colors.B30 + ''';
  padding: 4px 24px 4px 28px;
  /* Reserve space for selection border */
  border: 1px transparent ''' + colors.Border + ''';
}

QMenu::item:selected {
  color: ''' + colors.TextColor + ''';
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

QMenu::item:pressed {
  background-color: ''' + colors.Focus_and_HoverMenus + ''';
}

QMenu::icon {
  padding-left: 10px;
  width: 14px;
  height: 14px;
}

QMenu::indicator {
  padding-left: 8px;
  width: 12px;
  height: 12px;
  /* non-exclusive indicator = check box style indicator (see QActionGroup::setExclusive) */
  /* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
}

QMenu::indicator:non-exclusive:unchecked {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked.png");
}

QMenu::indicator:non-exclusive:unchecked:hover, QMenu::indicator:non-exclusive:unchecked:focus, QMenu::indicator:non-exclusive:unchecked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_focus.png");
}

QMenu::indicator:non-exclusive:unchecked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_disabled.png");
}

QMenu::indicator:non-exclusive:checked {
  image: url(":/qss_icons/dark/rc/checkbox_checked.png");
}

QMenu::indicator:non-exclusive:checked:hover, QMenu::indicator:non-exclusive:checked:focus, QMenu::indicator:non-exclusive:checked:pressed {
  border: none;
  image: url(":/qss_icons/dark/rc/checkbox_checked_focus.png");
}

QMenu::indicator:non-exclusive:checked:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_checked_disabled.png");
}

QMenu::indicator:non-exclusive:indeterminate {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate.png");
}

QMenu::indicator:non-exclusive:indeterminate:disabled {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate_disabled.png");
}

QMenu::indicator:non-exclusive:indeterminate:focus, QMenu::indicator:non-exclusive:indeterminate:hover, QMenu::indicator:non-exclusive:indeterminate:pressed {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate_focus.png");
}

QMenu::indicator:exclusive:unchecked {
  image: url(":/qss_icons/dark/rc/radio_unchecked.png");
}

QMenu::indicator:exclusive:unchecked:hover, QMenu::indicator:exclusive:unchecked:focus, QMenu::indicator:exclusive:unchecked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_unchecked_focus.png");
}

QMenu::indicator:exclusive:unchecked:disabled {
  image: url(":/qss_icons/dark/rc/radio_unchecked_disabled.png");
}

QMenu::indicator:exclusive:checked {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked.png");
}

QMenu::indicator:exclusive:checked:hover, QMenu::indicator:exclusive:checked:focus, QMenu::indicator:exclusive:checked:pressed {
  border: none;
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked_focus.png");
}

QMenu::indicator:exclusive:checked:disabled {
  outline: none;
  image: url(":/qss_icons/dark/rc/radio_checked_disabled.png");
}

QMenu::right-arrow {
  margin: 5px;
  padding-left: 12px;
  image: url(":/qss_icons/dark/rc/arrow_right.png");
  height: 12px;
  width: 12px;
}

/* QAbstractItemView ------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcombobox

--------------------------------------------------------------------------- */
QAbstractItemView {
  alternate-background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
}

QAbstractItemView QLineEdit {
  padding: 2px;
}

/* QAbstractScrollArea ----------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qabstractscrollarea

--------------------------------------------------------------------------- */
QAbstractScrollArea {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  /* fix #159 */
  padding: 2px;
  /* remove min-height to fix #244 */
  color: ''' + colors.TextColor + ''';
}

QAbstractScrollArea:disabled {
  color: ''' + colors.DeactivatedTextColor + ''';
}

/* QScrollArea ------------------------------------------------------------

--------------------------------------------------------------------------- */
QScrollArea QWidget QWidget:disabled {
  background-color: ''' + colors.Background + ''';
}

/* QScrollBar -------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qscrollbar

--------------------------------------------------------------------------- */
QScrollBar:horizontal {
  height: 16px;
  margin: 2px 16px 2px 16px;
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  background-color: ''' + colors.Background + ''';
}

QScrollBar:vertical {
  background-color: ''' + colors.Background + ''';
  width: 16px;
  margin: 16px 2px 16px 2px;
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
}

QScrollBar::handle:horizontal {
  background-color: ''' + colors.B60 + ''';
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  min-width: 8px;
}

QScrollBar::handle:horizontal:hover {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
  border: ''' + colors.Hover_and_SelectTable + ''';
  border-radius: 4px;
  min-width: 8px;
}

QScrollBar::handle:horizontal:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QScrollBar::handle:vertical {
  background-color: ''' + colors.B60 + ''';
  border: 1px solid ''' + colors.Border + ''';
  min-height: 8px;
  border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
  border: ''' + colors.Hover_and_SelectTable + ''';
  border-radius: 4px;
  min-height: 8px;
}

QScrollBar::handle:vertical:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QScrollBar::add-line:horizontal {
  margin: 0px 0px 0px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_right_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: right;
  subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
  border-image: url(":/qss_icons/dark/rc/arrow_right.png");
  height: 12px;
  width: 12px;
  subcontrol-position: right;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
  border-image: url(":/qss_icons/dark/rc/arrow_down.png");
  height: 12px;
  width: 12px;
  subcontrol-position: bottom;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
  margin: 0px 3px 0px 3px;
  border-image: url(":/qss_icons/dark/rc/arrow_left_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: left;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
  border-image: url(":/qss_icons/dark/rc/arrow_left.png");
  height: 12px;
  width: 12px;
  subcontrol-position: left;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
  margin: 3px 0px 3px 0px;
  border-image: url(":/qss_icons/dark/rc/arrow_up_disabled.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on {
  border-image: url(":/qss_icons/dark/rc/arrow_up.png");
  height: 12px;
  width: 12px;
  subcontrol-position: top;
  subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
  background: none;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
  background: none;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
  background: none;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
  background: none;
}

/* QTextEdit --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-specific-widgets

--------------------------------------------------------------------------- */
QTextEdit {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  border: 1px solid ''' + colors.Border + ''';
}

QTextEdit:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QTextEdit:selected {
  background: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

/* QPlainTextEdit ---------------------------------------------------------

--------------------------------------------------------------------------- */
QPlainTextEdit {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  border: 1px solid ''' + colors.Border + ''';
}

QPlainTextEdit:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QPlainTextEdit:selected {
  background: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

/* QSizeGrip --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qsizegrip

--------------------------------------------------------------------------- */
QSizeGrip {
  background: transparent;
  width: 12px;
  height: 12px;
  image: url(":/qss_icons/dark/rc/window_grip.png");
}

/* QStackedWidget ---------------------------------------------------------

--------------------------------------------------------------------------- */
QStackedWidget {
  padding: 2px;
  border: 1px solid ''' + colors.Border + ''';
  border: 1px solid ''' + colors.Background + ''';
}

/* QToolBar ---------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbar

--------------------------------------------------------------------------- */
QToolBar {
  background-color: ''' + colors.Border + ''';
  border-bottom: 1px solid ''' + colors.Background + ''';
  padding: 1px;
  font-weight: bold;
  spacing: 2px;
}

QToolBar:disabled {
  /* Fixes #272 */
  background-color: ''' + colors.Border + ''';
}

QToolBar::handle:horizontal {
  width: 16px;
  image: url(":/qss_icons/dark/rc/toolbar_move_horizontal.png");
}

QToolBar::handle:vertical {
  height: 16px;
  image: url(":/qss_icons/dark/rc/toolbar_move_vertical.png");
}

QToolBar::separator:horizontal {
  width: 16px;
  image: url(":/qss_icons/dark/rc/toolbar_separator_horizontal.png");
}

QToolBar::separator:vertical {
  height: 16px;
  image: url(":/qss_icons/dark/rc/toolbar_separator_vertical.png");
}

QToolButton#qt_toolbar_ext_button {
  background: ''' + colors.Border + ''';
  border: 0px;
  color: ''' + colors.TextColor + ''';
  image: url(":/qss_icons/dark/rc/arrow_right.png");
}

/* QAbstractSpinBox -------------------------------------------------------

--------------------------------------------------------------------------- */
QAbstractSpinBox {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  /* This fixes 103, 111 */
  padding-top: 2px;
  /* This fixes 103, 111 */
  padding-bottom: 2px;
  padding-left: 4px;
  padding-right: 4px;
  border-radius: 4px;
  /* min-width: 5px; removed to fix 109 */
}

QAbstractSpinBox:up-button {
  background-color: transparent ''' + colors.Background + ''';
  subcontrol-origin: border;
  subcontrol-position: top right;
  border-left: 1px solid ''' + colors.Border + ''';
  border-bottom: 1px solid ''' + colors.Border + ''';
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin: 1px;
  width: 12px;
  margin-bottom: -1px;
}

QAbstractSpinBox::up-arrow, QAbstractSpinBox::up-arrow:disabled, QAbstractSpinBox::up-arrow:off {
  image: url(":/qss_icons/dark/rc/arrow_up_disabled.png");
  height: 8px;
  width: 8px;
}

QAbstractSpinBox::up-arrow:hover {
  image: url(":/qss_icons/dark/rc/arrow_up.png");
}

QAbstractSpinBox:down-button {
  background-color: transparent ''' + colors.Background + ''';
  subcontrol-origin: border;
  subcontrol-position: bottom right;
  border-left: 1px solid ''' + colors.Border + ''';
  border-top: 1px solid ''' + colors.Border + ''';
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  margin: 1px;
  width: 12px;
  margin-top: -1px;
}

QAbstractSpinBox::down-arrow, QAbstractSpinBox::down-arrow:disabled, QAbstractSpinBox::down-arrow:off {
  image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QAbstractSpinBox::down-arrow:hover {
  image: url(":/qss_icons/dark/rc/arrow_down.png");
}

QAbstractSpinBox:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.TextColor + ''';
}

QAbstractSpinBox:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QAbstractSpinBox:selected {
  background: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

/* ------------------------------------------------------------------------ */
/* DISPLAYS --------------------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QLabel -----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qframe

--------------------------------------------------------------------------- */
QLabel {
  background-color: ''' + colors.Background + ''';
  border: 0px solid ''' + colors.Border + ''';
  padding: 2px;
  margin: 0px;
  color: ''' + colors.TextColor + ''';
}

QLabel:disabled {
  background-color: ''' + colors.Background + ''';
  border: 0px solid ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

/* QTextBrowser -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qabstractscrollarea

--------------------------------------------------------------------------- */
QTextBrowser {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
}

QTextBrowser:disabled {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
}

QTextBrowser:hover, QTextBrowser:!hover, QTextBrowser:selected, QTextBrowser:pressed {
  border: 1px solid ''' + colors.Border + ''';
}

/* QGraphicsView ----------------------------------------------------------

--------------------------------------------------------------------------- */
QGraphicsView {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
}

QGraphicsView:disabled {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
}

QGraphicsView:hover, QGraphicsView:!hover, QGraphicsView:selected, QGraphicsView:pressed {
  border: 1px solid ''' + colors.Border + ''';
}

/* QCalendarWidget --------------------------------------------------------

--------------------------------------------------------------------------- */
QCalendarWidget {
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
}

QCalendarWidget:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

/* QLCDNumber -------------------------------------------------------------

--------------------------------------------------------------------------- */
QLCDNumber {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
}

QLCDNumber:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

/* QProgressBar -----------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qprogressbar

--------------------------------------------------------------------------- */
QProgressBar {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  text-align: center;
}

QProgressBar:disabled {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
  text-align: center;
}

QProgressBar::chunk {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Background + ''';
  border-radius: 4px;
}

QProgressBar::chunk:disabled {
  background-color: ''' + colors.C20 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
}

/* ------------------------------------------------------------------------ */
/* BUTTONS ---------------------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QPushButton ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qpushbutton

--------------------------------------------------------------------------- */
QPushButton {
  background-color: ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
  border: none;
}

QPushButton:disabled {
  background-color: ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
  padding: 2px;
}

QPushButton:checked {
  background-color: ''' + colors.B60 + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

QPushButton:checked:disabled {
  background-color: ''' + colors.B60 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

QPushButton:checked:selected {
  background: ''' + colors.B60 + ''';
}

QPushButton:hover {
  background-color: ''' + colors.B50 + ''';
  color: ''' + colors.TextColor + ''';
}

QPushButton:pressed {
  background-color: ''' + colors.B60 + ''';
}

QPushButton:selected {
  background: ''' + colors.B60 + ''';
  color: ''' + colors.TextColor + ''';
}

QPushButton::menu-indicator {
  subcontrol-origin: padding;
  subcontrol-position: bottom right;
  bottom: 4px;
}

QDialogButtonBox QPushButton {
  /* Issue #194 #248 - Special case of QPushButton inside dialogs, for better UI */
  min-width: 80px;
}

/* QToolButton ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbutton

--------------------------------------------------------------------------- */
QToolButton {
  background-color: ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
  border: none;
  /* The subcontrols below are used only in the DelayedPopup mode */
  /* The subcontrols below are used only in the MenuButtonPopup mode */
  /* The subcontrol below is used only in the InstantPopup or DelayedPopup mode */
}

QToolButton:disabled {
  background-color: ''' + colors.Border + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
  padding: 2px;
}

QToolButton:checked {
  background-color: ''' + colors.B60 + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

QToolButton:checked:disabled {
  background-color: ''' + colors.B60 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  border-radius: 4px;
  padding: 2px;
  outline: none;
}

QToolButton:checked:hover {
  background-color: ''' + colors.B50 + ''';
  color: ''' + colors.TextColor + ''';
}

QToolButton:checked:pressed {
  background-color: ''' + colors.B60 + ''';
}

QToolButton:checked:selected {
  background: ''' + colors.B60 + ''';
  color: ''' + colors.TextColor + ''';
}

QToolButton:hover {
  background-color: ''' + colors.B50 + ''';
  color: ''' + colors.TextColor + ''';
}

QToolButton:pressed {
  background-color: ''' + colors.B60 + ''';
}

QToolButton:selected {
  background: ''' + colors.B60 + ''';
  color: ''' + colors.TextColor + ''';
}

QToolButton[popupMode="0"] {
  /* Only for DelayedPopup */
  padding-right: 2px;
}

QToolButton[popupMode="1"] {
  /* Only for MenuButtonPopup */
  padding-right: 20px;
}

QToolButton[popupMode="1"]::menu-button {
  border: none;
}

QToolButton[popupMode="1"]::menu-button:hover {
  border: none;
  border-left: 1px solid ''' + colors.Border + ''';
  border-radius: 0;
}

QToolButton[popupMode="2"] {
  /* Only for InstantPopup */
  padding-right: 2px;
}

QToolButton::menu-button {
  padding: 2px;
  border-radius: 4px;
  width: 12px;
  border: none;
  outline: none;
}

QToolButton::menu-button:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QToolButton::menu-button:checked:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QToolButton::menu-indicator {
  image: url(":/qss_icons/dark/rc/arrow_down.png");
  height: 8px;
  width: 8px;
  top: 0;
  /* Exclude a shift for better image */
  left: -2px;
  /* Shift it a bit */
}

QToolButton::menu-arrow {
  image: url(":/qss_icons/dark/rc/arrow_down.png");
  height: 8px;
  width: 8px;
}

QToolButton::menu-arrow:hover {
  image: url(":/qss_icons/dark/rc/arrow_down_focus.png");
}

/* QCommandLinkButton -----------------------------------------------------

--------------------------------------------------------------------------- */
QCommandLinkButton {
  background-color: transparent;
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 4px;
  padding: 0px;
  margin: 0px;
}

QCommandLinkButton:disabled {
  background-color: transparent;
  color: ''' + colors.DeactivatedTextColor + ''';
}

/* ------------------------------------------------------------------------ */
/* INPUTS - NO FIELDS ----------------------------------------------------- */
/* ------------------------------------------------------------------------ */
/* QComboBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qcombobox

--------------------------------------------------------------------------- */
QComboBox {
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
  padding-left: 4px;
  padding-right: 4px;
  /* padding-right = 36; 4 + 16*2 See scrollbar size */
  /* changed to 4px to fix #239 */
  /* Fixes #103, #111 */
  min-height: 1.5em;
  /* padding-top: 2px;     removed to fix #132 */
  /* padding-bottom: 2px;  removed to fix #132 */
  /* min-width: 75px;      removed to fix #109 */
  /* Needed to remove indicator - fix #132 */
}

QComboBox QAbstractItemView {
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 0;
  background-color: ''' + colors.Background + ''';
  selection-background-color: ''' + colors.Hover_Combo + ''';
}

QComboBox QAbstractItemView:hover {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.TextColor + ''';
}

QComboBox QAbstractItemView:selected {
  background: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

QComboBox QAbstractItemView:alternate {
  background: ''' + colors.Background + ''';
}

QComboBox:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

QComboBox:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QComboBox:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QComboBox:on {
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QComboBox::indicator {
  border: none;
  border-radius: 0;
  background-color: transparent;
  selection-background-color: transparent;
  color: transparent;
  selection-color: transparent;
  /* Needed to remove indicator - fix #132 */
}

QComboBox::indicator:alternate {
  background: ''' + colors.Background + ''';
}

QComboBox::item:alternate {
  background: ''' + colors.Background + ''';
}

QComboBox::item:checked {
  font-weight: bold;
}

QComboBox::item:selected {
  border: 0px solid transparent;
}

QComboBox::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 12px;
  border-left: 1px solid ''' + colors.Border + ''';
}

QComboBox::down-arrow {
  image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QComboBox::down-arrow:on, QComboBox::down-arrow:hover, QComboBox::down-arrow:focus {
  image: url(":/qss_icons/dark/rc/arrow_down.png");
}

/* QSlider ----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qslider

--------------------------------------------------------------------------- */
QSlider:disabled {
  background: ''' + colors.Background + ''';
}

QSlider:focus {
  border: none;
}

QSlider::groove:horizontal {
  background: ''' + colors.Border + ''';
  border: 1px solid ''' + colors.Border + ''';
  height: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::groove:vertical {
  background: ''' + colors.Border + ''';
  border: 1px solid ''' + colors.Border + ''';
  width: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::add-page:vertical {
  background: ''' + colors.Hover_and_SelectTable + ''';
  border: 1px solid ''' + colors.Border + ''';
  width: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::add-page:vertical :disabled {
  background: ''' + colors.C20 + ''';
}

QSlider::sub-page:horizontal {
  background: ''' + colors.Hover_and_SelectTable + ''';
  border: 1px solid ''' + colors.Border + ''';
  height: 4px;
  margin: 0px;
  border-radius: 4px;
}

QSlider::sub-page:horizontal:disabled {
  background: ''' + colors.C20 + ''';
}

QSlider::handle:horizontal {
  background: ''' + colors.DeactivatedTextColor + ''';
  border: 1px solid ''' + colors.Border + ''';
  width: 8px;
  height: 8px;
  margin: -8px 0px;
  border-radius: 4px;
}

QSlider::handle:horizontal:hover {
  background: ''' + colors.Hover_and_SelectTable + ''';
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QSlider::handle:horizontal:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QSlider::handle:vertical {
  background: ''' + colors.DeactivatedTextColor + ''';
  border: 1px solid ''' + colors.Border + ''';
  width: 8px;
  height: 8px;
  margin: 0 -8px;
  border-radius: 4px;
}

QSlider::handle:vertical:hover {
  background: ''' + colors.Hover_and_SelectTable + ''';
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QSlider::handle:vertical:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

/* QLineEdit --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qlineedit

--------------------------------------------------------------------------- */
QLineEdit {
  background-color: ''' + colors.Background + ''';
  padding-top: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-bottom: 2px;
  /* This QLineEdit fix  103, 111 */
  padding-left: 4px;
  padding-right: 4px;
  border-style: solid;
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  color: ''' + colors.TextColor + ''';
}

QLineEdit:disabled {
  background-color: ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
}

QLineEdit:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.TextColor + ''';
}

QLineEdit:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QLineEdit:selected {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

/* QTabWiget --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtabwidget-and-qtabbar

--------------------------------------------------------------------------- */
QTabWidget {
  padding: 2px;
  selection-background-color: ''' + colors.Border + ''';
}

QTabWidget QWidget {
  /* Fixes #189 */
  border-radius: 4px;
}

QTabWidget::pane {
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  margin: 0px;
  /* Fixes double border inside pane with pyqt5 */
  padding: 0px;
}

QTabWidget::pane:selected {
  background-color: ''' + colors.Border + ''';
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

/* QTabBar ----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtabwidget-and-qtabbar

--------------------------------------------------------------------------- */
QTabBar, QDockWidget QTabBar {
  qproperty-drawBase: 0;
  border-radius: 4px;
  margin: 0px;
  padding: 2px;
  border: 0;
  /* left: 5px; move to the right by 5px - removed for fix */
}

QTabBar::close-button, QDockWidget QTabBar::close-button {
  border: 0;
  margin: 0;
  padding: 4px;
  image: url(":/qss_icons/dark/rc/window_close.png");
}

QTabBar::close-button:hover, QDockWidget QTabBar::close-button:hover {
  image: url(":/qss_icons/dark/rc/window_close_focus.png");
}

QTabBar::close-button:pressed, QDockWidget QTabBar::close-button:pressed {
  image: url(":/qss_icons/dark/rc/window_close_pressed.png");
}

QTabBar::tab, QDockWidget QTabBar::tab {
  /* !selected and disabled ----------------------------------------- */
  /* selected ------------------------------------------------------- */
}

QTabBar::tab:top:selected:disabled, QDockWidget QTabBar::tab:top:selected:disabled {
  border-bottom: 3px solid ''' + colors.C20 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Border + ''';
}

QTabBar::tab:bottom:selected:disabled, QDockWidget QTabBar::tab:bottom:selected:disabled {
  border-top: 3px solid ''' + colors.C20 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Border + ''';
}

QTabBar::tab:left:selected:disabled, QDockWidget QTabBar::tab:left:selected:disabled {
  border-right: 3px solid ''' + colors.C20 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Border + ''';
}

QTabBar::tab:right:selected:disabled, QDockWidget QTabBar::tab:right:selected:disabled {
  border-left: 3px solid ''' + colors.C20 + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Border + ''';
}

QTabBar::tab:top:!selected:disabled, QDockWidget QTabBar::tab:top:!selected:disabled {
  border-bottom: 3px solid ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Background + ''';
}

QTabBar::tab:bottom:!selected:disabled, QDockWidget QTabBar::tab:bottom:!selected:disabled {
  border-top: 3px solid ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Background + ''';
}

QTabBar::tab:left:!selected:disabled, QDockWidget QTabBar::tab:left:!selected:disabled {
  border-right: 3px solid ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Background + ''';
}

QTabBar::tab:right:!selected:disabled, QDockWidget QTabBar::tab:right:!selected:disabled {
  border-left: 3px solid ''' + colors.Background + ''';
  color: ''' + colors.DeactivatedTextColor + ''';
  background-color: ''' + colors.Background + ''';
}

QTabBar::tab:top:!selected, QDockWidget QTabBar::tab:top:!selected {
  border-bottom: 2px solid ''' + colors.Background + ''';
  margin-top: 2px;
}

QTabBar::tab:bottom:!selected, QDockWidget QTabBar::tab:bottom:!selected {
  border-top: 2px solid ''' + colors.Background + ''';
  margin-bottom: 2px;
}

QTabBar::tab:left:!selected, QDockWidget QTabBar::tab:left:!selected {
  border-left: 2px solid ''' + colors.Background + ''';
  margin-right: 2px;
}

QTabBar::tab:right:!selected, QDockWidget QTabBar::tab:right:!selected {
  border-right: 2px solid ''' + colors.Background + ''';
  margin-left: 2px;
}

QTabBar::tab:top, QDockWidget QTabBar::tab:top {
  background-color: ''' + colors.Border + ''';
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  min-width: 5px;
  border-bottom: 3px solid ''' + colors.Border + ''';
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

QTabBar::tab:top:selected, QDockWidget QTabBar::tab:top:selected {
  background-color: ''' + colors.B50 + ''';
  border-bottom: 3px solid ''' + colors.C70 + ''';
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

QTabBar::tab:top:!selected:hover, QDockWidget QTabBar::tab:top:!selected:hover {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
  border-bottom: 3px solid ''' + colors.Focus_and_HoverMenus + ''';
  /* Fixes spyder-ide/spyder#9766 and #243 */
  padding-left: 3px;
  padding-right: 3px;
}

QTabBar::tab:bottom, QDockWidget QTabBar::tab:bottom {
  border-top: 3px solid ''' + colors.Border + ''';
  background-color: ''' + colors.Border + ''';
  margin-left: 2px;
  padding-left: 4px;
  padding-right: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  min-width: 5px;
}

QTabBar::tab:bottom:selected, QDockWidget QTabBar::tab:bottom:selected {
  background-color: ''' + colors.B50 + ''';
  border-top: 3px solid ''' + colors.C70 + ''';
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}

QTabBar::tab:bottom:!selected:hover, QDockWidget QTabBar::tab:bottom:!selected:hover {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
  border-top: 3px solid ''' + colors.Focus_and_HoverMenus + ''';
  /* Fixes spyder-ide/spyder#9766 and #243 */
  padding-left: 3px;
  padding-right: 3px;
}

QTabBar::tab:left, QDockWidget QTabBar::tab:left {
  background-color: ''' + colors.Border + ''';
  margin-top: 2px;
  padding-left: 2px;
  padding-right: 2px;
  padding-top: 4px;
  padding-bottom: 4px;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
  min-height: 5px;
}

QTabBar::tab:left:selected, QDockWidget QTabBar::tab:left:selected {
  background-color: ''' + colors.B50 + ''';
  border-right: 3px solid ''' + colors.C70 + ''';
}

QTabBar::tab:left:!selected:hover, QDockWidget QTabBar::tab:left:!selected:hover {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
  border-right: 3px solid ''' + colors.Focus_and_HoverMenus + ''';
  /* Fixes different behavior #271 */
  margin-right: 0px;
  padding-right: -1px;
}

QTabBar::tab:right, QDockWidget QTabBar::tab:right {
  background-color: ''' + colors.Border + ''';
  margin-top: 2px;
  padding-left: 2px;
  padding-right: 2px;
  padding-top: 4px;
  padding-bottom: 4px;
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
  min-height: 5px;
}

QTabBar::tab:right:selected, QDockWidget QTabBar::tab:right:selected {
  background-color: ''' + colors.B50 + ''';
  border-left: 3px solid ''' + colors.C70 + ''';
}

QTabBar::tab:right:!selected:hover, QDockWidget QTabBar::tab:right:!selected:hover {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
  border-left: 3px solid ''' + colors.Focus_and_HoverMenus + ''';
  /* Fixes different behavior #271 */
  margin-left: 0px;
  padding-left: 0px;
}

QTabBar QToolButton, QDockWidget QTabBar QToolButton {
  /* Fixes #136 */
  background-color: ''' + colors.Border + ''';
  height: 12px;
  width: 12px;
}

QTabBar QToolButton:pressed, QDockWidget QTabBar QToolButton:pressed {
  background-color: ''' + colors.Border + ''';
}

QTabBar QToolButton:pressed:hover, QDockWidget QTabBar QToolButton:pressed:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
}

QTabBar QToolButton::left-arrow:enabled, QDockWidget QTabBar QToolButton::left-arrow:enabled {
  image: url(":/qss_icons/dark/rc/arrow_left.png");
}

QTabBar QToolButton::left-arrow:disabled, QDockWidget QTabBar QToolButton::left-arrow:disabled {
  image: url(":/qss_icons/dark/rc/arrow_left_disabled.png");
}

QTabBar QToolButton::right-arrow:enabled, QDockWidget QTabBar QToolButton::right-arrow:enabled {
  image: url(":/qss_icons/dark/rc/arrow_right.png");
}

QTabBar QToolButton::right-arrow:disabled, QDockWidget QTabBar QToolButton::right-arrow:disabled {
  image: url(":/qss_icons/dark/rc/arrow_right_disabled.png");
}

/* QDockWiget -------------------------------------------------------------

--------------------------------------------------------------------------- */
QDockWidget {
  outline: 1px solid ''' + colors.Border + ''';
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  titlebar-close-icon: url(":/qss_icons/dark/rc/transparent.png");
  titlebar-normal-icon: url(":/qss_icons/dark/rc/transparent.png");
}

QDockWidget::title {
  /* Better size for title bar */
  padding: 3px;
  spacing: 4px;
  border: none;
  background-color: ''' + colors.Border + ''';
}

QDockWidget::close-button {
  icon-size: 12px;
  border: none;
  background: transparent;
  background-image: transparent;
  border: 0;
  margin: 0;
  padding: 0;
  image: url(":/qss_icons/dark/rc/window_close.png");
}

QDockWidget::close-button:hover {
  image: url(":/qss_icons/dark/rc/window_close_focus.png");
}

QDockWidget::close-button:pressed {
  image: url(":/qss_icons/dark/rc/window_close_pressed.png");
}

QDockWidget::float-button {
  icon-size: 12px;
  border: none;
  background: transparent;
  background-image: transparent;
  border: 0;
  margin: 0;
  padding: 0;
  image: url(":/qss_icons/dark/rc/window_undock.png");
}

QDockWidget::float-button:hover {
  image: url(":/qss_icons/dark/rc/window_undock_focus.png");
}

QDockWidget::float-button:pressed {
  image: url(":/qss_icons/dark/rc/window_undock_pressed.png");
}

/* QTreeView QListView QTableView -----------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtreeview
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qlistview
https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtableview

--------------------------------------------------------------------------- */
QTreeView:branch:selected, QTreeView:branch:hover {
  background: url(":/qss_icons/dark/rc/transparent.png");
}

QTreeView:branch:has-siblings:!adjoins-item {
  border-image: url(":/qss_icons/dark/rc/branch_line.png") 0;
}

QTreeView:branch:has-siblings:adjoins-item {
  border-image: url(":/qss_icons/dark/rc/branch_more.png") 0;
}

QTreeView:branch:!has-children:!has-siblings:adjoins-item {
  border-image: url(":/qss_icons/dark/rc/branch_end.png") 0;
}

QTreeView:branch:has-children:!has-siblings:closed, QTreeView:branch:closed:has-children:has-siblings {
  border-image: none;
  image: url(":/qss_icons/dark/rc/branch_closed.png");
}

QTreeView:branch:open:has-children:!has-siblings, QTreeView:branch:open:has-children:has-siblings {
  border-image: none;
  image: url(":/qss_icons/dark/rc/branch_open.png");
}

QTreeView:branch:has-children:!has-siblings:closed:hover, QTreeView:branch:closed:has-children:has-siblings:hover {
  image: url(":/qss_icons/dark/rc/branch_closed_focus.png");
}

QTreeView:branch:open:has-children:!has-siblings:hover, QTreeView:branch:open:has-children:has-siblings:hover {
  image: url(":/qss_icons/dark/rc/branch_open_focus.png");
}

QTreeView::indicator:checked,
QListView::indicator:checked,
QTableView::indicator:checked,
QColumnView::indicator:checked {
  image: url(":/qss_icons/dark/rc/checkbox_checked.png");
}

QTreeView::indicator:checked:hover, QTreeView::indicator:checked:focus, QTreeView::indicator:checked:pressed,
QListView::indicator:checked:hover,
QListView::indicator:checked:focus,
QListView::indicator:checked:pressed,
QTableView::indicator:checked:hover,
QTableView::indicator:checked:focus,
QTableView::indicator:checked:pressed,
QColumnView::indicator:checked:hover,
QColumnView::indicator:checked:focus,
QColumnView::indicator:checked:pressed {
  image: url(":/qss_icons/dark/rc/checkbox_checked_focus.png");
}

QTreeView::indicator:unchecked,
QListView::indicator:unchecked,
QTableView::indicator:unchecked,
QColumnView::indicator:unchecked {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked.png");
}

QTreeView::indicator:unchecked:hover, QTreeView::indicator:unchecked:focus, QTreeView::indicator:unchecked:pressed,
QListView::indicator:unchecked:hover,
QListView::indicator:unchecked:focus,
QListView::indicator:unchecked:pressed,
QTableView::indicator:unchecked:hover,
QTableView::indicator:unchecked:focus,
QTableView::indicator:unchecked:pressed,
QColumnView::indicator:unchecked:hover,
QColumnView::indicator:unchecked:focus,
QColumnView::indicator:unchecked:pressed {
  image: url(":/qss_icons/dark/rc/checkbox_unchecked_focus.png");
}

QTreeView::indicator:indeterminate,
QListView::indicator:indeterminate,
QTableView::indicator:indeterminate,
QColumnView::indicator:indeterminate {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate.png");
}

QTreeView::indicator:indeterminate:hover, QTreeView::indicator:indeterminate:focus, QTreeView::indicator:indeterminate:pressed,
QListView::indicator:indeterminate:hover,
QListView::indicator:indeterminate:focus,
QListView::indicator:indeterminate:pressed,
QTableView::indicator:indeterminate:hover,
QTableView::indicator:indeterminate:focus,
QTableView::indicator:indeterminate:pressed,
QColumnView::indicator:indeterminate:hover,
QColumnView::indicator:indeterminate:focus,
QColumnView::indicator:indeterminate:pressed {
  image: url(":/qss_icons/dark/rc/checkbox_indeterminate_focus.png");
}

QTreeView,
QListView,
QTableView,
QColumnView {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  gridline-color: ''' + colors.Border + ''';
  border-radius: 4px;
}

QTreeView:disabled,
QListView:disabled,
QTableView:disabled,
QColumnView:disabled {
  background-color: ''' + colors.Background + ''';
}

QTreeView:selected,
QListView:selected,
QTableView:selected,
QColumnView:selected {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QTreeView:focus,
QListView:focus,
QTableView:focus,
QColumnView:focus {
  border: 1px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QTreeView::item:pressed,
QListView::item:pressed,
QTableView::item:pressed,
QColumnView::item:pressed {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QTreeView::item:selected:active,
QListView::item:selected:active,
QTableView::item:selected:active,
QColumnView::item:selected:active {
  background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QTreeView::item:selected:!active,
QListView::item:selected:!active,
QTableView::item:selected:!active,
QColumnView::item:selected:!active {
  background-color: ''' + colors.B30 + ''';
}

QTreeView::item:!selected:hover,
QListView::item:!selected:hover,
QTableView::item:!selected:hover,
QColumnView::item:!selected:hover {
  outline: 0;
  background-color: ''' + colors.B30 + ''';
}

QTableCornerButton::section {
  background-color: ''' + colors.Background + ''';
  border: 1px transparent ''' + colors.Border + ''';
  border-radius: 0px;
}

/* QHeaderView ------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qheaderview

--------------------------------------------------------------------------- */
QHeaderView {
  background-color: ''' + colors.Border + ''';
  border: 0px transparent ''' + colors.Border + ''';
  padding: 0;
  margin: 0;
  border-radius: 0;
}

QHeaderView:disabled {
  background-color: ''' + colors.Border + ''';
  border: 1px transparent ''' + colors.Border + ''';
}

QHeaderView::section {
  background-color: ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-radius: 0;
  text-align: left;
  font-size: 13px;
}

QHeaderView::section::horizontal {
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
  border-left: 1px solid ''' + colors.Background + ''';
}

QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one {
  border-left: 1px solid ''' + colors.Border + ''';
}

QHeaderView::section::horizontal:disabled {
  color: ''' + colors.DeactivatedTextColor + ''';
}

QHeaderView::section::vertical {
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
  border-top: 1px solid ''' + colors.Background + ''';
}

QHeaderView::section::vertical::first, QHeaderView::section::vertical::only-one {
  border-top: 1px solid ''' + colors.Border + ''';
}

QHeaderView::section::vertical:disabled {
  color: ''' + colors.DeactivatedTextColor + ''';
}

QHeaderView::down-arrow {
  /* Those settings (border/width/height/background-color) solve bug */
  /* transparent arrow background and size */
  background-color: ''' + colors.Border + ''';
  border: none;
  height: 12px;
  width: 12px;
  padding-left: 2px;
  padding-right: 2px;
  image: url(":/qss_icons/dark/rc/arrow_down.png");
}

QHeaderView::up-arrow {
  background-color: ''' + colors.Border + ''';
  border: none;
  height: 12px;
  width: 12px;
  padding-left: 2px;
  padding-right: 2px;
  image: url(":/qss_icons/dark/rc/arrow_up.png");
}

/* QToolBox --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtoolbox

--------------------------------------------------------------------------- */
QToolBox {
  padding: 0px;
  border: 0px;
  border: 1px solid ''' + colors.Border + ''';
}

QToolBox:selected {
  padding: 0px;
  border: 2px solid ''' + colors.Hover_and_SelectTable + ''';
}

QToolBox::tab {
  background-color: ''' + colors.Background + ''';
  border: 1px solid ''' + colors.Border + ''';
  color: ''' + colors.TextColor + ''';
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

QToolBox::tab:disabled {
  color: ''' + colors.DeactivatedTextColor + ''';
}

QToolBox::tab:selected {
  background-color: ''' + colors.B60 + ''';
  border-bottom: 2px solid ''' + colors.Hover_and_SelectTable + ''';
}

QToolBox::tab:selected:disabled {
  background-color: ''' + colors.Border + ''';
  border-bottom: 2px solid ''' + colors.C20 + ''';
}

QToolBox::tab:!selected {
  background-color: ''' + colors.Border + ''';
  border-bottom: 2px solid ''' + colors.Border + ''';
}

QToolBox::tab:!selected:disabled {
  background-color: ''' + colors.Background + ''';
}

QToolBox::tab:hover {
  border-color: ''' + colors.Focus_and_HoverMenus + ''';
  border-bottom: 2px solid ''' + colors.Focus_and_HoverMenus + ''';
}

QToolBox QScrollArea QWidget QWidget {
  padding: 0px;
  border: 0px;
  background-color: ''' + colors.Background + ''';
}

/* QFrame -----------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qframe
https://doc.qt.io/qt-5/qframe.html#-prop
https://doc.qt.io/qt-5/qframe.html#details
https://stackoverflow.com/questions/14581498/qt-stylesheet-for-hline-vline-color

--------------------------------------------------------------------------- */
/* (dot) .QFrame  fix #141, #126, #123 */
.QFrame {
  border-radius: 4px;
  border: 1px solid ''' + colors.Border + ''';
  /* No frame */
  /* HLine */
  /* HLine */
}

.QFrame[frameShape="0"] {
  border-radius: 4px;
  border: 1px transparent ''' + colors.Border + ''';
}

.QFrame[frameShape="4"] {
  max-height: 2px;
  border: none;
  background-color: ''' + colors.Border + ''';
}

.QFrame[frameShape="5"] {
  max-width: 2px;
  border: none;
  background-color: ''' + colors.Border + ''';
}

/* QSplitter --------------------------------------------------------------

https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qsplitter

--------------------------------------------------------------------------- */
QSplitter {
  background-color: ''' + colors.Border + ''';
  spacing: 0px;
  padding: 0px;
  margin: 0px;
}

QSplitter::handle {
  background-color: ''' + colors.Border + ''';
  border: 0px solid ''' + colors.Background + ''';
  spacing: 0px;
  padding: 1px;
  margin: 0px;
}

QSplitter::handle:hover {
  background-color: ''' + colors.DeactivatedTextColor + ''';
}

QSplitter::handle:horizontal {
  width: 5px;
  image: url(":/qss_icons/dark/rc/line_vertical.png");
}

QSplitter::handle:vertical {
  height: 5px;
  image: url(":/qss_icons/dark/rc/line_horizontal.png");
}

/* QDateEdit, QDateTimeEdit -----------------------------------------------

--------------------------------------------------------------------------- */
QDateEdit, QDateTimeEdit {
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
  border-style: solid;
  border: 1px solid ''' + colors.Border + ''';
  border-radius: 4px;
  /* This fixes 103, 111 */
  padding-top: 2px;
  /* This fixes 103, 111 */
  padding-bottom: 2px;
  padding-left: 4px;
  padding-right: 4px;
  min-width: 10px;
}

QDateEdit:on, QDateTimeEdit:on {
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
}

QDateEdit::drop-down, QDateTimeEdit::drop-down {
  subcontrol-origin: padding;
  subcontrol-position: top right;
  width: 12px;
  border-left: 1px solid ''' + colors.Border + ''';
}

QDateEdit::down-arrow, QDateTimeEdit::down-arrow {
  image: url(":/qss_icons/dark/rc/arrow_down_disabled.png");
  height: 8px;
  width: 8px;
}

QDateEdit::down-arrow:on, QDateEdit::down-arrow:hover, QDateEdit::down-arrow:focus, QDateTimeEdit::down-arrow:on, QDateTimeEdit::down-arrow:hover, QDateTimeEdit::down-arrow:focus {
  image: url(":/qss_icons/dark/rc/arrow_down.png");
}

QDateEdit QAbstractItemView, QDateTimeEdit QAbstractItemView {
  background-color: ''' + colors.Background + ''';
  border-radius: 4px;
  border: 1px solid ''' + colors.Border + ''';
  selection-background-color: ''' + colors.Hover_and_SelectTable + ''';
}

/* QAbstractView ----------------------------------------------------------

--------------------------------------------------------------------------- */
QAbstractView:hover {
  border: 1px solid ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.TextColor + ''';
}

QAbstractView:selected {
  background: ''' + colors.Hover_and_SelectTable + ''';
  color: ''' + colors.Border + ''';
}

/* PlotWidget -------------------------------------------------------------

--------------------------------------------------------------------------- */
PlotWidget {
  /* Fix cut labels in plots #134 */
  padding: 0px;
}

QMenu::item {
    padding: 4px 24px 4px 6px;
}
''' + colors.custom_css

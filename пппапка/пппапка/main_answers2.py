import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, # Діалог відкриття файлів (і папок)
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
 
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap # оптимізована для показу на екрані картинка
 
from PIL import Image
from PIL import ImageFilter  # Імпортуємо модуль ImageFilter для застосування фільтрів до зображень
from PIL.ImageQt import Image  # Імпортуємо Image для конвертації зображень Pillow в формат, сумісний з Qt
from PIL.ImageFilter import (
    # BLUR - Розмиває зображення, зменшуючи деталі та створюючи ефект м'якості.
    BLUR,
    # CONTOUR - Підкреслює контури об'єктів на зображенні, створюючи ефект малюнка.
    CONTOUR,
    # DETAIL - Підвищує деталі зображення, роблячи його більш чітким і виразним.
    DETAIL,
    # EDGE_ENHANCE - Підсилює краї об'єктів на зображенні, роблячи їх більш виразними.
    EDGE_ENHANCE,
    # EDGE_ENHANCE_MORE - Ще більше підсилює краї, ніж EDGE_ENHANCE, створюючи більш різкий ефект.
    EDGE_ENHANCE_MORE,
    # EMBOSS - Створює ефект рельєфу, надаючи зображенню тривимірний вигляд.
    EMBOSS,
    # FIND_EDGES - Виявляє краї на зображенні, підкреслюючи контури об'єктів.
    FIND_EDGES,
    # SMOOTH - Зменшує шум і деталі, роблячи зображення більш гладким.
    SMOOTH,
    # SMOOTH_MORE - Ще більше згладжує зображення, ніж SMOOTH, зменшуючи деталі.
    SMOOTH_MORE,
    # SHARPEN - Підвищує різкість зображення, роблячи його більш чітким.
    SHARPEN,
    # GaussianBlur - Застосовує гаусівське розмивання, яке м'яко розмиває зображення, зберігаючи при цьому його структуру.
    GaussianBlur,
    # UnsharpMask - Застосовує техніку "недострого маскування" для підвищення різкості зображення, підкреслюючи деталі.
    UnsharpMask
) 
app = QApplication([])
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()
 
btn_rotate = QPushButton("Поворот")
btn_blur = QPushButton("Розмити")
btn_flip = QPushButton("Відзеркалити")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")
 
row = QHBoxLayout()          # Головна лінія
col1 = QVBoxLayout()         # ділиться на два стовпці
col2 = QVBoxLayout()
col1.addWidget(btn_dir)      # в першому - кнопка вибору каталогу
col1.addWidget(lw_files)     # і список файлов
col2.addWidget(lb_image, 95) # в другому - картинка
row_tools = QHBoxLayout()    # і ряд кнопок
row_tools.addWidget(btn_rotate)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)
 
row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)
 
win.show()
 
workdir = ''
 
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()
 
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
 
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
 
btn_dir.clicked.connect(showFilenamesList)
 
class ImageProcessor():
   def __init__(self):
       self.image = None
       self.dir = None
       self.filename = None
       self.save_dir = "Modified/"
 
   def loadImage(self, dir, filename):
       ''' під час завантаження запам'ятовуємо шлях та ім'я файлу '''
       self.dir = dir
       self.filename = filename
       image_path = os.path.join(dir, filename)
       self.image = Image.open(image_path)
 
   def do_bw(self):
       self.image = self.image.convert("L")
       self.saveImage()
       image_path = os.path.join(self.dir, self.save_dir, self.filename)
       self.showImage(image_path)

   def do_smooth(self):
       self.image = self.image.filter(SMOOTH_MORE)
       self.saveImage()
       image_path = os.path.join(self.dir, self.save_dir, self.filename)
       self.showImage(image_path)
 
   def saveImage(self):
       ''' зберігає копію файлу у підпапці '''
       path = os.path.join(self.dir, self.save_dir)
       if not(os.path.exists(path) or os.path.isdir(path)):
           os.mkdir(path)
       image_path = os.path.join(path, self.filename)
       self.image.save(image_path)
 
   def showImage(self, path):
       lb_image.hide()
       pixmapimage = QPixmap(path)
       w, h = lb_image.width(), lb_image.height()
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       lb_image.show()
 
def showChosenImage():
    if lw_files.currentRow()>= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()  
lw_files.currentRowChanged.connect(showChosenImage)  


btn_bw.clicked.connect(workimage.do_bw)
btn_blur.clicked.connect(workimage.do_smooth)








 
app.exec()



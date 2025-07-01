import sys
import time
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton, QTabWidget, 
                             QGroupBox, QMessageBox, QCheckBox)
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class Worker(QThread):
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(str)
    
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    #остальной код доступен после покупки: tg: https://t.me/xnxdesignclub  | kwork: https://kwork.ru/user/dmitriynehaev
    
    def login_to_wildberries(self, driver):
        try:
            self.progress.emit("Открытие страницы входа...")
            driver.get("https://seller.wildberries.ru/")
            
            # Переход к форме входа
            self.progress.emit("Переход к форме входа...")
            login_btn = WebDriverWait(driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'login-button')]")))
            login_btn.click()
            
            # Ввод телефона
            self.progress.emit("Ввод телефона...")
            phone_field = WebDriverWait(driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='phone']")))
            phone_field.send_keys(self.login)
            
            # Нажатие кнопки "Получить код"
            get_code_btn = WebDriverWait(driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Получить код')]")))
            get_code_btn.click()
            
            # Ожидание ввода кода вручную
            self.progress.emit("Ожидание ввода кода подтверждения...")
            WebDriverWait(driver, 300).until(  # 5 минут на ввод кода
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'seller-home')]")))
            
            self.progress.emit("Авторизация успешна!")
            return True
            
        except Exception as e:
            self.progress.emit(f"Ошибка авторизации: {str(e)}")
            return False
    
    def process_reviews(self, driver):
        try:
            self.progress.emit("Переход в раздел отзывов...")
            driver.get("https://seller.wildberries.ru/feedback-question/feedbacks")
            
            # Ожидание загрузки отзывов
            WebDriverWait(driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'feedback__list')]")))
            
            # Получение непрочитанных отзывов
            unreplied_reviews = driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'feedback__item') and not(.//div[contains(@class, 'seller-answer')])]")
            
            if not unreplied_reviews:
                self.progress.emit("Нет новых отзывов для ответа")
                return True
            
            self.progress.emit(f"Найдено {len(unreplied_reviews)} отзывов без ответа")
            
            for i, review in enumerate(unreplied_reviews, 1):
                if not self._is_running:
                    self.progress.emit("Процесс остановлен пользователем")
                    return False
                
                try:
                    self.progress.emit(f"Обработка отзыва {i}/{len(unreplied_reviews)}...")
                    
                    # Получение рейтинга
                    rating_element = review.find_element(By.XPATH, ".//div[contains(@class, 'feedback__rating')]")
                    rating = int(rating_element.get_attribute("data-rate"))
                    
                    if rating >= 4:
                        response_text = self.positive
                    elif rating == 3:
                        response_text = self.neutral
                    else:
                        response_text = self.negative
                    
                    # Открытие формы ответа
                    reply_btn = review.find_element(By.XPATH, ".//button[contains(text(), 'Ответить')]")
                    driver.execute_script("arguments[0].click();", reply_btn)
                    
                    # Ввод ответа
                    response_field = WebDriverWait(driver, self.delay).until(
                        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@class, 'reply-textarea')]")))
                    response_field.send_keys(response_text)
                    
                    # Отправка ответа
                    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Отправить')]")
                    submit_btn.click()
                    
                    time.sleep(2)
                    
                except Exception as e:
                    self.progress.emit(f"Ошибка при обработке отзыва: {str(e)}")
                    continue
                    
            return True
            
        except Exception as e:
            self.progress.emit(f"Ошибка при обработке отзывов: {str(e)}")
            return False
    
    def stop(self):
        self._is_running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wildberries Autoresponder")
        self.setGeometry(100, 100, 600, 500)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.create_ui()
        self.worker = None
    
    def create_ui(self):
        # Вкладки
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Вкладка настроек
        self.settings_tab = QWidget()
        self.tabs.addTab(self.settings_tab, "Настройки")
        self.create_settings_tab()
        
        # Вкладка шаблонов
        self.templates_tab = QWidget()
        self.tabs.addTab(self.templates_tab, "Шаблоны ответов")
        self.create_templates_tab()
        
        # Вкладка логов
        self.logs_tab = QWidget()
        self.tabs.addTab(self.logs_tab, "Логи")
        self.create_logs_tab()
        
        # Кнопки управления
        self.control_layout = QHBoxLayout()
        self.start_btn = QPushButton("Старт")
        self.start_btn.clicked.connect(self.start_processing)
        self.control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Стоп")
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        self.control_layout.addWidget(self.stop_btn)
        
        self.layout.addLayout(self.control_layout)
    
    def create_settings_tab(self):
        layout = QVBoxLayout()
        self.settings_tab.setLayout(layout)
        
        # Группа учетных данных
        creds_group = QGroupBox("Учетные данные Wildberries")
        creds_layout = QVBoxLayout()
        
        self.login_label = QLabel("Телефон (логин):")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("+7XXXXXXXXXX")
        creds_layout.addWidget(self.login_label)
        creds_layout.addWidget(self.login_input)
        
        self.password_label = QLabel("Пароль (не требуется, код придёт по SMS):")
        self.password_input = QLineEdit()
        self.password_input.setEnabled(False)
        creds_layout.addWidget(self.password_label)
        creds_layout.addWidget(self.password_input)
        
        creds_group.setLayout(creds_layout)
        layout.addWidget(creds_group)
        
        # Группа настроек
        settings_group = QGroupBox("Настройки")
        settings_layout = QVBoxLayout()
        
        self.delay_label = QLabel("Задержка между действиями (сек):")
        self.delay_input = QLineEdit("5")
        self.delay_input.setValidator(QtGui.QIntValidator(1, 60))
        settings_layout.addWidget(self.delay_label)
        settings_layout.addWidget(self.delay_input)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        layout.addStretch()
    
    def create_templates_tab(self):
        layout = QVBoxLayout()
        self.templates_tab.setLayout(layout)
        
        # Положительный отзыв
        self.positive_label = QLabel("Шаблон для положительных отзывов (4-5 звезд):")
        self.positive_edit = QTextEdit()
        self.positive_edit.setPlainText("Благодарим вас за отзыв и высокую оценку! "
                                      "Мы рады, что вам понравился наш товар. Будем ждать ваших новых заказов!")
        layout.addWidget(self.positive_label)
        layout.addWidget(self.positive_edit)
        
        # Нейтральный отзыв
        self.neutral_label = QLabel("Шаблон для нейтральных отзывов (3 звезды):")
        self.neutral_edit = QTextEdit()
        self.neutral_edit.setPlainText("Спасибо за ваш отзыв. Мы ценим ваше мнение и "
                                     "постараемся стать лучше для вас!")
        layout.addWidget(self.neutral_label)
        layout.addWidget(self.neutral_edit)
        
        # Отрицательный отзыв
        self.negative_label = QLabel("Шаблон для отрицательных отзывов (1-2 звезды):")
        self.negative_edit = QTextEdit()
        self.negative_edit.setPlainText("Приносим извинения за доставленные неудобства. "
                                      "Наша служба заботы о клиентах уже занимается вашим вопросом. "
                                      "Пожалуйста, напишите нам в личные сообщения для решения проблемы.")
        layout.addWidget(self.negative_label)
        layout.addWidget(self.negative_edit)
        
        layout.addStretch()
    
    def create_logs_tab(self):
        layout = QVBoxLayout()
        self.logs_tab.setLayout(layout)
        
        self.logs_edit = QTextEdit()
        self.logs_edit.setReadOnly(True)
        layout.addWidget(self.logs_edit)
    
    def start_processing(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Внимание", "Процесс уже запущен!")
            return
        
        # Проверка заполнения полей
        if not self.login_input.text():
            QMessageBox.critical(self, "Ошибка", "Введите номер телефона!")
            return
        
        if not self.positive_edit.toPlainText() or not self.neutral_edit.toPlainText() or not self.negative_edit.toPlainText():
            QMessageBox.critical(self, "Ошибка", "Заполните все шаблоны ответов!")
            return
        
        try:
            delay = int(self.delay_input.text())
        except ValueError:
            delay = 5
        
        # Запуск потока обработки
        self.worker = Worker(
            self.login_input.text(),
            "",  # Пароль не используется для Wildberries
            self.positive_edit.toPlainText(),
            self.neutral_edit.toPlainText(),
            self.negative_edit.toPlainText(),
            delay
        )
        
        self.worker.finished.connect(self.on_finished)
        self.worker.progress.connect(self.update_logs)
        self.worker.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.logs_edit.clear()
        self.logs_edit.append("Запуск обработки отзывов...")
        self.logs_edit.append("После нажатия кнопки 'Получить код' у вас будет 5 минут для ввода кода из SMS")
    
    def stop_processing(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.logs_edit.append("Завершение процесса...")
            self.stop_btn.setEnabled(False)
    
    def on_finished(self, success, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if success:
            self.logs_edit.append(message)
            QMessageBox.information(self, "Успех", message)
        else:
            self.logs_edit.append(f"Ошибка: {message}")
            QMessageBox.critical(self, "Ошибка", message)
    
    def update_logs(self, message):
        self.logs_edit.append(message)
    
    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, 'Подтверждение',
                'Процесс еще выполняется. Вы уверены, что хотите закрыть приложение?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.worker.stop()
                self.worker.wait(2000)  # Даем 2 секунды на завершение
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
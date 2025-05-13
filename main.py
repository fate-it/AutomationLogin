import time
import random
from playwright.sync_api import sync_playwright, Playwright # підключаемо синхронну версію плейрайта та клас для зручної типізації

username = input("Please input username: ") #standard_user, locked_out_user, problem_user, performance_glitch_user, error_user, visual_user
password = input("Please input password: ") #secret_sauce


def run(playwright: Playwright, username: str, password: str) -> None:
    """
    Функція для логіну користувача на сайті

    :param playwright: основний класс бібліотеки Playwright
    :param username: Ім'я користувача
    :param password: Пароль користувача
    :return: None
    """
    browser = playwright.chromium.launch(headless=True) #створюємо браузер
    page = browser.new_page() #відкриваємо нову сторінку
    page.goto("https://www.saucedemo.com/") #переходимо на сайт тестування

    time.sleep(1.5)
    username_input = page.locator("input#user-name") #Знаходимо поле для вводу логіна
    password_input = page.locator("input#password") #Знаходимо поле для вводу пароля
    login_btn_input = page.locator("input#login-button") #знаходимо кнопку логіна

    username_location = username_input.bounding_box()
    password_location = password_input.bounding_box()
    login_btn_location = login_btn_input.bounding_box()
    #Знаходипо також координати цих полей

    page_size = page.viewport_size
    max_x, max_y = page_size["width"], page_size["height"]
    #розмір відкритого браузера

    time.sleep(0.1)
    page.mouse.move(random.randint(0, max_x-1), random.randint(0, max_y-1)) #початкова позиція миші

    print("Вводимо логін користувача")
    time.sleep(0.2)
    page.mouse.move(username_location['x'], username_location['y'], steps=10+random.randint(1, 5)) #переміщаемо мишу до поля вводу
    page.mouse.click(username_location['x']+1, username_location['y']+1) #натискаємо
    page.keyboard.type(username, delay=100+random.randint(1, 15)) #вводимо логін

    print("Вводимо пароль користувача")
    time.sleep(0.2)
    page.mouse.move(password_location['x'], password_location['y'], steps=10+random.randint(1, 5)) #переміщаемо мишу до поля вводу
    page.mouse.click(password_location['x']+1, password_location['y']+1) #натискаємо
    page.keyboard.type(password, delay=100+random.randint(1, 15)) #вводимо пароль

    page.mouse.move(login_btn_location['x'], login_btn_location['y'], steps=10 + random.randint(1, 5)) # переміщаемо мишу на кнопку логіна
    try:
        with page.expect_navigation(wait_until="load"): # і через контекстний менеджер очикуємо завантаження нової сторінки
            page.mouse.click(login_btn_location['x'] + 1, login_btn_location['y'] + 1) #натискаємо кнопку
            error_message = page.locator(".error-message-container.error") #якщо з'явиться помилка
            if error_message.is_visible():
                print(f"Користувач {username} заблокований або не вірні дані") #значить юзер заблокований або не вірні дані
                browser.close() # закриття браузеру
    except Exception:
        return

    print(f"Вхід користувача {username} пройшов успішно")

    # time.sleep(200)
    print("Завантаження динамічних товарів")
    page.evaluate("""
        window.scrollTo({ top: document.body.scrollHeight, left: 0, behavior: 'smooth' });
    """) # на сайтах де динапічно підвантажуються дані через ajax наприклад потрібно проскролювати до низу

    elements = page.locator(".btn_inventory").all() # знаходимо елементи/товари

    print(elements)
    flag = 1
    for el in elements:
        #Цей цикл показово додає товари у кошик якщо функція додавання працює
        time.sleep(1)
        print(f"Скролимо до товару №{flag}")
        el.scroll_into_view_if_needed()
        el_coord = el.bounding_box()
        x, y = el_coord['x'], el_coord['y']
        page.mouse.move(x, y, steps=15 + random.randint(5, 20))
        if el.text_content() == "Add to cart":
            page.mouse.click(x + 1, y + 1)

        if el.text_content() == "Remove":
            print(f"Товар №{flag} додано")
        else:
            print(f"Помилка! Товар №{flag} не додано, кнопка не працює!")
        flag += 1

    page.screenshot(path="screenshot.png", full_page=True) #робить знімок екрану
    print("Зроблено фінальний знімок")
    browser.close()


with sync_playwright() as p: #запуск з контекстного менеджеру Playwright
    run(p, username, password)

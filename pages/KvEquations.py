import streamlit as st
import random
import math

st.set_page_config(page_title="Генератор квадратных уравнений", page_icon="📐")

# --- 1. ЛОГИКА И ФУНКЦИИ ---

# Функция генерации уравнения (ваша логика, без изменений)
def generate_equation_data(diff):
    while True:
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        if x1 == x2: continue
        
        if diff == "Легко":
            a = 1
        else:
            choices = [x for x in range(-10, 11) if x not in [0, 1, -1]]
            a = random.choice(choices)
            
        b = -a * (x1 + x2)
        c = a * x1 * x2
        D = b ** 2 - 4 * a * c
        
        # Проверка на полный квадрат
        sqrt_D = int(math.isqrt(abs(D)))
        if D > 0 and sqrt_D * sqrt_D == D:
            return {'a': a, 'b': b, 'c': c, 'x1': x1, 'x2': x2}

# --- 2. CALLBACKS (Обработчики событий) ---

def start_new_game():
    """Сбрасывает поля ввода и генерирует новое уравнение"""
    st.session_state.equation = generate_equation_data(st.session_state.difficulty_level)
    # Очищаем поля ввода (через привязку к ключам виджетов)
    st.session_state.input_x1 = ""
    st.session_state.input_x2 = ""
    st.session_state.checked = False
    st.session_state.result_msg = ""

def check_answer():
    """Проверяет ответ при нажатии Enter или кнопки"""
    # Если уравнения нет, ничего не делаем
    if 'equation' not in st.session_state:
        return

    # Получаем значения из session_state (куда их кладет input автоматически)
    val_x1 = st.session_state.input_x1
    val_x2 = st.session_state.input_x2
    
    # Если поля пустые — не проверяем (чтобы не ругаться раньше времени)
    if val_x1 == "" or val_x2 == "":
        st.session_state.result_msg = "empty"
        st.session_state.checked = True
        return

    try:
        u1 = int(val_x1)
        u2 = int(val_x2)
        
        real_roots = {st.session_state.equation['x1'], st.session_state.equation['x2']}
        user_roots = {u1, u2}
        
        if user_roots == real_roots:
            st.session_state.result_msg = "success"
        else:
            st.session_state.result_msg = "fail"
            
    except ValueError:
        st.session_state.result_msg = "error"
    
    st.session_state.checked = True

# --- 3. ИНИЦИАЛИЗАЦИЯ (Первый запуск) ---
if 'equation' not in st.session_state:
    # Задаем дефолтную сложность, если ее еще нет
    if 'difficulty_level' not in st.session_state:
        st.session_state.difficulty_level = "Легко"
    start_new_game()

# --- 4. ИНТЕРФЕЙС (UI) ---

st.title("📐 Генератор уравнений")
st.markdown("Генерация квадратных уравнений вида $ax^2 + bx + c = 0$")

# Радио-кнопка с ключом (автоматически пишет в session_state)
st.radio(
    "Выберите сложность:",
    ["Легко", "Сложно"],
    horizontal=True,
    key="difficulty_level",
    on_change=start_new_game # При смене сложности сразу генерируем новое
)

# Отображение уравнения
eq = st.session_state.equation
a, b, c = eq['a'], eq['b'], eq['c']

# Форматирование (ваша функция, немного сжатая для компактности)
def fmt(n, is_first=False):
    if n == 0: return ""
    if is_first:
        if n == 1: return ""
        if n == -1: return "-"
        return str(n)
    if n > 0: return f"+ {n}" if n != 1 else "+ "
    return f"- {abs(n)}" if n != -1 else "- "

eq_str = f"{fmt(a, True)}x^2 {fmt(b)}x {fmt(c)} = 0".replace("  ", " ") # Убираем двойные пробелы
st.markdown(f"## ${eq_str}$")

# Поля ввода
col_in1, col_in2 = st.columns(2)
with col_in1:
    # ВАЖНО: on_change=check_answer делает магию с Enter
    st.text_input("Первый корень $x_1$", key="input_x1", on_change=check_answer)
with col_in2:
    st.text_input("Второй корень $x_2$", key="input_x2", on_change=check_answer)

# Кнопки управления (РЯДОМ)
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    # Кнопка Проверить (также вызывает функцию проверки)
    st.button("Проверить ответ", on_click=check_answer, use_container_width=True)

with col_btn2:
    # Кнопка Новое (Зеленая, вызывает функцию сброса)
    st.button("🎲 Новое уравнение", type="primary", on_click=start_new_game, use_container_width=True)

# --- 5. ВЫВОД РЕЗУЛЬТАТА ---
if st.session_state.checked:
    res = st.session_state.result_msg
    true_x1, true_x2 = eq['x1'], eq['x2']
    
    if res == "success":
        st.success("🎉 Абсолютно верно! Молодец!")
        st.balloons()
        
    elif res == "fail":
        st.error("Неверно. Попробуй еще раз или разбери решение.")
        st.warning(f"Правильный ответ: $x_1 = {true_x1}$, $x_2 = {true_x2}$")
        
        # Разбор (Expander делает интерфейс чище, открывается по клику)
        with st.expander("🔍 Показать подробное решение"):
            D = b**2 - 4*a*c
            sqrt_D = int(math.isqrt(D))
            st.latex(rf"D = {b}^2 - 4 \cdot {a} \cdot {c} = {D}")
            st.latex(rf"\sqrt{{D}} = {sqrt_D}")
            st.latex(rf"x_{{1,2}} = \frac{{-{b} \pm {sqrt_D}}}{{2 \cdot {a}}}")
            
    elif res == "error":
        st.warning("Пожалуйста, вводите только целые числа.")
    elif res == "empty":
        st.info("Введите оба корня и нажмите Enter.")
    # -- Сайдбар с информацией --
with st.sidebar:
    st.header("ℹ️ Информация")
    st.markdown("""
    **Как это работает:**
    
    1. Выберите уровень сложности
    2. Нажмите "Новое уравнение"
    3. Решите уравнение и введите свои ответы
    4. Нажмите "Enter или Проверить ответ"
    """)
    
    st.markdown("---")
    
        
    st.markdown("**Теорема Виета:**")
    st.caption("Сумма и произведение корней:")
    # Используем окружение cases для красивой системы
    st.latex(r"\begin{cases} x_1 + x_2 = -\frac{b}{a} \\ x_1 \cdot x_2 = \frac{c}{a} \end{cases}")

    st.markdown("---")
    
    st.markdown("**Формула дискриминанта (но лучше по т. Виета😉):**")
    st.latex(r"D = b^2 - 4ac")
    
    st.markdown("**Формула корней:**")
    st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{D}}{2a}")
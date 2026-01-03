import streamlit as st
import random
import math

st.set_page_config(page_title="Генератор квадратных уравнений", page_icon="📐")

st.title("📐 Генератор квадратных уравнений")
st.markdown("Генерация квадратных уравнений вида $ax^2 + bx + c = 0$ с целыми корнями")

# -- Настройка сложности --
difficulty = st.radio(
    "Выберите сложность:",
    ["Легко", "Сложно"],
    horizontal=True,
    help="Легко: a=1, Сложно: a≠1"
)

def generate_equation(diff):
    while True:
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        if x1 == x2:
            continue  # Для разнообразия избегаем равных корней
        if diff == "Легко":
            a = 1
        else:
            a = random.choice([x for x in range(-10, 11) if x not in [0, 1, -1]])
        b = -a * (x1 + x2)
        c = a * x1 * x2
        D = b ** 2 - 4 * a * c
        # Дискриминант должен быть полным квадратом, иначе бывают проблемы со случайным выбором
        sqrt_D = int(math.isqrt(abs(D)))
        if D > 0 and sqrt_D * sqrt_D == D:
            return {'a': a, 'b': b, 'c': c, 'x1': x1, 'x2': x2}
    # Если все плохо, никогда сюда не придём, цикл уйдёт только при успехе

# -- Кнопка генерации нового примера --
if st.button("🎲 Новое уравнение", type="primary"):
    st.session_state['equation'] = generate_equation(difficulty)
    st.session_state['user_x1'] = ""
    st.session_state['user_x2'] = ""
    st.session_state['last_result'] = None
    st.session_state['show_answer'] = False

# Если уравнения еще нет, генерируем при первом запуске
if 'equation' not in st.session_state:
    st.session_state['equation'] = generate_equation(difficulty)
    st.session_state['user_x1'] = ""
    st.session_state['user_x2'] = ""
    st.session_state['last_result'] = None
    st.session_state['show_answer'] = False

eq = st.session_state['equation']
a, b, c = eq['a'], eq['b'], eq['c']
true_x1, true_x2 = eq['x1'], eq['x2']

# -- Форматирование вывода уравнения --
def format_coefficient(coef, is_first=False):
    if coef == 0:
        return ""
    if is_first:
        if coef == 1:
            return ""
        elif coef == -1:
            return "-"
        else:
            return str(coef)
    else:
        if coef > 0:
            return f" + {coef}" if coef != 1 else " + "
        elif coef < 0:
            return f" - {abs(coef)}" if coef != -1 else " - "
        else:
            return ""

eq_str = ""
# Коэффициент при x^2
if a != 0:
    eq_str += f"{format_coefficient(a, is_first=True)}x^2"
# Коэффициент при x
if b != 0:
    eq_str += f"{format_coefficient(b)}x"
# Свободный член
if c != 0:
    eq_str += f"{format_coefficient(c)}"
if eq_str == "":
    eq_str = "0"
eq_str += " = 0"

st.markdown("### 📝 Уравнение:")
st.markdown(f"## ${eq_str}$")

# -- Ввод пользователем своих корней --
col1, col2 = st.columns(2)
with col1:
    user_x1 = st.text_input("Ваш $x_1$", value=st.session_state.get('user_x1', ""), key="user_x1_input")
with col2:
    user_x2 = st.text_input("Ваш $x_2$", value=st.session_state.get('user_x2', ""), key="user_x2_input")

check_pressed = st.button("Проверить ответ")

if check_pressed:
    # Попробуем преобразовать ввод к int
    try:
        ux1 = int(user_x1.strip())
        ux2 = int(user_x2.strip())
        user_roots = {ux1, ux2}
        real_roots = {true_x1, true_x2}
        if user_roots == real_roots:
            st.session_state['last_result'] = "success"
            st.session_state['show_answer'] = False
        else:
            st.session_state['last_result'] = "fail"
            st.session_state['show_answer'] = True
        st.session_state['user_x1'] = user_x1
        st.session_state['user_x2'] = user_x2
    except Exception:
        st.session_state['last_result'] = "input_error"
        st.session_state['show_answer'] = False
        st.session_state['user_x1'] = user_x1
        st.session_state['user_x2'] = user_x2

# -- Сообщение о результате --
if st.session_state.get('last_result') == "success":
    st.success("Отлично! Ваши корни совпадают с верными. 🎉")
elif st.session_state.get('last_result') == "fail":
    st.error("Ошибка. Ваши корни не совпадают.")
    st.markdown(f"**Правильный ответ:** $x_1 = {true_x1}$, $x_2 = {true_x2}$")
    # Показываем полные вычисления, полезно для обучения
    D = b ** 2 - 4 * a * c
    sqrt_D = int(math.sqrt(D))
    st.markdown(f"$D = {b}^2 - 4 \\times {a} \\times {c} = {D}$")
    st.markdown(f"$\\sqrt{{D}} = {sqrt_D}$")
    st.markdown(f"$x_1 = \\frac{{-b + \\sqrt{{D}}}}{{2a}} = \\frac{{-({b}) + {sqrt_D}}}{{2 \\cdot {a}}} = {true_x1}$")
    st.markdown(f"$x_2 = \\frac{{-b - \\sqrt{{D}}}}{{2a}} = \\frac{{-({b}) - {sqrt_D}}}{{2 \\cdot {a}}} = {true_x2}$")
    if a == 1:
        st.markdown(f"$x^2 + {b}x + {c} = (x - {true_x1})(x - {true_x2})$")
    else:
        st.markdown(f"${a}x^2 + {b}x + {c} = {a}(x - {true_x1})(x - {true_x2})$")
elif st.session_state.get('last_result') == "input_error":
    st.error("Ошибка ввода. Введите целые числа для корней.")

# -- Сайдбар с информацией --
with st.sidebar:
    st.header("ℹ️ Информация")
    st.markdown("""
    **Как это работает:**
    
    1. Выберите уровень сложности
    2. Нажмите "Новое уравнение"
    3. Решите уравнение и введите свои ответы
    4. Нажмите "Проверить ответ"
    5. Если ошиблись — увидите правильный ответ и разбор

    **Особенности:**
    - Все корни - целые числа
    - Дискриминант - полный квадрат
 
    """)
    st.markdown("---")
    st.markdown("**Формула дискриминанта:**")
    st.latex(r"D = b^2 - 4ac")
    st.markdown("**Формула корней:**")
    st.latex(r"x_{1,2} = \frac{-b \pm \sqrt{D}}{2a}")


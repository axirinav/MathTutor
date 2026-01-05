import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Тригонометрия", page_icon="📐")

st.title("📐 Практика: Отношения")

# --- 1. ЛОГИКА ---

def generate_pythagorean_triple():
    m = random.randint(2, 7)
    n = random.randint(1, m - 1)
    k = random.choice([1, 1, 2, 3]) 
    
    a = k * (m**2 - n**2)
    b = k * (2 * m * n)
    c = k * (m**2 + n**2)
    
    if random.choice([True, False]):
        return b, a, c
    return a, b, c

funcs = ["sin", "cos", "tg", "ctg"]

# Функция запуска новой игры
def new_task():
    a, b, c = generate_pythagorean_triple()
    st.session_state.side_a = a
    st.session_state.side_b = b
    st.session_state.side_c = c
    st.session_state.target_func = random.choice(funcs)
    st.session_state.num = None
    st.session_state.den = None
    st.session_state.checked = False
    st.session_state.result_msg = ""

# Функция проверки
def check_answer():
    user_num = st.session_state.num
    user_den = st.session_state.den
    
    a = st.session_state.side_a
    b = st.session_state.side_b
    c = st.session_state.side_c
    func = st.session_state.target_func
    
    if func == "sin":
        correct_num, correct_den = a, c
    elif func == "cos":
        correct_num, correct_den = b, c
    elif func == "tg":
        correct_num, correct_den = a, b
    elif func == "ctg":
        correct_num, correct_den = b, a
        
    st.session_state.checked = True
    
    if user_num is None or user_den is None:
        st.session_state.result_msg = "empty_error"
    elif user_den == 0:
        st.session_state.result_msg = "zero_error"
    elif user_num * correct_den == user_den * correct_num:
        st.session_state.result_msg = "success"
        st.session_state.correct_str = f"{correct_num}/{correct_den}"
    else:
        st.session_state.result_msg = "fail"
        st.session_state.correct_str = f"{correct_num}/{correct_den}"

# --- 2. ИНИЦИАЛИЗАЦИЯ ---
if 'side_a' not in st.session_state:
    if 'num' not in st.session_state: st.session_state.num = None
    if 'den' not in st.session_state: st.session_state.den = None
    a, b, c = generate_pythagorean_triple()
    st.session_state.side_a = a
    st.session_state.side_b = b
    st.session_state.side_c = c
    st.session_state.target_func = random.choice(funcs)
    st.session_state.checked = False
    st.session_state.result_msg = ""

# Текущие данные
a = st.session_state.side_a
b = st.session_state.side_b
c = st.session_state.side_c
func = st.session_state.target_func

# --- 3. КОМПАКТНЫЙ САЙДБАР ---
with st.sidebar:
    st.header("ℹ️ Шпаргалка")
    
    # Используем HTML для цветной легенды (занимает меньше места, чем markdown списки)
    st.markdown("""
    <div style="font-size: 14px; margin-bottom: 10px;">
    <b>Легенда:</b><br>
    <span style='color: green;'>■</span> Противолежащий (a)<br>
    <span style='color: blue;'>■</span> Прилежащий (b)<br>
    <span style='color: gray;'>■</span> Гипотенуза (c)
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Формулы в одну строку (LaTeX) для экономии места
    st.markdown("**Формулы:**")
    st.latex(r"\sin \alpha = \frac{a}{c}, \quad \cos \alpha = \frac{b}{c}")
    st.latex(r"\text{tg} \alpha = \frac{a}{b}, \quad \text{ctg} \alpha = \frac{b}{a}")

# --- 4. ТЕКСТОВОЕ УСЛОВИЕ И ЧЕРТЕЖ ---

# Четкое текстовое условие
st.markdown(f"""
### Дано: 
Прямоугольный треугольник со сторонами:
* :green[**Противолежащий катет a = {a}**]
* :blue[**Прилежащий катет b = {b}**]
* :grey[**Гипотенуза c = {c}**]

Нужно найти: :red[**$\\{func}(\\alpha)$**]
""")

# Свернутый компактный чертеж
with st.expander("👁️ Показать чертеж", expanded=False):
    fig, ax = plt.subplots(figsize=(3.5, 2.5), dpi=100)

    triangle = patches.Polygon([[0, 0], [b, 0], [b, a]], closed=True, fill=None, edgecolor='black', linewidth=2)
    ax.add_patch(triangle)

    arc = patches.Arc((0, 0), b*0.3, a*0.3, theta1=0, theta2=30, color='red', linewidth=2)
    ax.add_patch(arc)
    ax.text(b*0.15, a*0.05, r'$\alpha$', fontsize=12, color='red')

    ax.text(b/2, -a*0.08, f'{b}', ha='center', fontsize=12, color='blue', fontweight='bold')
    ax.text(b + b*0.02, a/2, f'{a}', va='center', fontsize=12, color='green', fontweight='bold')
    ax.text(b/2, a/2 + a*0.1, f'{c}', ha='center', fontsize=12, color='gray', fontweight='bold')

    ax.set_xlim(-b*0.1, b * 1.2)
    ax.set_ylim(-a*0.1, a * 1.2)
    ax.axis('off')
    
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

# --- 5. ВВОД ОТВЕТА ---
st.write("") # Небольшой отступ
st.subheader("Введите ответ:")

col1, col_slash, col2, col_btns = st.columns([2, 0.5, 2, 4])

with col1:
    st.number_input("Числитель", step=1, key="num", on_change=check_answer, value=None)

with col_slash:
    st.markdown("## /") 

with col2:
    st.number_input("Знаменатель", step=1, key="den", on_change=check_answer, value=None)

# Кнопки
with col_btns:
    st.write("") 
    st.write("") 
    
    btn_check, btn_next = st.columns(2)
    
    with btn_check:
        st.button("✅ Проверить", on_click=check_answer)
        
    with btn_next:
        st.button("➡️ Дальше", on_click=new_task)

# --- 6. РЕЗУЛЬТАТ ---
if st.session_state.get('checked'):
    msg = st.session_state.result_msg
    
    if msg == "success":
        st.success(f"Верно! {st.session_state.correct_str}")
     #   st.balloons()
    elif msg == "fail":
        st.error(f"Ошибка. Правильный ответ: {st.session_state.correct_str}")
    elif msg == "zero_error":
        st.error("На ноль делить нельзя!")
    elif msg == "empty_error":
        st.warning("Пожалуйста, введите оба числа.")
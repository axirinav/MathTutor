import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
st.set_page_config(page_title="Тригонометрия", page_icon="📐")

st.title("📐 Практика: Вычисли функции")
st.write("Даны стороны треугольника. Найди значение указанной функции.")

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

# Инициализация переменных при первом запуске
if 'side_a' not in st.session_state:
    a, b, c = generate_pythagorean_triple()
    st.session_state.side_a = a
    st.session_state.side_b = b
    st.session_state.side_c = c
    st.session_state.target_func = random.choice(funcs)
    # Инициализируем значения полей ввода (если их нет)
    if 'num' not in st.session_state: st.session_state.num = 0
    if 'den' not in st.session_state: st.session_state.den = 1

# Функция для кнопки "Следующая задача"
def new_task():
    # 1. Генерируем новые числа
    a, b, c = generate_pythagorean_triple()
    st.session_state.side_a = a
    st.session_state.side_b = b
    st.session_state.side_c = c
    st.session_state.target_func = random.choice(funcs)
    
    # 2. ОЧИЩАЕМ ПОЛЯ ВВОДА (сбрасываем значения ключей)
    st.session_state.num = 0
    st.session_state.den = 1

# Достаем текущие значения
a = st.session_state.side_a
b = st.session_state.side_b
c = st.session_state.side_c
func = st.session_state.target_func

# --- 2. ВИЗУАЛИЗАЦИЯ ---
fig, ax = plt.subplots(figsize=(5, 4))

triangle = patches.Polygon([[0, 0], [b, 0], [b, a]], closed=True, fill=None, edgecolor='black', linewidth=2)
ax.add_patch(triangle)

arc = patches.Arc((0, 0), b*0.3, a*0.3, theta1=0, theta2=30, color='red', linewidth=2)
ax.add_patch(arc)
ax.text(b*0.15, a*0.05, r'$\alpha$', fontsize=14, color='red')

ax.text(b/2, -a*0.08, f'{b}', ha='center', fontsize=14, color='blue', fontweight='bold')
ax.text(b + b*0.02, a/2, f'{a}', va='center', fontsize=14, color='green', fontweight='bold')
ax.text(b/2, a/2 + a*0.1, f'{c}', ha='center', fontsize=14, color='gray', fontweight='bold')

ax.set_xlim(-b*0.1, b * 1.2)
ax.set_ylim(-a*0.1, a * 1.2)
ax.axis('off')
st.pyplot(fig)

# --- 3. ИНТЕРФЕЙС ---
st.subheader(rf"Найдите: $\mathbf{{\{func}}}(\alpha)$")

# Разметка колонок: Ввод (2) / Черта (0.5) / Ввод (2) / КНОПКИ (4)
# Сделали последнюю колонку пошире, чтобы влезло две кнопки
col1, col_slash, col2, col_btns = st.columns([2, 0.5, 2, 4])

with col1:
    # Важно: добавили key="num", чтобы управлять этим полем из кода
    user_num = st.number_input("Числитель", step=1, key="num")

with col_slash:
    st.markdown("## /") 

with col2:
    # Важно: добавили key="den"
    user_den = st.number_input("Знаменатель", step=1, key="den")

# Логика правильного ответа
if func == "sin":
    correct_num, correct_den = a, c
elif func == "cos":
    correct_num, correct_den = b, c
elif func == "tg":
    correct_num, correct_den = a, b
elif func == "ctg":
    correct_num, correct_den = b, a

# --- БЛОК КНОПОК ---
with col_btns:
    st.write("") # Отступы, чтобы кнопки встали ровно напротив полей ввода
    st.write("")
    
    # Разбиваем колонку кнопок еще на две части
    btn_check, btn_next = st.columns(2)
    
    with btn_check:
        check_clicked = st.button("✅ Проверить")
        
    with btn_next:
        # Кнопка вызывает функцию new_task, которая очищает поля
        st.button("➡️ Дальше", on_click=new_task)

# Логика проверки (срабатывает только при нажатии Проверить)
if check_clicked:
    if user_den == 0:
        st.error("На ноль делить нельзя!")
    else:
        if user_num * correct_den == user_den * correct_num:
            st.success(f"Верно! {correct_num}/{correct_den}")
            st.balloons()
        else:
            st.error(f"Ошибка. Ответ: {correct_num} / {correct_den}")
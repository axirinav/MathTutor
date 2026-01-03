import streamlit as st

# Настройка страницы (Заголовок в браузере и иконка)
st.set_page_config(
    page_title="MathTutor",
    page_icon="🎓",
    layout="centered"
)

# 1. ЗАГОЛОВОК И ПРИВЕТСТВИЕ
st.title("🎓 MathTutor")
st.markdown("### Тренажер, который не ставит двойки")

st.write("""
Добро пожаловать! Меня зовут Ирина и я репетитор по математике. Мои ученики знают, что занятие всегда начинается с разминки — устного счета.
Давно хотела сделать свои примеры. А еще хотелось повайбкодить. Пока я экспериментирую, вы можете попробовать тренажеры.
""")

st.divider()  # Горизонтальная линия

# 2. СПИСОК ТРЕНАЖЕРОВ (Табличный вид)
st.subheader("🛠 Что будем тренировать?")

# --- Логика: Данные храним отдельно ---
tools = [
    {
        "page": "pages/KvEquations.py", # Проверьте имя файла!
        "name": "🧮 Уравнения",
        "desc": "Генератор квадратных уравнений. Тренируй счет и теорему Виета."
    },
    {
        "page": "pages/Trigonometry (relations).py",      # Проверьте имя файла!
        "name": "📐 Тригонометрия",
        "desc": "Визуальный тренажер. Пойми связь между сторонами и углами."
    }
]

# --- Визуализация: Рисуем таблицу ---

# Заголовки таблицы
# [1, 2] означает, что вторая колонка в 2 раза шире первой
header1, header2 = st.columns([1, 2]) 
header1.markdown("**Название**")
header2.markdown("**Описание**")

st.divider() # Линия-разделитель (как граница в таблице)

# Выводим строки циклом
for tool in tools:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Это ссылка, которая выглядит как часть таблицы
        st.page_link(tool["page"], label=tool["name"], use_container_width=True)
        
    with col2:
        st.write(tool["desc"])
        
    st.divider() # Линия между строками

# 3. ПОДВАЛ (Контакты и ссылки)
# st.divider()

col_social, col_contact = st.columns(2)

with col_social:
    st.markdown("**🔗 Полезное:**")
    # Красивая ссылка-кнопка
    st.link_button("Квадратный кореш (Telegram)", "https://t.me/kvkoresh")

with col_contact:
    st.markdown("**📬 Связь:**")
    st.write("Есть идея или нашли ошибку?")

    st.markdown("[Написать мне (@nazmiika)](https://t.me/nazmiika)")

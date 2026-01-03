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

# --- Функция для тонкой линии (CSS хак внутри Python) ---
def thin_divider():
    # margin: 5px 0 -> 5 пикселей отступа сверху/снизу (вместо стандартных 20+)
    st.markdown("<hr style='margin: 5px 0; border-top: 1px solid #ddd; opacity: 0.2;'>", unsafe_allow_html=True)

# --- Визуализация: Таблица ---

# Заголовки
col_h1, col_h2 = st.columns([1, 2]) 
col_h1.markdown("**Название**")
col_h2.markdown("**Описание**")

thin_divider() # Используем нашу компактную линию

# Строки
for tool in tools:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.page_link(tool["page"], label=tool["name"], use_container_width=True)
        
    with col2:
        # st.write добавляет свои отступы, заменим на markdown для плотности
        st.markdown(tool["desc"])
        
    thin_divider() # Линия между строками

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
import streamlit as st

st.title("🎓 MathTutor")
st.markdown("### Тренажер, который не ставит двойки")

st.write("""
Добро пожаловать! Меня зовут Ирина и я репетитор по математике. Мои ученики знают, что занятие всегда начинается с разминки — устного счета.
Давно хотела сделать свои примеры. А еще хотелось повайбкодить. Пока я экспериментирую, вы можете попробовать тренажеры.
""")

st.divider()

st.subheader("🛠 Что будем тренировать?")

tools = [
        {
        "page": "pages/kv_equations.py",
        "name": "🧮 Уравнения",
        "desc": "Генератор квадратных уравнений. Тренируй счет и теорему Виета."
    },
    {
        "page": "pages/trig_relations.py",
        "name": "📐 Тригонометрия",
        "desc": "Визуальный тренажер. Пойми связь между сторонами и углами."
    },
    {
        "page": "pages/areas.py",
        "name": "▭ Площади треугольников",
        "desc": "Формулы площади треугольников (ф. Герона, через угол и через высоту)."
    }
]

def thin_divider():
    st.markdown(
        "<hr style='margin: 5px 0; border-top: 1px solid #ddd; opacity: 0.2;'>",
        unsafe_allow_html=True
    )

col_h1, col_h2 = st.columns([1, 2])
col_h1.markdown("**Название**")
col_h2.markdown("**Описание**")

thin_divider()

for tool in tools:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.page_link(tool["page"], label=tool["name"], use_container_width=True)
    with col2:
        st.markdown(tool["desc"])
    thin_divider()

col_social, col_contact = st.columns(2)

with col_social:
    st.markdown("**🔗 Полезное:**")
    st.link_button("Квадратный кореш (Telegram)", "https://t.me/kvkoresh")

with col_contact:
    st.markdown("**📬 Связь:**")
    st.write("Есть идея или нашли ошибку?")
    st.markdown("[Написать мне (@nazmiika)](https://t.me/nazmiika)")


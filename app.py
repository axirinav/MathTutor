import streamlit as st

st.set_page_config(page_title="MathTutor", page_icon="🎓", layout="centered")

home = st.Page("main.py", title="Главная", icon="🏠")

kv_eq = st.Page("pages/kv_equations.py", title="Уравнения", icon="🧮")
trig = st.Page("pages/trig_relations.py", title="Тригонометрия", icon="📐")
areas = st.Page("pages/areas.py", title="Площади треугольников", icon="🔺")

pg = st.navigation(
    [home, kv_eq, trig, areas],
    position="sidebar",
)

pg.run()

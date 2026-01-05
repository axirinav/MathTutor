import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, List, Optional

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# -----------------------------
# 1. МОДЕЛИ ДАННЫХ
# -----------------------------

class TaskType(Enum):
    HERON = "Формула Герона"
    BASE_HEIGHT = "Основание и высота"
    TWO_SIDES_ANGLE = "Две стороны и угол"

@dataclass
class GeometryTask:
    task_type: TaskType
    question: str
    correct_answer: float
    # Координаты: A, B, C
    coords: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]
    # Подписи: (x, y, текст, цвет)
    labels: List[Tuple[float, float, str, str]]
    # Доп. элементы
    extras: dict = field(default_factory=dict)

HERONIAN_TRIPLES = [
    (3, 4, 5), (5, 5, 6), (5, 5, 8), (5, 12, 13), (6, 8, 10),
    (10, 10, 12), (10, 13, 13), (13, 14, 15), (15, 15, 18), (20, 20, 24)
]

# -----------------------------
# 2. ГЕНЕРАТОРЫ
# -----------------------------

def calculate_heron_coords(a, b, c) -> list:
    try:
        cos_a = (b**2 + c**2 - a**2) / (2 * b * c)
        x = b * cos_a
        y = b * math.sqrt(1 - cos_a**2)
    except ValueError:
        return [(0,0), (c,0), (c/2, 1)] 
    return [(0, 0), (c, 0), (x, y)]

def gen_heron_task() -> GeometryTask:
    a, b, c = random.choice(HERONIAN_TRIPLES)
    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    
    coords = calculate_heron_coords(a, b, c)
    C = coords[2]
    
    labels = [
        (c / 2, -0.6, f"c={c}", "black"),
        (C[0] / 2 - 0.6, C[1] / 2, f"b={b}", "blue"),
        ((c + C[0]) / 2 + 0.6, C[1] / 2, f"a={a}", "green")
    ]
    
    return GeometryTask(
        task_type=TaskType.HERON,
        question=f"Найди площадь треугольника со сторонами {a}, {b}, {c}.",
        correct_answer=area,
        coords=tuple(coords),
        labels=labels
    )

def gen_base_height_task() -> GeometryTask:
    b = random.randint(6, 18)
    h = random.randint(4, 14)
    offset = random.uniform(0.2 * b, 0.8 * b)
    
    coords = [(0, 0), (b, 0), (offset, h)]
    labels = [
        (b / 2, -0.8, f"b={b}", "black"),
        (offset + 0.5, h / 2, f"h={h}", "red")
    ]
    
    return GeometryTask(
        task_type=TaskType.BASE_HEIGHT,
        question=f"Найди площадь, если основание b={b}, а высота h={h}.",
        correct_answer=0.5 * b * h,
        coords=tuple(coords),
        labels=labels,
        extras={"height_line": ((offset, 0), (offset, h))}
    )

def gen_angle_task() -> GeometryTask:
    angle = random.choice([30, 90, 150])
    while True:
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        area = 0.5 * a * b * (1 if angle == 90 else 0.5)
        if abs(area * 2 - round(area * 2)) < 1e-9:
            break
            
    rad = math.radians(angle)
    coords = [(0, 0), (b, 0), (a * math.cos(rad), a * math.sin(rad))]
    C = coords[2]
    
    labels = [
        (b / 2, -0.8, f"b={b}", "black"),
        (C[0] / 2 - 0.6, C[1] / 2 + 0.6, f"a={a}", "blue"),
        (0.5, 0.5, f"{angle}°", "red")
    ]
    
    return GeometryTask(
        task_type=TaskType.TWO_SIDES_ANGLE,
        question=f"Стороны: {a} и {b}, угол между ними: {angle}°.",
        correct_answer=area,
        coords=tuple(coords),
        labels=labels,
        extras={"angle_arc": (angle, 1.5)}
    )

def generate_task(mode_name: str) -> GeometryTask:
    if mode_name == TaskType.HERON.value:
        return gen_heron_task()
    elif mode_name == TaskType.BASE_HEIGHT.value:
        return gen_base_height_task()
    else:
        return gen_angle_task()

# -----------------------------
# 3. ВИЗУАЛИЗАЦИЯ
# -----------------------------

def plot_triangle(task: GeometryTask):
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_aspect('equal')
    ax.axis('off')
    
    pts = task.coords
    poly = patches.Polygon(pts, closed=True, 
                           edgecolor='#333333', facecolor='#E0F7FA', 
                           linewidth=2, joinstyle='round')
    ax.add_patch(poly)
    
    if "height_line" in task.extras:
        start, end = task.extras["height_line"]
        ax.plot([start[0], end[0]], [start[1], end[1]], 
                color='red', linestyle='--', linewidth=1.5)
        
    if "angle_arc" in task.extras:
        angle_val, radius = task.extras["angle_arc"]
        arc = patches.Arc((0, 0), radius*2, radius*2, 
                          theta1=0, theta2=angle_val, 
                          color='red', linewidth=1.5)
        ax.add_patch(arc)

    for x, y, text, color in task.labels:
        ax.text(x, y, text, color=color, fontsize=11, fontweight='bold', 
                ha='center', va='center', 
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    xs, ys = zip(*pts)
    margin = 1.5
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)
    
    return fig

# -----------------------------
# 4. ОБРАБОТЧИКИ
# -----------------------------

def parse_input(text: str) -> Optional[float]:
    try:
        return float(text.replace(',', '.').strip())
    except ValueError:
        return None

def check_answer():
    user_val = parse_input(st.session_state.user_input)
    task: GeometryTask = st.session_state.current_task
    
    if user_val is None:
        st.session_state.feedback = ("warning", "Введи число (например, 24.5)")
        return

    if abs(user_val - task.correct_answer) < 1e-6:
        # Убрали st.balloons()
        st.session_state.feedback = ("success", f"Верно! Ответ: {task.correct_answer:g}")
    else:
        st.session_state.feedback = ("error", f"Ошибка. Правильный ответ: {task.correct_answer:g}")

def next_task():
    st.session_state.current_task = generate_task(st.session_state.mode_select)
    st.session_state.user_input = "" 
    st.session_state.feedback = None

# -----------------------------
# 5. ИНТЕРФЕЙС
# -----------------------------

st.set_page_config(page_title="Площади фигур", page_icon="📐")

# Инициализация
if 'mode_select' not in st.session_state:
    st.session_state.mode_select = TaskType.HERON.value
if 'current_task' not in st.session_state:
    next_task()

# Заголовок
st.title("📐 Площадь треугольника")

# --- ВЫБОР ТИПА ЗАДАЧИ (ПЕРЕНЕСЕН СЮДА) ---
# Находится сразу под заголовком, удобно с телефона
st.selectbox(
    "Выбери тип задачи:", 
    [t.value for t in TaskType], 
    key='mode_select',
    on_change=next_task 
)

# Разделитель для визуальной чистоты
st.divider()

task = st.session_state.current_task

# 1. Текст задачи
st.markdown(f"#### {task.question}")

# 2. Рисунок (Спрятан)
with st.expander("👁️ Показать чертеж", expanded=False):
    fig = plot_triangle(task)
    st.pyplot(fig, use_container_width=True) 
    plt.close(fig)

# 3. Ввод и кнопки
col_input, col_check = st.columns([2, 1])

with col_input:
    st.text_input(
        "Ответ:", 
        key="user_input", 
        on_change=check_answer,
        placeholder="Например: 24"
    )

with col_check:
    st.write("") 
    st.write("") 
    st.button("Проверить", on_click=check_answer, type="primary", use_container_width=True)

# 4. Результат
if st.session_state.feedback:
    status, msg = st.session_state.feedback
    if status == "success":
        st.success(msg)
    elif status == "error":
        st.error(msg)
    else:
        st.warning(msg)

# 5. Кнопка Дальше
st.divider()
st.button("Следующая задача ➡️", on_click=next_task, use_container_width=True)
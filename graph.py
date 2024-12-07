import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# Настройка страницы
st.set_page_config(layout="centered", page_title="Рулетка 🎲")

# Числа в порядке расположения на колесе рулетки
roulette_numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11,
                    30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
                    29, 7, 28, 12, 35, 3, 26]

# Создание графа рулетки
roulette_graph = nx.Graph()
for i in range(len(roulette_numbers)):
    current = roulette_numbers[i]
    next_num = roulette_numbers[(i + 1) % len(roulette_numbers)] 
    roulette_graph.add_edge(current, next_num)

# Функция для получения соседей числа
def get_neighbors(number, graph, n_neighbors=2):
    neighbors = [number]
    current_index = roulette_numbers.index(number)
    for i in range(1, n_neighbors + 1):
        neighbors.append(roulette_numbers[(current_index + i) % len(roulette_numbers)])
        neighbors.append(roulette_numbers[(current_index - i) % len(roulette_numbers)])
    return sorted(set(neighbors))

# Визуализация рулетки с анимацией вращения
def animate_roulette(graph, bets, winning_number):
    nodes = list(graph.nodes)
    plot_placeholder = st.empty()  # Контейнер для переиспользования
    
    for step in range(20):
        current_number = nodes[step % len(nodes)]
        color_map = ['yellow' if node in bets else
                     'green' if node == winning_number else
                     'lightblue' for node in nodes]
        color_map[nodes.index(current_number)] = 'red' 

        # Отрисовка графа
        fig, ax = plt.subplots(figsize=(10, 8))
        nx.draw_circular(
            graph,
            with_labels=True,
            node_color=color_map,
            node_size=500,
            font_size=10,
            ax=ax
        )
        ax.set_title(f"Вращение рулетки: {current_number}", fontsize=16)
        plot_placeholder.pyplot(fig)  # Отображение в одном контейнере
        time.sleep(0.1)

    # Финальная визуализация
    color_map = ['green' if node == winning_number else
                 'yellow' if node in bets else
                 'lightblue' for node in nodes]
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_circular(
        graph,
        with_labels=True,
        node_color=color_map,
        node_size=500,
        font_size=10,
        ax=ax
    )
    ax.set_title(f"Выигрышное число: {winning_number}", fontsize=16)
    plot_placeholder.pyplot(fig)  # Финальная картинка в том же контейнере

# Основная страница игры
def main_game():
    st.title("Мини-игра: Рулетка 🎲")
    st.write("""Добро пожаловать в игру!  
        Выберите число и количество соседей, чтобы сделать ставку.  
        После вращения рулетки, вы узнаете результат!""")

    bet_number = st.selectbox("Выберите число для ставки", roulette_numbers)
    n_neighbors = st.slider("Сколько соседей учитывать?", min_value=1, max_value=5, value=2)

    # Кнопка для запуска игры
    if st.button("Запустить рулетку"):
        bets = get_neighbors(bet_number, roulette_graph, n_neighbors)
        st.write(f"Вы ставите на числа: {bets}")
        winning_number = random.choice(roulette_numbers)
        animate_roulette(roulette_graph, bets, winning_number)

        # Проверяем результат
        if winning_number in bets:
            st.success("Поздравляем! Вы выиграли! 🎉")
        else:
            st.error("К сожалению, вы проиграли. Попробуйте снова!")

        # Сохраняем данные для страницы информации
        st.session_state['bets'] = bets
        st.session_state['winning_number'] = winning_number
        st.session_state['bet_number'] = bet_number
        st.session_state['page'] = 'info'

    # Кнопка перехода на страницу информации
    if st.button("Узнать, как это работает"):
        st.session_state['page'] = 'info'

# Страница с информацией
# Страница с информацией
def info_page():
    st.title("Как работает рулетка? 🤔")
    st.write("""<div style="font-size: 20px; line-height: 1.8; text-align: justify;">
        Рулетка использует принципы теории графов, вероятности и визуализации данных.<br>
        <ul>
            <li><b>Граф:</b> Колесо моделируется как граф, где каждая вершина (узел) представляет число рулетки.</li>
            <li><b>Ребра:</b> Соединяют числа в порядке их расположения на колесе, создавая циклический граф.</li>
            <li><b>Циклический граф:</b> Граф имеет замкнутую структуру, где последнее число соединено с первым.</li>
            <li><b>Подсветка:</b> Числа вашей ставки и их соседи визуально выделяются на графе.</li>
        </ul>
        <b>Процесс работы рулетки:</b>
        <ol>
            <li>Вы выбираете число и задаёте диапазон соседей (например, 2 ближайших числа).</li>
            <li>Программа определяет ваши числа ставки, включая выбранное и соседние.</li>
            <li>Рулетка визуализируется как циклический граф, где текущий сектор подсвечивается.</li>
            <li>Генератор случайных чисел выбирает итоговое число (выигрышное).</li>
            <li>Граф обновляется, выделяя выигрышное число.</li>
        </ol>
        </div>
    """, unsafe_allow_html=True)

    st.write("""<div style="font-size: 20px; line-height: 1.8; text-align: justify;">
        <b>Теория графов в рулетке:</b><br>
        <ul>
            <li><b>Вершины:</b> Представляют числа рулетки от 0 до 36.</li>
            <li><b>Рёбра:</b> Связывают числа, образуя замкнутый цикл.</li>
            <li><b>Цвета:</b> Узлы окрашиваются в зависимости от их роли:
                <ul>
                    <li><b>Красный и чёрный:</b> Стандартные цвета секторов рулетки.</li>
                    <li><b>Жёлтый:</b> Ваши числа ставки.</li>
                    <li><b>Зелёный:</b> Выигрышное число.</li>
                </ul>
            </li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    st.write("""<div style="font-size: 20px; line-height: 1.8; text-align: justify;">
        <b>Вероятность выигрыша:</b><br>
        <ul>
            <li>Вероятность выигрыша зависит от количества выбранных чисел.</li>
            <li>Если вы ставите на одно число, вероятность выигрыша составляет 1/37 (около 2,7%).</li>
            <li>С увеличением диапазона соседей вероятность возрастает:
                <ul>
                    <li>Например, при выборе 5 чисел вероятность выигрыша составляет 5/37 (около 13,5%).</li>
                </ul>
            </li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    # Показ результатов игры
    if 'winning_number' in st.session_state and 'bets' in st.session_state:
        st.subheader("Ваши результаты:")
        st.write(f"**Ваше число:** {st.session_state['bet_number']}")
        st.write(f"**Выигрышное число:** {st.session_state['winning_number']}")
        st.write(f"**Ваши числа ставки:** {', '.join(map(str, st.session_state['bets']))}")

    st.write("""<div style="font-size: 20px; line-height: 1.8; text-align: justify;">
        <b>Заключение:</b><br>
        Этот проект демонстрирует, как можно использовать теорию графов и визуализацию данных для моделирования реальных систем, таких как рулетка. Он также подчеркивает роль вероятности в анализе и понимании случайных процессов.
        </div>
    """, unsafe_allow_html=True)

    if st.button("Вернуться к игре"):
        st.session_state['page'] = 'game'

# Управление страницами
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'game'

    if st.session_state['page'] == 'game':
        main_game()
    elif st.session_state['page'] == 'info':
        info_page()

# Запуск приложения
if __name__ == "__main__":
    main()

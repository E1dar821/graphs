import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

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
def info_page():
    st.title("Как работает рулетка? 🤔")
    st.write("""Рулетка использует принципы теории графов и вероятности:
        - Колесо моделируется как граф, где вершины представляют числа рулетки.
        - Ребра соединяют числа в порядке их расположения на колесе.
        - Выбранное вами число и его соседи визуально подсвечиваются.""")

    # Показ результатов игры
    if 'winning_number' in st.session_state and 'bets' in st.session_state:
        st.write(f"Ваше число: {st.session_state['bet_number']}")
        st.write(f"Выигрышное число: {st.session_state['winning_number']}")
        st.write(f"Ваши ставки: {st.session_state['bets']}")

    st.write("""### Принципы работы:
        - Колесо рулетки моделируется с использованием циклического графа.
        - При вращении каждое число подсвечивается в порядке, соответствующем его положению.
        - Рулетка останавливается на случайном числе, используя генератор случайных чисел.""")

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

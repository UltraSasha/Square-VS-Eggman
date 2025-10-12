from tkinter import *

INST = """Инструкция к игре «Squares And Coins»

Управление
    WASD или стрелки — движение персонажа
    Пробел — активация турбо-режима
    I — вызов инструкции

Цель игры
    Собрать как можно больше монет за отведенное время, избегая красного квадрата (врага).

Элементы игры
    Зеленый квадрат — ваш персонаж
    Красный квадрат — враг, которого нужно избегать
    Цветные круги — монеты разных типов
    Верхняя панель — отображает время, уровень и счет

Типы монет
    Желтые монеты (+3 очка) — крупные бонусы
    Зеленые монеты (+1 очко) — стандартные монеты
    Оранжевые мины (-1 очко) — опасные предметы
    Синие монеты (+2 очка) — средние бонусы
    Белые монеты (+5 очков) — редкие крупные бонусы

Особенности игры
    Турбо-режим — увеличивает скорость персонажа при зажатом пробеле
    Автоматическое ускорение — скорость растет с набором очков
    Система уровней — переход на следующий уровень при наборе определенного количества очков
    Таймер — игра заканчивается при истечении времени

Советы по игре
    Используйте турбо-режим для быстрого сбора монет
    Избегайте столкновения с красным квадратом
    Следите за временем на верхней панели
    Собирайте белые монеты для быстрого набора очков
    При опасности используйте маневренность персонажа

Завершение игры
    Игра заканчивается в следующих случаях:
    
    Истечение времени
    Столкновение с красным квадратом
    Наезд на мину (потеря всех очков)
    Нажатие на крестик окна

Для повторного запуска нажмите пробел после завершения игры"""


def instruction(settings_config=None, initial_settings=None):
    """
    Универсальное окно инструкций и настроек
    
    Args:
        settings_config: словарь с конфигурацией параметров
        initial_settings: начальные значения настроек
    """
    # Конфигурация параметров по умолчанию
    default_config = {
        'player_speed': {
            'type': 'scale',
            'label': 'Скорость игрока',
            'min': 3,
            'max': 10,
            'default': 5
        },
        'enemy_speed': {
            'type': 'scale',
            'label': 'Скорость врага',
            'min': 1.0,
            'max': 5.0,
            'resolution': 0.1,
            'default': 2.3
        },
        'game_time': {
            'type': 'scale', 
            'label': 'Время игры (сек)',
            'min': 60,
            'max': 300,
            'default': 120
        },
        'sound_volume': {
            'type': 'scale',
            'label': 'Громкость звука',
            'min': 0,
            'max': 100,
            'default': 80
        },
        'player_name': {
            'type': 'entry',
            'label': 'Имя игрока',
            'default': 'Игрок'
        },
        'show_tutorial': {
            'type': 'checkbox',
            'label': 'Показывать обучение',
            'default': True
        },
        'difficulty': {
            'type': 'radiobutton',
            'label': 'Сложность',
            'options': ['Легкая', 'Средняя', 'Сложная'],
            'default': 'Средняя'
        },
        'resolution': {
            'type': 'combobox',
            'label': 'Разрешение',
            'options': ['800x600', '1024x768', '1280x720', '1920x1080'],
            'default': '1024x768'
        }
    }
    
    # Объединяем с переданной конфигурацией
    config = {**default_config, **(settings_config or {})}
    
    # Собираем начальные значения
    current_settings = {}
    for key, params in config.items():
        if initial_settings and key in initial_settings:
            current_settings[key] = initial_settings[key]
        else:
            current_settings[key] = params['default']
    
    # Словарь для хранения переменных Tkinter
    tk_vars = {}
    
    def create_widget(parent, key, params):
        """Создает виджет для параметра"""
        frame = Frame(parent)
        frame.pack(fill=X, padx=20, pady=5)
        
        Label(frame, text=params['label']).pack(side=LEFT)
        
        widget_frame = Frame(frame)
        widget_frame.pack(side=RIGHT, fill=X, expand=True)
        
        if params['type'] == 'scale':
            var = None
            if isinstance(params['default'], int):
                var = IntVar(value=current_settings[key])
            else:
                var = DoubleVar(value=current_settings[key])
            
            scale = Scale(widget_frame, from_=params['min'], to=params['max'],
                         variable=var, orient=HORIZONTAL)
            if 'resolution' in params:
                scale.config(resolution=params['resolution'])
            scale.pack(fill=X, expand=True)
            tk_vars[key] = var
            
        elif params['type'] == 'entry':
            var = StringVar(value=current_settings[key])
            entry = Entry(widget_frame, textvariable=var)
            entry.pack(fill=X, expand=True)
            tk_vars[key] = var
            
        elif params['type'] == 'checkbox':
            var = BooleanVar(value=current_settings[key])
            check = Checkbutton(widget_frame, variable=var, text="")
            check.pack(anchor=W)
            tk_vars[key] = var
            
        elif params['type'] == 'radiobutton':
            var = StringVar(value=current_settings[key])
            for i, option in enumerate(params['options']):
                rb = Radiobutton(widget_frame, text=option, variable=var, 
                               value=option)
                rb.pack(anchor=W)
            tk_vars[key] = var
            
        elif params['type'] == 'combobox':
            var = StringVar(value=current_settings[key])
            from tkinter import ttk
            combo = ttk.Combobox(widget_frame, textvariable=var, 
                               values=params['options'], state="readonly")
            combo.pack(fill=X, expand=True)
            tk_vars[key] = var
            
        return frame
    
    def save_settings():
        """Сохраняет текущие настройки"""
        nonlocal current_settings
        for key, var in tk_vars.items():
            current_settings[key] = var.get()
        settings_frame.pack_forget()
        main_frame.pack()
    
    def show_settings():
        """Показывает экран настроек"""
        main_frame.pack_forget()
        settings_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    def show_instructions():
        """Возвращает к инструкции"""
        settings_frame.pack_forget()
        main_frame.pack(fill=BOTH, expand=True)
    
    def close():
        """Закрывает окно и возвращает настройки"""
        root.destroy()
        root.quit()
        return current_settings

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", close)
    root.geometry("600x800")
    root.title("Инструкция и настройки")
    
    # Главный фрейм с инструкцией
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Текст инструкции с прокруткой
    text_frame = Frame(main_frame)
    text_frame.pack(fill=BOTH, expand=True)
    
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    text_widget = Text(text_frame, wrap=WORD, yscrollcommand=scrollbar.set,
                      font=("Arial", 10), padx=10, pady=10)
    text_widget.pack(side=LEFT, fill=BOTH, expand=True)
    text_widget.insert(END, INST)
    text_widget.config(state=DISABLED)
    
    scrollbar.config(command=text_widget.yview)
    
    # Кнопки в главном меню
    button_frame = Frame(main_frame)
    button_frame.pack(fill=X, pady=10)
    
    Button(button_frame, text="Настройки", command=show_settings,
           width=15).pack(side=LEFT, padx=5)
    Button(button_frame, text="Закрыть", command=close,
           width=15).pack(side=RIGHT, padx=5)
    
    # Фрейм настроек
    settings_frame = Frame(root)
    
    Label(settings_frame, text="Настройки игры",
          font=("Arial", 14, "bold")).pack(pady=10)
    
    # Создаем виджеты для всех параметров
    for key, params in config.items():
        create_widget(settings_frame, key, params)
    
    # Кнопки в настройках
    settings_buttons = Frame(settings_frame)
    settings_buttons.pack(fill=X, pady=20)
    
    Button(settings_buttons, text="Сохранить", command=save_settings,
           width=15).pack(side=LEFT, padx=10)
    Button(settings_buttons, text="Отмена", command=show_instructions,
           width=15).pack(side=RIGHT, padx=10)
    
    root.mainloop()
    return current_settings

"""
Примеры использования:

1. Базовое использование
settings = instruction()

2. С кастомной конфигурацией
custom_config = {
    'game_time': {
        'type': 'scale',
        'label': 'Длительность раунда',
        'min': 30,
        'max': 600,
        'default': 180
    },
    'music_enabled': {
        'type': 'checkbox', 
        'label': 'Включить музыку',
        'default': True
    }
}

3. С начальными значениями
initial_values = {
    'player_speed': 7,
    'player_name': 'СуперИгрок'
}

settings = instruction(custom_config, initial_values)




Поддерживаемые типы виджетов:

scale - ползунок (требует min, max)

entry - поле ввода текста

checkbox - флажок

radiobutton - переключатель (требует options)

combobox - выпадающий список (требует options)
"""
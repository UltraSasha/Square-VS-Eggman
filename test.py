result = """"""

while True:
    str_name = '"' + input("Введите название параметра: ") + '"'
    last1 = input("Введите значение 1 для 1920 на 1080: "); last2 = input("Введите значение 2 для 1920 на 1080: ")
    result += f"""
        if type_element == {str_name}:
                x = {last1} // (size_window_x / 100) * 100
                y = {last2} // (size_window_x / 100) * 100

                result.append(x); result.append(y)"""
    print(result)
 
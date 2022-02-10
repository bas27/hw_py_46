

class Stack:

    def __init__(self):
        self.some_list = []
    """
isEmpty - проверка стека на пустоту. Метод возвращает True или False.
push - добавляет новый элемент на вершину стека. Метод ничего не возвращает.
pop - удаляет верхний элемент стека. Стек изменяется. Метод возвращает верхний элемент стека
peek - возвращает верхний элемент стека, но не удаляет его. Стек не меняется.
size - возвращает количество элементов в стеке.
    """

    def isEmpty(self) -> bool:
        return len(self.some_list) == 0

    def push(self, element):
        self.some_list.append(element)

    def pop(self):
        if not self.isEmpty():
            return self.some_list.pop()

    def peek(self):
        if not self.isEmpty():
            return self.some_list[-1]

    def size(self):
        return len(self.some_list)



def check(symbolString):
    s = Stack()
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        if symbol == "(":
            s.push(symbol)
        elif symbol == "{":
            s.push(symbol)
        elif symbol == "[":
            s.push(symbol)
        elif s.peek() == "(" and symbol == ")":
            s.pop()
        elif s.peek() == "{" and symbol == "}":
            s.pop()
        elif s.peek() == "[" and symbol == "]":
            s.pop()
        else:
            balanced = False

        index += 1

    if balanced and s.isEmpty():
        return 'Сбалансированно'
    else:
        return 'Несбалансированно'


if __name__ == '__main__':
    print('Example:')
    print(check('(((({}[]))))'))
    
    assert check('(((([{}]))))') == 'Сбалансированно'
    assert check('[([])((([[[]]])))]{()}') == 'Сбалансированно'
    assert check('{{[()]}}') == 'Сбалансированно'
    assert check('}{}}{}') == 'Несбалансированно'
    assert check('{{[(])]}}') == 'Несбалансированно'
    assert check('[[{())}]') == 'Несбалансированно'
    print("Задание выполнено")
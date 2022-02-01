import time


def log_decorator(some_function):

    def logs(*args, **kwargs):
        now_time = time.localtime()
        old_result = some_function(*args, **kwargs)

        with open("logs.txt", encoding='utf8', mode='a') as file:

            file.write(
                f'{time.strftime("%d-%m-%Y, %H:%M:%S", now_time)} - {some_function.__name__} - {args} {kwargs} - {old_result}\n')

        return old_result
    return logs

@log_decorator
def my_test(name):
    print('Мой тест', name)
    return 'Finish', name


my_test('Ваня')

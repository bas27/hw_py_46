import time


def add_log_to_function(log_file):

    def log_decorator(some_function):
        def logs(*args, **kwargs):

            now_time = time.localtime()
            result = some_function(*args, **kwargs)

            with open(log_file, encoding='utf8', mode='a') as file:

                file.write(
                    f'{time.strftime("%d-%m-%Y, %H:%M:%S", now_time)} - {some_function.__name__} - {args} {kwargs} - {result}\n')

            return result
        return logs
    return log_decorator
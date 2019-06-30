import threading


class NewThread(threading.Thread):
    flag = True

    def __init__(self, func, args=()):
        super(NewThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(self.args)

    def stop(self):
        self.flag = False


if __name__ == '__main__':
    a = NewThread(None)

import time


class Clock:
    def now(self):
        return time.strftime("%I:%M:%S")


class Cuckoo(Clock):
    def alarm(self):
        t = super().now()
        hr = int(t.split(':')[0])
        print(f'{hr}點了…')
        print('咕！' * hr)

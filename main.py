import itchat
import tkinter as tk
import threading
import time
import random


def itchat_thread(app):
    @itchat.msg_register(itchat.content.TEXT)
    def print_content(msg):
        print(msg.text)
        app.add_msg(msg)

    itchat.auto_login()
    itchat.run()


class FlyingText():
    def __init__(self, id, time_left):
        self.id = id
        self.time_left = time_left

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # self.overrideredirect(True)
        self._width, self._height = self.maxsize()
        self.geometry('{w}x{h}+0+0'.format(w=self._width, h=self._height))
        self._time_left = 1000
        self._span = 0.01
        self._vx = self._width / self._time_left
        self.attributes('-transparentcolor', 'blue')
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.5)
        self._canvas = tk.Canvas(self, bg='blue')
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._texts = []
        threading.Thread(target=App._move_once, args=[self], daemon=True).start()

    def add_msg(self, msg):
        id = self._canvas.create_text(0, random.random() * self._height, text=msg.text, fill='black', font=('微软雅黑', 24))
        self._texts.append(FlyingText(id, self._time_left))

    def _move_once(self):
        while True:
            new_texts = []
            for i in self._texts:
                self._canvas.move(i.id, self._vx, 0)
                i.time_left -= 1
                if(i.time_left > 0):
                    new_texts.append(i)
                else:
                    self._canvas.delete(i.id)
            self._texts = new_texts
            time.sleep(self._span)


if __name__ == '__main__':
    app = App()
    threading.Thread(target=itchat_thread, args=[app], daemon=True).start()
    app.mainloop()


 

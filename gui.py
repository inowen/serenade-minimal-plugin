import tkinter as tk
import asyncio as async_io


class Window(tk.Tk):
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text='This is a testing label')

    # instead of running the main loop, just create a task that executes this
    async def asynchronous_update_loop(self):
        while True:
            self.root.update()
            await async_io.sleep(0.1)


if __name__ == '__main__':
    pass

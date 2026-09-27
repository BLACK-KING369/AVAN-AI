import tkinter as tk
import math
import random


class AvanOrb:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("AVAN")
        self.root.geometry("600x600")
        self.root.configure(bg="#05070d")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=600,
            height=600,
            bg="#05070d",
            highlightthickness=0
        )

        self.canvas.pack()

        self.center_x = 300
        self.center_y = 270

        self.angle = 0
        self.pulse = 0
        self.status = "IDLE"

        self.create_ui()

        self.animate()

    def create_ui(self):

        # Outer glow circles
        self.glow = []

        for radius in range(170, 70, -15):

            circle = self.canvas.create_oval(
                self.center_x - radius,
                self.center_y - radius,
                self.center_x + radius,
                self.center_y + radius,
                outline="#162447",
                width=2
            )

            self.glow.append(circle)

        # Main orb
        self.orb = self.canvas.create_oval(
            205,
            175,
            395,
            365,
            fill="#071426",
            outline="#35a7ff",
            width=3
        )

        # Inner core
        self.core = self.canvas.create_oval(
            250,
            220,
            350,
            320,
            fill="#0c4f7a",
            outline="#72d8ff",
            width=2
        )

        # Center
        self.center = self.canvas.create_oval(
            280,
            250,
            320,
            290,
            fill="#b8f3ff",
            outline=""
        )

        # AVAN text
        self.canvas.create_text(
            300,
            410,
            text="A V A N",
            fill="#8edfff",
            font=("Segoe UI", 22, "bold")
        )

        self.status_text = self.canvas.create_text(
            300,
            450,
            text="IDLE",
            fill="#7188a8",
            font=("Segoe UI", 11)
        )

    def set_status(self, status):

        self.status = status.upper()

        self.status_text.config(
            text=self.status
        )

    def animate(self):

        self.angle += 0.05
        self.pulse += 0.08

        # Breathing effect
        size = 90 + math.sin(self.pulse) * 8

        self.canvas.coords(
            self.orb,
            self.center_x - size,
            self.center_y - size,
            self.center_x + size,
            self.center_y + size
        )

        # Rotating inner core effect
        core_size = 50 + math.sin(
            self.pulse * 1.5
        ) * 8

        self.canvas.coords(
            self.core,
            self.center_x - core_size,
            self.center_y - core_size,
            self.center_x + core_size,
            self.center_y + core_size
        )

        # Center pulse
        center_size = 20 + math.sin(
            self.pulse * 2
        ) * 5

        self.canvas.coords(
            self.center,
            self.center_x - center_size,
            self.center_y - center_size,
            self.center_x + center_size,
            self.center_y + center_size
        )

        # Rotating wave points
        for i, circle in enumerate(self.glow):

            offset = math.sin(
                self.angle + i * 0.5
            ) * 5

            radius = 170 - i * 15 + offset

            self.canvas.coords(
                circle,
                self.center_x - radius,
                self.center_y - radius,
                self.center_x + radius,
                self.center_y + radius
            )

        self.root.after(
            30,
            self.animate
        )

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    avan = AvanOrb()
    avan.run()
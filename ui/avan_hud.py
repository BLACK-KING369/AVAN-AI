import sys
import os
import math
import random
import socket
import threading

# =========================================================
# PATH SETUP
# =========================================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# =========================================================
# PYSIDE6
# =========================================================

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPointF,
    QRectF
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
    QRadialGradient,
    QPainterPath
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget
)


# =========================================================
# AVAN UI BRIDGE
# =========================================================

from avan_ui_bridge import ui_bridge


# =========================================================
# AUDIO UDP
# =========================================================

AUDIO_HOST = "127.0.0.1"
AUDIO_PORT = 5055


# =========================================================
# AVAN HUD
# =========================================================

class AvanHUD(QWidget):

    def __init__(self):

        super().__init__()

        # -------------------------------------------------
        # WINDOW
        # -------------------------------------------------

        self.setWindowTitle("AVAN AI")

        self.setMinimumSize(
            1200,
            700
        )

        self.resize(
            1400,
            800
        )

        self.setStyleSheet(
            """
            QWidget {
                background: #02050b;
            }
            """
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.status = "IDLE"

        self.last_command = "None"

        # -------------------------------------------------
        # ANIMATION
        # -------------------------------------------------

        self.rotation = 0.0
        self.rotation_2 = 0.0

        self.pulse = 0.0
        self.wave_phase = 0.0

        self.orb_breath = 0.0

        # Smooth audio level
        self.audio_level = 0.0
        self.smoothed_audio = 0.0

        # Listening pulse
        self.listening_pulse = 0.0

        # Thinking orbit
        self.thinking_angle = 0.0

        # -------------------------------------------------
        # PARTICLES
        # -------------------------------------------------

        self.particles = []

        self.create_particles()

        # -------------------------------------------------
        # AUDIO UDP SOCKET
        # -------------------------------------------------

        self.audio_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        self.audio_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        try:

            self.audio_socket.bind(
                (
                    AUDIO_HOST,
                    AUDIO_PORT
                )
            )

            print(
                f"🎤 Audio receiver listening on "
                f"{AUDIO_HOST}:{AUDIO_PORT}"
            )

        except OSError as e:

            print(
                f"❌ Audio UDP bind error: {e}"
            )

        self.audio_socket.settimeout(
            0.2
        )

        # -------------------------------------------------
        # AUDIO THREAD
        # -------------------------------------------------

        self.audio_thread = threading.Thread(
            target=self.receive_audio_level,
            daemon=True
        )

        self.audio_thread.start()

        # -------------------------------------------------
        # UI BRIDGE
        # -------------------------------------------------

        try:

            ui_bridge.status_changed.connect(
                self.set_status
            )

        except Exception as e:

            print(
                "⚠️ UI bridge connection error:",
                e
            )

        # -------------------------------------------------
        # ANIMATION TIMER
        # -------------------------------------------------

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(
            16
        )

    # =====================================================
    # CREATE PARTICLES
    # =====================================================

    def create_particles(self):

        self.particles.clear()

        # Main orb particles
        for _ in range(520):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            # More particles toward center,
            # fewer particles at extreme edge
            radius = random.random() ** 0.62

            self.particles.append(
                {
                    "angle": angle,

                    "radius": radius,

                    "speed": random.uniform(
                        0.15,
                        0.75
                    ),

                    "size": random.uniform(
                        0.7,
                        2.8
                    ),

                    "alpha": random.uniform(
                        80,
                        230
                    ),

                    "phase": random.uniform(
                        0,
                        math.pi * 2
                    ),

                    "drift": random.uniform(
                        -1,
                        1
                    ),

                    "layer": random.randint(
                        0,
                        2
                    )
                }
            )

        # Extra tiny particles
        for _ in range(180):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            radius = random.uniform(
                0.72,
                1.15
            )

            self.particles.append(
                {
                    "angle": angle,

                    "radius": radius,

                    "speed": random.uniform(
                        0.2,
                        1.0
                    ),

                    "size": random.uniform(
                        0.4,
                        1.7
                    ),

                    "alpha": random.uniform(
                        50,
                        180
                    ),

                    "phase": random.uniform(
                        0,
                        math.pi * 2
                    ),

                    "drift": random.uniform(
                        -1,
                        1
                    ),

                    "layer": random.randint(
                        0,
                        2
                    )
                }
            )

    # =====================================================
    # RECEIVE AUDIO LEVEL
    # =====================================================

    def receive_audio_level(self):

        while True:

            try:

                data, _ = self.audio_socket.recvfrom(
                    1024
                )

                level = float(
                    data.decode(
                        "utf-8"
                    )
                )

                self.audio_level = max(
                    0.0,
                    min(
                        1.0,
                        level
                    )
                )

            except socket.timeout:

                continue

            except Exception:

                continue

    # =====================================================
    # ANIMATION
    # =====================================================

    def animate(self):

        # -------------------------------------------------
        # GENERAL ROTATION
        # -------------------------------------------------

        self.rotation += 0.55

        self.rotation_2 -= 0.32

        self.pulse += 0.075

        self.wave_phase += 0.18

        self.orb_breath += 0.045

        # -------------------------------------------------
        # THINKING
        # -------------------------------------------------

        if self.status == "THINKING":

            self.thinking_angle += 2.5

        else:

            self.thinking_angle += 0.7

        # -------------------------------------------------
        # LISTENING
        # -------------------------------------------------

        if self.status == "LISTENING":

            self.listening_pulse += 0.08

        else:

            self.listening_pulse += 0.025

        # -------------------------------------------------
        # SMOOTH AUDIO
        # -------------------------------------------------

        self.smoothed_audio += (
            self.audio_level
            -
            self.smoothed_audio
        ) * 0.25

        # -------------------------------------------------
        # REFRESH
        # -------------------------------------------------

        self.update()

    # =====================================================
    # SET STATUS
    # =====================================================

    def set_status(
        self,
        status
    ):

        self.status = str(
            status
        ).upper()

        self.update()

    # =====================================================
    # PAINT EVENT
    # =====================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        width = self.width()
        height = self.height()

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        painter.fillRect(
            0,
            0,
            width,
            height,
            QColor("#02050b")
        )

        # -------------------------------------------------
        # BACKGROUND EFFECT
        # -------------------------------------------------

        self.draw_background(
            painter,
            width,
            height
        )

        # -------------------------------------------------
        # FLOATING BACKGROUND PARTICLES
        # -------------------------------------------------

        self.draw_background_particles(
            painter,
            width,
            height
        )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.draw_header(
            painter,
            width
        )

        # -------------------------------------------------
        # LEFT PANEL
        # -------------------------------------------------

        self.draw_left_panel(
            painter
        )

        # -------------------------------------------------
        # RIGHT PANEL
        # -------------------------------------------------

        self.draw_right_panel(
            painter,
            width
        )

        # -------------------------------------------------
        # MAIN ENERGY CORE
        # -------------------------------------------------

        self.draw_core(
            painter,
            width,
            height
        )

        # -------------------------------------------------
        # BOTTOM BAR
        # -------------------------------------------------

        self.draw_bottom_bar(
            painter,
            width,
            height
        )

    # =====================================================
    # BACKGROUND
    # =====================================================

    def draw_background(
        self,
        painter,
        width,
        height
    ):

        # Main subtle radial glow

        gradient = QRadialGradient(
            width * 0.5,
            height * 0.48,
            min(
                width,
                height
            ) * 0.52
        )

        gradient.setColorAt(
            0.0,
            QColor(
                8,
                35,
                60,
                180
            )
        )

        gradient.setColorAt(
            0.35,
            QColor(
                3,
                18,
                35,
                100
            )
        )

        gradient.setColorAt(
            0.72,
            QColor(
                2,
                7,
                15,
                60
            )
        )

        gradient.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(
            gradient
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawRect(
            0,
            0,
            width,
            height
        )

        # -------------------------------------------------
        # FUTURISTIC GRID
        # -------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    20,
                    100,
                    150,
                    18
                ),
                1
            )
        )

        grid_size = 50

        for x in range(
            0,
            width,
            grid_size
        ):

            painter.drawLine(
                x,
                0,
                x,
                height
            )

        for y in range(
            0,
            height,
            grid_size
        ):

            painter.drawLine(
                0,
                y,
                width,
                y
            )

    # =====================================================
    # BACKGROUND PARTICLES
    # =====================================================

    def draw_background_particles(
        self,
        painter,
        width,
        height
    ):

        painter.setPen(
            Qt.NoPen
        )

        for i in range(70):

            x = (
                (i * 173)
                %
                max(width, 1)
            )

            y = (
                (i * 97)
                %
                max(height, 1)
            )

            twinkle = (
                math.sin(
                    self.pulse * 0.8
                    +
                    i
                )
                +
                1
            ) * 0.5

            alpha = int(
                25
                +
                twinkle * 60
            )

            size = (
                0.5
                +
                (i % 3) * 0.45
            )

            painter.setBrush(
                QColor(
                    100,
                    190,
                    255,
                    alpha
                )
            )

            painter.drawEllipse(
                QPointF(
                    x,
                    y
                ),
                size,
                size
            )

    # =====================================================
    # HEADER
    # =====================================================

    def draw_header(
        self,
        painter,
        width
    ):

        # AVAN AI

        painter.setPen(
            QColor(
                70,
                210,
                255
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        painter.drawText(
            35,
            45,
            "AVAN AI"
        )

        # Subtitle

        painter.setFont(
            QFont(
                "Segoe UI",
                10
            )
        )

        painter.setPen(
            QColor(
                110,
                160,
                190
            )
        )

        painter.drawText(
            38,
            65,
            "PERSONAL INTELLIGENT ASSISTANT"
        )

        # -------------------------------------------------
        # STATUS COLOR
        # -------------------------------------------------

        status_color = self.get_status_color()

        painter.setBrush(
            status_color
        )

        painter.setPen(
            Qt.NoPen
        )

        # Status dot

        painter.drawEllipse(
            QPointF(
                width - 175,
                32
            ),
            5,
            5
        )

        # Status text

        painter.setPen(
            status_color
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                11,
                QFont.Bold
            )
        )

        painter.drawText(
            width - 155,
            38,
            self.status
        )

    # =====================================================
    # STATUS COLOR
    # =====================================================

    def get_status_color(self):

        if self.status == "LISTENING":

            return QColor(
                80,
                230,
                255
            )

        if self.status == "THINKING":

            return QColor(
                170,
                100,
                255
            )

        if self.status == "SPEAKING":

            return QColor(
                60,
                220,
                255
            )

        if self.status == "ERROR":

            return QColor(
                255,
                70,
                90
            )

        return QColor(
            0,
            230,
            150
        )

    # =====================================================
    # LEFT PANEL
    # =====================================================

    def draw_left_panel(
        self,
        painter
    ):

        self.draw_panel(
            painter,
            30,
            100,
            250,
            230
        )

        painter.setPen(
            QColor(
                100,
                190,
                230
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Bold
            )
        )

        painter.drawText(
            50,
            135,
            "SYSTEM STATUS"
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10
            )
        )

        painter.setPen(
            QColor(
                150,
                180,
                200
            )
        )

        lines = [

            "AI CORE        ONLINE",

            "VOICE          READY",

            "MIC            ACTIVE",

            "VISION         READY",

            "MEMORY         ONLINE",

            "NETWORK        READY"

        ]

        y = 165

        for line in lines:

            painter.drawText(
                50,
                y,
                line
            )

            y += 25

    # =====================================================
    # RIGHT PANEL
    # =====================================================

    def draw_right_panel(
        self,
        painter,
        width
    ):

        panel_x = width - 280

        self.draw_panel(
            painter,
            panel_x,
            100,
            250,
            230
        )

        painter.setPen(
            QColor(
                100,
                190,
                230
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Bold
            )
        )

        painter.drawText(
            panel_x + 20,
            135,
            "AVAN ACTIVITY"
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10
            )
        )

        painter.setPen(
            QColor(
                150,
                180,
                200
            )
        )

        painter.drawText(
            panel_x + 20,
            170,
            "STATUS"
        )

        painter.setPen(
            self.get_status_color()
        )

        painter.drawText(
            panel_x + 100,
            170,
            self.status
        )

        # -------------------------------------------------
        # VOICE LEVEL
        # -------------------------------------------------

        painter.setPen(
            QColor(
                150,
                180,
                200
            )
        )

        painter.drawText(
            panel_x + 20,
            200,
            "VOICE LEVEL"
        )

        painter.setBrush(
            QColor(
                10,
                25,
                40
            )
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawRoundedRect(
            QRectF(
                panel_x + 20,
                215,
                205,
                12
            ),
            6,
            6
        )

        painter.setBrush(
            QColor(
                40,
                190,
                255
            )
        )

        painter.drawRoundedRect(
            QRectF(
                panel_x + 20,
                215,
                205 * self.smoothed_audio,
                12
            ),
            6,
            6
        )

        # -------------------------------------------------
        # COMMAND
        # -------------------------------------------------

        painter.setPen(
            QColor(
                150,
                180,
                200
            )
        )

        painter.drawText(
            panel_x + 20,
            265,
            "COMMAND"
        )

        painter.setPen(
            QColor(
                100,
                200,
                240
            )
        )

        painter.drawText(
            panel_x + 20,
            285,
            self.last_command
        )

    # =====================================================
    # MAIN ENERGY CORE
    # =====================================================

    def draw_core(
        self,
        painter,
        width,
        height
    ):

        cx = width / 2
        cy = height / 2 + 20

        # -------------------------------------------------
        # CORE SIZE
        # -------------------------------------------------

        base_radius = 185

        breathing = (
            math.sin(
                self.orb_breath
            )
            * 5
        )

        audio_expand = (
            self.smoothed_audio
            *
            55
        )

        if self.status == "SPEAKING":

            core_radius = (
                base_radius
                +
                breathing
                +
                audio_expand
            )

        elif self.status == "LISTENING":

            core_radius = (
                base_radius
                +
                breathing
                +
                math.sin(
                    self.listening_pulse
                ) * 10
            )

        elif self.status == "THINKING":

            core_radius = (
                base_radius
                +
                breathing
                +
                4
            )

        else:

            core_radius = (
                base_radius
                +
                breathing
            )

        # -------------------------------------------------
        # LARGE SOFT ENERGY GLOW
        # -------------------------------------------------

        glow_radius = (
            core_radius
            +
            80
        )

        gradient = QRadialGradient(
            cx,
            cy,
            glow_radius
        )

        if self.status == "THINKING":

            gradient.setColorAt(
                0.0,
                QColor(
                    150,
                    70,
                    255,
                    60
                )
            )

            gradient.setColorAt(
                0.5,
                QColor(
                    80,
                    40,
                    180,
                    22
                )
            )

        else:

            gradient.setColorAt(
                0.0,
                QColor(
                    30,
                    180,
                    255,
                    55
                )
            )

            gradient.setColorAt(
                0.5,
                QColor(
                    20,
                    100,
                    180,
                    20
                )
            )

        gradient.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0
            )
        )

        painter.setBrush(
            gradient
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawEllipse(
            QPointF(
                cx,
                cy
            ),
            glow_radius,
            glow_radius
        )

        # -------------------------------------------------
        # ENERGY RINGS
        # -------------------------------------------------

        self.draw_energy_rings(
            painter,
            cx,
            cy,
            core_radius
        )

        # -------------------------------------------------
        # PARTICLE ORB
        # -------------------------------------------------

        self.draw_particle_orb(
            painter,
            cx,
            cy,
            core_radius
        )

        # -------------------------------------------------
        # LISTENING RAYS
        # -------------------------------------------------

        if self.status == "LISTENING":

            self.draw_listening_rays(
                painter,
                cx,
                cy,
                core_radius
            )

        # -------------------------------------------------
        # THINKING ORBITS
        # -------------------------------------------------

        if self.status == "THINKING":

            self.draw_thinking_orbits(
                painter,
                cx,
                cy,
                core_radius
            )

        # -------------------------------------------------
        # SPEAKING RAYS
        # -------------------------------------------------

        if self.status == "SPEAKING":

            self.draw_speaking_rays(
                painter,
                cx,
                cy,
                core_radius
            )

        # -------------------------------------------------
        # AUDIO WAVE
        # -------------------------------------------------

        self.draw_wave(
            painter,
            cx,
            cy + core_radius + 45
        )

    # =====================================================
    # PARTICLE ORB
    # =====================================================

    def draw_particle_orb(
        self,
        painter,
        cx,
        cy,
        core_radius
    ):

        painter.setPen(
            Qt.NoPen
        )

        # -------------------------------------------------
        # STATUS TINT
        # -------------------------------------------------

        if self.status == "THINKING":

            base_color = (
                165,
                95,
                255
            )

        elif self.status == "LISTENING":

            base_color = (
                80,
                225,
                255
            )

        elif self.status == "SPEAKING":

            base_color = (
                55,
                210,
                255
            )

        else:

            base_color = (
                100,
                190,
                255
            )

        # -------------------------------------------------
        # DRAW PARTICLES
        # -------------------------------------------------

        for index, particle in enumerate(
            self.particles
        ):

            angle = (
                particle["angle"]
                +
                self.rotation
                *
                0.004
                *
                particle["speed"]
            )

            # Normalized radius
            normalized_radius = particle[
                "radius"
            ]

            # Convert to actual radius
            radius = (
                normalized_radius
                *
                core_radius
            )

            # Organic movement
            movement = math.sin(
                self.pulse
                *
                particle["speed"]
                +
                particle["phase"]
            )

            movement_2 = math.cos(
                self.pulse
                *
                0.7
                +
                particle["phase"]
            )

            radius += (
                movement
                *
                4
            )

            # Audio reaction
            if self.status == "SPEAKING":

                radius += (
                    self.smoothed_audio
                    *
                    35
                    *
                    math.sin(
                        particle["phase"]
                    )
                )

            # Thinking reaction
            if self.status == "THINKING":

                angle += (
                    math.sin(
                        self.thinking_angle
                        *
                        0.03
                        +
                        particle["phase"]
                    )
                    *
                    0.05
                )

            # Organic x/y distortion
            x = (
                cx
                +
                math.cos(angle)
                *
                radius
            )

            y = (
                cy
                +
                math.sin(angle)
                *
                radius
            )

            x += (
                math.sin(
                    self.pulse
                    +
                    particle["phase"]
                )
                *
                3
            )

            y += (
                math.cos(
                    self.pulse * 0.8
                    +
                    particle["phase"]
                )
                *
                3
            )

            # -------------------------------------------------
            # PARTICLE SIZE
            # -------------------------------------------------

            size = particle["size"]

            if self.status == "SPEAKING":

                size += (
                    self.smoothed_audio
                    *
                    1.8
                )

            # -------------------------------------------------
            # TWINKLE
            # -------------------------------------------------

            twinkle = (
                math.sin(
                    self.pulse * 2
                    +
                    particle["phase"]
                )
                +
                1
            ) * 0.5

            alpha = int(
                particle["alpha"]
                *
                (
                    0.55
                    +
                    twinkle * 0.45
                )
            )

            # -------------------------------------------------
            # COLOR VARIATION
            # -------------------------------------------------

            color_shift = (
                index % 9
            )

            if color_shift == 0:

                color = QColor(
                    230,
                    245,
                    255,
                    alpha
                )

            elif color_shift == 1:

                color = QColor(
                    150,
                    220,
                    255,
                    alpha
                )

            elif color_shift == 2:

                color = QColor(
                    190,
                    160,
                    255,
                    alpha
                )

            else:

                color = QColor(
                    base_color[0],
                    base_color[1],
                    base_color[2],
                    alpha
                )

            painter.setBrush(
                color
            )

            painter.drawEllipse(
                QPointF(
                    x,
                    y
                ),
                size,
                size
            )

    # =====================================================
    # ENERGY RINGS
    # =====================================================

    def draw_energy_rings(
        self,
        painter,
        cx,
        cy,
        core_radius
    ):

        painter.save()

        painter.translate(
            cx,
            cy
        )

        # -------------------------------------------------
        # RING 1
        # -------------------------------------------------

        painter.rotate(
            self.rotation
        )

        painter.setBrush(
            Qt.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    50,
                    190,
                    255,
                    80
                ),
                1.5
            )
        )

        painter.drawEllipse(
            QRectF(
                -core_radius - 15,
                -core_radius - 15,
                (core_radius + 15) * 2,
                (core_radius + 15) * 2
            )
        )

        # -------------------------------------------------
        # RING 2
        # -------------------------------------------------

        painter.rotate(
            self.rotation_2
        )

        painter.setPen(
            QPen(
                QColor(
                    170,
                    220,
                    255,
                    45
                ),
                1
            )
        )

        painter.drawEllipse(
            QRectF(
                -core_radius - 32,
                -core_radius - 32,
                (core_radius + 32) * 2,
                (core_radius + 32) * 2
            )
        )

        # -------------------------------------------------
        # RING 3 - DASHED
        # -------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    80,
                    210,
                    255,
                    70
                ),
                2,
                Qt.DashLine
            )
        )

        painter.drawEllipse(
            QRectF(
                -core_radius - 50,
                -core_radius - 50,
                (core_radius + 50) * 2,
                (core_radius + 50) * 2
            )
        )

        painter.restore()

    # =====================================================
    # LISTENING RAYS
    # =====================================================

    def draw_listening_rays(
        self,
        painter,
        cx,
        cy,
        core_radius
    ):

        painter.save()

        painter.setPen(
            QPen(
                QColor(
                    70,
                    220,
                    255,
                    130
                ),
                2
            )
        )

        ray_count = 32

        pulse_value = (
            math.sin(
                self.listening_pulse
            )
            +
            1
        ) * 0.5

        for i in range(
            ray_count
        ):

            angle = (
                i
                /
                ray_count
                *
                math.pi
                *
                2
            )

            # Slightly irregular rays
            irregular = math.sin(
                self.pulse * 1.5
                +
                i
            ) * 8

            start_radius = (
                core_radius
                +
                8
            )

            end_radius = (
                core_radius
                +
                20
                +
                pulse_value * 28
                +
                irregular
            )

            x1 = (
                cx
                +
                math.cos(angle)
                *
                start_radius
            )

            y1 = (
                cy
                +
                math.sin(angle)
                *
                start_radius
            )

            x2 = (
                cx
                +
                math.cos(angle)
                *
                end_radius
            )

            y2 = (
                cy
                +
                math.sin(angle)
                *
                end_radius
            )

            painter.drawLine(
                QPointF(
                    x1,
                    y1
                ),
                QPointF(
                    x2,
                    y2
                )
            )

        painter.restore()

    # =====================================================
    # THINKING ORBITS
    # =====================================================

    def draw_thinking_orbits(
        self,
        painter,
        cx,
        cy,
        core_radius
    ):

        painter.save()

        painter.translate(
            cx,
            cy
        )

        # -------------------------------------------------
        # ORBIT 1
        # -------------------------------------------------

        painter.rotate(
            self.thinking_angle
        )

        painter.setBrush(
            Qt.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    180,
                    100,
                    255,
                    120
                ),
                2
            )
        )

        painter.drawEllipse(
            QRectF(
                -core_radius - 35,
                -core_radius * 0.55,
                (core_radius + 35) * 2,
                core_radius * 1.1
            )
        )

        # -------------------------------------------------
        # ORBIT 2
        # -------------------------------------------------

        painter.rotate(
            70
        )

        painter.setPen(
            QPen(
                QColor(
                    100,
                    180,
                    255,
                    90
                ),
                1.5
            )
        )

        painter.drawEllipse(
            QRectF(
                -core_radius - 20,
                -core_radius * 0.65,
                (core_radius + 20) * 2,
                core_radius * 1.3
            )
        )

        painter.restore()

        # -------------------------------------------------
        # ORBIT NODES
        # -------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        for i in range(6):

            angle = (
                self.thinking_angle
                *
                0.03
                +
                i
                *
                math.pi
                /
                3
            )

            radius = (
                core_radius
                +
                35
            )

            x = (
                cx
                +
                math.cos(angle)
                *
                radius
            )

            y = (
                cy
                +
                math.sin(angle)
                *
                radius
                *
                0.55
            )

            painter.setBrush(
                QColor(
                    190,
                    120,
                    255,
                    190
                )
            )

            painter.drawEllipse(
                QPointF(
                    x,
                    y
                ),
                3,
                3
            )

    # =====================================================
    # SPEAKING RAYS
    # =====================================================

    def draw_speaking_rays(
        self,
        painter,
        cx,
        cy,
        core_radius
    ):

        level = self.smoothed_audio

        if level < 0.015:

            return

        painter.save()

        painter.setPen(
            QPen(
                QColor(
                    70,
                    220,
                    255,
                    int(
                        60
                        +
                        level * 140
                    )
                ),
                2
            )
        )

        ray_count = 44

        for i in range(
            ray_count
        ):

            angle = (
                i
                /
                ray_count
                *
                math.pi
                *
                2
            )

            wave = math.sin(
                self.wave_phase * 2
                +
                i * 1.7
            )

            start_radius = (
                core_radius
                +
                5
            )

            length = (
                8
                +
                level * 80
                +
                wave * 10
            )

            end_radius = (
                start_radius
                +
                max(
                    2,
                    length
                )
            )

            x1 = (
                cx
                +
                math.cos(angle)
                *
                start_radius
            )

            y1 = (
                cy
                +
                math.sin(angle)
                *
                start_radius
            )

            x2 = (
                cx
                +
                math.cos(angle)
                *
                end_radius
            )

            y2 = (
                cy
                +
                math.sin(angle)
                *
                end_radius
            )

            painter.drawLine(
                QPointF(
                    x1,
                    y1
                ),
                QPointF(
                    x2,
                    y2
                )
            )

        painter.restore()

    # =====================================================
    # BOTTOM BAR
    # =====================================================

    def draw_bottom_bar(
        self,
        painter,
        width,
        height
    ):

        bar_y = (
            height
            -
            70
        )

        painter.setPen(
            QPen(
                QColor(
                    30,
                    120,
                    170,
                    100
                ),
                1
            )
        )

        painter.drawLine(
            30,
            bar_y,
            width - 30,
            bar_y
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10
            )
        )

        painter.setPen(
            QColor(
                100,
                150,
                175
            )
        )

        painter.drawText(
            35,
            height - 35,
            "AVAN AI • PERSONAL ASSISTANT"
        )

        painter.drawText(
            width - 230,
            height - 35,
            "VOICE SYSTEM • ONLINE"
        )

    # =====================================================
    # PANEL
    # =====================================================

    def draw_panel(
        self,
        painter,
        x,
        y,
        width,
        height
    ):

        painter.setBrush(
            QColor(
                3,
                12,
                22,
                220
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    25,
                    120,
                    170,
                    110
                ),
                1
            )
        )

        painter.drawRoundedRect(
            QRectF(
                x,
                y,
                width,
                height
            ),
            12,
            12
        )

        # Top highlight

        painter.setPen(
            QPen(
                QColor(
                    40,
                    190,
                    255,
                    120
                ),
                2
            )
        )

        painter.drawLine(
            x + 15,
            y,
            x + width - 15,
            y
        )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = AvanHUD()

    window.show()

    sys.exit(
        app.exec()
    )
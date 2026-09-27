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
# PYQT / PYSIDE
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
    QBrush,
    QFont,
    QRadialGradient,
    QPixmap,
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
# FILES
# =========================================================

FACE_PATH = os.path.join(
    ROOT_DIR,
    "assets",
    "avan_face.png"
)


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
        # ANIMATION VARIABLES
        # -------------------------------------------------

        self.rotation = 0.0

        self.pulse = 0.0

        self.wave_phase = 0.0

        self.mouth_open = 0.0

        self.voice_level = 0.0

        self.audio_level = 0.0

        self.face_breath = 0.0


        # -------------------------------------------------
        # BLINK
        # -------------------------------------------------

        self.eye_blink = 0

        # Approximately 1.9 - 2.4 seconds
        # at ~60 FPS

        self.blink_timer = random.randint(
            115,
            145
        )


        # -------------------------------------------------
        # FACE
        # -------------------------------------------------

        self.face_pixmap = QPixmap()


        if os.path.exists(FACE_PATH):

            self.face_pixmap.load(
                FACE_PATH
            )

            if self.face_pixmap.isNull():

                print(
                    "❌ Face file exists but could not be loaded:"
                )

                print(
                    FACE_PATH
                )

            else:

                print(
                    "✅ Avan realistic face loaded:"
                )

                print(
                    FACE_PATH
                )

                print(
                    "Face size:",
                    self.face_pixmap.width(),
                    "x",
                    self.face_pixmap.height()
                )

        else:

            print(
                "❌ Realistic face not found:"
            )

            print(
                FACE_PATH
            )


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
        # PARTICLES
        # -------------------------------------------------

        self.particles = []


        for _ in range(180):

            self.particles.append(
                {
                    "x": random.uniform(
                        0,
                        1
                    ),

                    "y": random.uniform(
                        0,
                        1
                    ),

                    "speed": random.uniform(
                        0.1,
                        0.6
                    ),

                    "size": random.uniform(
                        1,
                        3
                    )
                }
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

        # ---------------------------------------------
        # General animation
        # ---------------------------------------------

        self.rotation += 0.7

        self.pulse += 0.08

        self.wave_phase += 0.15

        self.face_breath += 0.04


        # ---------------------------------------------
        # Blink timer
        # ---------------------------------------------

        self.blink_timer -= 1


        if self.blink_timer <= 0:

            self.eye_blink = 1

            # Blink duration
            QTimer.singleShot(
                120,
                self.open_eyes
            )

            # Next blink
            self.blink_timer = random.randint(
                115,
                145
            )


        # ---------------------------------------------
        # Mouth
        # ---------------------------------------------

        if self.status == "SPEAKING":

            self.voice_level = self.audio_level

            self.mouth_open += (
                self.voice_level
                -
                self.mouth_open
            ) * 0.45

        else:

            self.voice_level = 0.0

            self.mouth_open += (
                0.0
                -
                self.mouth_open
            ) * 0.30


        # ---------------------------------------------
        # Refresh
        # ---------------------------------------------

        self.update()


    # =====================================================
    # OPEN EYES
    # =====================================================

    def open_eyes(self):

        self.eye_blink = 0


    # =====================================================
    # SET STATUS
    # =====================================================

    def set_status(
        self,
        status
    ):

        self.status = status.upper()

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

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform
        )


        width = self.width()

        height = self.height()


        # Background

        painter.fillRect(
            0,
            0,
            width,
            height,
            QColor("#02050b")
        )


        # Background

        self.draw_background(
            painter,
            width,
            height
        )


        # Particles

        self.draw_particles(
            painter,
            width,
            height
        )


        # Header

        self.draw_header(
            painter,
            width
        )


        # Left panel

        self.draw_left_panel(
            painter
        )


        # Right panel

        self.draw_right_panel(
            painter,
            width
        )


        # Main core

        self.draw_core(
            painter,
            width,
            height
        )


        # Bottom bar

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

        # Radial glow

        gradient = QRadialGradient(
            width * 0.5,
            height * 0.48,
            min(width, height) * 0.45
        )

        gradient.setColorAt(
            0.0,
            QColor(
                5,
                30,
                55,
                180
            )
        )

        gradient.setColorAt(
            0.5,
            QColor(
                2,
                12,
                25,
                100
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


        # Grid

        painter.setPen(
            QPen(
                QColor(
                    20,
                    100,
                    150,
                    25
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
    # PARTICLES
    # =====================================================

    def draw_particles(
        self,
        painter,
        width,
        height
    ):

        painter.setPen(
            Qt.NoPen
        )


        for particle in self.particles:

            x = particle["x"] * width

            y = particle["y"] * height

            size = particle["size"]


            alpha = random.randint(
                40,
                130
            )


            painter.setBrush(
                QColor(
                    30,
                    170,
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

        painter.setPen(
            QColor(
                50,
                200,
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


        # Status

        status_color = QColor(
            0,
            230,
            150
        )


        if self.status == "SPEAKING":

            status_color = QColor(
                50,
                200,
                255
            )

        elif self.status == "ERROR":

            status_color = QColor(
                255,
                70,
                90
            )


        painter.setBrush(
            status_color
        )

        painter.setPen(
            Qt.NoPen
        )


        painter.drawEllipse(
            QPointF(
                width - 175,
                32
            ),
            5,
            5
        )


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
            QColor(
                40,
                210,
                255
            )
        )


        painter.drawText(
            panel_x + 100,
            170,
            self.status
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
            200,
            "VOICE LEVEL"
        )


        # Voice level bar

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
                205 * self.audio_level,
                12
            ),
            6,
            6
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
    # MAIN CORE
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
        # Outer rotating ring
        # -------------------------------------------------

        painter.save()


        painter.translate(
            cx,
            cy
        )


        painter.rotate(
            self.rotation
        )


        painter.setBrush(
            Qt.NoBrush
        )


        painter.setPen(
            QPen(
                QColor(
                    20,
                    160,
                    240,
                    100
                ),
                2
            )
        )


        painter.drawEllipse(
            QRectF(
                -230,
                -230,
                460,
                460
            )
        )


        painter.setPen(
            QPen(
                QColor(
                    40,
                    210,
                    255,
                    150
                ),
                3
            )
        )


        painter.drawArc(
            QRectF(
                -250,
                -250,
                500,
                500
            ),
            20 * 16,
            110 * 16
        )


        painter.drawArc(
            QRectF(
                -250,
                -250,
                500,
                500
            ),
            200 * 16,
            100 * 16
        )


        painter.restore()


        # -------------------------------------------------
        # Core glow
        # -------------------------------------------------

        glow_radius = (
            225
            +
            math.sin(
                self.pulse
            ) * 5
        )


        gradient = QRadialGradient(
            cx,
            cy,
            glow_radius
        )


        gradient.setColorAt(
            0.0,
            QColor(
                20,
                150,
                255,
                30
            )
        )


        gradient.setColorAt(
            0.65,
            QColor(
                10,
                80,
                160,
                15
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
        # Face
        # -------------------------------------------------

        self.draw_realistic_face(
            painter,
            cx,
            cy
        )


        # -------------------------------------------------
        # Audio wave
        # -------------------------------------------------

        self.draw_wave(
            painter,
            cx,
            cy + 235
        )


    # =====================================================
    # REALISTIC FACE
    # =====================================================

    def draw_realistic_face(
        self,
        painter,
        cx,
        cy
    ):

        if self.face_pixmap.isNull():

            painter.setPen(
                QColor(
                    40,
                    200,
                    255
                )
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    18,
                    QFont.Bold
                )
            )

            painter.drawText(
                int(cx - 100),
                int(cy),
                "AVAN"
            )

            return


        # -------------------------------------------------
        # Face size
        # -------------------------------------------------

        face_size = 430


        # -------------------------------------------------
        # Scale image
        # -------------------------------------------------

        pixmap = self.face_pixmap.scaled(
            face_size,
            face_size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )


        face_x = int(
            cx - face_size / 2
        )

        face_y = int(
            cy - face_size / 2
        )


        # -------------------------------------------------
        # Circular clipping
        # -------------------------------------------------

        painter.save()


        circle_path = QPainterPath()


        circle_path.addEllipse(
            QRectF(
                face_x,
                face_y,
                face_size,
                face_size
            )
        )


        painter.setClipPath(
            circle_path
        )


        painter.drawPixmap(
            face_x,
            face_y,
            pixmap
        )


        painter.restore()


        # -------------------------------------------------
        # Outer face border
        # -------------------------------------------------

        painter.setBrush(
            Qt.NoBrush
        )


        painter.setPen(
            QPen(
                QColor(
                    20,
                    170,
                    255,
                    210
                ),
                3
            )
        )


        painter.drawEllipse(
            face_x,
            face_y,
            face_size,
            face_size
        )


        # -------------------------------------------------
        # Blink
        # -------------------------------------------------

        if self.eye_blink:

            self.draw_blink(
                painter,
                face_x,
                face_y,
                face_size
            )


        # -------------------------------------------------
        # Mouth
        # -------------------------------------------------

        self.draw_mouth_animation(
            painter,
            face_x,
            face_y,
            face_size
        )


    # =====================================================
    # BLINK
    # =====================================================

    def draw_blink(
        self,
        painter,
        face_x,
        face_y,
        face_size
    ):

        # -------------------------------------------------
        # ACTUAL EYE POSITIONS FOR THE UPLOADED FACE
        # -------------------------------------------------

        left_eye_x = (
            face_x
            +
            face_size * 0.405
        )


        right_eye_x = (
            face_x
            +
            face_size * 0.680
        )


        eye_y = (
            face_y
            +
            face_size * 0.375
        )


        eye_width = (
            face_size * 0.135
        )


        eye_height = (
            face_size * 0.040
        )


        # -------------------------------------------------
        # Skin overlay
        # -------------------------------------------------

        skin = QColor(
            215,
            174,
            157,
            245
        )


        painter.setBrush(
            skin
        )


        painter.setPen(
            Qt.NoPen
        )


        painter.drawEllipse(
            QRectF(
                left_eye_x - eye_width / 2,
                eye_y - eye_height / 2,
                eye_width,
                eye_height
            )
        )


        painter.drawEllipse(
            QRectF(
                right_eye_x - eye_width / 2,
                eye_y - eye_height / 2,
                eye_width,
                eye_height
            )
        )


        # -------------------------------------------------
        # Closed eyelid line
        # -------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    85,
                    50,
                    45,
                    220
                ),
                2
            )
        )


        painter.drawLine(
            int(
                left_eye_x
                -
                eye_width / 2
            ),
            int(
                eye_y
            ),
            int(
                left_eye_x
                +
                eye_width / 2
            ),
            int(
                eye_y
            )
        )


        painter.drawLine(
            int(
                right_eye_x
                -
                eye_width / 2
            ),
            int(
                eye_y
            ),
            int(
                right_eye_x
                +
                eye_width / 2
            ),
            int(
                eye_y
            )
        )


    # =====================================================
    # MOUTH ANIMATION
    # =====================================================

    def draw_mouth_animation(
        self,
        painter,
        face_x,
        face_y,
        face_size
    ):

        # -------------------------------------------------
        # ACTUAL LIPS POSITION
        # -------------------------------------------------

        mouth_x = (
            face_x
            +
            face_size * 0.500
        )


        mouth_y = (
            face_y
            +
            face_size * 0.645
        )


        level = max(
            0.0,
            min(
                1.0,
                self.mouth_open
            )
        )


        # -------------------------------------------------
        # CLOSED MOUTH
        # -------------------------------------------------

        if level < 0.04:

            painter.setPen(
                QPen(
                    QColor(
                        105,
                        45,
                        50,
                        170
                    ),
                    2
                )
            )


            painter.setBrush(
                Qt.NoBrush
            )


            painter.drawArc(
                int(
                    mouth_x - 24
                ),
                int(
                    mouth_y - 3
                ),
                48,
                10,
                200 * 16,
                140 * 16
            )


            return


        # -------------------------------------------------
        # SPEAKING MOUTH
        # -------------------------------------------------

        mouth_width = (
            38
            +
            level * 10
        )


        mouth_height = (
            3
            +
            level * 20
        )


        # Outer mouth

        painter.setBrush(
            QColor(
                55,
                15,
                20,
                220
            )
        )


        painter.setPen(
            QPen(
                QColor(
                    130,
                    55,
                    65,
                    180
                ),
                1
            )
        )


        painter.drawEllipse(
            QPointF(
                mouth_x,
                mouth_y
            ),
            mouth_width / 2,
            mouth_height / 2
        )


        # Inner mouth

        painter.setBrush(
            QColor(
                18,
                5,
                8,
                235
            )
        )


        painter.setPen(
            Qt.NoPen
        )


        painter.drawEllipse(
            QPointF(
                mouth_x,
                mouth_y
            ),
            mouth_width * 0.30,
            max(
                2,
                mouth_height * 0.30
            )
        )


    # =====================================================
    # AUDIO WAVE
    # =====================================================

    def draw_wave(
        self,
        painter,
        cx,
        cy
    ):

        painter.setPen(
            QPen(
                QColor(
                    40,
                    190,
                    255,
                    170
                ),
                2
            )
        )


        path = QPainterPath()


        width = 260

        points = 80


        for i in range(
            points
        ):

            x = (
                cx
                -
                width / 2
                +
                (width / (points - 1)) * i
            )


            normalized = (
                i
                /
                (points - 1)
            )


            wave = math.sin(
                self.wave_phase
                +
                normalized * math.pi * 8
            )


            amplitude = (
                4
                +
                self.audio_level * 28
            )


            y = (
                cy
                +
                wave * amplitude
            )


            if i == 0:

                path.moveTo(
                    x,
                    y
                )

            else:

                path.lineTo(
                    x,
                    y
                )


        painter.drawPath(
            path
        )


    # =====================================================
    # BOTTOM BAR
    # =====================================================

    def draw_bottom_bar(
        self,
        painter,
        width,
        height
    ):

        bar_y = height - 70


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
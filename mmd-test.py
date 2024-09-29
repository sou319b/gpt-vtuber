import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import struct

class PMXModel:
    def __init__(self, path):
        self.path = path
        self.vertices = []
        self.faces = []
        self.load_pmx(path)

    def load_pmx(self, path):
        with open(path, 'rb') as f:
            header = f.read(4)
            if header != b'PMX ':
                raise ValueError('Not a valid PMX file')
            version = struct.unpack('f', f.read(4))[0]
            print(f'PMX version: {version}')
            
            # グローバル設定の読み込み
            global_settings_size = struct.unpack('B', f.read(1))[0]
            f.read(global_settings_size)  # グローバル設定をスキップ

            # モデル情報
            name_length = struct.unpack('i', f.read(4))[0]
            f.read(name_length)  # モデル名
            name_length = struct.unpack('i', f.read(4))[0]
            f.read(name_length)  # モデル名（英語）
            name_length = struct.unpack('i', f.read(4))[0]
            f.read(name_length)  # コメント
            name_length = struct.unpack('i', f.read(4))[0]
            f.read(name_length)  # コメント（英語）

            # 頂点データ
            vertex_count = struct.unpack('i', f.read(4))[0]
            for _ in range(vertex_count):
                position = struct.unpack('3f', f.read(12))
                f.read(12)  # 法線
                f.read(8)  # UV
                self.vertices.append(position)

            # 面データ
            face_count = struct.unpack('i', f.read(4))[0]
            for _ in range(face_count // 3):
                face = struct.unpack('3I', f.read(12))  # 4バイトのインデックス
                self.faces.append(face)

    def draw(self):
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_index in face:
                vertex = self.vertices[vertex_index]
                glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

class MMDWidget(QOpenGLWidget):
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path
        self.model = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # 約60FPS

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        self.load_model(self.model_path)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # カメラを少し後ろに移動
        self.draw_model()

    def load_model(self, path):
        print(f"Loading model from {path}")
        self.model = PMXModel(path)

    def draw_model(self):
        if self.model is None:
            return
        self.model.draw()

if __name__ == '__main__':
    mmd_model_path = 'mmd_model/申鹤.pmx'  # ここにMMDモデルのパスを指定
    app = QApplication(sys.argv)
    widget = MMDWidget(mmd_model_path)
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
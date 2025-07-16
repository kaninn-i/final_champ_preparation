class Waypoint:
    def __init__(self, pose, smoothing_factor=0.1, next_segment_velocity_factor=1.0):
        self.pose = pose
        self.smoothing_factor = smoothing_factor
        self.next_segment_velocity_factor = next_segment_velocity_factor
        print(f"[FAKE] Создан Waypoint: {pose}, сглаживание: {smoothing_factor}, скорость: {next_segment_velocity_factor}")

    def __repr__(self):
        return f"Waypoint({self.pose})"


class PoseTransformer:
    def __init__(self, req, motorcortex_types):
        print("[FAKE] PoseTransformer инициализирован")
        self.__req = req
        self.__motorcortex_types = motorcortex_types

    def calcCartToJointPose(self, cart_coord, ref_joint_coord_rad):
        print(f"[FAKE] Перевод из картезианской в суставную систему: {cart_coord} → {ref_joint_coord_rad}")
        return {"joint_result": ref_joint_coord_rad}

    def calcJointToCartPose(self, joint_coord_rad, cart_coord):
        print(f"[FAKE] Перевод из суставной в картезианскую систему: {joint_coord_rad} → {cart_coord}")
        return {"cart_result": cart_coord}


class MotionProgram:
    def __init__(self, req, motorcortex_types):
        print("[FAKE] MotionProgram инициализирован")
        self.name = None
        self.commands = []
        self.id = 1

    def clear(self):
        print("[FAKE] Программа очищена")
        self.commands = []

    def addMoveC(self, waypoints, angle, *args, **kwargs):
        print(f"[FAKE] Добавлено MoveC: точки={waypoints}, угол={angle}")
        self.commands.append(("MoveC", waypoints))

    def addMoveL(self, waypoints, *args, **kwargs):
        print(f"[FAKE] Добавлено MoveL: точки={waypoints}")
        self.commands.append(("MoveL", waypoints))

    def addMoveJ(self, waypoints, *args, **kwargs):
        print(f"[FAKE] Добавлено MoveJ: точки={waypoints}")
        self.commands.append(("MoveJ", waypoints))

    def addWait(self, timeout_s, path=None, value=1):
        print(f"[FAKE] Добавлено ожидание: {timeout_s} сек. путь={path} значение={value}")
        self.commands.append(("Wait", timeout_s))

    def send(self, program_name='Undefined'):
        self.name = program_name
        print(f"[FAKE] Программа отправлена: {self.name} с {len(self.commands)} командами")
        return self  # можно имитировать .get()

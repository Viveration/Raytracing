"""Содержит класс, описывающий распространение луча в цилиндрическом волокне"""
import numpy as np

class Ray_cylinder:
    """Класс конического волокна

    Атрибуты
    --------
    azimut : `float`
        Азимутальный угол, радианы
    latitude : `float`
        Зенитный угол, радианы
    startpoint : `numpy.ndarray` [`float`]
        Начальная координата луча
    vector : `numpy.ndarray` [`float`]
        Единичный вектор направления распространения луча
    
    Методы
    ------
    `set_values`(self, azimut, latitude, startpoint):
        Задает параметры луча
    `calculate_angles_from_vector`(self, vector):
        Считает азимутальный и зенитный углы из направляющего вектора
    `calculate_intersection`(self, core_radius):
        Рассчет точки пересечения луча с заданной поверхностью
    `calculate_reflection`(self, point, normal):
        Рассчет направления отражения луча в заданной точке
    `generate_startpoint`(self, radius):
        Генерация случайной стартовой точки
    `set_startpoint`(self, x = 0, y = 0, z = 0):
        Задание определенной стартовой точки
    `generate_angles`(self, max_latitude = 30):
        Генерация случайных углов распространения
    `set_angles`(self, azimut, latitude):
        Задание определенных углов распределения
    `calculate_trajectory`(self, fiber, max_reflection = 1000, angle_elimination = True, output = False):
        Рассчет траектории луча в заданной среде
    """  
    azimut : float
    latitude : float
    startpoint : np.ndarray[float]
    vector : np.ndarray[float]

    def __init__(self, azimut = 0.0, latitude = 0.0, startpoint = np.array([0.0,0.0,0.0])): #все углы принимаются в радианах   
        """Рассчитывает параметры луча по заданным значениям

        Parameters
        ----------
        azimut : `float`, optional
            Азимутальный угол, радианы, by default 0.0
        latitude : `float`, optional
            Зенитный угол, радианы, by default 0.0
        startpoint : `numpy.ndarray` [`float`], optional
            Начальная точка луча, by default [0.0, 0.0, 0.0]
        """             
        self.azimut = azimut
        self.latitude = latitude
        self.startpoint = startpoint
        self.vector = [np.sin(latitude)*np.cos(azimut),
                      np.sin(latitude)*np.sin(azimut), 
                      np.cos(latitude)]
    
    def set_values(self, azimut, latitude, startpoint):
        """Задать параметры луча

        Parameters
        ----------
        azimut : `float`, optional
            Азимутальный угол, радианы, by default 0.0
        latitude : `float`, optional
            Зенитный угол, радианы, by default 0.0
        startpoint : `numpy.ndarray` [`float`], optional
            Начальная точка луча, by default [0.0, 0.0, 0.0]
        """    
        self.azimut = azimut
        self.latitude = latitude
        self.startpoint = startpoint
        self.vector = [np.sin(latitude)*np.cos(azimut),
                      np.sin(latitude)*np.sin(azimut), 
                      np.cos(latitude)]
    def calculate_angles_from_vector(self, vector):
        """Рассчет углов распространения на основе вектора распространения

        Parameters
        ----------
        vector : `numpy.ndarray` [`float`]
            Единичный направляющий вектор, декартова СК, метры

        Returns
        -------
        `numpy.ndarray` [`float`]
            Массив углов распространения [азимуталььный, зенитный]
        """        
        latitude = np.arccos(vector[2])
        if latitude == 0:
            return [0, 0]
        cos = vector[0] / np.linalg.norm(vector[:2])
        sin = vector[1] / np.linalg.norm(vector[:2])
        if sin > 0:
            azimut = np.arccos(cos)
        else:
            azimut = -np.arccos(cos)
        return np.array([azimut, latitude])
    
    def calculate_intersection(self, core_radius):
        """Рассчет точки  пересечения луча с поверхностью

        Parameters
        ----------
        core_radius : `float`
            Радиус сердцевины

        Returns
        -------
        `numpy.ndarray` [`float`]
            Координаты пересечения луча с поверхностью сердцевины
        """        
        if self.latitude == 0:
            return [*self.startpoint[:2], -1]
        x0, y0, z0 = self.startpoint
        phi, alpha = self.azimut, self.latitude
        R = core_radius
        gamma = np.cos(phi)*x0 + np.sin(phi)*y0
        x = x0 + np.cos(phi) * (-gamma + np.sqrt(gamma**2 - x0**2 - y0**2 + R**2))
        y = y0 + np.sin(phi) * (-gamma + np.sqrt(gamma**2 - x0**2 - y0**2 + R**2))
        z = z0 + np.cos(alpha) / np.sin(alpha) * (-gamma + np.sqrt(gamma**2 - x0**2 - y0**2 + R**2))

        return [x, y, z]
    
    def calculate_reflection(self, point, normal):
        """Функция рассчитывает углы распространения луча после отражения в заданной точке

        Parameters
        ----------
        point : `numpy.ndarray` [`float`]
            Координата отражения
        normal : `numpy.ndarray` [`float`]
            Нормаль к поверхности в точке отражения(направлена к оси волокна)

        Returns
        -------
        `float`
            Азимутальный угол распространения вектора
        `float`
            Зенитный угол распространения вектора
        `float`
            Угол отражения
        """        
        angle  = np.dot(normal, self.vector)
        proection = normal * angle
        reflected_vector = -2 * proection + self.vector
        return *self.calculate_angles_from_vector(reflected_vector), angle
    
    def generate_startpoint(self, radius):
        """Создание случайной точки начала для луча в заданной области

        Parameters
        ----------
        radius : `float`
            Радиус сердцевины волокна

        Returns
        -------
        `numpy.ndarray` [`float`]
            Координаты начала луча
        """        
        phi = np.random.random() * np.pi
        r = np.random.random() * radius
        coords = [r*np.cos(phi), r*np.sin(phi)]
        self.startpoint = [*coords, 0]
        return np.array([*coords, 0])
    
    def set_startpoint(self, x = 0.0, y = 0.0, z = 0.0):
        """_summary_

        Parameters
        ----------
        x : `float`, optional
            Координата х, метры, by default 0.0
        y : `float`, optional
            Координата у, метры, by default 0.0
        z : `float`, optional
            Координата z, метры, by default 0.0

        Returns
        -------
        `numpy.ndarray` [`float`]
            Координаты заданной точки начала 
        """        
        self.startpoint = [x, y, z]
        return self.startpoint
    
    def generate_angles(self, max_latitude = 30.0):
        """Генерация случайных углов распространения для луча

        Parameters
        ----------
        max_latitude : `float`, optional
            Предельный зенитный угол, градусы, by default 30.0

        Returns
        -------
        `float`
            Зенитный угол
        `float`
            Азимутальный угол
        """        
        latitude = np.deg2rad(np.random.random() * max_latitude)
        azimut = np.deg2rad(np.random.random() * 360)
        self.azimut = azimut
        self.latitude = latitude
        self.vector = [np.sin(latitude)*np.cos(azimut),
                      np.sin(latitude)*np.sin(azimut), 
                      np.cos(latitude)]
        return [latitude, azimut]
        
    def set_angles(self, azimut, latitude):
        """Задать углы распространения

        Parameters
        ----------
        azimut : `float`
            Азимутальный угол, радианы
        latitude : `float`
            Зенитный угол, радианы

        Returns
        -------
        `numpy.ndarray` [`float`]
            Зенитный угол, азимутальный угол. радианы
        """        
        self.azimut = azimut
        self.latitude = latitude
        self.vector = [np.sin(latitude)*np.cos(azimut),
                      np.sin(latitude)*np.sin(azimut), 
                      np.cos(latitude)]
        return [latitude, azimut]
    
    def calculate_trajectory(self, fiber, max_reflection = 1000, angle_elimination = True, output = False):
        """Рассчет траектории движения луча

        Parameters
        ----------
        fiber : `Fiber_cylinder`
            Класс описываемого волокна
        max_reflection : `int`, optional
            Максимальное количество отражений, by default 1000
        angle_elimination : `bool`, optional
            Учитывать ли максимальный угол отражения, by default True
        output : `bool`, optional
            Дополнительный вывод, by default False

        Returns
        -------
        `numpy.ndarray` [[`float`]]
            Массив координат отражения луча, метры
        `numpy.ndarray` [[`float`]]
            Массив углов распространения после каждого отражения, радианы
        `int`
            Максимальное количество отражений
        `string`
            Причина, по которой луч перестал распространяться
        """        
        z_max = fiber.z_max
        termination_angle = np.arcsin(fiber.clad_n / fiber.core_n)
        Dots = np.zeros((max_reflection, 3))
        reflection_angle = self.latitude
        Angles = np.zeros((max_reflection, 3))
        z_start = self.startpoint[2]
        Dots[0] = self.startpoint
        Angles[0] = [self.azimut, self.latitude, 0]
        for i in range(1, max_reflection):
            intersection_point = self.calculate_intersection(fiber.core_r)
            if intersection_point[2] > z_max:
                intersection_final = intersection_point - self.vector / self.vector[2] * (intersection_point[2] - z_max) 
                Dots[i] = intersection_final
                Angles[i] = [self.azimut, self.latitude, abs(reflection_angle)]
                if output:
                    print('Ray reached z_max.')
                return Dots, np.rad2deg(Angles), i + 1, 'z_max'
            normal = fiber.find_normal(intersection_point)
            azimut, latitude, reflection_angle = self.calculate_reflection(intersection_point, normal)
            if fiber.diffusion:
                azimut += (np.random.random() - 0.5 ) * 2 * fiber.diffusion
                latitude += (np.random.random() - 0.5 ) * 2 * fiber.diffusion
            Dots[i] = intersection_point
            Angles[i] = [azimut, latitude, abs(reflection_angle)]
            if angle_elimination:
                if np.pi / 2 - abs(reflection_angle) < termination_angle:
                    if output:
                        print('Ray terminated, termination angle: ', np.rad2deg(termination_angle),' reflection_angle: ',  np.rad2deg(np.pi / 2 - abs(reflection_angle)))
                    return Dots, np.rad2deg(Angles), i + 1, 'reflection_angle'
            self.set_values(azimut, latitude, intersection_point)
        if output:
            print('Reflections exceeded', max_reflection)
        return Dots, np.rad2deg(Angles), max_reflection, 'max_reflections'
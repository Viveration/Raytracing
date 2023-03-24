"""Имплементация волокон"""
import numpy as np


class Fiber_cylinder:
    """Класс цилиндрического волокна

    Атрибуты
    --------
    diffusion : `None` or `float`
        Угол диффузного отражения, радианы
    core_r : `float`
        Радиус сердцевины, метры
    clad_r : `float`
        Радиус оболочки, метры
    core_n : `float`
        Показатель преломления сердцевины
    clad_n : `float`
        Показатель преломления оболочки
    z_max : `float`
        Максимальная длина волокна, метры
    
    Методы
    ------
    `set_geometry`(self, core_r, clad_r, z):
        Задает радиусы сердцевины, оболочки и длину волокна.
    `set_refr`(self, core_n, clad_n):
        Задает показатели преломления оболочки и сердцевины.
    `radius`(self):
        Возвращает значения радиусов сердцевины и оболочки
    `ref`r(self):
        Возвращает значения показателей преломления сердцевины и оболочки
    `find_normal`(self, intersection_point):
        Возвращает нормаль к поверхности, направленную к центру цилиндра в заданной точке.
    """    
    
    diffusion : float
    core_r : float
    clad_r : float
    core_n : float
    clad_n : float
    z_max : float

    def __init__(self, core_r = 0.0, clad_r = 0.0, core_n = 0.0, clad_n = 0.0, z_max = 0.0, diffusion = None):
        """Описывает цилиндрическое волокно

        Parameters
        ----------
        core_r : `float`, optional
            Радиус сердцевины, метры, by default 0.0
        clad_r : `float`, optional
            Радиус оболочки. метры, by default 0.0
        core_n : `float`, optional
            Показатель преломления сердцевины, by default 0.0
        clad_n : `float`, optional
            Показатель преломления оболочки, by default 0.0
        z_max : `float`, optional
            Максимальная длина волокна, метры, by default 0.0
        diffusion : `None` or `float`, optional
            Угол диффузного отражения, радианы, by default None
        Returns
        -------
        
        """        
        self.diffusion = diffusion
        self.core_r = core_r
        self.clad_r = clad_r
        self.core_n = core_n
        self.clad_n = clad_n
        self.z_max = z_max
    def set_geometry(self, core_r, clad_r, z):
        """Установить определенную геометрию волокна

        Parameters
        ----------
        core_r : `float`
            Радиус сердцевины, метры
        clad_r : `float`
            Радиус оболочки, метры
        z : `float`
            Длина волокна, метры
        """        
        self.core_r = core_r
        self.clad_r = clad_r
        self.z_max = z
    def set_refr(self, core_n, clad_n):
        """Задать показатели преломления волокна

        Parameters
        ----------
        core_n : `float`
            Показатель преломления сердцевины
        clad_n : `float`
            Показатель преломления оболочки
        """        
        self.core_n = core_n
        self.clad_n = clad_n
    def radius(self):
        """Возвращает радиусы сердцевины и оболочки

        Returns
        -------
        `float`
            Радиус сердцевины, метры
        `float`
            Радиус оболочки, метры
        """        
        return self.core_r, self.clad_r
    def refr(self):
        """Возвращает показатели преломления сердцевины и оболочки

        Returns
        -------
        `float`
            Показатель преломления сердцевины
        `float`
            Показатель преломления оболочки 
        """        
        return self.core_n, self.clad_n
    
    def find_normal(self, intersection_point):
        """Возвращает нормаль, направленную к центру цилиндра в определенной точке

        Parameters
        ----------
        intersection_point : `numpy.ndarray` [`float`]
            Массив координат точки на поверхности цилиндра, декартовы координаты, метры

        Returns
        -------
        `numpy.ndarray` [`float`]
            Единичный вектор нормали к поверхности, направленной к центру цилиндра, метры
        """        
        x, y = intersection_point[:2]
        result = -1 * np.array([x, y, 0])/np.sqrt(x**2 + y**2)
        return result # Возвращает нормаль к поверхности, направленную к центру цилиндра

class Fiber_cone:
    """Класс конического волокна

    Атрибуты
    --------
    diffusion : `None` or `float`
        Угол диффузного отражения, радианы
    core_r : `float`
        Радиус сердцевины, метры
    clad_r : `float`
        Радиус оболочки, метры
    core_n : `float`
        Показатель преломления сердцевины
    clad_n : `float`
        Показатель преломления оболочки
    z_max : `float`
        Максимальная длина волокна, метры
    angle : `float`
        Угол раствора, радианы
    c : `float`
        Переменная для промежуточных вычислений
    
    Методы
    ------
    `set_geometry`(self, z_max = 1, base_r = 0, top_r = 0):
        Задает геометрию волокна через длину и радиусы начала и конца 
    `set_refr`(self, core_n, clad_n):
        Задает показатели преломления оболочки и сердцевины.
    `radius`(self):
        Возвращает значения радиусов сердцевины и оболочки
    `refr`(self):
        Возвращает значения показателей преломления сердцевины и оболочки
    `find_normal`(self, intersection_point):
        Возвращает нормаль к поверхности, направленную к центру цилиндра в заданной точке.
    """    
    diffusion : float
    top_r : float
    base_r : float
    core_n : float
    clad_n : float
    z_max : float
    angle : float
    c : float

    def __init__(self, z_max = 1.0, base_r = 0.0, top_r = 0.0, core_n = 1.445, clad_n = 1.44, diffusion = None):       
        """Описывает коническое волокно

        Parameters
        ----------
        z_max : `float`, optional
            Длина волокна, метры, by default 1.0
        base_r : `float`, optional
            Радиус начала волокна, метры, by default 0.0
        top_r : `float`, optional
            Радиус конца волокна, метры, by default 0.0
        core_n : `float`, optional
            Показатель преломления сердцевины, by default 1.445
        clad_n : `float`, optional
            Показатель преломления оболочки, by default 1.44
        diffusion : `float`, optional
            Угол диффузного отражения, радианы, by default None
        """         
        self.diffusion = diffusion
        self.z_max = z_max
        self.angle = np.arcsin((base_r - top_r) / z_max)
        self.base_r = base_r
        self.top_r = top_r
        self.c = np.sin(self.angle) / np.cos(self.angle)
        self.core_n = core_n
        self.clad_n = clad_n
    def set_geometry(self, z_max = 1, base_r = 0, top_r = 0):
        """Задать геометрию конического волокна

        Parameters
        ----------
        z_max : `float`, optional
            Длина волокна, метры, by default 1.0
        base_r : `float`, optional
            Радиус начала волокна, метры, by default 0.0
        top_r : `float`, optional
            Радиус конца волокна, метры, by default 0.0
        """        
        self.base_r = base_r
        self.top_r = top_r
        self.angle = np.arcsin((base_r - top_r) / z_max)
        self.z_max = z_max
        self.c = np.sin(self.angle) / np.cos(self.angle)
    def set_refr(self, core_n, clad_n):
        """Задать показатели преломления волокна

        Parameters
        ----------
        core_n : `float`
            Показатель преломления сердцевины
        clad_n : `float`
            Показатель преломления оболочки
        """        
        self.core_n = core_n
        self.clad_n = clad_n
    def refr(self):
        """Возвращает показатели преломления сердцевины и оболочки

        Returns
        -------
        `float`
            Показатель преломления сердцевины
        `float`
            Показатель преломления оболочки
        """        
        return self.core_n, self.clad_n
    def find_normal(self, intersection_point):
        """Найти нормаль к поверхности в заданной точке, направленную к оси конуса

        Parameters
        ----------
        intersection_point : `numpy.ndarray` [`float`]
            Координаты точки на поверхности, декартова СК, метры

        Returns
        -------
        `numpy.ndarray` [`float`]
            Единичный вектор нормали, направленной к оси конуса
        """        
        x, y = intersection_point[:2]
        z = -self.c**2*(intersection_point[2] - self.base_r / self.c)
        result = -1 * np.array([x, y, z])/np.sqrt(x**2 + y**2 + z**2)
        return result # Возвращает нормаль к поверхности, направленную к центру цилиндра
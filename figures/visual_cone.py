""" Набор функций для построения 3д изображения конуса."""

import numpy as np
import plotly.graph_objects as go

def create_cone(xs, ys, zs, r_base, z_max, angle, n_slices = 40):
    """Генерация точек конуса

    Parameters
    ----------
    xs : `float`
        Координата центра x.
    ys : `float`
        Координата центра y.
    zs : `float`
        Координата центра z.
    r_base : `float`
        Радиус основания конуса.
    z_max : `float`
        Высота конуса.
    angle : `float`
        Угол раствора.
    n_slices : `int`, optional
        Количество сегментов разбиения, by default 40

    Returns
    -------
     `ndarray` [`float`],
     `ndarray` [`float`],
     `ndarray` [`float`]
        3 массива координат цилиндра.
    """    
    theta = np.linspace(0, 2 * np.pi, n_slices + 1)
    r_top = r_base - (z_max-zs) * np.sin(angle)
    r1 = np.linspace(r_base, r_top, n_slices + 1)
    x = np.array([xs + r1[i] * np.cos(theta) for i in range(len(r1))]).flatten()
    y = np.array([ys + r1[i] * np.sin(theta) for i in range(len(r1))]).flatten()
    z_init = np.linspace(0, z_max-zs, n_slices + 1)
    z = np.array([z_init[i] * np.ones(len(theta)) for i in range(len(r1))]).flatten()
    return x, y, z

def show_trajectory_cone(data, index, fiber, n_slices = 40):
    """Показывает траекторию луча в конусе.

    Parameters
    ----------
    data : `DataFrame`
        Содержит следующую информацию: 'angles'-углы отражения,
        'trajectories'-координаты отражения,'reflections'-максимум отражений,'termination'-причина уничтожения.
    index : `int`
        Номер луча из data для отображения.
    fiber : `Fiber_cone`
        Класс волокна по которому распространяется луч.
    n_slices : int, optional
        Количество элементов разбиения конуса, by default 40
    """    
    trajectory = np.array(data['trajectories'][index][:int(data['reflections'][index])])
    x, y, z = create_cone(*[0,0,0], fiber.base_r, trajectory[-1, 2], fiber.angle, n_slices = n_slices)
    
    fig = go.Figure(data=[go.Mesh3d(
      x=x, y=y, z=z, color='green', opacity=0.20)])
    fig.add_traces(data=go.Scatter3d(
        x=trajectory[:, 0], y=trajectory[:, 1], z=trajectory[:, 2],
        marker=dict(
            size=3,
            color='black',
            colorscale='Viridis',
        ),
        line=dict(
            color='darkblue',
            width=2
        )
    ))
    fig.update_layout(
        autosize=False,
        width=1000,
        height=1000,)
    fig.show()
""" Набор функций для построения 3д изображения цилиндра."""

import numpy as np
import plotly.graph_objects as go

def slice_triangles(z, n, i, j, k, l):
    """Create the triangles of a single slice"""
    return [[z, j, i], [i, j, l], [l, j, k], [k, n, l]]


def cylinder_mesh(r, xs, ys, zs, h, n_slices=40):
    """Create a cylindrical mesh"""
    theta = np.linspace(0, 2 * np.pi, n_slices + 1)
    x = xs + r * np.cos(theta)
    y = ys + r * np.sin(theta)
    z1 = zs + 0 * np.ones_like(x)
    z2 = (zs + h) * np.ones_like(x)
# index of the final point in the mesh
    n = n_slices * 2 + 1

    # build triangulation
    triangles = []
    for s in range(1, n_slices + 1):
        j = (s + 1) if (s <= n_slices - 1) else 1
        k = j + n_slices if (s <= n_slices - 1) else n_slices + 1
        l = s + n_slices
        triangles += slice_triangles(0, n, s, j, k, l)
    triangles = np.array(triangles)

    # coordinates of the vertices
    x_coords = np.hstack([xs, x[:-1], x[:-1], xs])
    y_coords = np.hstack([ys, y[:-1], y[:-1], ys])
    z_coords = np.hstack([zs, z1[:-1], z2[:-1], (zs + h)])
    vertices = np.stack([x_coords, y_coords, z_coords]).T

    return vertices, triangles, x, y, z1, z2


def cylinder_traces(r, xs, ys, zs, h, n_slices=40, show_mesh=False, n_sub=4, surface_kw=dict(), line_kw=dict()):
    """

    Parameters
    ----------
    r : `float`
        Радиус цилиндра.
    xs : `float`
        Набор х-координат.
    ys : `float`
        Набор y-координат.
    zs : `float`
        Набор z-координат.
    h : `float`
        Высота цилиндра.
    n_slices : `int`, optional
        Разбиение по углу, by default 40
    show_mesh : `bool`, optional
        Показать сеть, by default False
    n_sub : `int`, optional
        Разбиение по высоте, by default 4
    surface_kw : `dict()`, optional
        Дополнительные аргументы поверхности, by default dict()
    line_kw : `dict()`, optional
        Дополнительные аргументы линии, by default dict()

    Returns
    -------
    `array_like`
        Набор координат для изображения цилиндра
    """ 

    vertices, triangles, x, y, z1, z2 = cylinder_mesh(
        r, xs, ys, zs, h, n_slices)
    surface = go.Mesh3d(
        x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
        i=triangles[:, 0], j=triangles[:, 1], k=triangles[:, 2],
        **surface_kw)

    traces = [surface]
    if not show_mesh:
        return traces

    line_kw.setdefault("showlegend", False)
    # horizontal mesh lines
    zsubs = np.linspace(zs, zs + h, n_sub + 1)
    for zc in zsubs:
        traces.append(go.Scatter3d(x=x, y=y, z=zc *
                      np.ones_like(x), mode="lines", **line_kw))
    # vertical mesh lines
    for _x, _y in zip(x, y):
        traces.append(go.Scatter3d(x=[_x, _x], y=[_y, _y], z=[
                      zs, zs + h], mode="lines", **line_kw))
    return traces

def show_trajectory(data, index, fiber):
    """Показывает траекторию луча в цилиндре.

    Parameters
    ----------
    data : `DataFrame`
        Содержит следующую информацию: 'angles'-углы отражения,
        'trajectories'-координаты отражения,'reflections'-максимум отражений,'termination'-причина уничтожения.
    index : `int`
        Номер луча из data для отображения.
    fiber : `Fiber_cylinder`
        Класс волокна по которому распространяется луч.
    """    
    dots = np.array(data['trajectories'][index])
    reflection_count = int(data['reflections'][index])
    fig = go.Figure()
    fig.add_traces(
        cylinder_traces(fiber.core_r, 0, 0, 0, dots[reflection_count - 2][2], 100, n_sub=8, line_kw={"line_color":"#202020", "line_width": 3})
    )
    fig.update_traces(opacity=0.15, selector=dict(type='mesh3d'))
    fig.add_traces(data=go.Scatter3d(
        x=dots[:reflection_count-1, 0], y=dots[:reflection_count-1, 1], z=dots[:reflection_count-1, 2],
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
    fig.show()

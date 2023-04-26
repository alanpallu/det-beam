import anastruct as an


def get_esforcos(h, b, concrete_type, coords, point_loads, q_loads):
    dict_concreto = {'C20': 21000000, 'C25': 24000000, 'C30': 27000000, 'C35': 29000000, 'C40': 32000000,
                     'C45': 34000000, 'C50': 37000000}
    area = h * b
    inertia = (b * h ** 3) / 12
    E = dict_concreto[concrete_type]
    ss = an.SystemElements(EA=area * E, EI=inertia * E)

    for index in range((len(coords) - 1)):
        ss.add_element(location=coords[index:index + 2])

    for node in range(len(coords)):
        ss.add_support_fixed(node_id=node + 1)

    for point_load in point_loads:
        node = point_load[0]
        load = point_load[1]
        ss.point_load(node_id=node, Fy=load)

    for q_load in q_loads:
        element_id = q_load[0]
        load = q_load[1]
        ss.q_load(q=load, element_id=[element_id], direction='element')

    ss.show_structure()
    ss.solve()
    moment_list = ss.get_element_result_range('moment')
    shear_list = ss.get_element_result_range('shear')
    results = ss.get_element_results()

    ss.show_bending_moment(factor=None, verbosity=0, scale=1, offset=(0, 0), figsize=None, show=True, values_only=False)

    return results, moment_list, shear_list


if __name__ == '__main__':
    coords = [[0, 0], [4.48, 0], [8.68, 0]]
    # point_loads = [[1, -20], [4, -50]]
    point_loads = []
    q_loads = [[1, -60], [2, -50]]
    res, node_res = get_esforcos(b=0.2, h=0.6, concrete_type='C30', coords=coords, point_loads=point_loads, q_loads=q_loads)
    print(res)

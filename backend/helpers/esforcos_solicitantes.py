import anastruct as an


def get_esforcos(h, b, concrete_type, coords, node_ids_fixed, point_loads, q_loads):
    dict_concreto = {'C20': 21000000, 'C25': 24000000, 'C30': 27000000, 'C35': 29000000, 'C40': 32000000,
                     'C45': 34000000, 'C50': 37000000}
    area = h * b
    inertia = (b * h ** 3) / 12
    E = dict_concreto[concrete_type]
    EA = area * E
    EI = inertia * E
    ss = an.SystemElements(EA=EA, EI=EI)

    for index in range((len(coords) - 1)):
        ss.add_element(location=coords[index:index + 2], EA=EA, EI=EI)

    for node in node_ids_fixed: #todo revisar tipos de vinculação
        node_id = int(coords.index([node, 0]) + 1)
        if node_id == 1 or node_id == len(coords):
            if len(node_ids_fixed) == 2:
                ss.add_support_hinged(node_id=node_id)
            else:
                ss.add_support_fixed(node_id=node_id)
        else:
            ss.add_support_hinged(node_id=node_id)

    for point_load in point_loads:
        node = int(point_load[0])
        load = float(point_load[1])
        ss.point_load(node_id=node, Fy=load)

    for q_load in q_loads:
        element_id = int(q_load[0])
        load = float(q_load[1])
        ss.q_load(q=load, element_id=[element_id], direction='element')

    ss.show_structure()
    ss.solve()
    moment_list = ss.get_element_result_range('moment')
    shear_list = ss.get_element_result_range('shear')
    results = ss.get_element_results(verbose=True)

    ss.show_bending_moment(factor=None, verbosity=0, scale=1, offset=(0, 0), figsize=None, show=True, values_only=False)

    return results, moment_list, shear_list


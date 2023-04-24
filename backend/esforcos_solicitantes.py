import anastruct as an

ss = an.SystemElements()

ss.add_element(location=[[1, 0], [4, 0]])
ss.add_element(location=[[4, 0], [10, 0]])
ss.add_support_hinged(node_id=[2])
ss.add_support_fixed(node_id=[1, 3])

ss.q_load(q=-20, element_id=[1], direction='element')
ss.q_load(q=-50, element_id=[2], direction='element')
ss.show_structure()

ss.solve()
res = ss.get_element_results()
res2 = ss.get_node_results_system(1)
print(res)

ss.show_bending_moment(factor=None, verbosity=0, scale=1, offset=(0, 0), figsize=None, show=True, values_only=False)

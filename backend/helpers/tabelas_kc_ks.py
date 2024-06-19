import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def create_table_from_excel_file(excel_file, table_name, database_name
                                 , server_name, port, user_name, password):
    engine = create_engine(f'postgresql://'
    f'{user_name}:{password}@{server_name}:{port}/{database_name}')

    conn = engine.connect()

    # read Excel file
    df = pd.read_excel(excel_file)

    # create a table in the database
    df.to_sql(table_name, conn, if_exists='replace', index=True)


def select_all():
    # conn = psycopg2.connect(
    #     host=host,
    #     port=port,
    #     user=user,
    #     password=password,
    #     database=database
    # )

    # sql1 = f"select * from {table_name}"

    dict_kc_ks = {20: {0.01: 103.355, 0.02: 51.886, 0.03: 34.73, 0.04: 26.154, 0.05: 21.008, 0.06: 17.579, 0.07: 15.13, 0.08: 13.293, 0.09: 11.865, 0.1: 10.723, 0.11: 9.789, 0.12: 9.011, 0.13: 8.353, 0.14: 7.789, 0.15: 7.301, 0.16: 6.874, 0.17: 6.497, 0.18: 6.163, 0.19: 5.864, 0.2: 5.595, 0.21: 5.351, 0.22: 5.131, 0.23: 4.929, 0.24: 4.745, 0.25: 4.575, 0.26: 4.419, 0.27: 4.274, 0.28: 4.14, 0.29: 4.015, 0.3: 3.899, 0.31: 3.791, 0.32: 3.689, 0.33: 3.594, 0.34: 3.504, 0.35: 3.42, 0.36: 3.341, 0.37: 3.265, 0.38: 3.195, 0.39: 3.127, 0.4: 3.064, 0.41: 3.003, 0.42: 2.946, 0.43: 2.891, 0.44: 2.839, 0.45: 2.79, 0.46: 2.742, 0.47: 2.697, 0.48: 2.654, 0.49: 2.613, 0.5: 2.574, 0.51: 2.536, 0.52: 2.5, 0.53: 2.465, 0.54: 2.432, 0.55: 2.4, 0.56: 2.369, 0.57: 2.339, 0.58: 2.311, 0.59: 2.284, 0.6: 2.257, 0.61: 2.232, 0.62: 2.208, 0.63: 2.184, 0.64: 2.162, 0.65: 2.14, 0.66: 2.119, 0.67: 2.099, 0.68: 2.079, 0.69: 2.061, 0.7: 2.042, 0.71: 2.025, 0.72: 2.008, 0.73: 1.992, 0.74: 1.976, 0.75: 1.961, 0.76: 1.946, 0.77: 1.932, 0.78: 1.918}, 25: {0.01: 82.684, 0.02: 41.509, 0.03: 27.784, 0.04: 20.923, 0.05: 16.807, 0.06: 14.063, 0.07: 12.104, 0.08: 10.634, 0.09: 9.492, 0.1: 8.578, 0.11: 7.831, 0.12: 7.209, 0.13: 6.682, 0.14: 6.231, 0.15: 5.841, 0.16: 5.499, 0.17: 5.198, 0.18: 4.93, 0.19: 4.691, 0.2: 4.476, 0.21: 4.281, 0.22: 4.105, 0.23: 3.943, 0.24: 3.796, 0.25: 3.66, 0.26: 3.535, 0.27: 3.419, 0.28: 3.312, 0.29: 3.212, 0.3: 3.119, 0.31: 3.033, 0.32: 2.951, 0.33: 2.875, 0.34: 2.803, 0.35: 2.736, 0.36: 2.672, 0.37: 2.612, 0.38: 2.556, 0.39: 2.502, 0.4: 2.451, 0.41: 2.403, 0.42: 2.357, 0.43: 2.313, 0.44: 2.271, 0.45: 2.232, 0.46: 2.194, 0.47: 2.158, 0.48: 2.123, 0.49: 2.09, 0.5: 2.059, 0.51: 2.029, 0.52: 2.0, 0.53: 1.972, 0.54: 1.945, 0.55: 1.92, 0.56: 1.895, 0.57: 1.871, 0.58: 1.849, 0.59: 1.827, 0.6: 1.806, 0.61: 1.786, 0.62: 1.766, 0.63: 1.748, 0.64: 1.73, 0.65: 1.712, 0.66: 1.695, 0.67: 1.679, 0.68: 1.664, 0.69: 1.649, 0.7: 1.634, 0.71: 1.62, 0.72: 1.606, 0.73: 1.593, 0.74: 1.581, 0.75: 1.569, 0.76: 1.557, 0.77: 1.546, 0.78: 1.535}, 30: {0.01: 68.903, 0.02: 34.59, 0.03: 23.154, 0.04: 17.436, 0.05: 14.006, 0.06: 11.719, 0.07: 10.086, 0.08: 8.862, 0.09: 7.91, 0.1: 7.149, 0.11: 6.526, 0.12: 6.007, 0.13: 5.569, 0.14: 5.193, 0.15: 4.867, 0.16: 4.582, 0.17: 4.331, 0.18: 4.108, 0.19: 3.909, 0.2: 3.73, 0.21: 3.568, 0.22: 3.42, 0.23: 3.286, 0.24: 3.163, 0.25: 3.05, 0.26: 2.946, 0.27: 2.85, 0.28: 2.76, 0.29: 2.677, 0.3: 2.6, 0.31: 2.527, 0.32: 2.459, 0.33: 2.396, 0.34: 2.336, 0.35: 2.28, 0.36: 2.227, 0.37: 2.177, 0.38: 2.13, 0.39: 2.085, 0.4: 2.042, 0.41: 2.002, 0.42: 1.964, 0.43: 1.928, 0.44: 1.893, 0.45: 1.86, 0.46: 1.828, 0.47: 1.798, 0.48: 1.769, 0.49: 1.742, 0.5: 1.716, 0.51: 1.69, 0.52: 1.666, 0.53: 1.643, 0.54: 1.621, 0.55: 1.6, 0.56: 1.579, 0.57: 1.56, 0.58: 1.541, 0.59: 1.522, 0.6: 1.505, 0.61: 1.488, 0.62: 1.472, 0.63: 1.456, 0.64: 1.441, 0.65: 1.427, 0.66: 1.413, 0.67: 1.399, 0.68: 1.386, 0.69: 1.374, 0.7: 1.362, 0.71: 1.35, 0.72: 1.339, 0.73: 1.328, 0.74: 1.317, 0.75: 1.307, 0.76: 1.297, 0.77: 1.288, 0.78: 1.279}, 35: {0.01: 59.06, 0.02: 29.649, 0.03: 19.846, 0.04: 14.945, 0.05: 12.005, 0.06: 10.045, 0.07: 8.645, 0.08: 7.596, 0.09: 6.78, 0.1: 6.127, 0.11: 5.594, 0.12: 5.149, 0.13: 4.773, 0.14: 4.451, 0.15: 4.172, 0.16: 3.928, 0.17: 3.713, 0.18: 3.522, 0.19: 3.351, 0.2: 3.197, 0.21: 3.058, 0.22: 2.932, 0.23: 2.817, 0.24: 2.711, 0.25: 2.614, 0.26: 2.525, 0.27: 2.442, 0.28: 2.366, 0.29: 2.295, 0.3: 2.228, 0.31: 2.166, 0.32: 2.108, 0.33: 2.054, 0.34: 2.002, 0.35: 1.954, 0.36: 1.909, 0.37: 1.866, 0.38: 1.825, 0.39: 1.787, 0.4: 1.751, 0.41: 1.716, 0.42: 1.683, 0.43: 1.652, 0.44: 1.622, 0.45: 1.594, 0.46: 1.567, 0.47: 1.541, 0.48: 1.517, 0.49: 1.493, 0.5: 1.471, 0.51: 1.449, 0.52: 1.428, 0.53: 1.408, 0.54: 1.389, 0.55: 1.371, 0.56: 1.354, 0.57: 1.337, 0.58: 1.321, 0.59: 1.305, 0.6: 1.29, 0.61: 1.276, 0.62: 1.262, 0.63: 1.248, 0.64: 1.235, 0.65: 1.223, 0.66: 1.211, 0.67: 1.199, 0.68: 1.188, 0.69: 1.178, 0.7: 1.167, 0.71: 1.157, 0.72: 1.147, 0.73: 1.138, 0.74: 1.129, 0.75: 1.12, 0.76: 1.112, 0.77: 1.104, 0.78: 1.096}, 40: {0.01: 51.677, 0.02: 25.943, 0.03: 17.365, 0.04: 13.077, 0.05: 10.504, 0.06: 8.789, 0.07: 7.565, 0.08: 6.647, 0.09: 5.933, 0.1: 5.362, 0.11: 4.895, 0.12: 4.505, 0.13: 4.176, 0.14: 3.895, 0.15: 3.65, 0.16: 3.437, 0.17: 3.249, 0.18: 3.081, 0.19: 2.932, 0.2: 2.797, 0.21: 2.676, 0.22: 2.565, 0.23: 2.465, 0.24: 2.372, 0.25: 2.288, 0.26: 2.209, 0.27: 2.137, 0.28: 2.07, 0.29: 2.008, 0.3: 1.95, 0.31: 1.895, 0.32: 1.845, 0.33: 1.797, 0.34: 1.752, 0.35: 1.71, 0.36: 1.67, 0.37: 1.633, 0.38: 1.597, 0.39: 1.564, 0.4: 1.532, 0.41: 1.502, 0.42: 1.473, 0.43: 1.446, 0.44: 1.42, 0.45: 1.395, 0.46: 1.371, 0.47: 1.349, 0.48: 1.327, 0.49: 1.306, 0.5: 1.287, 0.51: 1.268, 0.52: 1.25, 0.53: 1.232, 0.54: 1.216, 0.55: 1.2, 0.56: 1.184, 0.57: 1.17, 0.58: 1.155, 0.59: 1.142, 0.6: 1.129, 0.61: 1.116, 0.62: 1.104, 0.63: 1.092, 0.64: 1.081, 0.65: 1.07, 0.66: 1.06, 0.67: 1.049, 0.68: 1.04, 0.69: 1.03, 0.7: 1.021, 0.71: 1.012, 0.72: 1.004, 0.73: 0.996, 0.74: 0.988, 0.75: 0.98, 0.76: 0.973, 0.77: 0.966, 0.78: 0.959}, 45: {0.01: 45.935, 0.02: 23.06, 0.03: 15.436, 0.04: 11.624, 0.05: 9.337, 0.06: 7.813, 0.07: 6.724, 0.08: 5.908, 0.09: 5.273, 0.1: 4.766, 0.11: 4.351, 0.12: 4.005, 0.13: 3.712, 0.14: 3.462, 0.15: 3.245, 0.16: 3.055, 0.17: 2.888, 0.18: 2.739, 0.19: 2.606, 0.2: 2.487, 0.21: 2.378, 0.22: 2.28, 0.23: 2.191, 0.24: 2.109, 0.25: 2.033, 0.26: 1.964, 0.27: 1.9, 0.28: 1.84, 0.29: 1.785, 0.3: 1.733, 0.31: 1.685, 0.32: 1.64, 0.33: 1.597, 0.34: 1.557, 0.35: 1.52, 0.36: 1.485, 0.37: 1.451, 0.38: 1.42, 0.39: 1.39, 0.4: 1.362, 0.41: 1.335, 0.42: 1.309, 0.43: 1.285, 0.44: 1.262, 0.45: 1.24, 0.46: 1.219, 0.47: 1.199, 0.48: 1.18, 0.49: 1.161, 0.5: 1.144, 0.51: 1.127, 0.52: 1.111, 0.53: 1.095, 0.54: 1.081, 0.55: 1.066, 0.56: 1.053, 0.57: 1.04, 0.58: 1.027, 0.59: 1.015, 0.6: 1.003, 0.61: 0.992, 0.62: 0.981, 0.63: 0.971, 0.64: 0.961, 0.65: 0.951, 0.66: 0.942, 0.67: 0.933, 0.68: 0.924, 0.69: 0.916, 0.7: 0.908, 0.71: 0.9, 0.72: 0.892, 0.73: 0.885, 0.74: 0.878, 0.75: 0.871, 0.76: 0.865, 0.77: 0.859, 0.78: 0.853}, 50: {0.01: 41.342, 0.02: 20.754, 0.03: 13.892, 0.04: 10.462, 0.05: 8.403, 0.06: 7.032, 0.07: 6.052, 0.08: 5.317, 0.09: 4.746, 0.1: 4.289, 0.11: 3.916, 0.12: 3.604, 0.13: 3.341, 0.14: 3.116, 0.15: 2.92, 0.16: 2.749, 0.17: 2.599, 0.18: 2.465, 0.19: 2.345, 0.2: 2.238, 0.21: 2.141, 0.22: 2.052, 0.23: 1.972, 0.24: 1.898, 0.25: 1.83, 0.26: 1.768, 0.27: 1.71, 0.28: 1.656, 0.29: 1.606, 0.3: 1.56, 0.31: 1.516, 0.32: 1.476, 0.33: 1.438, 0.34: 1.402, 0.35: 1.368, 0.36: 1.336, 0.37: 1.306, 0.38: 1.278, 0.39: 1.251, 0.4: 1.225, 0.41: 1.201, 0.42: 1.178, 0.43: 1.157, 0.44: 1.136, 0.45: 1.116, 0.46: 1.097, 0.47: 1.079, 0.48: 1.062, 0.49: 1.045, 0.5: 1.029, 0.51: 1.014, 0.52: 1.0, 0.53: 0.986, 0.54: 0.973, 0.55: 0.96, 0.56: 0.948, 0.57: 0.936, 0.58: 0.924, 0.59: 0.913, 0.6: 0.903, 0.61: 0.893, 0.62: 0.883, 0.63: 0.874, 0.64: 0.865, 0.65: 0.856, 0.66: 0.848, 0.67: 0.84, 0.68: 0.832, 0.69: 0.824, 0.7: 0.817, 0.71: 0.81, 0.72: 0.803, 0.73: 0.797, 0.74: 0.79, 0.75: 0.784, 0.76: 0.778, 0.77: 0.773, 0.78: 0.767}, 'CA25': {0.01: 0.046, 0.02: 0.046, 0.03: 0.047, 0.04: 0.047, 0.05: 0.047, 0.06: 0.047, 0.07: 0.047, 0.08: 0.048, 0.09: 0.048, 0.1: 0.048, 0.11: 0.048, 0.12: 0.048, 0.13: 0.049, 0.14: 0.049, 0.15: 0.049, 0.16: 0.049, 0.17: 0.049, 0.18: 0.05, 0.19: 0.05, 0.2: 0.05, 0.21: 0.05, 0.22: 0.05, 0.23: 0.051, 0.24: 0.051, 0.25: 0.051, 0.26: 0.051, 0.27: 0.052, 0.28: 0.052, 0.29: 0.052, 0.3: 0.052, 0.31: 0.053, 0.32: 0.053, 0.33: 0.053, 0.34: 0.053, 0.35: 0.053, 0.36: 0.054, 0.37: 0.054, 0.38: 0.054, 0.39: 0.055, 0.4: 0.055, 0.41: 0.055, 0.42: 0.055, 0.43: 0.056, 0.44: 0.056, 0.45: 0.056, 0.46: 0.056, 0.47: 0.057, 0.48: 0.057, 0.49: 0.057, 0.5: 0.058, 0.51: 0.058, 0.52: 0.058, 0.53: 0.058, 0.54: 0.059, 0.55: 0.059, 0.56: 0.059, 0.57: 0.06, 0.58: 0.06, 0.59: 0.06, 0.6: 0.061, 0.61: 0.061, 0.62: 0.061, 0.63: 0.061, 0.64: 0.062, 0.65: 0.062, 0.66: 0.063, 0.67: 0.063, 0.68: 0.063, 0.69: 0.064, 0.7: 0.064, 0.71: 0.064, 0.72: 0.065, 0.73: 0.065, 0.74: 0.065, 0.75: 0.066, 0.76: 0.066, 0.77: 0.066, 0.78: 0}, 'CA50': {0.01: 0.023, 0.02: 0.023, 0.03: 0.023, 0.04: 0.023, 0.05: 0.023, 0.06: 0.024, 0.07: 0.024, 0.08: 0.024, 0.09: 0.024, 0.1: 0.024, 0.11: 0.024, 0.12: 0.024, 0.13: 0.024, 0.14: 0.024, 0.15: 0.024, 0.16: 0.025, 0.17: 0.025, 0.18: 0.025, 0.19: 0.025, 0.2: 0.025, 0.21: 0.025, 0.22: 0.025, 0.23: 0.025, 0.24: 0.025, 0.25: 0.026, 0.26: 0.026, 0.27: 0.026, 0.28: 0.026, 0.29: 0.026, 0.3: 0.026, 0.31: 0.026, 0.32: 0.026, 0.33: 0.026, 0.34: 0.027, 0.35: 0.027, 0.36: 0.027, 0.37: 0.027, 0.38: 0.027, 0.39: 0.027, 0.4: 0.027, 0.41: 0.028, 0.42: 0.028, 0.43: 0.028, 0.44: 0.028, 0.45: 0.028, 0.46: 0.028, 0.47: 0.028, 0.48: 0.028, 0.49: 0.029, 0.5: 0.029, 0.51: 0.029, 0.52: 0.029, 0.53: 0.029, 0.54: 0.029, 0.55: 0.029, 0.56: 0.03, 0.57: 0.03, 0.58: 0.03, 0.59: 0.03, 0.6: 0.03, 0.61: 0.03, 0.62: 0.031, 0.63: 0, 0.64: 0, 0.65: 0, 0.66: 0, 0.67: 0, 0.68: 0, 0.69: 0, 0.7: 0, 0.71: 0, 0.72: 0, 0.73: 0, 0.74: 0, 0.75: 0, 0.76: 0, 0.77: 0, 0.78: 0}, 'CA60': {0.01: 0.019, 0.02: 0.019, 0.03: 0.019, 0.04: 0.019, 0.05: 0.02, 0.06: 0.02, 0.07: 0.02, 0.08: 0.02, 0.09: 0.02, 0.1: 0.02, 0.11: 0.02, 0.12: 0.02, 0.13: 0.02, 0.14: 0.02, 0.15: 0.02, 0.16: 0.02, 0.17: 0.021, 0.18: 0.021, 0.19: 0.021, 0.2: 0.021, 0.21: 0.021, 0.22: 0.021, 0.23: 0.021, 0.24: 0.021, 0.25: 0.021, 0.26: 0.021, 0.27: 0.021, 0.28: 0.022, 0.29: 0.022, 0.3: 0.022, 0.31: 0.022, 0.32: 0.022, 0.33: 0.022, 0.34: 0.022, 0.35: 0.022, 0.36: 0.022, 0.37: 0.022, 0.38: 0.023, 0.39: 0.023, 0.4: 0.023, 0.41: 0.023, 0.42: 0.023, 0.43: 0.023, 0.44: 0.023, 0.45: 0.023, 0.46: 0.023, 0.47: 0.024, 0.48: 0.024, 0.49: 0.024, 0.5: 0.024, 0.51: 0.024, 0.52: 0.024, 0.53: 0.024, 0.54: 0.024, 0.55: 0.025, 0.56: 0.025, 0.57: 0.025, 0.58: 0.025, 0.59: 0, 0.6: 0, 0.61: 0, 0.62: 0, 0.63: 0, 0.64: 0, 0.65: 0, 0.66: 0, 0.67: 0, 0.68: 0, 0.69: 0, 0.7: 0, 0.71: 0, 0.72: 0, 0.73: 0, 0.74: 0, 0.75: 0, 0.76: 0, 0.77: 0, 0.78: 0}}
    res = pd.DataFrame.from_dict(dict_kc_ks)

    # res = pd.read_sql(sql1, conn)
    #res.set_index('index', inplace=True)
    return res

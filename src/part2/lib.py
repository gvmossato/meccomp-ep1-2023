# ============================= #
# Funções de suporte da Parte 2 #
# ============================= #

import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt


class Car:
    def __init__(self, x_range, y_range, h):
        self.x_center = (x_range[1] - x_range[0]) / 2
        self.y_center = h
        self.h_x = x_range[2]
        self.h_y = y_range[2]
        self.radius = 1.5

        self.x_min = self.x_center - self.radius
        self.x_max = self.x_center + self.radius

        self.xv_car, self.yv_car = self._gen_x_referred_nodes()
        self.xh_car, self.yh_car = self._gen_y_referred_nodes()
        self.plot_countour = self._gen_plot_countour()

    def _gen_x_referred_nodes(self):
        """
        Generates nodes with uniformly spaced abscissas, useful for
        calculating vertical distances in irreg contours.

        Returns:
            None
        """
        def y(x): return np.sqrt(self.radius**2 - (x-self.x_center)**2) + self.y_center

        x_arc = np.arange(
            self.x_center - self.radius,
            self.x_center + self.radius,
            self.h_x,
        )
        y_arc = y(x_arc)

        x_line = np.arange(
            self.x_center + self.radius,
            self.x_center - self.radius,
            -self.h_x,
        )
        y_line = np.ones(len(x_line)) * self.y_center

        x_car = np.hstack([x_arc, x_line])
        y_car = np.hstack([y_arc, y_line])
        return x_car, y_car

    def _gen_y_referred_nodes(self):
        """
        Generates nodes with uniformly spaced ordinateds, useful for
        calculating horizontal distances in irreg contours.

        Returns:
            None
        """
        def x(y): return np.sqrt(self.radius**2 - (y-self.y_center)**2) + self.x_center
        def y_mirror_semicircle(x_vals, x_center): return x_vals - 2*(x_vals-x_center)

        y_arc = np.arange(
            self.y_center,
            self.y_center + self.radius + self.h_y,
            self.h_y,
        )
        # Round avoids negatives in square root due to numerical error
        x_arc = x(np.round(y_arc, 2))
        x_arc_mirrored = y_mirror_semicircle(x_arc, self.x_center)

        y_car = np.hstack([y_arc, np.flip(y_arc[:-1])])
        x_car = np.hstack([x_arc_mirrored, np.flip(x_arc[:-1])])
        return x_car, y_car

    def _gen_plot_countour(self):
        return [
            go.Scatter3d(
                x=self.xh_car.ravel(),
                y=self.yh_car.ravel(),
                z=np.zeros(self.xh_car.shape).ravel(),
                mode="markers",
                showlegend=False,
                marker=dict(color="#000000", size=4),
            ),
            go.Scatter3d(
                x=self.xv_car.ravel(),
                y=self.yv_car.ravel(),
                z=np.zeros(self.xv_car.shape).ravel(),
                mode="markers",
                showlegend=False,
                marker=dict(color="#000000", size=4),
            ),
        ]

    def _specify_node_region(self, coordinates):
        def is_within_range(v, v_min, v_max):
            return (
                v_min < v < v_max
                or np.isclose(v, v_min)
                or np.isclose(v, v_max)
            )

        x, y = coordinates

        if (
            y < self.y_center
            and not np.isclose(y, self.y_center)
        ): return None
        if (
            np.isclose(y, self.y_center)
            and is_within_range(x, self.x_min, self.x_max)
        ): return 'line'

        center_distance = np.sqrt((x-self.x_center)**2 + (y-self.y_center)**2)

        if (
            not np.isclose(center_distance, self.radius)
            and center_distance < self.radius
        ): return 'interior'
        if (
            np.isclose(center_distance, self.radius)
        ): return 'arc'
        return None

    def get_normal_versors(self, x_vals, y_vals):
        x_lens = x_vals - self.x_center
        y_lens = y_vals - self.y_center
        lengths = np.sqrt(x_lens**2 + y_lens**2)
        return np.array([x_lens, y_lens]) / lengths


class Tunnel:
    def __init__(self, x_range, y_range, attributes, constants):
        self.C_params = attributes["C"]
        self.v_params = attributes["v"]
        self.u_params = attributes["u"]
        self.T_params = attributes["T"]
        self.z_params = attributes["z"]
        self.w_params = attributes["w"]

        self.V = constants["V"]

        self.k = constants["k"]
        self.cp = constants["cp"]
        self.rho = constants["rho"]
        self.gamma = constants["gamma"]

        self.T_in = constants["T_in"]
        self.T_out = constants["T_out"]
        self.T_engine = constants["T_engine"]

        self.F = None
        self.Q = None

        self.car = Car(x_range, y_range, constants["h"])

        self.h_x, self.h_y, self.x_vals, self.y_vals = self._gen_ranges(x_range, y_range)
        self.n_i, self.n_j = len(self.y_vals), len(self.x_vals)
        self.x_grid, self.y_grid, self.meshgrid = self._gen_initial_grid()

        self._set_node_attributes({
            "C": self.C_params,
            "u": self.u_params,
            "v": self.v_params,
            "T": self.T_params,
            "w": self.w_params,
            "z": self.z_params,
        })

        self._update_grid_irregs()
        self._update_corners()
        self._evaluate_general_coeffs()

    def _gen_ranges(self, x_range, y_range):
        x_start, x_stop, x_step = x_range
        y_start, y_stop, y_step = y_range

        h_x = x_step
        h_y = y_step

        x_vals = np.arange(x_start, x_stop+h_x, h_x)
        y_vals = np.arange(y_start, y_stop+h_y, h_y)
        return h_x, h_y, x_vals, y_vals

    def _get_primitive_matrix(self, element):
        return np.array([[element] * self.n_j] * self.n_i)

    def _find_car_node_params_by_region(self, node, name):
        if name != 'T':
            return {
                "coeffs"   : lambda T, n: [0, 0, 0, 0, 0],
                "value"    : 0,
                "color"    : "rgba(0, 0, 0, 0)",
                "constant" : True,
            }

        x_diff = node.x - self.car.x_center
        y_diff = node.y - self.car.y_center

        angle = np.arctan2(y_diff, x_diff)
        threshold = np.deg2rad(60)

        if angle < threshold or np.isclose(angle, threshold):
            return {
                "coeffs"   : lambda T, n: [0, 0, 0, 0, 0],
                "value"    : self.T_engine,
                "color"    : "#7D0000", # Vinho
                "constant" : True,
            }

        return {
            "coeffs"   : lambda T, n: [0, 0, 0, 0, 0],
            "value"    : self.T_in,
            "color"    : "#FA8C8C", # Vermelho Claro
            "constant" : True,
        }

    def _find_node_params_by_region(self, node, params):
        for i in range(len(params["regions"])):
            lower_x, upper_x, lower_y, upper_y = params["regions"][i]

            x_tests = [
                lower_x <= node.x <= upper_x,
                np.isclose(node.x, lower_x) or np.isclose(node.x, upper_x),
            ]
            y_tests = [
                lower_y <= node.y <= upper_y,
                np.isclose(node.y, lower_y) or np.isclose(node.y, upper_y),
            ]

            if np.any(x_tests) and np.any(y_tests):
                return {
                    "coeffs"   : params["coeffs"][i],
                    "value"    : params["initials"][i],
                    "constant" : params["constant"][i],
                    "color"    : params["colors"][i],
                }
        raise ValueError(f"Unable to assign params for {(node.x, node.y)}")

    def _gen_initial_grid(self):
        x_grid, y_grid = np.meshgrid(self.x_vals, self.y_vals)

        meshgrid = self._get_primitive_matrix(None)
        for i in range(self.n_i):
            for j in range(self.n_j):
                indexes = (i, j)
                coordinates = (self.x_vals[j], self.y_vals[i])
                car_loc = self.car._specify_node_region(coordinates)

                meshgrid[i, j] = Node(
                    indexes,
                    coordinates,
                    car_loc,
                )
        return x_grid, y_grid, meshgrid

    def _set_node_attributes(self, attributes):
        for node in self.meshgrid.ravel():
            for name, params in attributes.items():
                if node.is_car:
                    node_params = self._find_car_node_params_by_region(node, name)
                else:
                    node_params = self._find_node_params_by_region(node, params)
                node.set_attribute(name, node_params)

    def get_adjacents_values(self, adjacents, attribute, add_constant=True):
        attribute_values = [
            0 if node is None
              else node.get_attribute_value(attribute)
              for node in adjacents
        ]
        return attribute_values + ([1] if add_constant else [])

    def get_adjacents_nodes(self, node, direction='both', include_self=False):
        if direction not in ['row', 'col', 'both']:
            raise ValueError(f"Unexpected direction `{direction}`")

        i, j = node.i, node.j

        if direction == 'both': adjacents_idxs = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
        elif direction == 'row': adjacents_idxs = [(i, j+2), (i, j+1), (i, j-1), (i, j-2)]
        else: adjacents_idxs = [(i+2, j), (i+1, j), (i-1, j), (i-2, j)]

        if include_self: adjacents_idxs = [(i, j)] + adjacents_idxs

        return [
            self.meshgrid[row_idx, col_idx]
                if (0 <= row_idx < self.n_i) and (0 <= col_idx < self.n_j)
                else None
                for row_idx, col_idx in adjacents_idxs
        ]

    def _adjust_irreg_distances(self, node, irregs_locs_candidates):
        def idxs_of(arr, val): return np.nonzero(np.isclose(arr, val))
        def shortest(arr, val): return np.min(np.abs(arr - val))

        i, j = node.i, node.j
        irregs_locs = ''
        for c in irregs_locs_candidates:
            if c in ["r", "l"]:
                equal_y_idxs = idxs_of(self.car.yh_car, node.y)
                distance = shortest(self.car.xh_car[equal_y_idxs], node.x)
                adjustment_factor = distance / self.h_x

                if np.isclose(adjustment_factor, 1.0): continue

                self.meshgrid[i, j].a = adjustment_factor
                irregs_locs += c
            elif c == "b":
                equal_x_idxs = idxs_of(self.car.xv_car, node.x)
                distance = shortest(self.car.yv_car[equal_x_idxs], node.y)
                adjustment_factor = distance / self.h_y

                if np.isclose(adjustment_factor, 1.0): continue

                self.meshgrid[i, j].b = adjustment_factor
                irregs_locs += c
            else:
                raise ValueError(f'Unexpected irregular location `{c}`')
        return irregs_locs

    def _get_car_adjacents_locs(self, adjacents):
        top, right, bottom, left = [
            node.is_car if node is not None else False for node in adjacents
        ]
        return "".join( # Consolidate one or two car node adjacencies
            c for c in [bottom and "b", right and "r", left and "l"] if c
        )

    def _update_irreg_params(self, node, irregs_locs):
        if node.a is None and node.b is None: return

        i, j = node.i, node.j
        for param in ["coeffs", "color"]:
            self.meshgrid[i, j].C[param] = self.C_params["irregs"][irregs_locs][param]
            self.meshgrid[i, j].T[param] = self.T_params["irregs"][irregs_locs][param]

            if irregs_locs not in ['r', 'l']:
                self.meshgrid[i, j].u[param] = self.u_params["irregs"][irregs_locs][param]
                self.meshgrid[i, j].w[param] = self.w_params["irregs"][irregs_locs][param]
            if irregs_locs != 'b':
                self.meshgrid[i, j].v[param] = self.v_params["irregs"][irregs_locs][param]
                self.meshgrid[i, j].z[param] = self.z_params["irregs"][irregs_locs][param]

    def _update_grid_irregs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                node = self.meshgrid[i, j]

                if node.is_car: continue

                adjacents = self.get_adjacents_nodes(node)
                irregs_locs_candidates = self._get_car_adjacents_locs(adjacents)

                if irregs_locs_candidates:
                    irregs_locs = self._adjust_irreg_distances(node, irregs_locs_candidates)
                    self._update_irreg_params(node, irregs_locs)

    def _update_corners(self):
        for param in ["coeffs", "color", "initial", "constant"]:
            self.meshgrid[ 0,  0].C[param] = self.C_params['corners']['bl'][param]
            self.meshgrid[-1,  0].C[param] = self.C_params['corners']['tl'][param]
            self.meshgrid[-1, -1].C[param] = self.C_params['corners']['tr'][param]
            self.meshgrid[ 0, -1].C[param] = self.C_params['corners']['br'][param]

            self.meshgrid[ 0,  0].T[param] = self.T_params['corners']['bl'][param]
            self.meshgrid[-1,  0].T[param] = self.T_params['corners']['tl'][param]
            self.meshgrid[-1, -1].T[param] = self.T_params['corners']['tr'][param]
            self.meshgrid[ 0, -1].T[param] = self.T_params['corners']['br'][param]

    def _evaluate_general_coeffs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                if self.meshgrid[i, j].is_car: continue

                self.meshgrid[i, j].C['coeffs'] = self.meshgrid[i, j].C['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )
                self.meshgrid[i, j].u['coeffs'] = self.meshgrid[i, j].u['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )
                self.meshgrid[i, j].v['coeffs'] = self.meshgrid[i, j].v['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )
                self.meshgrid[i, j].z['coeffs'] = self.meshgrid[i, j].z['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )
                self.meshgrid[i, j].w['coeffs'] = self.meshgrid[i, j].w['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )

    def _evaluate_T_coeffs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                if self.meshgrid[i, j].is_car: continue
                self.meshgrid[i, j].T['coeffs'] = self.meshgrid[i, j].T['coeffs'](
                    self,
                    self.meshgrid[i, j],
                )

    def apply_liebmann_for(self, attribute, lamb, max_error, verbose=True):
        if attribute == 'T': self._evaluate_T_coeffs()

        liebmann = Liebmann(self, lamb, max_error, verbose)
        self.meshgrid = liebmann.solve_for(attribute)

    def get_attribute_value_matrix(self, name):
        attributes_values = {
            "C_color" : lambda n: n.C["color"],
            "C"       : lambda n: n.C["value"],
            "u_color" : lambda n: n.u["color"],
            "u"       : lambda n: n.u["value"],
            "v_color" : lambda n: n.v["color"],
            "v"       : lambda n: n.v["value"],
            "S"       : lambda n: n.S["value"],
            "p"       : lambda n: n.p["value"],
            "T"       : lambda n: n.T["value"],
            "T_color" : lambda n: n.T["color"],
            "z_color" : lambda n: n.z["color"],
            "z"       : lambda n: n.z["value"],
            "w_color" : lambda n: n.w["color"],
            "w"       : lambda n: n.w["value"],
            "q"       : lambda n: n.q["value"],
        }

        if name not in attributes_values:
            raise ValueError(f"Unexpected value '{name}' passed to `name`")

        matrix = (
            self._get_primitive_matrix(None)
                if "color" in name
                else self._get_primitive_matrix(0.0)
        )
        for node in self.meshgrid.ravel():
            matrix[node.i, node.j] = attributes_values[name](node)
        return matrix

    def _get_car_adjacents(self, split=False):
        def sort_nodes(arc, line):
            arc_mid = int(len(arc) / 2)
            sorted_arc = sorted(arc, key=lambda n: n.x)
            asc_quarter = sorted_arc[:arc_mid]
            desc_quarter = sorted(sorted_arc[arc_mid:], key=lambda n: (n.x, -n.y))

            desc_line = sorted(line, key=lambda n: -n.x)
            return (asc_quarter + desc_quarter, desc_line)

        arc_adjacents = []
        line_adjacents = []
        under_car = self.car.y_center - self.h_y

        for node in self.meshgrid.ravel():
            if node.is_car: continue

            car_adjacent = np.any([n.is_car for n in self.get_adjacents_nodes(node) if n])
            if not car_adjacent: continue

            if np.isclose(node.y, under_car):
                line_adjacents.append(node)
            else:
                arc_adjacents.append(node)

        sorted_arc, sorted_line = sort_nodes(arc_adjacents, line_adjacents)
        return (sorted_arc, sorted_line) if split else (sorted_arc + sorted_line)

    def _calculate_pressure(self):
        for node in self.meshgrid.ravel():
            node.set_attribute_value(
                'p',
                self.rho
                * (self.gamma - 1) / self.gamma
                * (self.V**2 - node.S['value']**2) / 2
            )

    def _calculate_lift_force(self):
        def arr_mean(arr): return (arr[1:] + arr[:-1]) / 2
        def arr_diff(arr): return arr[:-1] - arr[1:]

        def arc_force(nodes):
            pressures = np.array([n.p["value"] for n in nodes])
            abscisses = np.array([n.x for n in nodes])
            ordinates = np.array([n.y for n in nodes])

            # Assumes that x and y distances may not be self.h_x and self.h_y
            x_distances = arr_diff(abscisses)
            y_distances = arr_diff(ordinates)
            distances = np.sqrt(x_distances**2 + y_distances**2)

            midpoint_ordinates = arr_mean(ordinates)
            midpoint_pressures = arr_mean(pressures)

            # Lift force <=> Vertical component only (sine)
            normal_vec_sines = (midpoint_ordinates - self.car.y_center) / self.car.radius
            return np.sum(midpoint_pressures * distances * normal_vec_sines)

        def line_force(nodes):
            pressures = np.array([n.p["value"] for n in nodes])
            midpoint_pressures = arr_mean(pressures)
            return np.sum(midpoint_pressures * self.h_x)

        arc_nodes, line_nodes = self._get_car_adjacents(split=True)
        self.F = arc_force(arc_nodes) + line_force(line_nodes)

    def _calculate_velocity(self):
        for node in self.meshgrid.ravel():
            if node.is_car: continue

            i, j = node.i, node.j

            row_adjacents = self.get_adjacents_nodes(node, direction='row', include_self=True)
            col_adjacents = self.get_adjacents_nodes(node, direction='col', include_self=True)

            row_adj_vals = self.get_adjacents_values(row_adjacents, 'C', add_constant=False)
            col_adj_vals = self.get_adjacents_values(col_adjacents, 'C', add_constant=False)

            # v is vertical component of S, but is calculated from the horizontal component (row) of C
            v = self.meshgrid[i, j].calc_updated('v', row_adj_vals)
            u = self.meshgrid[i, j].calc_updated('u', col_adj_vals)

            self.meshgrid[i, j].set_attribute_value('v', v)
            self.meshgrid[i, j].set_attribute_value('u', u)

            # Considerating there's is a "constant" property in nodes attributes the calculated
            # value maybe was not set, therefore we get the values again for consistency
            v = self.meshgrid[i, j].get_attribute_value('v')
            u = self.meshgrid[i, j].get_attribute_value('u')

            magnitude = np.sqrt(v**2 + u**2)
            self.meshgrid[i, j].set_attribute_value('S', magnitude)

    def _calculate_car_heat_flux(self):
        def arr_mean(arr): return (arr[1:] + arr[:-1]) / 2
        def arr_diff(arr): return arr[:-1] - arr[1:]
        def dot_prod(x1, y1, x2, y2): return x1 * x2 + y1 * y2

        def arc_flux(nodes):
            x_heats = np.array([n.z["value"] for n in nodes])
            y_heats = np.array([n.w["value"] for n in nodes])

            abscisses = np.array([n.x for n in nodes])
            ordinates = np.array([n.y for n in nodes])

            # Assumes that x and y distances may not be self.h_x and self.h_y
            x_distances = arr_diff(abscisses)
            y_distances = arr_diff(ordinates)
            distances = np.sqrt(x_distances**2 + y_distances**2)

            midpoint_abscisses = arr_mean(abscisses)
            midpoint_ordinates = arr_mean(ordinates)
            midpoint_x_heats = arr_mean(x_heats)
            midpoint_y_heats = arr_mean(y_heats)

            normal_versors_x, normal_versors_y = self.car.get_normal_versors(
                midpoint_abscisses,
                midpoint_ordinates
            )
            normal_flux = dot_prod(
                normal_versors_x,
                normal_versors_y,
                midpoint_x_heats,
                midpoint_y_heats,
            )
            return np.sum(normal_flux * distances)

        def line_flux(nodes):
            y_heats = np.array([n.w["value"] for n in nodes])
            midpoint_heats = arr_mean(y_heats)
            return np.sum(midpoint_heats * self.h_x)

        arc_nodes, line_nodes = self._get_car_adjacents(split=True)
        self.Q = arc_flux(arc_nodes) + line_flux(line_nodes)

    def _calculate_heat_flux(self):
        for node in self.meshgrid.ravel():
            if node.is_car: continue

            i, j = node.i, node.j

            row_adjacents = self.get_adjacents_nodes(node, direction='row', include_self=True)
            col_adjacents = self.get_adjacents_nodes(node, direction='col', include_self=True)

            row_adj_vals = self.get_adjacents_values(row_adjacents, 'T', add_constant=False)
            col_adj_vals = self.get_adjacents_values(col_adjacents, 'T', add_constant=False)

            z = self.meshgrid[i, j].calc_updated('z', row_adj_vals)
            w = self.meshgrid[i, j].calc_updated('w', col_adj_vals)

            self.meshgrid[i, j].set_attribute_value('z', z)
            self.meshgrid[i, j].set_attribute_value('w', w)

            # Considerating there's is a "constant" property in nodes attributes the calculated
            # value maybe was not set, therefore we get the values again for consistency
            z = self.meshgrid[i, j].get_attribute_value('z')
            w = self.meshgrid[i, j].get_attribute_value('w')

            magnitude = np.sqrt(z**2 + w**2)
            self.meshgrid[i, j].set_attribute_value('q', magnitude)

    def calculate(self, attribute):
        attributes_calcs = {
            'V'    : lambda: self._calculate_velocity(),
            'p'    : lambda: self._calculate_pressure(),
            'F'    : lambda: self._calculate_lift_force(),
            'q'    : lambda: self._calculate_heat_flux(),
            'qcar' : lambda: self._calculate_car_heat_flux(),
        }

        if attribute not in attributes_calcs:
            raise ValueError(f"Unexpected value '{attribute}' passed to `attribute`")
        return attributes_calcs[attribute]()

    def plot_meshgrid(self, which):
        if which not in ["C", "u", "v", "T", "w", "z"]:
            raise ValueError(f"Unexpected value '{which}' passed to `which`")

        mesh_x_grid = self.x_grid
        mesh_y_grid = self.y_grid
        mesh_z_grid = np.zeros(self.x_grid.shape)
        mesh_color = self.get_attribute_value_matrix(f"{which}_color")

        plot_data = []
        plot_data.append(
            go.Scatter3d(
                x=mesh_x_grid.ravel(),
                y=mesh_y_grid.ravel(),
                z=mesh_z_grid.ravel(),
                mode="markers",
                showlegend=False,
                marker=dict(color=mesh_color.ravel(), size=4),
            )
        )

        if which != 'T': plot_data.extend(self.car.plot_countour)

        line_style = dict(color="#A3A3A3", width=2)
        for i, j, k in zip(mesh_x_grid, mesh_y_grid, mesh_z_grid):
            plot_data.append(
                go.Scatter3d(
                    x=i, y=j, z=k,
                    mode="lines",
                    line=line_style,
                    hoverinfo="none",
                    showlegend=False,
                )
            )
        for i, j, k in zip(mesh_x_grid.T, mesh_y_grid.T, mesh_z_grid.T):
            plot_data.append(
                go.Scatter3d(
                    x=i, y=j, z=k,
                    mode="lines",
                    line=line_style,
                    hoverinfo="none",
                    showlegend=False,
                )
            )

        fig = go.Figure(data=plot_data)
        fig.show()

    def _plot_C(self):
        title = "Função de Corrente do Escoamento"
        zlabel = "Ψ"
        C_grid = self.get_attribute_value_matrix('C')

        fig = go.Figure(data=[go.Surface(
            x=self.x_grid,
            y=self.y_grid,
            z=C_grid,
            colorscale='Viridis',
        )])
        fig.update_traces(
            contours_z=dict(
                show=True,
                project_z=True,
                color ='lightgreen',
                highlightcolor="limegreen",
                width=3,
                start=np.min(C_grid),
                end=np.max(C_grid),
                size=2,
            )
        )
        return fig, title, zlabel

    def _plot_T_heatmap(self):
        title = "Temperatura no Túnel (℃)"
        zlabel = "Temeratura (℃)"

        fig = go.Figure(data=[go.Heatmap(
            x=self.x_vals,
            y=self.y_vals,
            z=self.get_attribute_value_matrix('T') - 273.15,
            colorscale='Inferno',
        )])
        return fig, title, zlabel

    def _plot_T_surface(self):
        title = "Temperatura no Túnel (℃)"
        zlabel = "Temeratura (℃)"

        fig = go.Figure(data=[go.Surface(
            x=self.x_grid,
            y=self.y_grid,
            z=self.get_attribute_value_matrix('T') - 273.15,
            colorscale='Inferno',
        )])
        return fig, title, zlabel

    def _plot_V(self):
        plt.style.use('seaborn')
        plt.ion()
        plt.figure()
        plt.quiver(
            self.x_grid,
            self.y_grid,
            self.get_attribute_value_matrix('u'), # Horizontal
            self.get_attribute_value_matrix('v'), # Vertical
            self.get_attribute_value_matrix('S'), # Magnitude
            cmap=plt.cm.viridis,
            pivot='mid',
        )
        plt.pause(0.001)

        plt.title("Distribuição de Velocidades (m/s)")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.colorbar()

        plt.show()
        return None

    def _plot_q(self):
        plt.style.use('seaborn')
        plt.ion()
        plt.figure()
        plt.quiver(
            self.x_grid,
            self.y_grid,
            self.get_attribute_value_matrix('z'),
            self.get_attribute_value_matrix('w'),
            self.get_attribute_value_matrix('q'),
            cmap=plt.cm.plasma,
            scale=100,
        )
        plt.pause(0.001)

        plt.title("Fluxo de calor (W)")
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.colorbar()

        plt.show()
        return None

    def _plot_p(self):
        title = "Pressão Relativa"
        zlabel = "Pressão (Pa)"

        fig = go.Figure(data=[go.Surface(
            x=self.x_grid,
            y=self.y_grid,
            z=self.get_attribute_value_matrix('p'),
            colorscale='Jet',
        )])
        return fig, title, zlabel

    def _plot_pcar(self):
        title = "Pressão Relativa ao Longo da Carroceria (Pa)"
        zlabel = "Presão (Pa)"

        nodes = self._get_car_adjacents()
        plot_data = np.array([[n.x, n.y, n.p['value']] for n in nodes])
        x, y, z = plot_data[:, 0], plot_data[:, 1], plot_data[:, 2]
        minimun = plot_data[np.argmin(z), :]

        shapes = [
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='lines+markers',
                line=dict(color=z, width=2),
                marker=dict(color=z, size=4, colorscale='Jet'),
            ),
            go.Scatter3d(
                x=[minimun[0]],
                y=[minimun[1]],
                z=[minimun[2]],
                mode='markers',
                marker=dict(color="#FF0000", size=8),
            ),
        ]
        fig = go.Figure(data=shapes)
        return fig, title, zlabel

    def plot(self, attribute):
        plot_generators = {
            'C'     : lambda: self._plot_C(),
            'V'     : lambda: self._plot_V(),
            'p'     : lambda: self._plot_p(),
            'pcar'  : lambda: self._plot_pcar(),
            'Tsurf' : lambda: self._plot_T_surface(),
            'Tmap'  : lambda: self._plot_T_heatmap(),
            'q'     : lambda: self._plot_q()
        }

        if attribute not in plot_generators:
            raise ValueError(f"Unexpected value '{attribute}' passed to `which`")

        # Hacky: integrate matplotlib in this plotly handler function
        plot = plot_generators[attribute]()
        if plot is None: return

        fig, title, zlabel = plot
        fig.update_layout(
            title = title,
            showlegend = False,
            scene = dict(
                xaxis = dict(title="x (m)"),
                yaxis = dict(title="y (m)"),
                zaxis = dict(title=zlabel),
            )
        )
        fig.show()


class Node:
    def __init__(self, indexes, coordinates, car_loc):
        self.i, self.j = indexes
        self.x, self.y = coordinates
        self.car_loc = car_loc
        self.is_car = bool(car_loc)

        # Properties defined by Tunnel conditions
        self.a = self.b = None
        self.C = {}
        self.v = {}
        self.u = {}
        self.T = {}
        self.w = {}
        self.z = {}

        # Derived properties
        self.p = { "value": 0, "constant": False }
        self.S = { "value": 0, "constant": False }
        self.q = { "value": 0, "constant": False }

    def get_attribute_value(self, name):
        if name not in ['C', 'u', 'v', 'S', 'T', 'w', 'z', 'q']:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        return self.__dict__[name]['value']

    def set_attribute_value(self, name, value):
        if name not in ['C', 'u', 'v', 'S', 'p', 'T', 'w', 'z', 'q']:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        if self.__dict__[name]['constant']: return
        self.__dict__[name]['value'] = value

    def set_attribute(self, name, params):
        if name not in ['C', 'u', 'v', 'S', 'p', 'T',  'w', 'z', 'q']:
            raise ValueError(f"Unexpected value '{name}' passed to `name`")
        setattr(self, name, params)

    def calc_updated(self, attribute, adjacents): # This function do not sets
        attributes_update_rule = {
            "C": lambda adjs: np.sum(self.C["coeffs"] * adjs),
            "v": lambda adjs: np.sum(self.v["coeffs"] * adjs),
            "u": lambda adjs: np.sum(self.u["coeffs"] * adjs),
            "T": lambda adjs: np.sum(self.T["coeffs"] * adjs),
            "w": lambda adjs: np.sum(self.w["coeffs"] * adjs),
            "z": lambda adjs: np.sum(self.z["coeffs"] * adjs),
        }

        if attribute not in attributes_update_rule:
            raise ValueError(f"Unexpected value '{attribute}' passed to `prop`")
        return attributes_update_rule[attribute](np.array(adjacents))


class Liebmann:
    def __init__(self, tunnel, lamb, max_error, verbose):
        self.tunnel = tunnel
        self.lamb = lamb
        self.epsilon = max_error
        self.step_count = 0
        self.verbose = verbose

    def _SOR(self, new, curr):
        return self.lamb * new + (1-self.lamb) * curr

    def _get_relative_error(self, new, curr):
        # Uses tiny to prevent division by zero
        return np.max(np.abs(new - curr) / (new + np.finfo(float).tiny))

    def _next_step_for(self, attribute):
        meshgrid = self.tunnel.meshgrid

        n_rows = self.tunnel.n_i
        n_cols = self.tunnel.n_j

        for i in range(n_rows):
            for j in range(n_cols):
                if meshgrid[i, j].is_car: continue

                adjacents = self.tunnel.get_adjacents_nodes(meshgrid[i, j])
                adjacents_vals = self.tunnel.get_adjacents_values(
                    adjacents,
                    attribute,
                )

                updated_val = meshgrid[i, j].calc_updated(
                    attribute,
                    np.array(adjacents_vals),
                )
                adjusted_val = self._SOR(
                    updated_val,
                    meshgrid[i, j].get_attribute_value(attribute)
                )

                meshgrid[i, j].set_attribute_value(attribute, adjusted_val)

    def solve_for(self, attribute):
        error = np.inf

        while error >= self.epsilon:
            self.step_count += 1

            curr_tunnel = self.tunnel.get_attribute_value_matrix(attribute)
            self._next_step_for(attribute)
            new_tunnel = self.tunnel.get_attribute_value_matrix(attribute)
            error = self._get_relative_error(new_tunnel, curr_tunnel)

            if self.verbose: print(f"Erro máximo: {error}                 ", end='\r')

        if self.verbose: print()
        return self.tunnel.meshgrid

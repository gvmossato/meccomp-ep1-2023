# ============================= #
# Funções de suporte da Parte 2 #
# ============================= #

import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt

class Car:
    def __init__(self, x_range, y_range):
        self.x_center = (x_range[1] - x_range[0]) / 2
        self.y_center = (y_range[1] - y_range[0]) / 4
        self.h_x = x_range[2]
        self.h_y = y_range[2]
        self.radius = 1.5

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
        y_line = np.ones(len(x_line)) * 1.5

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

    def _contains_node(self, coordinates):
        x, y = coordinates

        if y < self.y_center: return (False, False)

        center_distance = np.sqrt((x-self.x_center)**2 + (y-self.y_center)**2)
        is_interior_node = center_distance < self.radius
        is_contour_node = np.isclose(center_distance, self.radius)

        return (is_interior_node, is_contour_node)

class Tunnel:
    def __init__(self, x_range, y_range, attributes):
        self.C_params = attributes["C"]
        self.v_params = attributes["v"]
        self.u_params = attributes["u"]

        self.V = 100.0
        self.rho = 1.25
        self.gamma = 1.4

        self.car = Car(x_range, y_range)

        self.h_x, self.h_y, self.x_vals, self.y_vals = self._gen_ranges(x_range, y_range)
        self.n_i, self.n_j = len(self.y_vals), len(self.x_vals)
        self.x_grid, self.y_grid, self.meshgrid = self._gen_initial_grid()

        self._set_node_attributes({
            "C": self.C_params,
            "u": self.u_params,
            "v": self.v_params,
        })

        self._update_grid_irregs()
        self._update_corners()
        self._evaluate_coeffs()

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

    def _find_node_params_by_region(self, node, params):
        if node.is_car:
            return {
                "coeffs" : lambda T, n: [0, 0, 0, 0, 0],
                "value"  : 0,
                "color"  : "rgba(0, 0, 0, 0)",
            }

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
                    "coeffs": params["coeffs"][i],
                    "value": params["initials"][i],
                    "color": params["colors"][i],
                }
        raise ValueError(f"Unable to assign params for {(node.x, node.y)}")

    def _gen_initial_grid(self):
        x_grid, y_grid = np.meshgrid(self.x_vals, self.y_vals)

        meshgrid = self._get_primitive_matrix(None)
        for i in range(self.n_i):
            for j in range(self.n_j):
                indexes = (i, j)
                coordinates = (self.x_vals[j], self.y_vals[i])
                car_interior, car_countour = self.car._contains_node(coordinates)

                meshgrid[i, j] = Node(
                    indexes,
                    coordinates,
                    car_interior,
                    car_countour
                )
        return x_grid, y_grid, meshgrid

    def _set_node_attributes(self, attributes):
        for node in self.meshgrid.ravel():
            for name, params in attributes.items():
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
            if irregs_locs not in ['r', 'l']:
                self.meshgrid[i, j].u[param] = self.u_params["irregs"][irregs_locs][param]
            if irregs_locs != 'b':
                self.meshgrid[i, j].v[param] = self.v_params["irregs"][irregs_locs][param]

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
        for param in ["coeffs", "color"]:
            self.meshgrid[ 0,  0].C[param] = self.C_params['corners']['bl'][param]
            self.meshgrid[-1,  0].C[param] = self.C_params['corners']['tl'][param]
            self.meshgrid[-1, -1].C[param] = self.C_params['corners']['tr'][param]
            self.meshgrid[ 0, -1].C[param] = self.C_params['corners']['br'][param]

    def _evaluate_coeffs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                if self.meshgrid[i, j].is_car: continue

                self.meshgrid[i, j].C['coeffs'] = self.meshgrid[i, j].C['coeffs'](
                    self,               # Tunnel
                    self.meshgrid[i, j] # Node itself
                )
                self.meshgrid[i, j].u['coeffs'] = self.meshgrid[i, j].u['coeffs'](
                    self,               # Tunnel
                    self.meshgrid[i, j] # Node itself
                )
                self.meshgrid[i, j].v['coeffs'] = self.meshgrid[i, j].v['coeffs'](
                    self,               # Tunnel
                    self.meshgrid[i, j] # Node itself
                )

    def apply_liebmann_for(self, attribute, lamb, max_error):
        liebmann = Liebmann(self, lamb, max_error)
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

    def _get_car_adjacents(self):
        nodes_in = []
        nodes_out = []
        for i in range(self.n_i):
            for j in range(self.n_j-1):
                curr = self.meshgrid[i, j]
                post = self.meshgrid[i, j+1]

                if not curr.is_car and post.is_car: nodes_in.append(curr)
                if curr.is_car and not post.is_car: nodes_out.append(post)
        nodes_out.reverse()
        return nodes_in + nodes_out

    def _calculate_pressure(self):
        for node in self.meshgrid.ravel():
            node.set_attribute_value(
                'p',
                self.rho
                * (self.gamma - 1) / self.gamma
                * (self.V**2 - node.S['value']**2) / 2
            )

    def _calculate_velocity(self):

        for node in self.meshgrid.ravel():
            if node.is_car: continue

            i, j = node.i, node.j

            row_adjacents = self.get_adjacents_nodes(node, direction='row', include_self=True)
            col_adjacents = self.get_adjacents_nodes(node, direction='col', include_self=True)

            row_adj_vals = self.get_adjacents_values(row_adjacents, 'C', add_constant=False)
            col_adj_vals = self.get_adjacents_values(col_adjacents, 'C', add_constant=False)

            v = self.meshgrid[i, j].calc_updated('v', row_adj_vals)
            u = self.meshgrid[i, j].calc_updated('u', col_adj_vals)



            magnitude = np.sqrt(v**2 + u**2)

            self.meshgrid[i, j].set_attribute_value('v', v)
            self.meshgrid[i, j].set_attribute_value('u', u)
            self.meshgrid[i, j].set_attribute_value('S', magnitude)

    def calculate(self, attribute):
        attributes_calcs = {
            'V'  : lambda: self._calculate_velocity(),
            'p'  : lambda: self._calculate_pressure(),
        }

        if attribute not in attributes_calcs:
            raise ValueError(f"Unexpected value '{attribute}' passed to `attribute`")
        return attributes_calcs[attribute]()

    def plot_meshgrid(self, which):
        if which not in ["C", "u", "v"]:
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

        plot_data.extend(self.car.plot_countour)

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

    def _plot_V(self):
        plt.style.use('seaborn')
        plt.ion()
        plt.quiver(
            self.x_grid,
            self.y_grid,
            self.get_attribute_value_matrix('u'),
            self.get_attribute_value_matrix('v'),
            self.get_attribute_value_matrix('S'),
            cmap=plt.cm.viridis,
        )
        plt.pause(0.001)
        plt.show()
        return None

    def _plot_p(self):
        title = "Pressão no túnel de vento"
        zlabel = "P"

        fig = go.Figure(data=[go.Surface(
            x=self.x_grid,
            y=self.y_grid,
            z=self.get_attribute_value_matrix('p'),
            colorscale='Jet',
        )])
        return fig, title, zlabel

    def _plot_pcar(self):
        title = "Pressão na carroceria (mínimo em destaque)"
        zlabel = "P"

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
            'C'    : lambda: self._plot_C(),
            'V'    : lambda: self._plot_V(),
            'p'    : lambda: self._plot_p(),
            'pcar' : lambda: self._plot_pcar(),
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
                xaxis = dict(title="x"),
                yaxis = dict(title="y"),
                zaxis = dict(title=zlabel),
            )
        )
        fig.show()


class Node:
    def __init__(self, index, locs, is_car_interior, is_car_countour):
        self.i, self.j = index
        self.x, self.y = locs
        self.a = self.b = None

        self.is_car_interior = is_car_interior
        self.is_car_countour = is_car_countour
        self.is_car = is_car_interior or is_car_countour

        self.C = {}
        self.v = {}
        self.u = {}
        self.S = { "value": 0 }
        self.p = {}

    def get_attribute_value(self, name):
        if name not in ['C', 'u', 'v', 'S']:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        return self.__dict__[name]['value']

    def set_attribute_value(self, name, value):
        if name not in ['C', 'u', 'v', 'S', 'p']:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        self.__dict__[name]['value'] = value

    def set_attribute(self, name, params):
        if name not in ['C', 'u', 'v', 'S', 'p']:
            raise ValueError(f"Unexpected value '{name}' passed to `name`")
        setattr(self, name, params)

    def calc_updated(self, attribute, adjacents): # This function do not sets
        attributes_update_rule = {
            "C": lambda adjs: np.sum(self.C["coeffs"] * adjs),
            "v": lambda adjs: np.sum(self.v["coeffs"] * adjs),
            "u": lambda adjs: np.sum(self.u["coeffs"] * adjs),
        }

        if attribute not in attributes_update_rule:
            raise ValueError(f"Unexpected value '{attribute}' passed to `prop`")
        return attributes_update_rule[attribute](np.array(adjacents))


class Liebmann:
    def __init__(self, tunnel, lamb, max_error):
        self.tunnel = tunnel
        self.lamb = lamb
        self.epsilon = max_error
        self.step_count = 0

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

                meshgrid[i, j].set_attribute_value(attribute, updated_val)

    def solve_for(self, attribute):
        error = np.inf

        while error >= self.epsilon:
            self.step_count += 1

            curr_tunnel = self.tunnel.get_attribute_value_matrix(attribute)
            self._next_step_for(attribute)
            new_tunnel = self.tunnel.get_attribute_value_matrix(attribute)

            error = self._get_relative_error(new_tunnel, curr_tunnel)

            print(f"Erro máximo: {error}                ", end='\r')

        print()
        return self.tunnel.meshgrid

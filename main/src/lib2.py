# ============================= #
# Funções de suporte da Parte 2 #
# ============================= #

import numpy as np
import plotly.graph_objs as go


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

    def _contains_node(self, locs):
        x, y = locs

        if y < self.y_center: return False

        center_distance = np.sqrt((x-self.x_center)**2 + (y-self.y_center)**2)
        return center_distance <= self.radius


class Tunnel:
    def __init__(self, x_range, y_range, attributes):
        self.V_params = attributes["V"]
        self.V = 100

        self.car = Car(x_range, y_range)

        self.h_x, self.h_y, self.x_vals, self.y_vals = self._gen_ranges(x_range, y_range)
        self.n_i, self.n_j = len(self.y_vals), len(self.x_vals)
        self.x_grid, self.y_grid, self.meshgrid = self._gen_initial_grid()

        self._set_node_attributes({
            "V": self.V_params,
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

    def _find_node_region(self, node, params):
        if node.is_car:
            return {
                "coeffs" : lambda T, n: [0, 0, 0, 0, 0],
                "value"  : 0,
                "color"  : "rgba(0, 0, 0, 0)",
            }

        boundaries = params["regions"]

        for i in range(len(boundaries)):
            lower_x, upper_x, lower_y, upper_y = boundaries[i]

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
                locs = (self.x_vals[j], self.y_vals[i])
                is_car = self.car._contains_node(locs)

                meshgrid[i, j] = Node(indexes, locs, is_car)
        return x_grid, y_grid, meshgrid

    def _set_node_attributes(self, attributes):
        for node in self.meshgrid.ravel():
            for name, params in attributes.items():
                node_params = self._find_node_region(node, params)
                node.set_attribute(name, node_params)

    def _get_adjacents_nodes(self, node):
        i, j = node.i, node.j
        adjacents_idxs = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

        return [
            self.meshgrid[row_idx, col_idx]
                if (0 <= row_idx < self.n_j) and (0 <= col_idx < self.n_i)
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

                if np.isclose(adjustment_factor, 1): continue

                self.meshgrid[i, j].a = adjustment_factor
                irregs_locs += c
            elif c == "b":
                equal_x_idxs = idxs_of(self.car.xv_car, node.x)
                distance = shortest(self.car.yv_car[equal_x_idxs], node.y)
                adjustment_factor = distance / self.h_y

                if np.isclose(adjustment_factor, 1): continue

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
            self.meshgrid[i, j].V[param] = self.V_params["irregs"][irregs_locs][param]

    def _update_grid_irregs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                node = self.meshgrid[i, j]

                if node.is_car: continue

                adjacents = self._get_adjacents_nodes(node)
                irregs_locs_candidates = self._get_car_adjacents_locs(adjacents)

                if irregs_locs_candidates:
                    irregs_locs = self._adjust_irreg_distances(node, irregs_locs_candidates)
                    self._update_irreg_params(node, irregs_locs)

    def _update_corners(self):
        for param in ["coeffs", "color"]:
            self.meshgrid[ 0,  0].V[param] = self.V_params['corners']['bl'][param]
            self.meshgrid[-1,  0].V[param] = self.V_params['corners']['tl'][param]
            self.meshgrid[-1, -1].V[param] = self.V_params['corners']['tr'][param]
            self.meshgrid[ 0, -1].V[param] = self.V_params['corners']['br'][param]

    def _evaluate_coeffs(self):
        for i in range(self.n_i):
            for j in range(self.n_j):
                if self.meshgrid[i, j].is_car: continue

                self.meshgrid[i, j].V['coeffs'] = self.meshgrid[i, j].V['coeffs'](
                    self,               # Tunnel
                    self.meshgrid[i, j] # Node itself
                )

    def apply_liebmann_for(self, attribute, lamb, max_error):
        liebmann = Liebmann(self, lamb, max_error)
        self.meshgrid = liebmann.solve_for(attribute)

    def get_attribute_value_matrix(self, name):
        attributes_values = {
            "V_color": lambda p: p.V["color"],
            "V": lambda p: p.V["value"],
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

    def plot_meshgrid(self, which):
        if which not in ["V"]:
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

    def _plot_V(self):
        title = "Distribuição de Velocidades"
        zlabel = "Velocidade (m/s)"
        V_grid = self.get_attribute_value_matrix('V')

        fig = go.Figure(data=[go.Surface(
            x=self.x_grid,
            y=self.y_grid,
            z=V_grid,
            colorscale='Viridis',
        )])
        fig.update_traces(
            contours_z=dict(
                show=True,
                project_z=True,
                color ='lightgreen',
                highlightcolor="limegreen",
                width=3,
                start=1,
                end=np.max(V_grid),
                size=4,
            )
        )
        return fig, title, zlabel

    def plot(self, attribute):
        map_plots = {
            'V'     : lambda: self._plot_V(),
        }

        if attribute not in map_plots:
            raise ValueError(f"Unexpected value '{attribute}' passed to `which`")

        fig, title, zlabel = map_plots[attribute]()
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
    def __init__(self, index, locs, is_car):
        self.i, self.j = index
        self.x, self.y = locs
        self.a = self.b = None
        self.is_car = is_car

        self.V = None

    def get_attribute_value(self, name):
        attributes_values = {
            "V": lambda: self.V["value"],
        }

        if name not in attributes_values:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        return attributes_values[name]()

    def set_attribute_value(self, name, value):
        if name == "V":
            self.V["value"] = value
        else:
            raise ValueError(f"Unexpected value '{name}' passed to `attribute`")
        return

    def set_attribute(self, name, params):
        if name == "V":
            self.V = params
        else:
            raise ValueError(f"Unexpected value '{name}' passed to `name`")
        return

    def update_and_get(self, attribute, adjacents):
        attributes_update_rule = {
            "V": lambda n: np.sum(self.V["coeffs"] * n),
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

        n_rows = self.tunnel.n_j
        n_cols = self.tunnel.n_i

        for i in range(n_rows):
            for j in range(n_cols):
                if meshgrid[i, j].is_car: continue

                adjacents_vals  = []
                adjacents_idxs = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]

                for row_idx, col_idx in adjacents_idxs:
                    if (0 <= row_idx < n_cols) and (0 <= col_idx < n_cols):
                        adjacents_vals.append(
                            meshgrid[row_idx, col_idx].get_attribute_value(attribute)
                        )
                    else:
                        adjacents_vals.append(0)

                adjacents_vals.append(1) # Independent variable

                updated_val = meshgrid[i, j].update_and_get(
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

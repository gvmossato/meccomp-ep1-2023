# ============================== #
# Script para solução da Parte 2 #
# ============================== #

import numpy as np

from src.utils import ctext, validate_input, line_plot
from src.part2.params import params
from src.part2.constants import constants
from src.part2.lib import Tunnel


def run_a(x_min, x_max, y_min, y_max, params, constants):
    x_ranges = [
        [x_min, x_max, 0.500],
        [x_min, x_max, 0.100],
        [x_min, x_max, 0.050],
    ]
    y_ranges = [
        [y_min, y_max, 0.500],
        [y_min, y_max, 0.100],
        [y_min, y_max, 0.050],
    ]

    for x_range, y_range in zip(x_ranges, y_ranges):
        print('\033[F', end='')
        print("Gerando novas malhas...")
        print(ctext(f"Passos: ({x_range[-1]}, {y_range[-1]})", 'm'))

        tunnel = Tunnel(x_range, y_range, params, constants)

        print(f"{ctext('Meshgrids inicializadas!', 'g')}\n\n")

        tunnel.plot_meshgrid('C')


def run_b(x_min, x_max, y_min, y_max, params, constants):
    x_range = [x_min, x_max, 0.1]
    y_range = [y_min, y_max, 0.1]

    print('\033[F', end='')
    print("Gerando novas malhas...")
    print(ctext(f"Passos: ({x_range[-1]}, {y_range[-1]})", 'm'))

    tunnel = Tunnel(x_range, y_range, params, constants)

    print(f"\n{ctext('Meshgrids inicializadas!', 'g')}")
    print("\nDeseja visualizar alguma malha com seus contornos?")

    while True:
        print(f"{ctext('C.', 'c')} Corrente de escoamento")
        print(f"{ctext('u.', 'c')} Componente horizontal do gradiente de potencial de velocidade")
        print(f"{ctext('v.', 'c')} Componente vertical do gradiente de potencial de velocidade")
        print(f"{ctext('T.', 'c')} Temperatura")
        print(f"{ctext('w.', 'c')} Componente horizontal do fluxo de calor")
        print(f"{ctext('z.', 'c')} Componente vertical do fluxo de calor")

        choosen_mesh = validate_input(
            "Entre com "
                + f"{ctext('C', 'c')}, "
                + f"{ctext('u', 'c')}, "
                + f"{ctext('v', 'c')}, "
                + f"{ctext('T', 'c')}, "
                + f"{ctext('w', 'c')}, "
                + f"{ctext('z', 'c')}, "
                + f"ou pressione {ctext('ENTER', 'g')} para continuar: ",
            ['c', 'u', 'v', 't', 'w', 'z', 'ENTER'],
            'ENTER',
        )

        if choosen_mesh == "ENTER": break

        tunnel.plot_meshgrid(
            choosen_mesh.upper() if choosen_mesh in ['c', 't'] else choosen_mesh
        )

    print('\nCalculando e plotando a corrente de escoamento...')
    tunnel.apply_liebmann_for('C', 1.85, 0.01)
    tunnel.plot('C')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a velocidade...')
    tunnel.calculate('V')
    tunnel.plot('V')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a pressão no domínio e no carro...')
    tunnel.calculate('p')
    tunnel.plot('p')
    tunnel.plot('pcar')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando força de sustentação na carroceria...')
    tunnel.calculate('F')
    print(f"{ctext('Força de sustentação:', 'b')} {tunnel.F:.2f} N")

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\nCalculando e plotando a temperatura...')
    tunnel.apply_liebmann_for('T', 1.05, 0.01)
    tunnel.plot('Tsurf')
    tunnel.plot('Tmap')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando o fluxo de calor no domínio e no carro...')
    tunnel.calculate('q')
    tunnel.calculate('qcar')
    tunnel.plot('q')
    print(f"{ctext('Fluxo de calor através da carroceria:', 'b')} {tunnel.Q:.2f} W")

def run_c(x_min, x_max, y_min, y_max, params, constants):
    x_range = [x_min, x_max, 0.1]
    y_range = [y_min, y_max, 0.1]

    results = np.zeros((len(constants["V_vals"]), len(constants["h_vals"])))

    print(ctext(f"Passos: ({x_range[-1]}, {y_range[-1]})", 'm'))

    for i, V in enumerate(constants["V_vals"]):
        constants["V"] = V

        for j, h in enumerate(constants["h_vals"]):
            constants["h"] = h

            print("\nGerando novas malhas...")

            tunnel = Tunnel(x_range, y_range, params, constants)

            print('\033[F', end='')
            print(ctext('Efetuando cálculos (0/4)...', 'y'))

            tunnel.apply_liebmann_for('C', 1.85, 0.01)

            print('\033[F', end='')
            print('\033[F', end='')
            print(ctext('Efetuando cálculos (1/4)...', 'y'))

            tunnel.calculate('V')

            print('\033[F', end='')
            print(ctext('Efetuando cálculos (2/4)...', 'y'))

            tunnel.calculate('p')

            print('\033[F', end='')
            print(ctext('Efetuando cálculos (3/4)...', 'y'))

            tunnel.calculate('F')

            print('\033[F', end='')
            print(ctext('Efetuando cálculos (4/4)...', 'y'))

            results[i, j] = tunnel.F

            print('\033[F', end='')
            print(f"Simulção para {ctext(f'h={tunnel.car.y_center:.2f} m', 'g')} e {ctext(f'V={tunnel.V:.2f} m/s', 'g')} concluída!")
            print(f"{ctext('Força de sustentação:', 'b')} {tunnel.F:.2f} N                                ")

    print('Plotando resultados...')

    line_plot(
        constants["h_vals"],
        results,
        [f"V = {v:.2f} m/s" for v in constants["V_vals"]],
        "Comportamento da Força de Sustentação",
        "Distância do Veículo ao Solo (m)",
        "Força de Sustentação no Veículo (N)",
    )

def solve(item):
    constants["V"] = constants["V_vals"][1]
    constants["h"] = constants["h_vals"][2]

    x_min = 0.0
    y_min = 0.0
    x_max = constants["d"] + constants["L"] + constants["d"]
    y_max = constants["H"]

    if item == 'a': run_a(x_min, x_max, y_min, y_max, params, constants)
    elif item == 'b': run_b(x_min, x_max, y_min, y_max, params, constants)
    else: run_c(x_min, x_max, y_min, y_max, params, constants)


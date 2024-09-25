import traceback

import sympy
from sympy import parse_expr, lambdify, plot
from sympy.abc import y

MAX_ITER = 100


def main():
    while True:
        try:
            expression = parse_expr(input("Ingrese una expresion matematica para obtener una raiz: "),
                                    transformations='all')

            variables = expression.atoms(sympy.Symbol)

            if len(variables) > 1:
                print("Solo se puede tener 1 variable por expresion, ingrese una nueva expresion.")
                continue

            var = variables.pop()

            if var == y:
                print(
                    "La variable independiente no puede tener por nombre 'y', ingrese una expresion que no la contenga.")
                continue

            print(f"Expresion entendida: y({var}) = {expression}")

            f = lambdify(var, expression)
            a = float('-inf')
            b = float('inf')
            error = float(1)

            while True:
                try:
                    a = float(input("Ingrese el valor inferior del intervalo: "))
                except SyntaxError:
                    print("El numero dado no es valido, inserte uno nuevo.")
                    continue

                break

            while True:
                try:
                    b = float(input("Ingrese el valor superior del intervalo: "))
                except SyntaxError:
                    print("El numero dado no es valido, inserte uno nuevo.")
                    continue

                if b < a:
                    print("El intervalo dado no es valido, inserte uno nuevo.")
                    continue

                break

            while True:
                try:
                    error = float(input("Ingrese el valor esperado de error: "))
                except SyntaxError:
                    print("El numero dado no es valido, inserte uno nuevo.")
                    continue

                break

            plotted_expr = plot(expression, show=False, xlim=[a, b], ylim=[f(a), f(b)])
            plotted_expr.process_series()

            try:
                value, iterations = bisection(f, a, b, error, plotted_expr.plt)
                print(
                    f"La raiz de la expresion {expression} con un error de {error}% es: {value}, obtenido despues de {iterations} iteraciones.")
            except ValueError as e:
                print(repr(e))
                break

            plotted_expr.plt.show()

            break
        except Exception as e:
            print("La expresion dada no es valida, inserte una nueva.")
            print(traceback.format_exception(e))


def bisection(f, a: float, b: float, error: float, plt) -> (float, int):
    if f(b) * f(a) > 0:
        raise ValueError("No existe una raiz en el intervalo dado")

    if f(b) * f(a) == 0:
        if f(b) == 0:
            return b, 1
        else:
            return a, 1

    curr_it = 0
    last_val = 0

    while curr_it <= MAX_ITER:
        curr_it += 1
        c = (a + b) / 2

        if c == 0:
            raise ValueError("No se puede obtener una raiz en este intervalo.")

        if abs((c - last_val) / c) * 100 <= error:
            plt.plot(c,f(c), 'ro')
            plt.annotate(f"({c}, {round(f(c),6)})", (c,f(c)), xytext=(5, -20),
                textcoords='offset points', arrowprops=dict(arrowstyle='->'))
            return c, curr_it
        elif f(c) * f(a) < 0:
            b = c
        else:
            a = c

        last_val = c
        plt.plot(c, f(c), 'go')

    raise ValueError("El número máximo de iteraciones permitidas ha sido excedido.")


if __name__ == "__main__":
    main()

import math


FUNCS = ["cos", "sin", "exp"]

class Node:
    def value(self): ...
    def derivative(self): ...

    def __repr__(self):
        return self.val


class ExprNode(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return {
            # "infer": lambda x: math.exp(x),
            "string": self.val
        }

    def derivative(self):
        constant, var, power = self._get_constant_var_pow(self.val)
        if power == "":
            return {
            # "infer": lambda x: math.exp(x),
            "string": constant,
        }
        power = int(power)
        constant = int(constant if constant != "" else 1)
        return {
            # "infer": lambda x: math.exp(x),
            "string": f"{power * constant}{var}{'^' + str(power - 1) if power != 2 else ''}"
        }

    def _get_constant_var_pow(self, expr):
        reach_pow = False
        buf, constant, var, power = "", "", "", ""
        for char in expr:
            if not char.isnumeric() and char != "^":
                var = char
                constant = buf
            else:
                buf += char
            if char == "^":
                reach_pow = True
            elif reach_pow:
                power += char

        return constant, var, power


class FuncNode(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        funcs = {
            "cos": {
                "infer": lambda x: math.cos(math.radians(x)),
                "string": "cos"
            },
            "sin": {
                "infer": lambda x: math.sin(math.radians(x)),
                "string": "sin"
            },
            "exp": {
                "infer": lambda x: math.exp(x),
                "string": "exp"
            },
        }
        return funcs[self.val]

    def derivative(self):
        derivatives = {
            "cos": {
                "infer": lambda x: -math.sin(math.radians(x)),
                "string": "-sin"
            },
            "sin": {
                "infer": lambda x: math.cos(math.radians(x)),
                "string": "cos"
            },
            "exp": {
                "infer": lambda x: math.exp(x),
                "string": "exp"
            },
        }
        return derivatives[self.val]

        
class Parser:
    def __init__(self, expr):
        self.expr = expr

    def parse(self):
        queue = []
        idx, buf = 0, ""
        for char in self.expr:
            if char in ["(", ")"]:
                queue.append(buf)
                buf = ""
            else:
                buf += char
            if char == ")":
                break
        return [self._forge_node(x) for x in queue]

    def _forge_node(self, buf: str):
        if buf in FUNCS:
            return FuncNode(buf)
        return ExprNode(buf)


class AutoDiff:
    def __init__(self, expr):
        self.parser = Parser(expr)
        self.nodes = self.parser.parse()

    def differentiate(self, x=None):
        expr = ""
        nodes = self.nodes

        for i, derivative_node in enumerate(nodes):
            expr += self._update_expr(derivative_node, derivative=True, field="string")
            for no_derivative_node in nodes[i+1:]:
                expr += self._update_expr(no_derivative_node, derivative=False, field="string")

            nb_funcs = len([n for n in nodes[i+1:] \
                if isinstance(derivative_node, FuncNode)])
            expr += ')' * nb_funcs
            expr += " * " if i != len(nodes) - 1 else ""
        return expr

    def _update_expr(self, node, derivative: bool, field: str):
        if derivative:
            expr = node.derivative()[field]
        else:
            expr = node.value()[field]
        if isinstance(node, FuncNode):
            expr += "("
        return expr

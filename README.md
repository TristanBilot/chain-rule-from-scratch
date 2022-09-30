# Automatic differentation from scracth

Simple automatic differentiation engine to differentiate simple composite functions using the chain rule. The aim of this repo is to understand easily how autodiff works and how derivatives are computed automatically inside Neural Nets framework in order to compute the gradients needed for training. 

Only `cos`, `sin`, `exp` and `pow` operations are implemented but additional ones could be easily added but require some parsing boilerplate code to develop.

## Example

```python
exp = "sin(exp(sin(5x^9)))"
derivative = AutoDiff(exp).differentiate()

derivative
# >>> "cos(exp(sin(5x^9))) * exp(sin(5x^9)) * cos(5x^9) * 45x^8"
```

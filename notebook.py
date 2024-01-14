import marimo

__generated_with = "0.1.76"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
    # Lotka-Volterra Equations

    Per [Wikipedia](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations), the Lotka-Volterra equations can be used to describe how predators and prey interact.

    The populations change over time according to the following pair of equations:

    \[
    \begin{align*}
    \frac{dx}{dt} &= \alpha x - \beta xy \\
    \frac{dy}{dt} &= \delta xy - \gamma y
    \end{align*}
    \]

    where

    $\quad \frac{dx}{dt} =$ instantaneous growth rate of prey

    $\quad \alpha =$ birth rate of prey

    $\quad x =$ current population of prey

    $\quad \beta =$ rate of predators ($y$) eating prey ($x$)

    $\quad \frac{dy}{dt} =$ instantaneous growth rate of predator

    $\quad \delta =$ birth rate of predators ($y$) based on eating prey ($x$)

    $\quad \gamma =$ natural death rate of predators

    $\quad y =$ current predator population
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    initial_prey_slider = mo.ui.slider(
        start=10, stop=100, step=10, value=50, label="Initial prey population"
    )
    alpha_slider = mo.ui.slider(
        start=1, stop=10, step=1, value=1, label=r"Birth rate of prey ($\alpha$)"
    )
    beta_slider = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=1,
        label=r"Rate of predators eating prey ($\beta$)",
    )
    initial_predator_slider = mo.ui.slider(
        start=10, stop=100, step=10, value=10, label="Initial predator population"
    )
    delta_slider = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=1,
        label=r"Birth rate of predators ($\delta$)",
    )
    gamma_slider = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=1,
        label=r"Death rate of predators ($\gamma$)",
    )
    mo.vstack(
        [
            mo.hstack([initial_prey_slider, alpha_slider, beta_slider]),
            mo.hstack([initial_predator_slider, delta_slider, gamma_slider]),
        ],
        align="center",
        gap="1.5",
    )
    return (
        alpha_slider,
        beta_slider,
        delta_slider,
        gamma_slider,
        initial_predator_slider,
        initial_prey_slider,
    )


@app.cell
def __(data, mo, plt, time_points):
    fig, (ax1, ax2) = plt.subplots(2)
    (line1,) = ax1.plot(time_points, data[:, 0], color="b")
    (line2,) = ax2.plot(time_points, data[:, 1], color="r")
    ax1.set_ylabel("Prey")
    ax2.set_ylabel("Predator")
    ax2.set_xlabel("Time")
    mo.mpl.interactive(plt.show())
    return ax1, ax2, fig, line1, line2


@app.cell(hide_code=True)
def __(
    alpha_slider,
    beta_slider,
    delta_slider,
    gamma_slider,
    initial_predator_slider,
    initial_prey_slider,
    np,
    odeint,
    solve_diff_eqs,
):
    initial_populations = [
        initial_prey_slider.value,
        initial_predator_slider.value,
    ]

    # time 0 to 50 with 1000 points between them
    time_points = np.linspace(0, 50, num=1000)

    constants = [
        alpha_slider.value,
        beta_slider.value,
        delta_slider.value,
        gamma_slider.value,
    ]

    data = odeint(
        solve_diff_eqs, initial_populations, time_points, args=(constants,)
    )
    return constants, data, initial_populations, time_points


@app.cell(hide_code=True)
def __():
    def solve_diff_eqs(populations, time, constants):
        x = populations[0]  # prey population
        y = populations[1]  # predator population

        alpha = constants[0]
        beta = constants[1]
        delta = constants[2]
        gamma = constants[3]

        dx_dt = (alpha * x) - (beta * x * y)
        dy_dt = (delta * x * y) - (gamma * y)

        return [dx_dt, dy_dt]
    return solve_diff_eqs,


@app.cell(hide_code=True)
def __():
    from scipy.integrate import odeint

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    return mo, np, odeint, plt


if __name__ == "__main__":
    app.run()

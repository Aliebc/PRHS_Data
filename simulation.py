import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Parameters
alpha = 0.6
beta = 0.35
n = 100
rho_a = 1.2
rho_b = 0.3
theta = 1
delta_a = 0
C = 4
S = 1.5
Z_a = 10
Z_b = 10
A_b = 0
A_a = 1

# Equations
def equations(vars, delta_b, alpha, beta, n, rho_a, rho_b, theta, delta_a, C, S, Z_a, Z_b, A_a, A_b):
    r_a, r_b, w_a, w_b, n_a, n_b = vars
    eq1 = (3 - delta_b) * (1 / theta * (w_b - w_a) + r_a - 1 / theta * (A_a - A_b) - S/theta * (n_b - n_a) / n) - rho_b * n_b - Z_b
    eq2 = (3 - delta_a) * (1 / theta * (w_a - w_b) + r_b - 1 / theta * (A_b - A_a) - S/theta * (n_a - n_b) / n) - rho_a * n_a - Z_a
    eq3 = w_b - w_a - theta * (r_b - r_a) - (A_a - A_b) - S * (n_b - n_a) / n
    eq4 = w_a + (1 - alpha - beta) / (1 - beta) * n_a - C
    eq5 = w_b + (1 - alpha - beta) / (1 - beta) * n_b - C
    eq6 = n_a + n_b - n
    return [eq1, eq2, eq3, eq4, eq5, eq6]

# Main function to plot the results
def plot_results(alpha=0.6, beta=0.35, n=100, rho_a=1.3, rho_b=0.2, delta_a=0, C=4, S=1.5, Z_a=10, Z_b=10, A_a=1, A_b=0):
    theta = alpha / (alpha + beta)
    theta = 0.9
    delta_b_values = np.linspace(0, 2, 100)
    
    r_a_values = []
    w_a_values = []
    n_a_values = []
    n_b_values = []

    initial_guess = [0.1, 0.1, 0.1, 0.1, 50, 50]

    for delta_b in delta_b_values:
        try:
            solution = fsolve(equations, initial_guess, args=(delta_b, alpha, beta, n, rho_a, rho_b, theta, delta_a, C, S, Z_a, Z_b, A_a, A_b))
            r_a, r_b, w_a, w_b, n_a, n_b = solution
            r_a_values.append(r_a)
            w_a_values.append(w_a)
            n_a_values.append(n_a)
            n_b_values.append(n_b)
            initial_guess = solution
        except Exception as e:
            r_a_values.append(np.nan)
            w_a_values.append(np.nan)
            n_a_values.append(np.nan)
            n_b_values.append(np.nan)

    # Plot 1: w_a and r_a
    fig, ax1 = plt.subplots(1, 2, figsize=(12, 6))

    for ax in ax1:
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    ax1[0].plot(delta_b_values, w_a_values, color='black', linewidth=1.5)
    ax1[0].set_xlabel(r'$\delta_b$', fontsize=12)
    ax1[0].set_ylabel(r'$w_a$', fontsize=12)
    ax1[0].set_title(r'Simulation of $w_a$', fontsize=14)

    ax1[1].plot(delta_b_values, r_a_values, color='black', linewidth=1.5)
    ax1[1].set_xlabel(r'$\delta_b$', fontsize=12)
    ax1[1].set_ylabel(r'$r_a$', fontsize=12)
    ax1[1].set_title(r'Simulation of $r_a$', fontsize=14)

    plt.tight_layout()
    plt.savefig('./Output/sim_wa_ra.png')
    plt.savefig('./Output/sim_wa_ra.pdf')
    plt.close(fig)

    # Plot 2: n_a and n_b
    fig, ax2 = plt.subplots(1, 2, figsize=(12, 6))

    for ax in ax2:
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    ax2[0].plot(delta_b_values, n_a_values, color='black', linewidth=1.5)
    ax2[0].set_xlabel(r'$\delta_b$', fontsize=12)
    ax2[0].set_ylabel(r'$n_a$', fontsize=12)
    ax2[0].set_title(r'Simulation of $n_a$', fontsize=14)

    ax2[1].plot(delta_b_values, n_b_values, color='black', linewidth=1.5)
    ax2[1].set_xlabel(r'$\delta_b$', fontsize=12)
    ax2[1].set_ylabel(r'$n_b$', fontsize=12)
    ax2[1].set_title(r'Simulation of $n_b$', fontsize=14)

    plt.tight_layout()
    plt.savefig('./Output/sim_na_nb.png')
    plt.savefig('./Output/sim_na_nb.pdf')
    plt.close(fig)

plot_results(alpha=alpha, beta=beta, n=n, rho_a=rho_a, rho_b=rho_b, delta_a=delta_a, C=C, S=S, Z_a=Z_a, Z_b=Z_b, A_a=A_a, A_b=A_b)

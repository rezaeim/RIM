import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class VehicleModel:
    def __init__(self, L=2.5):
        self.L = L  # Wheelbase distance

    def objective_function(self, params):
        A0, B0 = params
        tf = self.tf
        x0, v0, xf, vf = self.x0, self.v0, self.xf, self.vf

        # Define the acceleration function
        a = lambda t: A0 * t + B0

        # Define the velocity function
        v = lambda t: 0.5 * A0 * t**2 + B0 * t + v0

        # Define the position function
        x = lambda t: (1/6) * A0 * t**3 + 0.5 * B0 * t**2 + v0 * t + x0

        # Define the objective function to minimize acceleration
        integrand = lambda t: a(t)**2
        J = np.trapz(integrand(np.linspace(0, tf, 100)), np.linspace(0, tf, 100))

        return J

    def optimize_trajectory(self):
        # Perform optimization to find A0 and B0
        result = minimize(self.objective_function, x0=[0, 0], bounds=[(-10, 10), (-10, 10)])
        A0_opt, B0_opt = result.x
        return A0_opt, B0_opt

    def generate_trajectory(self, A0, B0):
        tf = self.tf
        t_values = np.linspace(0, tf, 100)
        x_values = [(1/6) * A0 * t**3 + 0.5 * B0 * t**2 + self.v0 * t + self.x0 for t in t_values]
        return t_values, x_values

    def simulate(self, x0, v0, xf, vf, tf):
        self.x0, self.v0, self.xf, self.vf, self.tf = x0, v0, xf, vf, tf

        # Optimize trajectory
        A0_opt, B0_opt = self.optimize_trajectory()

        # Generate trajectory based on optimized parameters
        t_values, x_values = self.generate_trajectory(A0_opt, B0_opt)

        return t_values, x_values

# Example usage
vehicle_model = VehicleModel()

# Define initial and final conditions
x0 = 0.0
v0 = 3.0
xf = 15.0
vf = 2.5
tf = 4.0

# Simulate trajectory
t_values, x_values = vehicle_model.simulate(x0, v0, xf, vf, tf)

# Plot the trajectory
plt.plot(t_values, x_values, label='Vehicle Trajectory')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()
plt.show()

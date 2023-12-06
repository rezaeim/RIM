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
        v_values = [0.5 * A0 * t**2 + B0 * t + self.v0 for t in t_values]
        a_values = [A0 for _ in t_values]  # Constant acceleration A0

        return t_values, x_values, v_values, a_values

    def simulate(self, x0, v0, xf, vf, tf, wcrt_delay):
        self.x0, self.v0, self.xf, self.vf, self.tf, self.wcrt_delay = x0, v0, xf, vf, tf, wcrt_delay

        # Optimize trajectory
        A0_opt, B0_opt = self.optimize_trajectory()

        # Generate trajectory based on optimized parameters
        t_values, x_values, v_values, a_values = self.generate_trajectory(A0_opt, B0_opt)

        # Simulate worst-case delay effect
        t_values_with_delay = t_values + self.wcrt_delay / 1000.0  # Convert delay to seconds

        return t_values_with_delay, x_values, v_values, a_values

# Example usage
vehicle_model = VehicleModel()

# Define scenario parameters
x0 = 0.0
v0 = 3.0
xf = 15.0
vf = 2.5
tf = 4.0
wcrt_delay = 1350.0  # Worst-case round-trip delay in milliseconds

# Simulate trajectory with worst-case delay
t_values_with_delay, x_values, v_values, a_values = vehicle_model.simulate(x0, v0, xf, vf, tf, wcrt_delay)

# Plot the trajectory, velocity, and acceleration
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t_values_with_delay, x_values, label='Position (WCRTD)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t_values_with_delay, v_values, label='Velocity (WCRTD)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t_values_with_delay, a_values, label='Acceleration (WCRTD)')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.legend()

plt.tight_layout()
plt.show()

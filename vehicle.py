import numpy as np
import matplotlib.pyplot as plt

class VehicleModel:
    def __init__(self):
        # Vehicle parameters
        self.x = 0.0  # Initial x position
        self.y = 0.0  # Initial y position
        self.theta = 0.0  # Initial heading angle
        self.v = 0.0  # Initial linear velocity
        self.L = 2.5  # Vehicle's wheelbase distance
        self.u = 0.0  # Control input for the motor (PWM signal)

        # PID controller parameters
        self.Kp = 1.0
        self.Ki = 0.1
        self.Kd = 0.01

        # Other parameters
        self.disturbance = 0.0
        self.prev_error = 0.0  # Initialize prev_error attribute

    def update_state(self, dt):
        # Vehicle dynamics based on the provided model
        Kp, Ki, Kd = self.Kp, self.Ki, self.Kd
        e = self.v - self.target_velocity()  # Error
        self.u = Kp * e + Ki * np.sum(e) * dt + Kd * (e - self.prev_error) / dt
        self.prev_error = e

        # Vehicle motion model (simplified 2D)
        self.theta += self.u * dt
        self.v = self.target_velocity()  # Placeholder: replace with your own velocity control logic
        self.x += self.v * np.cos(self.theta) * dt
        self.y += self.v * np.sin(self.theta) * dt

    def target_velocity(self):
        # Function to calculate the target velocity (can be customized)
        return 10.0  # Placeholder value; replace with the desired logic

    def apply_disturbance(self):
        # Apply external disturbance (can be customized)
        self.disturbance = 0.1 * np.random.randn()  # Placeholder value; replace with desired disturbance

    def simulate(self, duration, dt):
        # Simulation loop
        num_steps = int(duration / dt)
        trajectory = []

        for _ in range(num_steps):
            self.apply_disturbance()
            self.update_state(dt)
            trajectory.append((self.x, self.y))

        return np.array(trajectory)

# Example usage
vehicle = VehicleModel()
trajectory = vehicle.simulate(duration=10.0, dt=0.1)

# Plot the trajectory
plt.plot(trajectory[:, 0], trajectory[:, 1], label='Vehicle Trajectory')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.show()

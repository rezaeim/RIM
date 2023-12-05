import numpy as np
import matplotlib.pyplot as plt

class IntersectionManager:
    def __init__(self, vmax, vmin, amax, distance_threshold):
        self.vmax = vmax
        self.vmin = vmin
        self.amax = amax
        self.distance_threshold = distance_threshold

    def calculate_trajectory(self, toa, voa):
        # Replace this with your actual trajectory calculation logic
        a0 = 0.2  # Replace with your calculated values
        b0 = 1.0  # Replace with your calculated values
        return a0, b0

    def simulate_vehicle_trajectory(self, toa, voa):
        t = np.linspace(0, 10, 100)  # Example time points, adjust as needed
        a0, b0 = self.calculate_trajectory(toa, voa)
        velocity = a0 * t + b0
        position = 0.5 * a0 * t**2 + b0 * t
        return t, position, velocity

    def feasibility_check(self, toa, voa):
        t, position, velocity = self.simulate_vehicle_trajectory(toa, voa)

        if max(velocity) < self.vmax and min(velocity) > self.vmin:
            if max(abs(velocity)) < self.amax:
                for other_toa, other_voa in zip([1.0, 2.0, 3.0], [2.0, 3.0, 4.0]):
                    _, other_position, _ = self.simulate_vehicle_trajectory(other_toa, other_voa)
                    distance = abs(position - other_position)
                    if min(distance) < self.distance_threshold:
                        return "Not OK"

                return "OK"
            else:
                return "Not OK"
        else:
            return "Not OK"

    def plot_trajectory(self, toa, voa):
        t, position, velocity = self.simulate_vehicle_trajectory(toa, voa)

        # Plotting position vs time
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(t, position, label='Position')
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.title('Position vs Time')
        plt.legend()

        # Plotting velocity vs time
        plt.subplot(1, 2, 2)
        plt.plot(t, velocity, label='Velocity', color='orange')
        plt.xlabel('Time')
        plt.ylabel('Velocity')
        plt.title('Velocity vs Time')
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example Usage
vmax = 5.0
vmin = 1.0
amax = 2.0
distance_threshold = 2.0
im = IntersectionManager(vmax, vmin, amax, distance_threshold)
toa_example = 4.0
voa_example = 2.5
result = im.feasibility_check(toa_example, voa_example)
print(f"Feasibility Check Result: {result}")
im.plot_trajectory(toa_example, voa_example)

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def load_charges(json_data):
    return json.loads(json_data)

def electric_field(x, y, charges):
    Ex, Ey = np.zeros_like(x), np.zeros_like(y)
    k = 8.99e9  # Coulomb Constant
    
    for charge in charges:
        q = charge['value']
        sign = 1 if charge['positive'] else -1
        cx, cy = charge['position']
        
        dx, dy = x - cx, y - cy
        r2 = dx**2 + dy**2
        r = np.sqrt(r2)
        
        Ex += k * q * sign * dx / (r2 + 1e-9)  # Avoid division by zero
        Ey += k * q * sign * dy / (r2 + 1e-9)
    
    return Ex, Ey

def plot_field(particles):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    # Create grid of points
    X, Y = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
    Ex, Ey = electric_field(X, Y, particles)
    
    # Plot field lines
    ax.streamplot(X, Y, Ex, Ey, color='blue', density=1.5, linewidth=0.8, arrowstyle='->')
    
    # Plot particles
    for particle in particles:
        q = particle['value']
        sign = '+' if particle['positive'] else '-'
        cx, cy = particle['position']
        
        color = 'red' if particle['positive'] else 'blue'
        ax.add_patch(Circle((cx, cy), 0.5, color=color, fill=True))
        ax.text(cx, cy, sign, color='white', fontsize=12, ha='center', va='center', fontweight='bold')
    
    plt.show()

# JSON example with particles
json_data = '[{"value": 5, "positive": true, "position": [3, 3]}, {"value": 5, "positive": true, "position": [-3, -3]}, {"value": 7, "positive": false, "position": [5, -5]}]'
charges = load_charges(json_data)
plot_field(charges)

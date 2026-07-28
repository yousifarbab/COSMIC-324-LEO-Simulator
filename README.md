# COSMIC-324: LEO Satellite Constellation Simulation Framework

> A lightweight, efficient software framework for simulating and analyzing Low Earth Orbit (LEO) satellite constellations and routing data across space.

---

## 📌 Overview
**COSMIC-324** is an advanced MVP (Minimum Viable Product) designed specifically to help researchers, graduate students, and engineering labs simulate LEO satellite networks and routing trajectories quickly and cost-effectively, bypassing the extreme complexity and high costs of legacy proprietary software (such as STK and MATLAB).

## 👥 The Team
- **Dr. Yusif Zakria Eissa Arbab** - Co-Founder (Strategic Management, Legal & Regulatory Affairs).
- **Ali Zaid Al-Sheri** - Co-Founder (Systems Engineering, Technical Development & Documentation).

---

## ⚙️ Core Modules
The framework is built on a clean, modular Python architecture:
1. **Orbital Dynamics Module (`orbital_dynamics.py`):** Calculates 3D satellite positions and real-time spatial distances with high precision.
2. **Routing & Network Engine (`app.py`):** Uses `NetworkX` to model constellation topology and apply speed-of-light shortest-path routing algorithms.
3. **Interactive Workspace (`cosmic_simulation_demo.ipynb`):** A Jupyter notebook allowing step-by-step simulation execution and live result visualization.
4. **Visualization Layer (`Matplotlib`):** Generates graphs tracking latency evolution and handover events over time.

---

## 🚀 Installation & Quick Start

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/COSMIC-324-LEO-Simulator.git](https://github.com/YOUR_USERNAME/COSMIC-324-LEO-Simulator.git)
   cd COSMIC-324-LEO-Simulator
![Simulation Output](latency_simulation_output.png)

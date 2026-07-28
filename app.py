import networkx as nx
import matplotlib.pyplot as plt
from orbital_dynamics import calculate_orbital_distance, compute_propagation_delay

def run_and_plot_simulation():
    print("==================================================")
    print("  COSMIC-324: LEO Satellite Simulation Engine v1.1  ")
    print("==================================================")
    
    # بيانات محاكاة لسلسلة من القياسات عبر الزمن (لتوليد المنحنى البياني)
    time_steps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    latencies = []
    
    ground_station = {"name": "Riyadh Station", "lat": 24.7136, "lon": 46.6753}
    
    # محاكاة حركة القمر الصناعي وتغير المسافة وزمن التأخير تدريجياً
    for t in time_steps:
        # تغيير طفيف في إحداثيات القمر لمحاكاة حركة المدار
        simulated_lat = 25.0 + (t * 0.5)
        simulated_lon = 47.0 + (t * 0.3)
        
        dist = calculate_orbital_distance(
            simulated_lat, simulated_lon, 550.0,
            ground_station['lat'], ground_station['lon']
        )
        latency = compute_propagation_delay(dist)
        latencies.append(latency)
    
    print("\n[+] تمت معالجة بيانات المدار وحساب منحنى الـ Latency بنجاح.")
    
    # توليد الرسم البياني (Plotting the Latency Curve)
    plt.figure(figsize=(8, 5))
    plt.plot(time_steps, latencies, marker='o', color='b', linestyle='-', linewidth=2, label='Signal Latency (ms)')
    plt.title('COSMIC-324: LEO Satellite Latency Evolution over Time', fontsize=12)
    plt.xlabel('Simulation Time Steps', fontsize=10)
    plt.ylabel('Latency (ms)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # حفظ الرسم البياني تلقائياً كصورة
    output_image_name = 'latency_simulation_output.png'
    plt.savefig(output_image_name, dpi=300, bbox_inches='tight')
    print(f"[+] تم حفظ الرسم البياني بنجاح كصورة تحت اسم: {output_image_name}")
    print("==================================================")

if __name__ == "__main__":
    run_and_plot_simulation()

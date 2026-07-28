import networkx as nx
from orbital_dynamics import calculate_orbital_distance, compute_propagation_delay

def run_cosmic_simulation():
    print("==================================================")
    print("  COSMIC-324: LEO Satellite Simulation Engine v1.0  ")
    print("==================================================")
    
    # بيانات تجريبية لسيناريو كوكبة LEO ومحطات أرضية
    # المحطة الأرضية: الرياض (24.7136° N, 46.6753° E)
    ground_station = {"name": "Riyadh Station", "lat": 24.7136, "lon": 46.6753}
    
    # محاكاة موقع قمر صناعي منخفض (LEO) على ارتفاع 550 كم
    satellite = {"id": "COSMIC-SAT-01", "lat": 26.0, "lon": 48.0, "alt_km": 550.0}
    
    print(f"\n[+] محطة الاتصال الأرضية: {ground_station['name']} ({ground_station['lat']}, {ground_station['lon']})")
    print(f"[+] القمر الصناعي المستهدف: {satellite['id']} (الارتفاع: {satellite['alt_km']} كم)")
    
    # حساب المسافة وزمن التأخير
    dist = calculate_orbital_distance(
        satellite['lat'], satellite['lon'], satellite['alt_km'],
        ground_station['lat'], ground_station['lon']
    )
    
    latency = compute_propagation_delay(dist)
    
    print("\n--- نتائج التحليل الفضائي (Simulation Results) ---")
    print(f"-> المسافة المحسوبة بين القمر والمحطة: {round(dist, 2)} كم")
    print(f"-> زمن التأخير اللحظي (Latency): {latency} ميلي ثانية (ms)")
    
    # بناء نموذج شبكي تجريبي باستخدام NetworkX لنمذجة العقد والاتصال
    G = nx.Graph()
    G.add_node(ground_station['name'], type="GroundStation")
    G.add_node(satellite['id'], type="LEO-Satellite")
    G.add_edge(ground_station['name'], satellite['id'], weight=latency)
    
    print(f"\n[+] طوبولوجيا الشبكة: تم ربط العقد بنجاح عبر مسار فضائي نشط.")
    print("[+] حالة التشغيل: ناجحة (MVP Status: Operational).")
    print("==================================================")

if __name__ == "__main__":
    run_cosmic_simulation()

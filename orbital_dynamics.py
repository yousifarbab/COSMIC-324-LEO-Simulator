import numpy as np

def calculate_orbital_distance(sat_lat, sat_lon, sat_alt_km, ground_lat, ground_lon):
    """
    حساب المسافة التقريبية بين القمر الصناعي والمحطة الأرضية 
    باستخدام الحسابات الهندسية الكروية المبسطة لتحديد التأخير الفضائي.
    """
    R_earth = 6371.0 # نصف قطر الأرض بالكيلومتر
    
    # تحويل الإحداثيات إلى راديان
    lat1 = np.radians(sat_lat)
    lon1 = np.radians(sat_lon)
    lat2 = np.radians(ground_lat)
    lon2 = np.radians(ground_lon)
    
    # حساب المسافة الزاوية
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # المسافة السطحية
    surface_dist = R_earth * c
    
    # المسافة الكلية الثلاثية مع ارتفاع القمر (LEO Altitude)
    total_distance = np.sqrt(surface_dist**2 + sat_alt_km**2)
    return total_distance

def compute_propagation_delay(distance_km):
    """
    حساب زمن التأخير (Latency) بناءً على سرعة الضوء في الفراغ.
    سرعة الضوء تقريباً = 300,000 كم/ثانية
    """
    c = 300000.0 # كم/ث
    delay_seconds = (distance_km / c) * 2 # الذهاب والإياب (Round Trip Time)
    delay_ms = delay_seconds * 1000 # التحويل إلى الميلي ثانية
    return round(delay_ms, 2)

def fallback_math_reasoner(farmer_data) -> float:
    """Offline DeepSeek-Math-V2 mock"""
    certainty = 0.85
    
    if farmer_data.plasma_dha_pct < 3.0:
        certainty += 0.05
    
    if farmer_data.mri_volume_norm < 0.4:
        certainty += 0.07
    
    risk_score = 0.7 * (farmer_data.plasma_dha_pct/10) + 0.3 * farmer_data.mri_volume_norm
    if 0.35 <= risk_score <= 0.45:
        certainty -= 0.15
    
    return max(0.6, min(0.99, certainty))

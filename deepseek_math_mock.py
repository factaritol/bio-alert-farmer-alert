def fallback_math_reasoner(farmer_data) -> float:
    """
    Offline medical certainty calculator - mimics DeepSeek-Math-V2 reasoning
    Returns certainty score between 0.6 and 0.99
    """
    # Base certainty for normal calculations
    certainty = 0.85
    
    # Increase certainty for critical values (more certain about dangerous cases)
    if farmer_data.plasma_dha_pct < 3.0:
        certainty += 0.05  # Very low DHA = high certainty this is problematic
    
    if farmer_data.mri_volume_norm < 0.4:
        certainty += 0.07  # Critically low MRI volume = high certainty
    
    # Calculate risk score for context
    normalized_dha = farmer_data.plasma_dha_pct / 10.0
    risk_score = 0.7 * normalized_dha + 0.3 * farmer_data.mri_volume_norm
    
    # Reduce certainty when near threshold (less certain about borderline cases)
    if 0.35 <= risk_score <= 0.45:
        certainty -= 0.15
    
    # Clamp between 60% and 99% certainty
    certainty = max(0.60, min(0.99, certainty))
    
    return round(certainty, 3)

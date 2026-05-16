import re
from typing import Optional

TECH_KEYWORDS = {
    "quantum_computing": [
        "quantum", "qubit", "superposition", "entanglement", "quantum gate",
        "quantum circuit", "quantum error correction", "quantum algorithm",
    ],
    "artificial_intelligence": [
        "machine learning", "neural network", "deep learning", "artificial intelligence",
        "ai ", "llm", "transformer", "natural language processing", "computer vision",
        "classification", "regression", "reinforcement learning", "generative",
    ],
    "biotechnology": [
        "gene", "crispr", "dna", "rna", "protein", "enzyme", "antibody",
        "vaccine", "cell therapy", "genome", "sequencing", "biomarker",
    ],
    "semiconductor": [
        "transistor", "integrated circuit", "chip", "semiconductor", "wafer",
        "lithography", "cmos", "finfet", "processor", "microprocessor", "gpu",
    ],
    "software": [
        "software", "algorithm", "cloud computing", "api", "database",
        "microservices", "container", "kubernetes", "devops", "saas",
    ],
    "mechanical": [
        "engine", "gear", "turbine", "pump", "valve", "compressor",
        "mechanical", "robotics", "actuator", "sensor", "bearing",
    ],
    "energy": [
        "battery", "solar", "wind", "fuel cell", "energy storage", "grid",
        "renewable", "nuclear", "hydrogen", "carbon capture", "photovoltaic",
    ],
    "telecommunications": [
        "5g", "lte", "wireless", "antenna", "signal processing", "modulation",
        "rf", "mmwave", "optical fiber", "network", "protocol",
    ],
    "medical_device": [
        "implant", "stent", "catheter", "pacemaker", "prosthetic", "orthopedic",
        "surgical", "endoscope", "diagnostic", "monitoring", "wearable",
    ],
    "materials": [
        "nanomaterial", "composite", "polymer", "ceramic", "alloy", "graphene",
        "carbon fiber", "coating", "adhesive", "superconductor",
    ],
}


def auto_tag_technology(text: str) -> Optional[str]:
    """Simple rule-based technology category tagging.

    Returns the category with the highest keyword match count,
    or None if no clear match.
    """
    text_lower = text.lower()
    scores = {}
    for category, keywords in TECH_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Use regex word boundary for short keywords, substring for longer
            if len(kw) <= 4:
                score += len(re.findall(rf"\b{re.escape(kw)}\b", text_lower))
            else:
                score += text_lower.count(kw)
        if score > 0:
            scores[category] = score
    if not scores:
        return None
    best = max(scores, key=scores.get)
    # Only return if there's a meaningful signal (at least 2 matches)
    if scores[best] < 2:
        return None
    return best

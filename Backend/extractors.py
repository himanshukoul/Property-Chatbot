import re
import spacy
#from transformers import pipeline

nlp = spacy.load("en_core_web_trf")
#classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_price(text):
    text = text.lower()
    pattern = r'(under|below|less than|within|costing|costs|around)\s*(\d+)\s*(lakhs|lacs|l|crore|cr|k|thousand|thousands)?'
    match = re.search(pattern, text)
    if match:
        _, val, unit = match.groups()
        val = int(val)
        factor = {'k': 1e3, 'thousand': 1e3, 'thousands': 1e3,'l': 1e5, 'lakhs': 1e5, 'lacs': 1e5,
                  'cr': 1e7, 'crore': 1e7}.get(unit, 1)
        return int(val * factor)

    # Fallback (3bhk not accepted here , 3 lakhs...)
    pattern = r'(\d+)\s*(lakhs|lacs|l|crore|cr|k|thousand|thousands)'
    match = re.search(pattern, text)
    if match:
        val, unit = match.groups()
        val = int(val)
        factor = {
            'k': 1e3, 'thousand': 1e3, 'thousands': 1e3,
            'l': 1e5, 'lakhs': 1e5, 'lacs': 1e5,
            'cr': 1e7, 'crore': 1e7
        }.get(unit, 1)
        return int(val * factor)

    # Fallback2 eg, under 400000
    if re.search(r'(under|below|less than|within|costing|costs|around)', text):
        raw_number = re.search(r'(?:under|below|less than|within)\s+(\d+)', text)
        if raw_number:
            return int(raw_number.group(1))

    return None


def extract_bhk(text):
    text = text.lower()
    match = re.search(r'(\d+)\s*(bhk|rooms|room | bedroom)',text)
    if not match : return None
    return int(match.group(1))

def extract_action(text):
    text = text.lower()
    if 'buy' in text or 'want' in text: return 'buy'
    elif 'on rent' in text or 'rent out' in text or 'put on rent' in text or 'rent my' in text : return 'rent_out'
    elif 'rent' in text or 'lease' in text: return 'rent'
    elif 'sell' in text : return 'sell'
    """candidate_labels = ["buy", "sell", "rent"]       #felt useless not good accuracy
    result = classifier(text, candidate_labels)
    print(result)
    if result["scores"][0] > 0.5 : return result["labels"][0]"""
    return None

# fuzzy location 
def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None
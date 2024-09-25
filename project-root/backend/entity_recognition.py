import spacy

nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

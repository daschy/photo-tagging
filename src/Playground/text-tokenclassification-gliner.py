from gliner import GLiNER

def merge_entities(entities):
    if not entities:
        return []
    merged = []
    current = entities[0]
    for next_entity in entities[1:]:
        if next_entity['label'] == current['label'] and (next_entity['start'] == current['end'] + 1 or next_entity['start'] == current['end']):
            current['text'] = text[current['start']: next_entity['end']].strip()
            current['end'] = next_entity['end']
        else:
            merged.append(current)
            current = next_entity
    # Append the last entity
    merged.append(current)
    return merged


model = GLiNER.from_pretrained("numind/NuNerZero")

# NuZero requires labels to be lower-cased!
labels = ["color", "noun"]
labels = [l.lower() for l in labels]

text = "red and green and magenta on the grass"

entities = model.predict_entities(text, labels)

entities = merge_entities(entities)

for entity in entities:
    print(entity["text"], "=>", entity["label"])
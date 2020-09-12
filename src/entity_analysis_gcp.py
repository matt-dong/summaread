from google.cloud import language
import pickle
import os

"""
Works well on first part of this lecture (test_text.txt)
https://www.youtube.com/watch?v=XbIfFY_fJ_s

"""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../gckey.json"


def process_file(path):
    client = language.LanguageServiceClient()

    file = open(path, "r")
    text = file.read()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT,
    )
    response = client.analyze_entities(
        document=document,
        encoding_type='UTF32',
    )
    wikipedia_entities = {}

    for entity in response.entities:
        if 'wikipedia_url' in entity.metadata:
            # print('=' * 20)
            # print('         name: {0}'.format(entity.name))
            # print('         type: {0}'.format(entity.type))
            # print('     metadata: {0}'.format(entity.metadata))
            # print('     salience: {0}'.format(entity.salience))
            wikipedia_entities[entity.name] = entity.metadata['wikipedia_url']

    pickle.dump(wikipedia_entities, open("../videos/note_entities.pkl", "wb"))
    print("All done!")


def load_pkl():
    entities = pickle.load(open("../videos/note_entities.pkl", "rb"))
    print(entities)
    return entities


if __name__ == "__main__":
    process_file("../videos/summary.txt")
    load_pkl()

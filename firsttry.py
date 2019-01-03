import os
import json
from os.path import join
import xmltodict
import spacy

if __name__ == '__main__':
    base_dir = join('data', 'alldata')
    nlp = spacy.load('en_core_web_sm')
    #with open("chattext.txt", "w+") as f:
        #f.write("hi")

    out_fn = "chattext2.txt"
    already_processed = []
    open_mode = "w+"
    if os.path.exists(out_fn):
        already_processed = list(open("chattext2.txt", encoding="utf8").readlines())
        print('loaded {} lines from {}'.format(len(already_processed), out_fn))
        open_mode = 'a'

    with open(out_fn, open_mode, encoding="utf8") as fout:
        file_names = list(os.listdir(base_dir))
        for i, fn in enumerate(file_names):
            # skip already processed files
            if i < len(already_processed):
                #fout.write(already_processed[i])
                continue
            current_sentences = []
            messagetext = ''
            try:
                fn = join(base_dir, fn)
                print('{:2.0f}%: {}'.format(100 * i / len(file_names), fn))
                with open(fn, encoding="utf8") as f:
                    doc = xmltodict.parse(f.read())
                # see https://docs.python-guide.org/scenarios/xml/
                for message in doc['conversation']['messages']['message']:
                    try:
                        messagetext = message['body']
                        processedtext = nlp(messagetext)
                        for sentence in processedtext.sents:
                            if sentence.text.strip() != '':
                                current_sentences.append(sentence.text.strip())
                    except Exception as e1:
                        print('skipped: {} WARNING: {}. messagetext: "{}" from file {}.'.format(message['@id'], e1, messagetext, fn))
                        continue
            except Exception as e:
                print('WARNING: {}. skipped: {}.'.format(e, fn))
                continue
            fout.write(json.dumps(current_sentences, ensure_ascii=False).encode('utf8') + "\n")

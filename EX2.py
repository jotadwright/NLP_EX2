import pandas as pd
import spacy
from collections import Counter
import urllib.request

nlp = spacy.load("en_core_web_sm")

# Load corpus
url = "https://raw.githubusercontent.com/jotadwright/NLP_EX2/main/eng_wikipedia_2016_100K-sentences.txt"
df = pd.read_csv(urllib.request.urlopen(url), header=None, sep='\t')
text = df[1].tolist()

# Process corpus with Spacy. This may be slow with a large corpus
docs = []
for s in text:
    doc = nlp(s)
    docs.append(doc)

# Define informational adjectives, eventive verbs, eventive prepositions and time nouns
info_adj = ['true','false','misleading','correct','incorrect','factual']
event_verbs = ['broadcast','initiate','occur','happen','begin']
event_pps = ['during','after','before']
time_nouns = ['period','season','time','year','month','week','day','summer','career','lifetime','century']

# Create empty lists for different noun/sentence categories
acl_sents = []
acl_nouns = []
acomp_sents = []
acomp_nouns = []

eventv_sents = []
eventv_nouns = []
eventp_sents = []
eventp_nouns = []

# Iterate over the corpus
for d in docs:
    for candidate in d:
        # Find nouns which are the head of an adjectival clause
        if candidate.dep_ == "acl" and candidate.head.pos_ == "NOUN":
            for child in candidate.children:
                if child.dep_ == "mark":
                    acl_sents.append(d.text)
                    acl_nouns.append(candidate.head.lemma_)
        # Find nouns which have an adjectival complement using an informational adjective
        if candidate.dep_ == "acomp" and candidate.text in info_adj:
            for child in candidate.head.children:
                if child.dep_ == "nsubj" and child.pos_ == "NOUN":
                    acomp_sents.append(d.text)
                    acomp_nouns.append(child.lemma_)
        # Find nouns which are the direct or passive subject of an event verb
        if (candidate.dep_ == "nsubj" or candidate.dep_ == "nsubjpass") \
                and candidate.pos_ == 'NOUN' and candidate.head.lemma_ in event_verbs:
            eventv_sents.append(d.text)
            eventv_nouns.append(candidate.lemma_)
        # Find nouns whose head is an eventive preposition, excluding time nouns
        if candidate.pos_ == "NOUN" and candidate.dep_ == "pobj" and candidate.lemma_ not in time_nouns \
                and candidate.head.lemma_ in event_pps:
            eventp_sents.append(d.text)
            eventp_nouns.append(candidate.lemma_)

# Save results in dataframes
df_acl = pd.DataFrame(list(zip(acl_nouns,acl_sents)),columns=["noun","sentence"])
df_acomp = pd.DataFrame(list(zip(acomp_nouns,acomp_sents)),columns=["noun","sentence"])
df_eventv = pd.DataFrame(list(zip(eventv_nouns,eventv_sents)),columns=["noun","sentence"])
df_eventp = pd.DataFrame(list(zip(eventp_nouns,eventp_sents)),columns=["noun","sentence"])

print(df_acl)
print(df_eventv)

# Get total frequencies of informational nouns
info = acl_nouns + acomp_nouns
info_count = Counter(info)
df_info = pd.DataFrame.from_dict(info_count, orient='index').reset_index()

# Get total frequencies of eventive nouns
event = eventv_nouns + eventp_nouns
event_count = Counter(event)
df_event = pd.DataFrame.from_dict(event_count, orient='index').reset_index()

# Save the two searches to CSV
df_info.to_csv('data/info_nouns.csv', index=False)
df_event.to_csv('data/event_nouns.csv', index=False)



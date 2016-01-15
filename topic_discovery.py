import textmining
import lda
import numpy as np
import matplotlib.pyplot as plt

# use matplotlib style sheet
try:
    plt.style.use('ggplot')
except:
    # version of matplotlib might not be recent
    pass


doc1 = 'John and Bob are brothers.'
doc2 = 'John went to the store. The store was closed.'
doc3 = 'Bob went to the store too.'

tdm = textmining.TermDocumentMatrix()

# Add the documents
tdm.add_doc(doc1)
tdm.add_doc(doc2)
tdm.add_doc(doc3)
tdm.add_doc(doc3 + doc1)
tdm.add_doc(doc3 + doc2)
tdm.add_doc(doc1 + doc3)
tdm.add_doc(doc2 + doc3)
tdm.add_doc(doc2 + doc3)
tdm.add_doc(doc2 + doc3)
tdm.add_doc(doc2 + doc3)


# create a temp variable with doc-term info
temp = list(tdm.rows(cutoff=1))


model = lda.LDA(n_topics=10, n_iter=3, random_state=1)
X = np.array(temp[1:])
vocab = tuple(temp[0])
model.fit(X)

topic_word = model.topic_word_
doc_topic = model.doc_topic_
vocab = tuple(temp[0])

for n in range(5):
    sum_pr = sum(topic_word[n,:])
    print("topic: {} sum: {}".format(n, sum_pr))

n = 5
topic = []
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
    topic.append(' '.join(topic_words))
	

# prob. plot
f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([0, 2, 3, 6, 9]):
    ax[i].stem(topic_word[k,:], linefmt='b-',
               markerfmt='bo', basefmt='w-')
    ax[i].set_xlim(0, len(vocab))
    ax[i].set_ylim(0, 1)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("topic {}".format(topic[k]))

ax[4].set_xlabel("word")

plt.tight_layout()
plt.savefig('topic_word.png')

f, ax= plt.subplots(5, 1, figsize=(8, 6), sharex=True)
for i, k in enumerate([1, 3, 4, 8, 9]):
    ax[i].stem(doc_topic[k,:], linefmt='r-',
               markerfmt='ro', basefmt='w-')
    ax[i].set_xlim(-1, 21)
    ax[i].set_ylim(0, 1)
    ax[i].set_ylabel("Prob")
    ax[i].set_title("Document {}".format(k))

ax[4].set_xlabel("Topic")

plt.tight_layout()
plt.savefig('topic_per_document.png')


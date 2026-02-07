CREATE TABLE IF NOT EXISTS mcq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    question TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mcq_id INTEGER,
    chosen TEXT,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(mcq_id) REFERENCES mcq(id)
);


-- Seed MCQs for NLP
INSERT INTO mcq (topic, question, option_a, option_b, option_c, option_d, correct) VALUES
('NLP', 'What is tokenization?', 'Splitting text into sentences', 'Splitting text into words/subwords', 'Removing stopwords', 'Stemming words', 'B'),
('NLP', 'NER stands for?', 'Natural Entity Recognition', 'Named Entity Recognition', 'Neural Embedding Representation', 'None of the above', 'B');

-- Seed MCQs for RAG
INSERT INTO mcq (topic, question, option_a, option_b, option_c, option_d, correct) VALUES
('RAG', 'What does RAG stand for?', 'Random Access Generator', 'Retrieval-Augmented Generation', 'Recurrent Attention Graph', 'None of the above', 'B'),
('RAG', 'Why use RAG?', 'To improve factual accuracy', 'To reduce training cost', 'To generate longer text', 'To replace embeddings', 'A');
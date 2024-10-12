## Understanding Disfluencies in Hindi Dialogue: A Psycholinguistic Analysis

Hypothesis: 
1. Following psycholinguistic metrics would predict disfluencies (अअ, ज_जब_भी,तू तेरा, etc.) in Spontaneous Hindi Speech Production:
    - Unigram Frequency
    - Bigram Frequency
    - Syllable Length
    - Word Length
    - Dependency Length
    - Word Similarity (Forward)
    - Word Similarity (Backward) 
    - Surprisal 
    - Surprisal Value (Hindi Dialogue corpus)

2. Model Disfluncies as Generalized Linear Mixed Models (GLMM) in R:

```bash
Disfluencies ~ 1 + scale(Uni_Freq) + scale(Bi_Freq) + Word_Len +  Syll_Len + WordSimForward + WordSimBackward + DepLen + surprisal_NC + surprisal_DC + (1 | SpeakerId) + (1|SentenceId)
## Goal

Rank spoonerism suggestions so that the most common, natural sounding words surface first (e.g. “blushing crow” before “blushing cro”). This requires a word-frequency score that can be applied to every candidate returned from CMUdict.

## Constraints / Unknowns

- CMUdict phoneme list includes obscure words and proper nouns with no obvious frequency information.
- Some candidates contain apostrophes or variants (“crowe”, “kroh”) that may not exist in standard frequency corpora.
- We need an approach that is reproducible, redistributable, and reasonably small to ship with the web app or load at runtime.

## Options & Trade‑offs

1. **Use an existing frequency list (e.g., wordfreq, SUBTLEX-US, Google Ngrams)**
   - *Pros*: Ready-made ranks; covers most common tokens; saves time.
   - *Cons*: Licensing varies; might not allow redistribution; may not include every CMU entry; may require bundling a large dataset or online lookups.

2. **Derive frequency from publicly available corpora (Project Gutenberg, Wikipedia dumps)**
   - *Pros*: Fully controllable licensing; can normalize casing/punctuation to match CMUdict; allows custom tokenization rules (e.g., handling “cro” vs “crow”).
   - *Cons*: Requires substantial preprocessing; accuracy depends on chosen corpus; might still miss rarer forms.

3. **Hybrid approach**
   - Start with an existing list for coverage, then backfill missing CMU words using heuristics (e.g., map inflected forms to lemmas, assign minimal scores to unknown words).
   - *Pros*: Balances quality with effort; ensures every CMU entry gets a score.
   - *Cons*: More moving parts (merging datasets, maintaining mappings).

## Proposed Plan

1. **Dataset Evaluation (1 day)**
   - Review licensing/redistribution terms for `wordfreq`, `SUBTLEX-US`, `Google Unigram` (1T), and `wordfreq`’s `zipf_frequency` output.
   - Measure coverage by sampling CMUdict entries and checking frequency availability.

2. **Select Source & Build Frequency Table (1–2 days)**
   - If `wordfreq` licensing permits, script an export mapping each lowercase word to a normalized “Zipf score” (log frequency). Otherwise, build our own frequency counts from a cleaned corpus (Wiki or subtitles).
   - Normalize CMUdict tokens: lowercase, strip apostrophes, but keep multiple variants distinct (`crow` vs `crowe`) by storing both the raw word and a fallback lemma.

3. **Companion Dataset Generation (0.5 day)**
   - Produce `data/word_frequency.json` (or similar) keyed by CMUdict words.
   - For unknown words, assign a baseline score (e.g., Zipf 1.5) so they appear after any known common word but still in results.

4. **Integration (1 day)**
   - When generating spoonerism candidates, look up each word’s frequency score.
   - Sort candidate pairs by descending min(score(word1), score(word2)), breaking ties via average score or alphabetical order.
   - Optionally expose scoring info in the API for UI debugging.

5. **Testing & Validation (0.5 day)**
   - Create regression tests verifying that “blushing crow” ranks before “blushing cro”.
   - Add fixtures covering edge cases (proper nouns, apostrophes).

6. **Performance Considerations**
   - Frequency file likely <10 MB compressed. Load once at application start into a dictionary.
   - Consider lazy loading or memory-mapped file if size becomes an issue.

## Future Enhancements

- Introduce user-facing toggles (“Prefer common words”) or display the top N ranked suggestions.
- Add telemetry to log which suggestions users click on, feeding future refinements.
- Periodically re-run corpus extraction to keep the frequency table current.

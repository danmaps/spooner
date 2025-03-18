# **Project Requirements Document (PRD)**
### **Project Name:** SpoonerJS  
### **Owner:** Danny  
### **Last Updated:** _(date)_

---

## **1. Overview**
### **1.1 Project Summary**
SpoonerJS is a **web-based application** that generates spoonerisms by swapping **phonemes** rather than just letters. It will provide a **visual, interactive experience** where users can **see and animate** how words transform into their spoonerized counterparts.

### **1.2 Goals**
- Provide a **fast, interactive** web interface for generating spoonerisms.
- **Visualize** the shift from words → phonemes → spoonerized phonemes → new words.
- Improve usability by **ranking results by word popularity**.
- Implement **color-coded IPA symbols** where colors make sense based on linguistic properties.
- Ensure **efficient client-side processing** for a smooth user experience.
- Create an **API for programmatic access** (optional).

---

## **2. Features**
### **2.1 Core Features**
| Feature                     | Description |
|-----------------------------|-------------|
| **Spoonerism Generator**    | Accepts input text and returns valid spoonerisms based on phoneme swaps. |
| **Phoneme Visualization**   | Breaks words into phonemes, coloring them based on their linguistic category. |
| **Animated Phoneme Swap**   | Swaps phonemes in an animated transition. |
| **Reverse Transformation**  | Animates the shift back into words, making the change easy to follow. |
| **Word Popularity Ranking** | Sorts spoonerisms by word frequency (using SUBTLEX, wordfreq, or a precomputed dataset). |
| **Customizable Output**     | Allows toggling between strict phoneme swaps vs. looser letter swaps. |

### **2.2 Stretch Features (Nice-to-Have)**
| Feature                     | Description |
|-----------------------------|-------------|
| **"Did You Mean?" Suggestions** | Auto-corrects typos and suggests spoonerisms for likely intended words. |
| **Voice Input (Web Speech API)** | Users can speak phrases and generate spoonerisms via speech recognition. |
| **Export Options**          | Enables users to copy, download, or share results. |
| **Mobile Optimization**     | Ensures smooth performance on smartphones and tablets. |

---

## **3. Technology Stack**
| Component          | Choice |
|--------------------|--------|
| **Frontend Framework** | Vanilla JS (or React/Vue if needed) |
| **Phoneme Processing** | CMU Pronouncing Dictionary (or equivalent in JS) |
| **Word Frequency Ranking** | wordfreq.js (or a pre-built frequency dataset) |
| **Visualization & Animation** | D3.js, GSAP (for smooth transitions) |
| **Hosting** | Netlify / Vercel / GitHub Pages |
| **Backend (if needed)** | Node.js + Express (optional for API) |

---

## **4. UI/UX Requirements**
| UI Component       | Description |
|--------------------|-------------|
| **Text Input Box** | Users enter a phrase to generate spoonerisms. |
| **Phoneme Breakdown** | Words transform into phonemes, each with a distinct color based on linguistic properties. |
| **Phoneme Animation** | Phonemes swap positions with a smooth transition. |
| **Reconstruction Animation** | The swapped phonemes morph back into new words. |
| **Sorting & Filtering** | Users can sort by popularity or restrict results. |
| **Copy/Share Button** | Allows users to easily copy or share results. |

---

## **5. Phoneme Color-Coding System**
Each **IPA phoneme** will be colored according to its linguistic category:

| Phoneme Type          | Example Sounds | Suggested Color |
|----------------------|---------------|----------------|
| **Vowels**          | /a/, /e/, /i/, /o/, /u/ | **Blue** (fluid, open sounds) |
| **Nasal Consonants** | /m/, /n/, /ŋ/ | **Green** (soft, flowing like air through the nose) |
| **Stops (Plosives)** | /p/, /t/, /k/, /b/, /d/, /g/ | **Red** (abrupt, explosive sounds) |
| **Fricatives**       | /f/, /v/, /s/, /z/, /ʃ/, /ʒ/, /θ/, /ð/ | **Yellow** (continuous, airy sounds) |
| **Affricates**       | /tʃ/, /dʒ/ | **Orange** (a mix of stop and fricative sounds) |
| **Liquids**          | /l/, /r/ | **Purple** (smooth, flowing sounds) |
| **Glides**           | /w/, /j/ | **Cyan** (semi-vowel, between vowel and consonant) |

---

## **6. Animation Design**
| Animation Type              | Description |
|-----------------------------|-------------|
| **Phoneme Breakdown**       | Words smoothly transition into individual phonemes. |
| **Phoneme Swap**            | Swapped phonemes move, fade, or morph in color to show the transformation. |
| **Phoneme Reconstruction**  | The new phoneme sequence forms the output words. |

### **Animation Technologies**
| Approach                    | Use Case |
|-----------------------------|----------|
| **CSS Keyframe Animations** | Basic fading and transitions. |
| **GSAP (GreenSock Animation Platform)** | Smooth, controlled animations for phoneme swaps. |
| **D3.js (for phoneme trees)** | Interactive phoneme structure visualization. |
| **Canvas/WebGL (Advanced)** | High-performance rendering for large datasets. |

---

## **7. Performance & Scalability**
| Requirement        | Solution |
|--------------------|-------------|
| **Fast Execution** | Perform all spoonerism generation **client-side** using WebAssembly or optimized JS. |
| **Efficient Lookup** | Store word frequency data in a **compressed JSON file** for quick lookups. |
| **Low Latency** | Avoid unnecessary API calls; process everything in the browser. |

---

## **8. Milestones & Timeline**
| Milestone                 | Estimated Completion |
|---------------------------|----------------------|
| **Research NLP Libraries** | (Date) |
| **Prototype Phoneme Swapper** | (Date) |
| **Implement UI & Sorting** | (Date) |
| **Deploy Beta Version** | (Date) |
| **Launch Public Version** | (Date) |

---

## **9. Open Questions**
- Which JavaScript NLP library is best for phoneme analysis? (e.g., [CMUdict](https://github.com/wordnik/cmudict), [natural](https://github.com/NaturalNode/natural))
- Should we offer an **offline mode** with a cached dictionary?
- How will we **handle homophones** and ambiguous cases?

---

## **10. Risks & Challenges**
| Risk                     | Mitigation Strategy |
|--------------------------|---------------------|
| **Complex Phoneme Mapping** | Use an existing pronunciation dictionary to avoid re-inventing phoneme parsing. |
| **Large Word Frequency Dataset** | Pre-load a **compressed frequency list** instead of calling APIs dynamically. |
| **Cross-Browser Compatibility** | Test on Chrome, Firefox, Safari, and Edge. |

---

## **11. Next Steps**
- Decide on the **NLP phoneme library** to use.
- Build a **basic phoneme swapper** in JavaScript.
- Create the **UI prototype** and test real-time results.

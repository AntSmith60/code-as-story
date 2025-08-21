# 📖 Code-as-Story  
**Python supporting the Narratival-Exposition Paradigm**

---

## CAVEAT
This is a Proof-of-Concept right now so the entry scripts (narrate.py and narration.ppy) are pure lash-up; a bit of framework to access the 'real' code in the module-scripts - so don;t be paying them that much heed.

---

## ✨ Background

To understand the *Narratival-Exposition Paradigm*, it’s best to begin with these foundational articles:

- [Feeling the Shape of Uncertainty](https://antsmith.net/articles/feeling-the-shape-of-uncertainty)  
- [The Expressive Coder](https://antsmith.net/articles/the-expressive-coder)

In essence: **cognition isn’t just knowing a thing—it’s experiencing it.**

Code, being abstract, is notoriously difficult to experience. We often engage with it using only the rational half of our minds. Yet coding is a creative act, even if we don’t fully understand how that creativity is harnessed.

Narrative—story—is a core cognitive function. Its purpose is not merely to inform, but to *immerse*. The *Narratival-Exposition Paradigm* is a grammar for writing code that allows story to be extracted from it, so the code can be **felt**, not just reasoned about.

---

## 🧠 What This Is

This repository contains a **Proof-of-Concept** for the paradigm. It generates a narratival exposition of the very scripts that extract narratival exposition—because those scripts themselves were written in the paradigm.

The narrative is **orthogonal** to the code. It’s not a replacement for technical documentation (e.g. docstrings), but an **alternative journey** through the code, spoken in unbroken metaphor.

So the question becomes:  
**Does the resulting `narration.md` help us *grok* what the scripts are doing?**

That’s why this is shared—so others might explore, comment, or even help evolve it into robust tooling for the paradigm.

---

## 🗂️ Files & Flow

### Entry Scripts

- `narrate.py`  
  Depends on `codices`, `granulator`, `lexicographics`, and `registrar`.  
  It scans itself to produce:
  - `expo.txt` (also saved as the unedited version)
  - `expo.json`

- `narration.py`  
  Reads both `expo.txt` and `expo.json` to generate:
  - `narration.md` — the full narrative exposition of `narrate.py`

### Editorial Workflow

- `expo.txt` is manually edited to define the **editorial arc** of the documentation.  
- It may be lightly adorned with additional **editorialisation**.  
- The final output lives in `narration.md`.

### Requirements

- Python **3.9+**
- No external dependencies

---

## 🪶 Final Thought

This is a beginning—a sketch of what it means to treat code as story. If it resonates, feel free to contribute, comment, or simply explore. The paradigm is open, expressive, and waiting to be lived.

---

Would you like a badge or tagline to accompany the repo—something like _“Code that narrates itself”_ or _“Documentation as dramaturgy”_? I’d be happy to help you design one.

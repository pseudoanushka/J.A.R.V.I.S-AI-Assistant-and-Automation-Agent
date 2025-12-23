# 🦾 J.A.R.V.I.S. — Intelligent Multi-Agent Automation System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?style=for-the-badge&logo=qt)
![AI-Classification](https://img.shields.io/badge/Intent_Engine-Cohere-purple?style=for-the-badge)
![LLM](https://img.shields.io/badge/LLM-Gemini_3_Flash-orange?style=for-the-badge)
![Automation](https://img.shields.io/badge/Automation-Selenium_|_AppOpener-red?style=for-the-badge)

**J.A.R.V.I.S.** (Just A Rather Very Intelligent System) is a sophisticated multi-agent AI assistant designed with a **Decision-First Architecture**. Unlike standard chatbots, J.A.R.V.I.S. acts as an Orchestrator—analyzing user intent via NLP to delegate tasks across three specialized engines: Conversational AI, Real-Time Web Intelligence, and OS-Level Automation.

---

## 🏗️ System Architecture & Workflow

The system is engineered to minimize latency and maximize accuracy through a modular pipeline:

1.  **Orchestration Layer:** Uses **Cohere NLP** to classify input into specific domains (General, Real-time, or System).
2.  **Logic Dispatcher:** * **Conversational:** Routes to a context-aware LLM buffer.
    * **Dynamic Intelligence:** Triggers **Serper API** & **Gemini** to frame live data into natural language.
    * **Generative AI:** Dispatches prompts to **Stability-AI** (Hugging Face Transformers) for on-the-fly image synthesis.
    * **Automation:** Executes hardware/software control via **Selenium** and **AppOpener**.
3.  **State Synchronization:** A lightweight, file-based reactive system manages hardware states (e.g., Mic, Camera) in real-time.



[Image of AI Agent Architecture Diagram]


---

## 🚀 Key Technical Features

### 🧠 Intent-Driven Orchestration
* Implemented a high-accuracy classification model using **Cohere API** to prevent "hallucinations" by ensuring queries are handled by the correct specialized engine.
* Custom **Query Modifiers** sanitize and optimize strings for search engines and automation scripts.

### 🌐 Real-Time Web Intelligence
* Integrated **Serper API** with **Gemini 3 Flash** to provide live data (Stock market, Weather, News) with summarized, human-like responses.

### 💻 OS & Web Automation
* Developed a hands-free experience using **AppOpener** for software management and **Selenium** for deep-web automation.
* Native support for hardware toggles (Microphone/Camera) using Python’s `sys` and `os` libraries.

### 🎨 Generative Vision
* Built an image generation pipeline leveraging **Hugging Face Transformers** (Stability 100 base) to convert textual descriptions into high-fidelity visual assets.

### 🖥️ Professional PyQt5 Interface
* Designed a multi-threaded GUI to ensure the interface remains responsive during heavy API calls or automation tasks.
* Persistent memory integration via `chatlog.json` for session-based history tracking.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Core Language** | Python 3.10+ |
| **Frontend** | PyQt5 (Custom UI/UX Design) |
| **NLP & LLM** | Cohere (Classification), Gemini 3 Flash (Synthesis) |
| **Automation** | Selenium, AppOpener, Keyboard, PyWhatKit |
| **GenAI** | Hugging Face Transformers (Stable Diffusion) |
| **Data/State** | JSON, .data (Reactive file-based state management) |

---

## 📂 Project Structure

```text
JARVIS/
├── core/                # Core AI logic and decision engines
│   ├── decision_model/  # Intent classification logic
│   ├── realtime/        # Live API & Web-scraping integration
│   └── automation/      # System & Web automation scripts
├── gui/                 # PyQt5 visual components and styling
├── image_generation/    # Diffusion model implementation
├── data/                # Reactive state files (mic.data, etc.)
├── main.py              # System entry point & multi-threading logic
└── requirements.txt     # Dependency manifest

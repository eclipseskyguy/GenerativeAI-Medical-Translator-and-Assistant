# Generative AI Medical Translator and Assistant

An intelligent, real-time multilingual translation platform designed to bridge the language gap between healthcare providers and patients. This application leverages state-of-the-art Generative AI to ensure seamless communication, handle complex medical terminology, and provide insightful assistance, all within a secure and user-friendly interface.

## ✨ Core Features

This application is more than just a translator; it's a complete communication assistant for the medical world.

* **Real-time Multilingual Dialogue:**
    * **Speech-to-Text:** Captures speech input via the microphone using the browser's native Web Speech API for low-latency transcription.
    * **Text Translation:** Translates text between 14+ languages (including English, Spanish, Hindi, Tamil, Arabic, and more) using the robust Google Translate engine.
    * **Text-to-Speech:** Converts translated text into clear, natural-sounding audio using Google Text-to-Speech, allowing for audible communication.

* **Intelligent & Dynamic Interface:**
    * **Conversation History:** Displays the dialogue in a familiar chat format, allowing users to scroll back and review the conversation.
    * **Dynamic Role Toggling:** Clearly labels each side of the conversation as "Doctor" or "Patient" and allows the roles to be swapped with a single click.
    * **Swap Languages:** Instantly switches the input and output languages to facilitate a natural back-and-forth conversational flow.

* **Advanced AI-Powered Assistance (via Google Gemini)**
    * **On-Demand Summarization:** Provides a concise, one-sentence summary of any translated message, perfect for getting the main point quickly.
    * **Medication Explainer:** A unique feature that can analyze a translated text, identify the primary medication mentioned, and provide a simple explanation of its purpose and common side effects.
    * **Bilingual AI Responses:** All AI-generated summaries and explanations are provided in both the doctor's and the patient's language simultaneously in a clean pop-up modal, ensuring both parties understand.

* **Conceptual Bonus Feature:**
    * **Text-to-Sign Language (Prototype):** Includes a UI placeholder and a conceptual endpoint for a future feature that would render translated text as a sign language animation, making the app accessible to deaf patients.

## 🛠️ Technology Stack

This project uses a modern, serverless architecture for scalability, speed, and low maintenance.

* **Backend:**
    * **Framework:** **FastAPI** for building high-performance, asynchronous Python APIs.
    * **Deployment:** **Vercel** for seamless, scalable serverless deployment.
    * **Translation Engine:** `googletrans` library.
    * **Text-to-Speech:** `gTTS` library.

* **Frontend:**
    * **Languages:** HTML, CSS, and modern JavaScript (`async/await`, Fetch API).
    * **Templating:** Served via FastAPI using **Jinja2Templates**.
    * **Speech Recognition:** Native Browser **Web Speech API**.

* **Generative AI:**
    * **Model:** **Google Gemini Pro (`gemini-1.5-flash`)** for all summarization and explanation tasks.
    * **API:** `google-generativeai` Python SDK.

## 🚀 How to Use

The application is designed to be intuitive and requires no setup for the end-user.

1.  **Set the Roles:** Use the `🩺/👤` button to assign the "Doctor" and "Patient" roles to the left and right sides of the screen.
2.  **Select Languages:** Choose the appropriate input and output languages from the dropdown menus for each role. Use the `⇄` button to quickly swap languages.
3.  **Input Text:**
    * **By Voice:** Click "Start Speaking" and talk into your microphone. Click "Stop Recording" when finished. The transcribed text will appear.
    * **By Typing:** Manually type or paste text into the text area.
4.  **Translate & Speak:** Click the "Translate & Speak" button.
5.  **View & Listen:**
    * The translated text will appear in the **Conversation History**.
    * The audio of the translation will play automatically.
6.  **Use AI Tools:** In the history entry for each translation, you will find buttons to:
    * **Summarize:** Get a quick summary of the message.
    * **Explain Medication:** Get a simple explanation of any medical drug mentioned.
7.  **Clear History:** Click the "Clear History" button at the top to reset the conversation.

## Future Development

This platform is built to be extensible. Future development plans include:
* **AI Medical Terminology Verifier:** An AI-powered second opinion to verify the accuracy of translated medical terms.
* **Prescription Image Scanner:** Use a vision AI model to read and digitize text from a photo of a prescription.
* **Full Sign Language Integration:** Develop the conceptual prototype into a fully functional text-to-sign-language animation feature.

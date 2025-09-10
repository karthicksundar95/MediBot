MediBot
=======

_Your AI-powered medical assistant chatbot._

MediBot is an AI-driven chatbot designed to provide users with medical information, assist in locating nearby healthcare providers, and offer support for various health-related queries. Built using LangChain, Pinecone, and Ollama, MediBot leverages Retrieval-Augmented Generation (RAG) techniques to deliver accurate and context-aware responses.

Features
--------

*   **Medical Q&A**: Get answers to health-related questions powered by large language models.
    
*   **Nearby Healthcare Providers**: Locate doctors, clinics, and pharmacies in your vicinity.
    
*   **Contextual Conversations**: Engage in meaningful dialogues with memory retention across interactions.
    
*   **Voice Integration**: (Optional) Use voice input/output for hands-free interaction.
    
*   **Secure & Private**: Designed with user privacy in mind; no personal data is stored.
    

Tech Stack
----------

*   **Backend**: Python 3.10+
    
*   **Web Framework**: Flask
    
*   **LLM Integration**: Ollama
    
*   **Vector Database**: Pinecone
    
*   **Prompt Engineering**: LangChain
    
*   **Frontend**: HTML, CSS, JavaScript (Bootstrap)
    
*   **Environment Management**: .env for API keys and configurations
    

Installation
------------

### 1\. Clone the Repository

``` bash
   git clone https://github.com/karthicksundar95/MediBot.git 
   
   cd MediBot   
```

### 2\. Set Up Virtual Environment

```bash
   python3 -m venv venv  source venv/bin/activate  # On Windows, use `venv\Scripts\activate
```
### 3\. Install Dependencies

```bash
   pip install -r requirements.txt
```
### 4\. Configure Environment Variables

Create a .env file in the root directory and add your API keys:

```bash
    PINECONE_API_KEY=your_pinecone_api_key  
    OPENAI_API_KEY=your_openai_api_key
```
### 5\. Initialize Pinecone Index

Run the following script to store embeddings:

```bash
    python store_index.py
```

### 6\. Run the Application

Start the Flask server:

```bash
    python app.py
```

Access the chatbot at http://localhost:8080 in your web browser.

Usage
-----

*   **Chat Interface**: Type your medical queries into the chatbox and receive instant responses.
    
*   **Voice Interaction**: (If enabled) Click the microphone icon to speak your queries.
    
*   **Nearby Providers**: Enter your location to find nearby doctors and pharmacies.
    

Contributing
------------

Contributions are welcome! To contribute:

1.  Fork the repository.
    
2.  Create a new branch (git checkout -b feature-name).
    
3.  Make your changes and commit them (git commit -am 'Add new feature').
    
4.  Push to your fork (git push origin feature-name).
    
5.  Open a pull request.
    

License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
----------------

*   **LangChain**: For facilitating prompt engineering and LLM integrations.
    
*   **Pinecone**: For providing vector database solutions.
    
*   **Ollama**: For offering LLM capabilities.
    
*   **Bootstrap**: For responsive front-end design.
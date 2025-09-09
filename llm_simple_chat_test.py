import ollama

def query_my_ollama(prompt: str, model: str='smollm:135m')-> str:
    """
    To query a llm model and get response using ollama
    which will bring a copy of model weights to the local without
    needing the dependency on the api call or internet
    Args:
        prompt (str) : input query sent by the user
        model (str)  : type of llm model to used to answer the user query
    Return:
        response (str) : response text from the llm model
    """
    messages = [
                {"role":"system", "content": """You are a helpful assistant who will answer always in less than 20 words and not add unnecessary long information.
                If the user says they want to end the conversation, thank them for the interaction in few words only"""},
                {"role" : "user", "content": prompt}]
    response = ollama.chat(model=model,
                messages=messages)
    
    return response

if __name__ == "__main__":
    prompt = ""
    while True:
        prompt = input("User:")
        if prompt.lower() not in ("exit", "stop", "end", "quit", "bye"):
            output = query_my_ollama(prompt)
            print("AI:", output['message']['content'])
        else:
            output = query_my_ollama("i am ending this conversation. see you later")
            print("AI:", output['message']['content'])
            print("--- Conversation ended -----")
            break
    
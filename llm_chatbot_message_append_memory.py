from ast import List
import ollama

def query_my_ollama(messages: List, model: str='llama2:latest')-> str:
    """
    To query a llm model and get response using ollama
    which will bring a copy of model weights to the local without
    needing the dependency on the api call or internet
    Args:
        messages (List) : list of dictionary which has conversation by role
        model (str)  : type of llm model to used to answer the user query
    Return:
        response (str) : response text from the llm modelc
    """
    response = ollama.chat(model=model,
                messages=messages)
    
    return response

if __name__ == "__main__":
    prompt = ""
    messages = [
                {"role":"system", "content": "You are a helpful chatbot. You will answer the user questions precisely."},
               ]
    while True:
        prompt = input("User:")
        if prompt.lower() not in ("exit", "stop", "end", "quit", "bye"):
            messages.append({"role" : "user", "content": prompt})
            output = query_my_ollama(messages)
            messages.append({"role" : "AI", "content": output['message']['content']})
            print("AI:", output['message']['content'])
        else:
            messages.append({"role" : "user", "content": prompt})
            output = query_my_ollama(messages)
            messages.append({"role" : "AI", "content": output['message']['content']})
            print("AI:", output['message']['content'])
            print("--- Conversation ended -----")
            break
    print(messages)
    
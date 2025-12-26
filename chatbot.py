import os
import google.generativeai as genai
from retriever import OfferRetriever
from prompts import SYSTEM_PROMPT


GOOGLE_API_KEY = "AIzaSyDNLIuHfKwdmtrSaXHIcUZMjai47j9SDpY"


retriever = OfferRetriever()


genai.configure(api_key=GOOGLE_API_KEY)


MODEL_NAME = "gemini-2.5-flash" 
model = genai.GenerativeModel(model_name=MODEL_NAME)

def generate_answer(user_query, top_k=5):
    context = retriever.prepare_context(user_query, top_k=top_k)


    full_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"მომხმარებლის შეკითხვა: {user_query}\n\n"
        f"შეთავაზებების კონტექსტი:\n{context}\n\n"
        f"უპასუხე შეკითხვას ქართულად, მეგობრულ ტონით, დეტალურად:"
    )


    response = model.generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            max_output_tokens=15000,
        ),
    )

    return response.text

def chat_loop():
    print("გამარჯობა, მკითხე რაც გაინტერესებს (აკრიფეთ 'exit' გამოსვლისთვის)")
    while True:
        query = input("შეკითხვა: ").strip()
        if query.lower() in ["exit", "გასვლა"]:
            print("საუბარი დასრულდა.")
            break
        
        try:
            answer = generate_answer(query)
            print(f"\n💡 პასუხი:\n{answer}\n")
        except Exception as e:
            print(f"შეცდომა: {e}")

if __name__ == "__main__":
    chat_loop()
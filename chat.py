from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from flask import Flask, request, jsonify,render_template

app = Flask(__name__)

# Initialize GPT-4 model
def initialize_gpt(api_key, model_name="gpt-4"):
    return ChatOpenAI(
        model_name=model_name,
        temperature=0.2,
        openai_api_key="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"
    )

# Custom prompt for Burmese (Education Domain)
burmese_prompt = PromptTemplate(
    input_variables=["conversation_history", "question", "context"],
    template="""
        သင်သည် ပညာရေးနှင့် အလုပ်အကိုင်ဆိုင်ရာ မေးခွန်းများအတွက် ကျောင်းသားများကို အကြံဉာဏ်ပေးသူ ဖြစ်ပါသည်။ အရေးပါတဲ့အချက်များသာ ပါဝင်သည့် အတိုချုံးအဖြေကို ပေးပါ။  အောက်ပါ conversation history နှင့် context ကို အခြေခံ၍ အမေးအဖြေကို ပေးပါ။

        Conversation History:
        {conversation_history}

        Context: {context}

        Question: {question}

        Answer:
    """
)

# Custom prompt for English (Education Domain)
english_prompt = PromptTemplate(
    input_variables=["conversation_history", "question", "context"],
    template="""
        You are an educational advisor helping students with their academic and career-related questions.The answers should be straightforward. Based on the conversation history and context below, answer the question.

        Conversation History:
        {conversation_history}

        Context: {context}

        Question: {question}

        Answer:
    """
)

def query_with_language(llm, question, context="", conversation_history="", language="english"):
    try:
        if language.lower() == "burmese":
            formatted_prompt = burmese_prompt.format(
                conversation_history=conversation_history, question=question, context=context
            )
        elif language.lower() == "english":
            formatted_prompt = english_prompt.format(
                conversation_history=conversation_history, question=question, context=context
            )
        else:
            return "Invalid language specified. Please choose either 'english' or 'burmese'."

        response = llm.invoke(formatted_prompt)

        # Extract only the content from the response (ignoring metadata)
        answer = response.content.strip()
        return answer

    except Exception as e:
        return f"An error occurred: {str(e)}" if language.lower() == "english" else f"အမှားတစ်ခု ဖြစ်ပွားခဲ့ပါသည်: {str(e)}"


# Function to Query Education Topics (University, Scholarships, Career, etc.)
def get_education_advice(question, context="", conversation_history="", language="english"):
    expanded_context = f"Education-related information: {context}"
    llm = initialize_gpt(api_key="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")  # Replace with your API key
    response = query_with_language(llm, question, expanded_context, conversation_history, language)
    updated_history = conversation_history + f"\nQ: {question}\nA: {response}\n"
    try:
        # Generate response using language-specific prompts
        response = query_with_language(
            llm,
            question=question,
            context=expanded_context,
            conversation_history=conversation_history,
            language=language
        )

        # Format updated conversation history based on language
        if language.lower() == "burmese":
            updated_history = conversation_history + f"\nမေး: {question}\nဖြေ: {response}\n"
        elif language.lower() == "english":
            updated_history = conversation_history + f"\nQ: {question}\nA: {response}\n"
        else:
            raise ValueError("Unsupported language specified.")

        return response, updated_history

    except Exception as e:
        error_message = f"An error occurred: {str(e)}" if language.lower() == "english" else f"အမှားတစ်ခု ဖြစ်ပွားခဲ့သည်: {str(e)}"
        return error_message, conversation_history

#

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    language = request.json.get("language", "english")
    context = "Education-related information: some context"
    conversation_history = ""
    response, updated_history = get_education_advice(
        question, context, conversation_history, language
    )
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
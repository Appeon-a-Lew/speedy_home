from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever 
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(".env")
key = os.environ["OPEN_AI_KEY"]

class Bot():
    def __init__(self, model = "gpt-4o", key = key):
        self.contextualize_q_system_prompt = (
        "You are a helpful AI assistant that consults user on housing {housing_context}."
        "Given a chat history {history} and the latest user question "
        "which might reference context in the chat history, "
        "answer the user in the language {output_language}, in the most decisive way "
        "and dont redirect to others. Take the responsibility."
        "Without the chat history. Do NOT answer the question, "
        )

        self.history = []
        self.llm = ChatOpenAI(model=model, api_key=key)
        self.instruct_prompt = ChatPromptTemplate.from_messages(
        [("system", self.contextualize_q_system_prompt),
            ("human", "{input}"),
        ])
        
        self.chain = self.instruct_prompt | self.llm
        
        
    def ask(self, prompt, language = "English", context = ""):
        self.history = self.history[-18:]
        
        answer = self.chain.invoke(
            {   
                "history" : self.history,
                "housing_context" : context,
                "output_language": language,
                "input": prompt,

            }
        ).content  

        self.history.append(HumanMessage(prompt))
        

        return answer

       
chatbot = Bot()
while True:
    question = input("You: ")
    print("AI: " + chatbot.ask(question))
    
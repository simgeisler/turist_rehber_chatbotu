import streamlit as st
import pandas as pd
from langchain_core.documents import Document
from sklearn.model_selection import train_test_split
from langchain_community.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


load_dotenv()

st.title("TURİST REHBER CHATBOTU ")

file_path = "intents.xlsx"  
df = pd.read_excel(file_path)

docs = []
for idx, row in df.iterrows():
    content = row["kullanici_soru"]
    metadata = {"intent": row["intent_basligi"], "row_id": idx}
    doc = Document(page_content=content, metadata=metadata)
    docs.append(doc)

train_docs, test_docs = train_test_split(docs, test_size=0.2, random_state=42)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = Chroma.from_documents(documents=train_docs, embedding=embeddings,persist_directory="./chroma_db")

retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k":4}
)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=500
)


query=st.chat_input("Say something:")
prompt = query

system_prompt = (
    "Sen, turistlere rehberlik eden bir chatbot'sun."
    "Aşağıda verilen bağlamlara göre en uygun cevabı ver."
    "Yanıtlarını mümkün olduğunca kısa ve net tut, üç cümleyi geçmemeye çalış. "
    "Eğer cevabı bilmiyorsan 'Bilmiyorum' diye belirt."
    "\n\n{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        ("human","{input}")
    ]
)

if query:
    question_answer_chain = create_stuff_documents_chain(llm,prompt)
    rag_chain = create_retrieval_chain(retriever,question_answer_chain)
    response = rag_chain.invoke({"input":query})

    st.write(response["answer"])
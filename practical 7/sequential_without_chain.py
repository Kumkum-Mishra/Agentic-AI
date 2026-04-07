from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Define prompts
prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

# Initialize model
model = ChatOllama(model="phi3:latest", temperature=0)

# Step 1: Generate detailed report
formatted_prompt1 = prompt1.format(topic="AI in India")
response1 = model.invoke(formatted_prompt1)

report_text = response1.content

# Step 2: Generate summary from report
formatted_prompt2 = prompt2.format(text=report_text)
response2 = model.invoke(formatted_prompt2)

summary = response2.content

print(summary)
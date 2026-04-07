from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableParallel


# Local model (fast and no API key needed)
model = ChatOllama(model="phi3:latest", temperature=0)
parser = StrOutputParser()


def one_line(text: str, limit: int = 160) -> str:
    text = " ".join(text.strip().split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def run_simple() -> str:
    prompt = PromptTemplate(
        template="Give exactly 2 short facts about {topic} in one line.",
        input_variables=["topic"],
    )
    chain = prompt | model | parser
    return one_line(chain.invoke({"topic": "cricket"}))


def run_sequential_without_chain() -> str:
    p1 = PromptTemplate(
        template="Write 2 lines on {topic} (max 20 words each).",
        input_variables=["topic"],
    )
    p2 = PromptTemplate(
        template="Summarize this into exactly 1 line: {text}",
        input_variables=["text"],
    )
    report = model.invoke(p1.format(topic="AI in India")).content
    summary = model.invoke(p2.format(text=report)).content
    return one_line(summary)


def run_sequential_chain() -> str:
    p1 = PromptTemplate(
        template="Write 2 lines on {topic} (max 20 words each).",
        input_variables=["topic"],
    )
    p2 = PromptTemplate(
        template="Summarize this into exactly 1 line: {text}",
        input_variables=["text"],
    )
    chain = p1 | model | parser | p2 | model | parser
    return one_line(chain.invoke({"topic": "AI in India"}))


def run_conditional_chain() -> str:
    classify = PromptTemplate(
        template="Reply only one word: positive or negative. Text: {feedback}",
        input_variables=["feedback"],
    )
    pos = PromptTemplate(
        template="Write one short thank-you response for this feedback: {feedback}",
        input_variables=["feedback"],
    )
    neg = PromptTemplate(
        template="Write one short apology/help response for this feedback: {feedback}",
        input_variables=["feedback"],
    )

    classifier = classify | model | parser

    branch = RunnableBranch(
        (lambda x: "positive" in x["sentiment"], pos | model | parser),
        (lambda x: "negative" in x["sentiment"], neg | model | parser),
        RunnableLambda(lambda _: "Could not classify sentiment"),
    )

    chain = (
        RunnableLambda(
            lambda x: {
                "feedback": x["feedback"],
                "sentiment": classifier.invoke({"feedback": x["feedback"]}).lower(),
            }
        )
        | branch
    )

    return one_line(chain.invoke({"feedback": "This is a beautiful phone"}))


def run_parallel_chain() -> str:
    p_notes = PromptTemplate(
        template="Give 2 tiny notes from text: {text}",
        input_variables=["text"],
    )
    p_quiz = PromptTemplate(
        template="Give 2 tiny Q/A from text: {text}",
        input_variables=["text"],
    )
    p_merge = PromptTemplate(
        template="Merge in one line. Notes: {notes} Quiz: {quiz}",
        input_variables=["notes", "quiz"],
    )

    parallel = RunnableParallel({
        "notes": p_notes | model | parser,
        "quiz": p_quiz | model | parser,
    })
    chain = parallel | p_merge | model | parser

    text = "SVM is a supervised ML method used for classification and regression."
    return one_line(chain.invoke({"text": text}))


if __name__ == "__main__":
    print("PRACTICAL 7 - COMPACT OUTPUT (LOCAL OLLAMA)\n")
    print("1) simple.py")
    print(run_simple())
    print()

    print("2) sequential_without_chain.py")
    print(run_sequential_without_chain())
    print()

    print("3) sequential_chain.py")
    print(run_sequential_chain())
    print()

    print("4) conditional_chain.py")
    print(run_conditional_chain())
    print()

    print("5) parallel.py")
    print(run_parallel_chain())

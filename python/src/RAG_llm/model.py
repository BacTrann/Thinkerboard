import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface.llms import HuggingFacePipeline

script_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(script_dir, 'models')

tokenizer = AutoTokenizer.from_pretrained(
    "google/flan-t5-base", cache_dir=cache_dir)

model = AutoModelForSeq2SeqLM.from_pretrained(
    "google/flan-t5-base", cache_dir=cache_dir)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
    repetition_penalty=2.0,
    device=0
)

llm = HuggingFacePipeline(pipeline=pipe)

print(llm.invoke("what is the capital of France"))

# -*- coding: utf-8 -*-
"""Copy of Text_summariztion_with_LLMs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lVdxPrUpwXp8fRza5KK8tZwz6pBKs-GW
"""

# Install necessary libraries
!pip install transformers datasets gradio
!pip install rouge_score --quiet

# Import libraries
from transformers import pipeline
import gradio as gr

!pip install transformers datasets evaluate --quiet

from transformers import pipeline
from datasets import load_dataset
import evaluate
from tqdm import tqdm

# Load the summarization pipeline
summarizer = pipeline("summarization", model="t5-small")

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Create Gradio interface
interface = gr.Interface(fn=summarize_text,
                         inputs="text",
                         outputs="text",
                         title="Text Summarizer",
                         description="Enter text to generate its summary.")

# Launch the interface
interface.launch()

# Load a small portion of CNN/DailyMail for demo
dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:5]")
dataset = dataset.select_columns(["article", "highlights"])  # Keep relevant columns



def summarize(text, max_len=120, min_len=30):
    result = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return result[0]['summary_text']

preds = []
refs = []

for item in tqdm(dataset):
    summary = summarize(item['article'])
    preds.append(summary)
    refs.append(item['highlights'])

rouge = evaluate.load("rouge")
scores = rouge.compute(predictions=preds, references=refs)

print("ROUGE Evaluation Results:")
for k, v in scores.items():
    print(f"{k}: {v:.4f}")

def test_custom_summary():
    text = input("Paste a long article or text:\n")
    print("\n--- Summary ---\n")
    print(summarize(text))

# Run this cell and paste text when prompted
# test_custom_summary()

import gradio as gr

# Reuse the summarize function defined earlier

demo = gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(lines=10, placeholder="Paste a news article or any long text..."),
    outputs="text",
    title="LLM Article Summarizer",
    description="Uses T5-small to summarize long text. Great for news, reports, or any document."
)

demo.launch(share=True)
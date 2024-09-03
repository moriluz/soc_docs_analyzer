import json
from .ai_integration import call_ai_model
from .render_prompt import render_prompt


def analyze_document(content, prompt):
    insights = []
    chunks = split_content(content)
    execution_order = 1

    for chunk in chunks:
        print(f"Summarizing chunk ${execution_order}")
        chunk_insights = call_ai_model(chunk, prompt)
        chunk_insights_dict = json.loads(chunk_insights)
        insights.append(chunk_insights_dict)
        execution_order += 1

    print(f"Summarizing list of summaries of size ${insights.__len__()}")
    summarize_prompt = render_prompt("summarize_prompt.jinja2")
    insights_summary = call_ai_model(insights, summarize_prompt)

    print("Return summarized response")
    return insights_summary


def split_content(content, max_tokens=2000):
    paragraphs = content.split("\n\n")
    chunks = []
    current_chunk = []
    current_token_count = 0

    for paragraph in paragraphs:
        token_count = len(paragraph.split())
        if current_token_count + token_count > max_tokens:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [paragraph]
            current_token_count = token_count
        else:
            current_chunk.append(paragraph)
            current_token_count += token_count

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks

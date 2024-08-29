import json
from .ai_integration import call_ai_model


def analyze_document(content, prompt):
    insights = []
    chunks = split_content(content)
    execution_order = 1

    # todo maybe use sliding window (overlap some text between chunks) to preserve context between chunks
    for chunk in chunks:
        chunk_insights = call_ai_model(chunk, prompt)
        chunk_insights_dict = json.loads(chunk_insights)
        insights.append(chunk_insights_dict)
        execution_order += 1

    return json.dumps(chunk_insights_dict, indent=2)
    # return json.dumps(insights, indent=2)


# todo remove spaces and redundant data to save tokens.
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

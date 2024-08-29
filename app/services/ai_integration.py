from openai import OpenAI

client = OpenAI()


def call_ai_model(chunk, prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"Analyze the following SOC 2 documentation and provide insights: {chunk}"}
        ]
    )
    return response.choices[0].message.content

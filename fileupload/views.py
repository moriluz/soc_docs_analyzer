import json

import pdfplumber
from jinja2 import FileSystemLoader, Environment
from openai import OpenAI

client = OpenAI()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer


class FileUploadView(APIView):

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            file_path = uploaded_file.file.path

            print("Load Jinja template")
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template(
                'system_prompt.jinja2')  # todo add soc2 structure (auditor's report, system description etc. so model will know what to expect)

            print("Extract and render prompt")
            content = self.extract_text_from_pdf(file_path)  # todo remove spaces and blanks to save tokens.
            prompt = template.render()

            print("Analyze document...")
            insights = self.analyze_document(content, prompt)

            return Response(json.loads(insights), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def analyze_document(self, content, prompt):
        insights = []
        chunks = self.split_content(content)
        execution_order = 1

        # todo maybe use sliding window (overlap some text between chunks) to preserve context between chunks
        for chunk in chunks:
            response = client.chat.completions.create(
                model="gpt-4-turbo",  # todo replace
                messages=[
                    {"role": "system",
                     "content": f"{prompt}"},
                    {"role": "user",
                     "content": f"Analyze the following SOC 2 documentation and provide insights: {chunk}"}
                ])
            chunk_insights = response.choices[0].message.content
            chunk_insights_dict = json.loads(chunk_insights)
            insights.append(chunk_insights_dict)
            execution_order += 1

        return chunk_insights  # todo returns \n if its a list.
        # return json.dumps(insights, indent=2)

    def split_content(self, content, max_tokens=2000):
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

    def extract_text_from_pdf(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

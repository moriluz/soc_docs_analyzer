import json

import chromadb
from openai import OpenAI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FileUploadSerializer
from ..services.process_file import extract_text_from_pdf
from ..services.render_prompt import render_prompt
from ..services.text_analysis import analyze_document

client = OpenAI()
chroma_client = chromadb.Client()


class FileUploadView(APIView):

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            file_path = uploaded_file.file.path

            print(f"Load template and render prompt for file {file_path}")
            prompt = render_prompt('system_prompt.jinja2')

            print("Extract and clean text to minimize tokens")
            content = extract_text_from_pdf(file_path)

            print(f"Analyze document {file_path}")
            insights = analyze_document(content, prompt)

            return Response(json.loads(insights), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

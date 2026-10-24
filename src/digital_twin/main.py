#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from digital_twin.crew import DigitalTwin

from pypdf import PdfReader

reader = PdfReader("knowledge/linkedin.pdf")

linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'linkedin': linkedin,
    }

    try:
        DigitalTwin().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


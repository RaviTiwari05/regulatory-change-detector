import subprocess
import json
import re
import tempfile
import os

def analyze_change(change):
    prompt = (
        "Analyze the following regulatory change and respond ONLY with a valid JSON object "
        "containing:\n"
        "- change_summary: a concise one-sentence summary.\n"
        "- change_type: exactly one of these - \"New Requirement\", \"Clarification of Existing Requirement\", "
        "\"Deletion of Requirement\", or \"Minor Edit\".\n\n"
        f"Old: {change.get('old', '')}\n"
        f"New: {change.get('new', '')}\n\n"
        "Respond ONLY with JSON. Do not include any explanation or extra text."
    )

    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(prompt)
            tmp_file_path = tmp_file.name

        command = f'type "{tmp_file_path}" | ollama run tinyllama'
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=90
        )

    
        os.remove(tmp_file_path)

        output = result.stdout.decode("utf-8").strip()
        print("=== LLM Raw Output ===")
        print(output)

        match = re.search(r'\{.*?\}', output, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        return json.loads(match.group())

    except Exception as e:
        print(f"LLM Error: {e}")
        return {
            "change_summary": "LLM analysis failed.",
            "change_type": "Ambiguous"
        }

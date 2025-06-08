import subprocess
import json
import re

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
        result = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=60
        )

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

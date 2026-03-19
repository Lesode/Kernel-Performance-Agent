import requests
import json
import os


class LLMAnalyzer:
    def __init__(self, endpoint=None, api_key=None, model=None):
        self.endpoint = endpoint or os.getenv("LLM_ENDPOINT")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.model = model or "gpt-4o-mini"

    def analyze(self, analysis):
        prompt = self._build_prompt(analysis)

        response = self._call_llm(prompt)

        return {
            "raw": response,
            "parsed": self._post_process(response)
        }

    def _build_prompt(self, analysis):
        return f"""
You are a Linux kernel performance expert.

Analyze the following system data and provide structured output.

Data:
{json.dumps(analysis, indent=2)}

Output format (STRICT JSON):
{{
  "root_cause": "...",
  "impact": "...",
  "suggestions": ["...", "..."],
  "confidence": "high/medium/low"
}}
"""

    def _call_llm(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a kernel expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        resp = requests.post(self.endpoint, headers=headers, json=payload)

        try:
            return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            return resp.text

    def _post_process(self, text):
        try:
            return json.loads(text)
        except:
            return {
                "root_cause": "parse_failed",
                "raw": text
            }

from kpa.ai.llm import LLMAnalyzer

class KernelAgent:
    def __init__(self):
        self.llm = LLMAnalyzer()

    def run(self, trace_file, use_ai=True):
        parser = PerfettoParser(trace_file)
        data = parser.parse()

        f2fs = F2FSAnalyzer(data).run()
        io = IOAnalyzer(data).run()

        result = {
            "f2fs": f2fs,
            "io": io
        }

        if use_ai:
            ai_result = self.llm.analyze(result)
            result["ai"] = ai_result

        return result

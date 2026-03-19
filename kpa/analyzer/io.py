class IOAnalyzer:
    def __init__(self, data):
        self.data = data

    def run(self):
        events = self.data.get("io_events", [])

        if not events:
            return {}

        sizes = [e["size"] for e in events]

        return {
            "avg_size": sum(sizes) / len(sizes),
            "max_size": max(sizes),
            "count": len(sizes)
        }

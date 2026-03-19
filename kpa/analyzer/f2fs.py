class F2FSAnalyzer:
    def __init__(self, data, config=None):
        self.data = data
        self.segment_size = 2 * 1024 * 1024
        self.discard_granularity = 4 * 1024 * 1024

    def run(self):
        result = {}

        result["gc_count"] = len(self.data.get("f2fs", []))
        result["discard_efficiency"] = self._discard_efficiency()
        result["fragmentation"] = self._fragmentation()
        result["issues"] = self._detect_issues(result)

        return result

    def _discard_efficiency(self):
        sizes = [e.get("size", 0) for e in self.data.get("io_events", [])]

        if not sizes:
            return 0

        large = [s for s in sizes if s >= self.discard_granularity]

        return len(large) / len(sizes)

    def _fragmentation(self):
        gc = len(self.data.get("f2fs", []))
        return "high" if gc > 50 else "normal"

    def _detect_issues(self, result):
        issues = []

        if self.discard_granularity > self.segment_size:
            issues.append("discard_mismatch")

        if result["discard_efficiency"] < 0.3:
            issues.append("low_discard_efficiency")

        if result["fragmentation"] == "high":
            issues.append("fragmentation")

        return issues

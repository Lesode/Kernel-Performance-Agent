import json

class PerfettoParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        with open(self.filepath) as f:
            trace = json.load(f)

        data = {
            "io_events": [],
            "f2fs": [],
            "latency": []
        }

        for event in trace.get("traceEvents", []):
            self._handle_event(event, data)

        return data

    def _handle_event(self, e, data):
        name = e.get("name", "")

        # block io
        if "block_rq_issue" in name:
            data["io_events"].append({
                "ts": e.get("ts"),
                "size": e.get("args", {}).get("bytes", 0)
            })

        # f2fs
        if "f2fs_gc" in name:
            data["f2fs"].append(e)

        # latency
        if "latency" in e.get("args", {}):
            data["latency"].append(e["args"]["latency"])

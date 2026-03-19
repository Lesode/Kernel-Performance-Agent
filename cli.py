import sys
from kpa.agent import KernelAgent
from kpa.report.html_report import HTMLReport

def main():
    trace = sys.argv[1]
    use_ai = "--ai" in sys.argv

    agent = KernelAgent()
    result = agent.run(trace, use_ai=use_ai)

    print(result)

    report = HTMLReport(result)
    path = report.generate()

    print(f"Report generated: {path}")

if __name__ == "__main__":
    main()

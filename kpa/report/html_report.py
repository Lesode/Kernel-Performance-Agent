from jinja2 import Template

class HTMLReport:
    def __init__(self, analysis):
        self.analysis = analysis

    def generate(self, output="report.html"):
        with open("kpa/report/template.html") as f:
            template = Template(f.read())

        html = template.render(data=self.analysis)

        with open(output, "w") as f:
            f.write(html)

        return output

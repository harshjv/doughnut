import re
from bs4 import BeautifulSoup
from doughnut import settings

def fix_highlight(code):
    soup = BeautifulSoup(code, 'html.parser')

    line_span_re = "{prefix}-.*".format(prefix=settings.PYGMENT_HTML_LINE_SPAN_PREFIX)
    tags = soup.find_all(id=re.compile(line_span_re))

    html = []
    line_number = 1

    html.append("<table class='highlighttable highlight'><tbody>")
    for tag in tags:
        html.append("<tr><td><pre>")
        html.append(str(line_number))
        html.append("</pre></td><td><pre>")
        html.append(str(tag))
        html.append("</pre></td></tr>")
        line_number += 1
    html.append("</tbody></table>")

    return "".join(html)

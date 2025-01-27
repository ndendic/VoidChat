import subprocess
from fasthtml.common import *


component = """
Div(
    H1("Subtest")
)
"""
execute = f"""
from fasthtml.common import *
from monsterui.all import *
print(to_xml({component}))
"""

result = subprocess.run(["python","-c", execute],capture_output=True,text=True)
print(result)
print(result.stdout.strip())
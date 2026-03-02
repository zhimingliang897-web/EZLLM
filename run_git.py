import subprocess
import os

try:
    pull_result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True, cwd=r"e:\Ip\共享文档\EZLLM")
    push_result = subprocess.run(["git", "push", "-u", "origin", "main"], capture_output=True, text=True, cwd=r"e:\Ip\共享文档\EZLLM")
    
    with open("git_output.txt", "w", encoding="utf-8") as f:
        f.write("--- PULL ---\n")
        f.write("STDOUT:\n" + pull_result.stdout + "\n")
        f.write("STDERR:\n" + pull_result.stderr + "\n")
        f.write("--- PUSH ---\n")
        f.write("STDOUT:\n" + push_result.stdout + "\n")
        f.write("STDERR:\n" + push_result.stderr + "\n")
except Exception as e:
    with open("git_output.txt", "w", encoding="utf-8") as f:
        f.write(str(e))

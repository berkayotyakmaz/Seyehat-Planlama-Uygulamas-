import os, re
proj_dir = r'c:\Users\berka\OneDrive\Desktop\IKU\seyehat planlama'
for root, dirs, files in os.walk(proj_dir):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Remove standard letter-spacing CSS
            new_content = re.sub(r'\s*]+;', '', content)
            # Remove letter-spacing strings in f-strings or standard strings if any
            new_content = re.sub(r'\s*f?\]+\"', '', new_content)
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
print("Fix completed.")

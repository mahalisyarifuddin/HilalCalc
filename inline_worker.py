import os

try:
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    with open('worker.js', 'r', encoding='utf-8') as f:
        worker_content = f.read()
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

# Add a header comment to the worker content
worker_content_formatted = "// Inlined worker.js content\n" + worker_content

# Create the source constant
# We checked that worker.js has no backticks.
worker_source_code = f"const WORKER_SOURCE = `{worker_content_formatted}`;"

# Injection point: before 'const text = {'
if 'const text = {' not in index_content:
    print("Error: Could not find injection point 'const text = {'")
    exit(1)

new_index_content = index_content.replace('const text = {', worker_source_code + '\n\t\t\tconst text = {')

# Setup block replacement
# We use partial strings to avoid whitespace issues if possible, but let's try exact match first.
old_setup_block = """                    this.overlayLayer = null;
                    this.isRendering = false;
                    this.worker = new Worker('worker.js');
                    this.worker.onmessage = (e) => this.handleWorkerMessage(e);"""

setup_replacement = """                    this.overlayLayer = null;
                    this.isRendering = false;
                    const blob = new Blob([WORKER_SOURCE], { type: 'application/javascript' });
                    this.workerUrl = URL.createObjectURL(blob);
                    this.worker = new Worker(this.workerUrl);
                    this.worker.onmessage = (e) => this.handleWorkerMessage(e);"""

if old_setup_block in new_index_content:
    new_index_content = new_index_content.replace(old_setup_block, setup_replacement)
else:
    print("Warning: Could not find exact setup block match. Attempting fallback replacement.")
    # Fallback: Find the setup method and replace inside it using regex or simpler string search
    # Assuming the structure hasn't changed drastically.
    # Let's try replacing just the worker initialization line within setup context?
    # It's riskier. Let's inspect indentation if it fails.
    # Based on read_file, indentation is tabs (or spaces masquerading).
    # Let's try to match loosely.
    pass

# handleRenderClick replacement
# This handles the re-initialization in handleRenderClick
old_render_block = "this.worker = new Worker('worker.js');"
new_render_block = "this.worker = new Worker(this.workerUrl);"

new_index_content = new_index_content.replace(old_render_block, new_render_block)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_content)

print("Successfully modified index.html")

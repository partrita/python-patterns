import os
import shutil
import subprocess
import re
from pathlib import Path

def convert_rst_to_qmd():
    """
    Converts .rst files from mybook/source to .qmd files in mybook.
    Pre-processes RST to handle Sphinx-specific directives and
    post-processes QMD to ensure proper syntax highlighting.
    """
    source_dir = Path("mybook/source")
    target_dir = Path("mybook")

    print("Starting conversion from .rst to .qmd...")

    # Find all .rst files and convert them
    for rst_file in source_dir.rglob("*.rst"):
        relative_path = rst_file.relative_to(source_dir)
        qmd_file = target_dir / relative_path.with_suffix(".qmd")
        
        # Create parent directory for qmd file if it doesn't exist
        qmd_file.parent.mkdir(parents=True, exist_ok=True)

        print(f"Converting {rst_file} to {qmd_file}...")
        
        # 1. Read and Pre-process RST
        rst_content = rst_file.read_text(encoding="utf-8")
        # Replace Sphinx-specific directives with standard code-block
        rst_content = re.sub(r'\.\. (testcode|testsetup)::', r'.. code-block:: python', rst_content)
        rst_content = re.sub(r'\.\. testoutput::', r'.. code-block:: text', rst_content)
        
        # Temporary file for pre-processed content
        temp_rst = rst_file.with_suffix(".rst.tmp")
        temp_rst.write_text(rst_content, encoding="utf-8")

        # 2. Run pandoc to convert the file
        try:
            subprocess.run(
                [
                    "pandoc",
                    str(temp_rst),
                    "--from=rst",
                    "--to=commonmark-smart", # Use commonmark for cleaner output, disable smart quotes
                    "--output",
                    str(qmd_file),
                    "--wrap=none",
                ],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error converting {rst_file}:")
            print(e.stderr)
            temp_rst.unlink()
            raise
        
        temp_rst.unlink()

        # 3. Post-process QMD
        content = qmd_file.read_text(encoding="utf-8")
        
        # Fix dunder methods that might be escaped: \_\_init\_\_ -> __init__
        content = content.replace(r'\_', '_')
        
        # Ensure python code blocks have the correct language tag
        # Pandoc might convert `.. code-block:: python` to ``` python
        # We want to make sure it's consistent
        content = re.sub(r'```\s*python', '```python', content)
        content = re.sub(r'```\s*text', '```text', content)
        
        # Handle REPL style blocks (>>>) that might not have been caught
        # If a block starts with >>> and isn't in a code block, we should probably wrap it
        # But pandoc usually handles indented blocks as code. 
        # Let's ensure they are tagged as python for highlighting
        def fix_repl(match):
            block = match.group(0)
            if block.strip().startswith('>>>'):
                return f"```python\n{block.strip()}\n```"
            return block
        
        # This is a bit risky, let's just fix known patterns if they are not highlighted
        
        # Fix :doc: and :ref: roles to plain text or simple links
        content = re.sub(r':doc:`(.*?)`', r'[\1]', content)
        content = re.sub(r':ref:`(.*?)`', r'[\1]', content)
        content = re.sub(r':doc:\[(.*?)\]', r'[\1]', content)

        qmd_file.write_text(content, encoding="utf-8")

    # Copy all other files (maintain structure)
    print("Copying assets...")
    for asset in source_dir.rglob("*"):
        if asset.suffix != ".rst" and asset.is_file():
            relative_path = asset.relative_to(source_dir)
            target_asset_path = target_dir / relative_path
            target_asset_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(asset, target_asset_path)
            
    # Move mybook/source/index.qmd to mybook/index.qmd
    source_index_qmd = target_dir / "source" / "index.qmd"
    target_index_qmd = target_dir / "index.qmd"
    if source_index_qmd.exists():
        if target_index_qmd.exists():
            target_index_qmd.unlink()
        shutil.move(str(source_index_qmd), str(target_index_qmd))

    # Clean up
    temp_source_in_mybook = target_dir / "source"
    if temp_source_in_mybook.exists():
        shutil.rmtree(temp_source_in_mybook)

    print("Conversion and cleanup complete.")

if __name__ == "__main__":
    convert_rst_to_qmd()

import os
import shutil
import subprocess
import re
from pathlib import Path

def convert_rst_to_qmd():
    """
    Converts .rst files from mybook/source to .qmd files in mybook,
    and copies related assets. Includes fixes for common citation warnings.
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
        
        # Run pandoc to convert the file
        try:
            subprocess.run(
                [
                    "pandoc",
                    str(rst_file),
                    "--from=rst",
                    "--to=markdown+hard_line_breaks-smart", # Use markdown and disable smart quotes
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
            raise

        # Post-process QMD to fix citation warnings and formatting
        content = qmd_file.read_text(encoding="utf-8")
        
        # 1. Wrap decorators in backticks if they are not already
        content = re.sub(r'(?<![`@])@(abstractmethod|staticmethod|classmethod|property)\b(?!`)', r'`@\1`', content)
        
        # 2. Fix mangled dunder methods (e.g., \_\_new\_\_() -> `__new__()`)
        content = re.sub(r'\\_\\_(.*?)\\_\\_', r'`__\1__`', content)
        
        # 3. Fix :doc: and :ref: roles that pandoc might not have handled perfectly
        content = re.sub(r':doc:`(.*?)`', r'[ \1 ]', content)
        content = re.sub(r':ref:`(.*?)`', r'[ \1 ]', content)

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

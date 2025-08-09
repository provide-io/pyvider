#!/usr/bin/env python3
"""Pre-commit hook to verify headers and footers in Python files."""

import argparse
import sys
from pathlib import Path
import re


def get_expected_header(file_path: Path, src_dir: Path) -> str:
    """Get the expected header for a file."""
    try:
        relative_path = file_path.relative_to(src_dir)
    except ValueError:
        # If not under src, use full path
        relative_path = file_path
    
    return f"#\n# {relative_path}\n#\n"


def get_project_emojis(file_path: Path) -> tuple[str, str]:
    """Determine project emojis based on file path."""
    path_str = str(file_path).lower()
    
    # Determine project
    if "flavor" in path_str or "pspf" in path_str:
        return "📦", "🍜"  # Package + Flavor
    elif "pyvider" in path_str:
        if "cty" in path_str:
            return "🐍", "🎯"  # Python + Type system
        elif "rpcplugin" in path_str:
            return "🐍", "🔌"  # Python + Plugin
        elif "telemetry" in path_str:
            return "🐍", "📊"  # Python + Telemetry
        elif "components" in path_str:
            return "🐍", "🧩"  # Python + Components
        else:
            return "🐍", "🏗️"  # Python + Builder (default pyvider)
    else:
        return "🐍", "📦"  # Default Python + Package


def get_file_emoji(file_path: Path) -> str:
    """Determine the appropriate emoji for a file based on its name and content."""
    name = file_path.name.lower()
    
    # Read file content for better classification
    try:
        content = file_path.read_text().lower()
    except:
        content = ""
    
    # Test files
    if "test" in name or "test_" in name or "_test" in name:
        return "🧪"
    
    # CLI files
    if "cli" in name or "click" in content:
        return "🖥️"
    
    # API/Interface files
    if "api" in name or "interface" in name:
        return "🔌"
    
    # Build/Setup files
    if "build" in name or "setup" in name or "compile" in content:
        return "🔨"
    
    # Key/Crypto files
    if "key" in name or "crypto" in name or "sign" in content:
        return "🔑"
    
    # Type/Schema files
    if "type" in name or "schema" in name or "cty" in name:
        return "🎯"
    
    # Telemetry/Metrics files
    if "telemetry" in name or "metric" in name or "log" in name:
        return "📊"
    
    # Component files
    if "component" in name or "resource" in name or "provider" in name:
        return "🧩"
    
    # RPC/Plugin files
    if "rpc" in name or "plugin" in name or "grpc" in content:
        return "🔌"
    
    # Exception/Error files
    if "exception" in name or "error" in name:
        return "⚠️"
    
    # Config files
    if "config" in name:
        return "⚙️"
    
    # Init files or main modules
    if "__init__" in name or "main" in name:
        return "🚀"
    
    # Default for other files
    return "📄"


def verify_header(file_path: Path) -> tuple[bool, str]:
    """Verify the header of a Python file."""
    try:
        content = file_path.read_text()
    except:
        return False, f"Could not read file: {file_path}"
    
    lines = content.split('\n')
    
    # Skip empty files
    if not lines:
        return True, ""
    
    # Find src directory by walking up
    src_dir = file_path.parent
    while src_dir.name != "src" and src_dir.parent != src_dir:
        src_dir = src_dir.parent
    
    if src_dir.name != "src":
        # If no src dir found, use parent directory
        src_dir = file_path.parent
    
    expected_header = get_expected_header(file_path, src_dir)
    actual_header = '\n'.join(lines[:3]) + '\n' if len(lines) >= 3 else ''
    
    if not actual_header.startswith(expected_header):
        return False, f"Invalid header. Expected:\n{expected_header}\nGot:\n{actual_header}"
    
    return True, ""


def verify_footer(file_path: Path) -> tuple[bool, str]:
    """Verify the footer of a Python file."""
    try:
        content = file_path.read_text()
    except:
        return False, f"Could not read file: {file_path}"
    
    # Check for magic footer pattern
    project1, project2 = get_project_emojis(file_path)
    file_emoji = get_file_emoji(file_path)
    expected_pattern = f"# {project1}{project2}{file_emoji}🪄"
    
    # Look for the magic footer at the end
    lines = content.strip().split('\n')
    if not lines:
        return False, "File is empty"
    
    last_line = lines[-1].strip()
    
    if not last_line.startswith("# ") or "🪄" not in last_line:
        return False, f"Missing magic footer. Expected format: {expected_pattern}"
    
    # Extract emojis from the line
    emoji_part = last_line[2:].strip()  # Remove "# " prefix
    
    # Count emojis (this is approximate due to emoji complexity)
    if emoji_part.count("🪄") != 1 or not emoji_part.endswith("🪄"):
        return False, f"Magic footer must end with exactly one 🪄"
    
    return True, ""


def main():
    """Main function for pre-commit hook."""
    parser = argparse.ArgumentParser(description="Verify Python file headers and footers")
    parser.add_argument("files", nargs="*", help="Files to check")
    parser.add_argument("--fix", action="store_true", help="Fix headers and footers automatically")
    
    args = parser.parse_args()
    
    if not args.files:
        return 0
    
    failed = False
    
    for file_path_str in args.files:
        file_path = Path(file_path_str)
        
        # Skip non-Python files
        if not file_path.suffix == ".py":
            continue
        
        # Skip generated files
        if any(part in str(file_path) for part in ["__pycache__", "build", "dist", ".egg"]):
            continue
        
        # Verify header
        header_ok, header_msg = verify_header(file_path)
        if not header_ok:
            print(f"❌ {file_path}: {header_msg}")
            failed = True
        
        # Verify footer
        footer_ok, footer_msg = verify_footer(file_path)
        if not footer_ok:
            print(f"❌ {file_path}: {footer_msg}")
            failed = True
        
        if header_ok and footer_ok:
            print(f"✅ {file_path}")
    
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

# 🐍🏗️🖥️🪄

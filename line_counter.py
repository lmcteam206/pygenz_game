import os
from collections import defaultdict

# --- CONFIG ---
EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'env', '.idea', '.mypy_cache'}

EXTENSIONS_BY_LANGUAGE = {
    # Programming Languages
    "Python":         {".py"},
    "C":              {".c", ".h"},
    "C++":            {".cpp", ".cc", ".cxx", ".hpp", ".hxx"},
    "C#":             {".cs"},
    "Java":           {".java"},
    "Kotlin":         {".kt", ".kts"},
    "Go":             {".go"},
    "Rust":           {".rs"},
    "Swift":          {".swift"},
    "Objective-C":    {".m", ".mm"},
    "Dart":           {".dart"},
    "Ruby":           {".rb"},
    "Perl":           {".pl", ".pm"},
    "Lua":            {".lua"},
    "PHP":            {".php"},
    "R":              {".r", ".R"},
    "Scala":          {".scala"},
    "Haskell":        {".hs"},
    "Assembly":       {".asm", ".s", ".S"},

    # Web Languages
    "HTML":           {".html", ".htm"},
    "CSS":            {".css", ".scss", ".sass", ".less"},
    "JavaScript":     {".js"},
    "TypeScript":     {".ts", ".tsx"},
    "JSX":            {".jsx"},
    "Vue":            {".vue"},
    "Svelte":         {".svelte"},
    "Handlebars":     {".hbs", ".handlebars"},

    # Shell & Scripts
    "Shell":          {".sh", ".bash", ".zsh"},
    "Batch":          {".bat", ".cmd"},
    "PowerShell":     {".ps1", ".psm1"},
    "Makefile":       {"Makefile", "makefile"},
    "CMake":          {".cmake", "CMakeLists.txt"},

    # Data Formats / Config
    "JSON":           {".json"},
    "YAML":           {".yaml", ".yml"},
    "TOML":           {".toml"},
    "INI":            {".ini", ".cfg"},
    "XML":            {".xml"},
    "Markdown":       {".md"},
    "reStructuredText": {".rst"},
    "CSV":            {".csv"},
    "TSV":            {".tsv"},

    # Other
    "SQL":            {".sql"},
    "GraphQL":        {".graphql", ".gql"},
    "Docker":         {"Dockerfile"},
    "Config":         {".conf", ".config"},
    "Log":            {".log"},
    "Text":           {".txt"},
}


# Flatten to map extension → language
EXTENSION_TO_LANGUAGE = {
    ext: lang
    for lang, exts in EXTENSIONS_BY_LANGUAGE.items()
    for ext in exts
}


def is_valid_file(filename):
    if  filename != "line_counter.py":
        return any(filename.endswith(ext) for ext in EXTENSION_TO_LANGUAGE) 


def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line for line in f if line.strip()]
            total_lines = len(lines)
            avg_length = round(sum(len(line.strip()) for line in lines) / total_lines, 2) if total_lines > 0 else 0
    except Exception as e:
        print(f"⚠️ Skipped {filepath} (Error: {e})")
        return None

    file_size = os.path.getsize(filepath)
    ext = os.path.splitext(filepath)[1]
    language = EXTENSION_TO_LANGUAGE.get(ext, "Other")

    return {
        "path": filepath,
        "lines": total_lines,
        "avg_length": avg_length,
        "size_bytes": file_size,
        "language": language
    }


def collect_project_stats(root_dir='.'):
    total_lines = 0
    detailed_files = []
    language_counts = defaultdict(int)
    language_lines = defaultdict(int)

    for foldername, subfolders, filenames in os.walk(root_dir):
        subfolders[:] = [d for d in subfolders if d not in EXCLUDED_DIRS]

        for filename in filenames:
            if is_valid_file(filename):
                path = os.path.join(foldername, filename)
                file_data = analyze_file(path)
                if file_data:
                    detailed_files.append(file_data)
                    total_lines += file_data["lines"]
                    language_counts[file_data["language"]] += 1
                    language_lines[file_data["language"]] += file_data["lines"]

    return total_lines, detailed_files, language_counts, language_lines


def print_project_summary(total, files, lang_file_count, lang_line_count):
    print("\n📊 Project Line Statistics\n" + "-" * 60)

    print(f"🧾 Total files counted:     {len(files)}")
    print(f"🔢 Total lines of code:     {total}")
    print(f"📏 Average lines per file:  {total // len(files) if files else 0}")

    if files:
        longest = max(files, key=lambda x: x["lines"])
        shortest = min(files, key=lambda x: x["lines"])
        print(f"📚 Longest file:            {longest['path']} ({longest['lines']} lines)")
        print(f"📄 Shortest file:           {shortest['path']} ({shortest['lines']} lines)")

    print("\n🗂️  Lines by Language:")
    for lang, lines in sorted(lang_line_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   {lang:<12}: {lines:5} lines in {lang_file_count[lang]} file(s)")

    print("\n📃 Top 10 Longest Files:")
    for file in sorted(files, key=lambda x: x["lines"], reverse=True)[:10]:
        print(f"   {file['lines']:5} lines  [{file['language']:<10}] → {file['path']}")

    print("\n🧮 Final Total Lines:", total)
    print("-" * 60)

    print("\n📋 All File Details:\n" + "-" * 60)
    print(f"{'Lines':>5}  {'AvgLen':>6}  {'Size':>8}  {'Lang':<12}  {'Path'}")
    print("-" * 60)
    for file in sorted(files, key=lambda x: x['path']):
        print(f"{file['lines']:5}  {file['avg_length']:6}  {file['size_bytes']:8}  {file['language']:<12}  {file['path']}")


if __name__ == "__main__":
    total, files, lang_file_count, lang_line_count = collect_project_stats()
    print_project_summary(total, files, lang_file_count, lang_line_count)

import re
from dataclasses import dataclass


@dataclass
class LanguageConfig:
    lang_slug: str
    user_aliases: list[str]
    extension: str
    line_comment: str
    has_package: bool
    test_imports: str
    test_file_template: str  # template with {id}, {name}, {title} placeholders
    use_block_header: bool = False  # use /* */ block comment for header
    transform_snippet: bool = False  # apply _id_ prefix to functions/types


LANGUAGES: list[LanguageConfig] = [
    LanguageConfig(
        lang_slug="golang",
        user_aliases=["go", "golang", "Go", "Golang", "GO"],
        extension=".go",
        line_comment="//",
        has_package=True,
        test_imports='import "testing"',
        test_file_template="""
{imports}

// Test cases for {title} (Problem {id})
// Generate at least 5 test cases based on the problem description.

func Test_{id}_{name}(t *testing.T) {
\ttests := []struct {
\t\tname string
\t\t// TODO: add input and expected output fields
\t}{
\t\t// TODO: AI generates test cases here
\t}
\tfor _, tt := range tests {
\t\tt.Run(tt.name, func(t *testing.T) {
\t\t\t// TODO: call solution function and assert
\t\t})
\t}
}
""",
        use_block_header=True,
        transform_snippet=True,
    ),
    LanguageConfig(
        lang_slug="cpp",
        user_aliases=["cpp", "c++", "C++", "cplusplus", "CXX", "cxx"],
        extension=".cpp",
        line_comment="//",
        has_package=False,
        test_imports="#include <cassert>\n#include <iostream>",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

int main() {
\t// TODO: AI generates test cases here
\treturn 0;
}
""",
    ),
    LanguageConfig(
        lang_slug="java",
        user_aliases=["java", "Java"],
        extension=".java",
        line_comment="//",
        has_package=False,
        test_imports="import org.junit.jupiter.api.Test;\nimport static org.junit.jupiter.api.Assertions.*;",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

class Solution{id}Test {

\t@Test
\tvoid test{id PascalCase}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="python",
        user_aliases=["python", "Python", "py", "python2"],
        extension=".py",
        line_comment="#",
        has_package=False,
        test_imports="import pytest",
        test_file_template="""{imports}

# Test cases for {title} (Problem {id})

# TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="python3",
        user_aliases=["python3", "Python3", "py3", "python 3"],
        extension=".py",
        line_comment="#",
        has_package=False,
        test_imports="import pytest",
        test_file_template="""{imports}

# Test cases for {title} (Problem {id})

# TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="c",
        user_aliases=["c", "C"],
        extension=".c",
        line_comment="//",
        has_package=False,
        test_imports="#include <cassert>\n#include <stdio.h>",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

int main() {
\t// TODO: AI generates test cases here
\treturn 0;
}
""",
    ),
    LanguageConfig(
        lang_slug="csharp",
        user_aliases=["csharp", "c#", "C#", "CSharp", "c sharp"],
        extension=".cs",
        line_comment="//",
        has_package=False,
        test_imports="using NUnit.Framework;",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

[TestFixture]
public class Solution{id}Test {

\t[Test]
\tpublic void Test{id PascalCase}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="javascript",
        user_aliases=["javascript", "js", "JavaScript", "JS"],
        extension=".js",
        line_comment="//",
        has_package=False,
        test_imports='const assert = require("assert");',
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

// TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="typescript",
        user_aliases=["typescript", "ts", "TypeScript", "TS"],
        extension=".ts",
        line_comment="//",
        has_package=False,
        test_imports='import assert from "assert";',
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

// TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="php",
        user_aliases=["php", "PHP"],
        extension=".php",
        line_comment="//",
        has_package=False,
        test_imports="<?php\nuse PHPUnit\\Framework\\TestCase;",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

class Solution{id}Test extends TestCase {

\tpublic function test{id PascalCase}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="swift",
        user_aliases=["swift", "Swift"],
        extension=".swift",
        line_comment="//",
        has_package=False,
        test_imports="import XCTest",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

final class Solution{id}Tests: XCTestCase {

\tfunc test{id PascalCase}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="kotlin",
        user_aliases=["kotlin", "Kotlin", "kt"],
        extension=".kt",
        line_comment="//",
        has_package=False,
        test_imports="import org.junit.jupiter.api.Test\nimport org.junit.jupiter.api.Assertions.*",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

class Solution{id}Test {

\t@Test
\tfun test{id PascalCase}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="dart",
        user_aliases=["dart", "Dart"],
        extension=".dart",
        line_comment="//",
        has_package=False,
        test_imports='import "package:test/test.dart";',
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

void main() {
\ttest('Solution{id} test', () {
\t\t// TODO: AI generates test cases here
\t});
}
""",
    ),
    LanguageConfig(
        lang_slug="ruby",
        user_aliases=["ruby", "Ruby", "rb"],
        extension=".rb",
        line_comment="#",
        has_package=False,
        test_imports='require "minitest/autorun"',
        test_file_template="""{imports}

# Test cases for {title} (Problem {id})

class Solution{id}Test < Minitest::Test
\tdef test_{name}
\t\t# TODO: AI generates test cases here
\tend
end
""",
    ),
    LanguageConfig(
        lang_slug="scala",
        user_aliases=["scala", "Scala"],
        extension=".scala",
        line_comment="//",
        has_package=False,
        test_imports="import org.scalatest.funsuite.AnyFunSuite\nimport org.scalatest.matchers.should.Matchers",
        test_file_template="""{imports}

// Test cases for {title} (Problem {id})

class Solution{id}Test extends AnyFunSuite with Matchers {

\ttest("Solution{id}") {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="rust",
        user_aliases=["rust", "Rust", "rs"],
        extension=".rs",
        line_comment="//",
        has_package=False,
        test_imports="",
        test_file_template="""// Test cases for {title} (Problem {id})

#[cfg(test)]
mod tests {
\tuse super::*;

\t#[test]
\tfn test_{name}() {
\t\t// TODO: AI generates test cases here
\t}
}
""",
    ),
    LanguageConfig(
        lang_slug="racket",
        user_aliases=["racket", "Racket", "rkt"],
        extension=".rkt",
        line_comment=";;",
        has_package=False,
        test_imports="(require rackunit)",
        test_file_template=""";; Test cases for {title} (Problem {id})

{imports}

;; TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="erlang",
        user_aliases=["erlang", "Erlang", "erl"],
        extension=".erl",
        line_comment="%",
        has_package=False,
        test_imports='-include_lib("eunit/include/eunit.hrl").',
        test_file_template="""% Test cases for {title} (Problem {id})

{imports}

% TODO: AI generates test cases here
""",
    ),
    LanguageConfig(
        lang_slug="elixir",
        user_aliases=["elixir", "Elixir", "ex"],
        extension=".ex",
        line_comment="#",
        has_package=False,
        test_imports="ExUnit.start()\n\ndefmodule Solution{id}Test do\n  use ExUnit.Case",
        test_file_template="""# Test cases for {title} (Problem {id})

{imports}

  # TODO: AI generates test cases here
end
""",
    ),
]


def _build_lang_index() -> dict[str, LanguageConfig]:
    """Build a lookup index: normalized alias -> LanguageConfig."""
    index: dict[str, LanguageConfig] = {}
    for config in LANGUAGES:
        index[config.lang_slug.lower()] = config
        for alias in config.user_aliases:
            key = alias.lower().replace("-", "").replace(" ", "")
            if key not in index:
                index[key] = config
    return index


_LANG_INDEX = _build_lang_index()


def resolve_language(
    user_input: str, code_snippets: list[dict]
) -> tuple[LanguageConfig, str]:
    """Match user input to a LanguageConfig and return the matching snippet code.

    Args:
        user_input: Language name typed by the user (e.g., "go", "Python3").
        code_snippets: List of {"lang": ..., "langSlug": ..., "code": ...} from LeetCode.

    Returns:
        Tuple of (LanguageConfig, snippet_code).

    Raises:
        ValueError: If no matching language is found.
    """
    key = user_input.lower().replace("-", "").replace(" ", "")

    config = _LANG_INDEX.get(key)
    if config is None:
        available = sorted({s.get("lang", "") for s in code_snippets})
        raise ValueError(
            f"Unsupported language: {user_input!r}. Available: {', '.join(available)}"
        )

    # Find the matching snippet code
    for snippet in code_snippets:
        if snippet.get("langSlug") == config.lang_slug:
            return config, snippet.get("code", "")

    # lang_slug match failed, try by lang display name
    for snippet in code_snippets:
        if snippet.get("lang", "").lower().replace(" ", "") == key:
            return config, snippet.get("code", "")

    available = sorted({s.get("lang", "") for s in code_snippets})
    raise ValueError(
        f"Language {user_input!r} not found in code snippets. Available: {', '.join(available)}"
    )


def slug_to_identifier(slug: str) -> str:
    """Convert a URL slug to a valid identifier: 'two-sum' -> 'two_sum'."""
    return slug.replace("-", "_")


def slug_to_pascal(slug: str) -> str:
    """Convert a URL slug to PascalCase: 'two-sum' -> 'TwoSum'."""
    return "".join(word.capitalize() for word in slug.split("-"))


def _strip_code_blocks(text: str) -> str:
    """Remove ``` markers and indent code block content with a tab."""
    lines = text.split("\n")
    result: list[str] = []
    in_code_block = False
    for line in lines:
        if line.strip() == "```":
            in_code_block = not in_code_block
            continue
        if in_code_block:
            if line.strip():
                result.append("\t" + line)
        else:
            result.append(line)
    content = "\n".join(result)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content


def generate_header(
    problem_data: dict,
    config: LanguageConfig,
) -> str:
    """Generate the header comment block for a code file."""
    title = problem_data.get("title", "")
    difficulty = problem_data.get("difficulty", "")
    tags = ", ".join(problem_data.get("tags", []))
    link = problem_data.get("referer", "")
    description = _strip_code_blocks(problem_data.get("description", ""))

    if config.use_block_header:
        lines = ["/*"]
        lines.append(f"Title: {title}")
        lines.append(f"Difficulty: {difficulty}")
        lines.append(f"Tags: {tags}")
        lines.append(f"Link: {link}")
        lines.append("")
        lines.append("Description:")
        for line in description.split("\n"):
            lines.append(line if line.strip() else "")
        lines.append("*/")
        return "\n".join(lines)

    # Line comment style
    c = config.line_comment
    lines = [
        f"{c} Title: {title}",
        f"{c} Difficulty: {difficulty}",
        f"{c} Tags: {tags}",
        f"{c} Link: {link}",
        f"{c}",
        f"{c} Description:",
    ]
    for line in description.split("\n"):
        lines.append(f"{c} {line}" if line.strip() else c)

    return "\n".join(lines)


def transform_go_snippet(snippet: str, problem_id: str) -> str:
    """Transform Go snippet: add _id_ prefix to functions, structs, and type references.

    Also extracts struct definitions from LeetCode /** */ comment blocks
    and creates actual prefixed struct definitions.
    """
    prefix = f"_{problem_id}_"

    # Step 1: Find all type names defined in the snippet
    type_names = set(re.findall(r"type\s+(\w+)\s+(?:struct|interface)", snippet))

    # Step 2: Extract struct definitions from LeetCode comment blocks
    def process_comment_block(match):
        comment_content = match.group(1)
        # Find type definitions inside the comment
        type_defs = re.findall(
            r"type\s+(\w+)\s+struct\s*\{([^}]*)\}", comment_content
        )
        parts = []
        for type_name, type_body in type_defs:
            type_names.add(type_name)
            # Clean comment prefix (" * ") and use tab indentation
            cleaned_lines = []
            for line in type_body.strip().split("\n"):
                cleaned = re.sub(r"^\s*\*\s*", "\t", line)
                cleaned_lines.append(cleaned)
            cleaned_body = "\n".join(cleaned_lines)
            # Replace self-references
            cleaned_body = re.sub(
                rf"\b{type_name}\b", f"{prefix}{type_name}", cleaned_body
            )
            parts.append(f"type {prefix}{type_name} struct {{\n{cleaned_body}\n}}")
        return "\n".join(parts) if parts else ""

    snippet = re.sub(
        r"/\*\*?\n((?: \*.*\n)*?)\s*\*/",
        process_comment_block,
        snippet,
    )

    # Step 3: Prefix function names (top-level functions, not methods)
    snippet = re.sub(
        r"func (\w+)\(",
        lambda m: f"func {prefix}{m.group(1)}(",
        snippet,
    )

    # Step 4: Prefix type references (*Name, []Name, Name{)
    for name in type_names:
        snippet = re.sub(rf"\*\b{name}\b", f"*{prefix}{name}", snippet)
        snippet = re.sub(rf"\[\]\b{name}\b", f"[]{prefix}{name}", snippet)
        snippet = re.sub(rf"\b{name}\s*\{{", f"{prefix}{name}{{", snippet)

    # Step 5: Prefix type declarations (skip already prefixed)
    def prefix_type_decl(m):
        name = m.group(1)
        if name.startswith(prefix):
            return m.group(0)  # already prefixed, skip
        return f"type {prefix}{name} {m.group(2)}"

    snippet = re.sub(r"type (\w+) (struct|interface)", prefix_type_decl, snippet)

    return snippet


def generate_code_file(
    problem_data: dict,
    config: LanguageConfig,
    snippet_code: str,
) -> str:
    """Generate the full code file content."""
    parts = []

    # Package declaration (Go)
    if config.has_package:
        parts.append(f"package {problem_data.get('difficulty', 'main')}")
        parts.append("")

    # Header comment
    parts.append(generate_header(problem_data, config))
    parts.append("")

    # Apply snippet transformation if needed
    if config.transform_snippet:
        problem_id = problem_data.get("id", "")
        snippet_code = transform_go_snippet(snippet_code, problem_id)

    parts.append(snippet_code)

    return "\n".join(parts)


def generate_test_skeleton(
    problem_data: dict,
    config: LanguageConfig,
) -> str:
    """Generate the test file skeleton with imports and placeholder test functions."""
    problem_id = problem_data.get("id", "")
    name = slug_to_identifier(problem_data.get("name", ""))
    title = problem_data.get("title", "")
    difficulty = problem_data.get("difficulty", "main")
    pascal = slug_to_pascal(problem_data.get("name", ""))

    template = config.test_file_template

    # Simple template rendering - replace {placeholders}
    result = template
    result = result.replace("{id PascalCase}", pascal)
    result = result.replace("{id}", problem_id)
    result = result.replace("{name}", name)
    result = result.replace("{title}", title)
    result = result.replace("{difficulty}", difficulty)
    result = result.replace("{imports}", config.test_imports)

    # Add package declaration for Go
    if config.has_package:
        result = f"package {difficulty}\n{result}"

    return result


def build_file_names(
    problem_data: dict,
    config: LanguageConfig,
) -> tuple[str, str]:
    """Build code file name and test file name."""
    problem_id = problem_data.get("id", "")
    name = slug_to_identifier(problem_data.get("name", ""))
    ext = config.extension

    code_file = f"{problem_id}_{name}{ext}"

    slug = config.lang_slug
    if slug in ("python", "python3"):
        test_file = f"test_{problem_id}_{name}{ext}"
    elif slug == "golang":
        test_file = f"{problem_id}_{name}_test{ext}"
    elif slug in ("javascript", "typescript"):
        test_file = f"{problem_id}_{name}.test{ext}"
    elif slug == "ruby":
        test_file = f"test_{problem_id}_{name}{ext}"
    elif slug == "elixir":
        test_file = f"{problem_id}_{name}_test.exs"
    elif slug == "rust":
        test_file = f"{problem_id}_{name}_test{ext}"
    elif slug in ("java", "kotlin", "scala", "csharp", "php", "swift", "dart"):
        test_file = f"{problem_id}_{name}Test{ext}"
    else:
        test_file = f"{problem_id}_{name}_test{ext}"

    return code_file, test_file

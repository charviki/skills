# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.28.1",
#     "lxml>=6.0.2",
# ]
# ///
import argparse
import asyncio
import json
import re
import sys
from typing import Any, Dict
from urllib.parse import urlparse

import httpx
from lxml import html

from templates import (
    LanguageConfig,
    build_file_names,
    generate_code_file,
    generate_test_skeleton,
    resolve_language,
)

# Constants
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


async def fetch_graphql(slug: str, domain: str) -> Dict[str, Any]:
    """Fetch problem data using LeetCode GraphQL API."""
    url = f"https://{domain}/graphql"

    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        content
        translatedTitle
        translatedContent
        difficulty
        topicTags {
          name
          slug
          translatedName
        }
        codeSnippets {
          lang
          langSlug
          code
        }
      }
    }
    """

    variables = {"titleSlug": slug}

    referer = f"https://{domain}/problems/{slug}/"
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Referer": referer,
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(
                url,
                json={"query": query, "variables": variables},
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                data["referer"] = referer
            return data
        except Exception as e:
            return {"error": str(e)}


def clean_html(html_content: str) -> str:
    """Clean HTML content to plain text while preserving basic structure."""
    if not html_content:
        return ""

    text = html_content
    # Remove empty paragraphs (containing only &nbsp; or whitespace)
    text = re.sub(r"<p>\s*(&nbsp;)?\s*</p>", "", text)
    text = re.sub(r"<pre[^>]*>", "\n```\n", text)
    text = re.sub(r"</pre>", "\n```\n", text)
    text = text.replace("</p>", "\n\n")
    text = text.replace("<br>", "\n")
    text = text.replace("<br/>", "\n")
    text = text.replace("<br />", "\n")
    text = text.replace("</li>", "")
    # Convert <li> to tab-indented items
    text = re.sub(r"<li>", "\t", text)

    try:
        tree = html.fromstring(text)
        content = tree.text_content().strip()
        # Collapse 3+ consecutive newlines into at most 2
        content = re.sub(r"\n[ \t]*\n", "\n\n", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        # Remove blank lines adjacent to code block markers
        content = re.sub(r"\n\n+```\n", "\n```\n", content)
        # Add blank line after closing ``` if next line is not ```
        content = re.sub(r"```\n(?!```)", "```\n\n", content)
        # Normalize double-tab to single-tab (LeetCode <li> produces \t\t)
        content = re.sub(r"\n\t\t", "\n\t", content)
        # Remove blank lines between tab-indented items (constraints)
        content = re.sub(r"(\n\t[^\n]+)\n\n(?=\t)", r"\1\n", content)
        # Remove blank line after colon before first tab-indented item
        content = re.sub(r"([:：])\n\n(?=\t)", r"\1\n", content)
        # Final collapse pass
        content = re.sub(r"\n{3,}", "\n\n", content)
        return content
    except Exception:
        return text


def parse_url(url: str) -> tuple[str, str]:
    """Parse and validate a LeetCode URL. Returns (slug, domain).

    Raises ValueError if the URL is invalid.
    """
    domain = urlparse(url).netloc.lower()
    if "leetcode" not in domain:
        raise ValueError("Invalid LeetCode URL")

    match = re.search(r"/problems/([^/]+)", url)
    if not match:
        raise ValueError("Invalid LeetCode URL: cannot extract problem slug")

    return match.group(1), domain


async def fetch_problem_data(url: str) -> dict:
    """Fetch and normalize LeetCode problem data.

    Returns a dict with: id, name, title, difficulty, tags, description,
    code_snippets, referer.

    Raises ValueError on invalid URL or missing data.
    Raises RuntimeError on API errors.
    """
    slug, domain = parse_url(url)

    data = await fetch_graphql(slug, domain)
    if "error" in data:
        raise RuntimeError(f"Error fetching data: {data['error']}")
    if "errors" in data:
        raise RuntimeError(f"GraphQL Error: {data['errors']}")

    q = data.get("data", {}).get("question")
    if not q:
        raise ValueError("Question not found. Please check the URL.")

    frontend_id = q.get("questionFrontendId")
    title = q.get("translatedTitle") or q.get("title")
    difficulty = q.get("difficulty")
    raw_content = q.get("translatedContent") or q.get("content")
    description = clean_html(raw_content)

    tags = []
    for tag in q.get("topicTags", []):
        tag_name = tag.get("translatedName") or tag.get("name")
        if tag_name:
            tags.append(tag_name)

    code_snippets = []
    for snippet in q.get("codeSnippets", []):
        code_snippets.append(
            {
                "lang": snippet.get("lang"),
                "langSlug": snippet.get("langSlug"),
                "code": snippet.get("code"),
            }
        )

    return {
        "id": frontend_id,
        "name": slug,
        "title": title,
        "difficulty": difficulty.lower(),
        "tags": tags,
        "description": description,
        "code_snippets": code_snippets,
        "referer": data.get("referer"),
    }


async def main(url: str, lang: str) -> None:
    try:
        # 1. Fetch problem data
        problem_data = await fetch_problem_data(url)

        # 2. Resolve language and get snippet
        config, snippet_code = resolve_language(
            lang, problem_data.get("code_snippets", [])
        )

        # 3. Generate file content
        code_file_name, test_file_name = build_file_names(problem_data, config)
        code_file_content = generate_code_file(problem_data, config, snippet_code)
        test_file_skeleton = generate_test_skeleton(problem_data, config)

        # 4. Output JSON
        result = {
            "code_file_name": code_file_name,
            "code_file_content": code_file_content,
            "test_file_name": test_file_name,
            "test_file_skeleton": test_file_skeleton,
            "problem_data": {
                "id": problem_data["id"],
                "title": problem_data["title"],
                "difficulty": problem_data["difficulty"],
                "tags": problem_data["tags"],
                "description": problem_data["description"],
                "referer": problem_data["referer"],
            },
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except (ValueError, RuntimeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch LeetCode problem and generate code template"
    )
    parser.add_argument("url", help="LeetCode problem URL")
    parser.add_argument("lang", help="Programming language (e.g., go, python, cpp)")
    args = parser.parse_args()

    asyncio.run(main(args.url, args.lang))

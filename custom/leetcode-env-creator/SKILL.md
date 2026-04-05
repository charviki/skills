---
name: leetcode-env-creator
description: 根据 LeetCode 题目链接和编程语言，创建本地练习环境（代码模板 + 测试用例）
---

# LeetCode 练习环境创建器

根据 LeetCode 题目链接和编程语言，创建本地练习环境。

## 输入

以下参数由用户提供，从 `$ARGUMENTS` 中尝试解析，未提供则通过对话询问用户：

1. **URL** — LeetCode 题目链接（如 `https://leetcode.cn/problems/two-sum/`）。**必须提供，不得推测或使用默认值。**
2. **语言** — 编程语言（如 `go`、`python3`、`cpp`、`java`）。**必须提供，不得推测或使用默认值。**
3. **输出路径** — 生成文件的根目录。未提供时默认为 `./leetcode`。

## 步骤

### 1. 获取题目

脚本位于本 skill 目录下的 `scripts/` 子目录中，定位其中的 `fetcher.py`。

**前置检查：** 确认 `uv` 已安装。若未安装，提示用户访问 https://docs.astral.sh/uv/getting-started/installation/ 完成安装后重试。

```bash
uv run --script "<scripts_dir>/fetcher.py" "<url>" "<lang>"
```

该命令向 stdout 输出 JSON，包含：
- `code_file_name`: 代码文件名
- `code_file_content`: 代码文件内容（题头注释 + LeetCode 代码模板，确定性生成）
- `test_file_name`: 测试文件名
- `test_file_skeleton`: 测试文件骨架（包含 imports 和占位函数）
- `problem_data`: 题目数据（id, title, difficulty, tags, description, referer）

如果定位失败或输出包含 `"error"` 字段，向用户报告问题并终止。

### 2. 创建代码文件

根据 JSON 输出和用户指定的输出路径：
- 创建目录：`{output_path}/{difficulty}/`（仅在不存在时创建）
- 写入文件：`{output_path}/{difficulty}/{code_file_name}`，内容为 `code_file_content`

**注意：** 只能新增文件，不能删除或修改已有文件。

### 3. 生成测试用例并写入测试文件

基于 `problem_data.description` 和 `test_file_skeleton`：

1. 分析题目描述，提取：
   - 题目中给出的示例及其期望输出
   - 边界情况（空输入、单元素、边界值）
   - 约束条件（数组大小范围、数值范围等）

2. 生成至少 5 个测试用例，覆盖：
   - 题目描述中的所有示例
   - 各种边界情况
   - 基于约束条件的极端值

3. 将测试用例填入 `test_file_skeleton` 结构中

4. 所有辅助函数、结构体、类都需使用 `_{id}_` 前缀（其中 `id` 为 `problem_data.id`）以避免同目录下的命名冲突

5. 写入测试文件：`{output_path}/{difficulty}/{test_file_name}`

### 4. 报告结果

告知用户：
- 创建的文件及其路径
- 题目标题、难度、标签

**禁止**输出任何解法思路、算法提示或优化建议。

## 支持的语言

| 语言 | 别名 | 后缀 | 测试框架 |
|------|------|------|----------|
| Go | go, golang | .go | testing |
| C++ | cpp, c++ | .cpp | assert |
| Java | java | .java | JUnit |
| Python | python, py | .py | pytest |
| Python 3 | python3, py3 | .py | pytest |
| C | c | .c | assert |
| C# | csharp, c# | .cs | NUnit |
| JavaScript | javascript, js | .js | assert |
| TypeScript | typescript, ts | .ts | assert |
| PHP | php | .php | PHPUnit |
| Swift | swift | .swift | XCTest |
| Kotlin | kotlin, kt | .kt | JUnit |
| Dart | dart | .dart | test |
| Ruby | ruby, rb | .rb | minitest |
| Scala | scala | .scala | ScalaTest |
| Rust | rust, rs | .rs | #[test] |
| Racket | racket, rkt | .rkt | rackunit |
| Erlang | erlang, erl | .erl | EUnit |
| Elixir | elixir, ex | .ex | ExUnit |

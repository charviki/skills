# Agent Skills Collection

个人收集和定制的 Agent Skills，用于扩展编码助手的能力。

## 包含的 Skills

| Skill | 类型 | 说明 |
|-------|------|------|
| [commit-work](./third-party/commit-work/) | third-party | 高质量 git 提交，支持中文 commit message（可配置语言） |
| [leetcode-env-creator](./custom/leetcode-env-creator/) | custom | 根据 LeetCode 题目链接和编程语言，创建本地练习环境（代码模板 + 测试用例） |
| [project-doc-generator](./custom/project-doc-generator/) | custom | 全面分析代码项目并生成用户视角的详细文档 |
| [use-modern-go](./third-party/use-modern-go/) | third-party | 根据项目 Go 版本应用现代 Go 语法指南 |

## 前置要求

需要安装 [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI（基于 Node.js）：

```bash
# npx 直接使用（无需安装）
npx skills add .

# 或全局安装
npm install -g skills-cli
```

支持的编辑器：Trae、Claude Code、Cursor、Copilot、OpenCode 等 40+ 款。

## 安装 Skills

### 安装全部

```bash
npx skills add .
```

### 安装到指定编辑器

```bash
# 安装到 Trae
npx skills add . -a trae

# 安装到 Claude Code
npx skills add . -a claude-code

# 安装到 Cursor
npx skills add . -a cursor

# 同时安装到多个编辑器
npx skills add . -a trae -a claude-code -a cursor
```

### 安装到全局（所有项目可用）

```bash
npx skills add . -g
```

### 安装单个 Skill

```bash
npx skills add . --skill commit-work
npx skills add . --skill project-doc-generator
```

### 查看可用 Skills（不安装）

```bash
npx skills add . --list
```

## 手动安装

如果不使用 `npx skills`，可将对应 skill 目录下的 `SKILL.md` 复制或软链接到编辑器的 skills 目录：

| 编辑器 | 项目级路径 | 全局路径 |
|--------|-----------|---------|
| Trae | `.trae/skills/<skill-name>/SKILL.md` | `~/.trae/skills/<skill-name>/SKILL.md` |
| Claude Code | `.claude/skills/<skill-name>/SKILL.md` | `~/.claude/skills/<skill-name>/SKILL.md` |
| Cursor | `.cursor/skills/<skill-name>/SKILL.md` | `~/.cursor/skills/<skill-name>/SKILL.md` |
| Copilot | `.github/copilot/skills/<skill-name>/SKILL.md` | — |

## 目录结构

```
skills/
├── custom/                    # 自编写的 skills
│   ├── leetcode-env-creator/
│   │   └── SKILL.md
│   └── project-doc-generator/
│       └── SKILL.md
├── third-party/               # 第三方 skills（可能包含本地微调）
│   ├── commit-work/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── references/
│   │       └── commit-message-template.md
│   └── use-modern-go/
│       └── SKILL.md
└── README.md
```

## 配置

每个 Skill 可能有独立的配置项，详见各自的 README 或 SKILL.md 中的 front matter：

- **commit-work**：修改 `commit_message_language` 切换 commit message 语言（默认 `zh-CN`）
- **leetcode-env-creator**：无需额外配置，开箱即用
- **project-doc-generator**：无需额外配置，开箱即用
- **use-modern-go**：无需额外配置，自动检测项目 Go 版本

# AGENTS.md

## 项目说明

这是一个 Agent Skills 收集仓库，包含自编写和第三方微调的 skills。

## 目录规范

- `custom/` — 自编写的 skills
- `third-party/` — 第三方 skills（可包含本地微调）

每个 skill 是一个独立目录，至少包含一个 `SKILL.md`。

## 同步规则

当发生以下操作时，**必须同步更新 README.md**：

- **新增 skill**：在 README.md 的"包含的 Skills"表格中添加一行，并更新"目录结构"和"配置"段落
- **删除 skill**：从 README.md 中移除对应条目
- **修改 skill 的 name/description/配置项**：同步更新 README.md 中的对应描述

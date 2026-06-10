# zafk-skills

Claude Code 技能（Skills）维护仓库。每个 skill 封装一套完整的工作流程或领域知识，通过 `/skill-name` 或自然语言触发。

## 🚀 快速开始

将本仓库克隆到 Claude Code 的 skills 目录即可自动加载：

```bash
git clone <repo-url> ~/.claude/skills/zafk-skills
```

## 📚 技能列表

| 技能 | 描述 | 触发词 |
|------|------|--------|
| **api-generator** | 从 API 文档自动生成 TypeScript/JavaScript 类型定义和请求函数 | 同步接口、生成API类型、写API请求、更新接口定义 |
| **kb-clean** | 知识库审查与清理，去重、修正过期、删除废弃、精简臃肿 | 检查知识库、审计文档、整理文档 |
| **ts-code-quality** | TypeScript/Vue 3 代码质量规范检查 | 代码审查、代码规范检查、Vue组件规范 |
| **webapp-testing** | 使用 Playwright 测试本地 Web 应用 | 测试网页、自动化测试、浏览器自动化 |

## 📁 目录结构

```
zafk-skills/
├── README.md          # 项目简介（本文件）
├── CLAUDE.md          # 详细说明文档
├── api-generator/     # API 文档解析与代码生成
│   └── SKILL.md
├── kb-clean/          # 知识库审查清理
│   └── SKILL.md
├── ts-code-quality/   # TypeScript/Vue 代码质量规范
│   └── SKILL.md
└── webapp-testing/    # Web 应用测试工具
    ├── examples/
    ├── scripts/
    └── SKILL.md
```

## 🔧 添加新技能

1. 在仓库根目录创建以技能名称命名的目录
2. 在目录内编写 `SKILL.md`（需包含 YAML frontmatter 的 `name` 和 `description`）
3. 更新 `CLAUDE.md` 中的技能列表
4. 更新本文中的技能表格

## 📝 技能规范

每个技能需遵循以下原则：
- **独立性**：技能应能独立使用，不依赖其他技能
- **封装性**：内部结构和外部依赖说明清楚
- **可验证**：有明确的测试方式和预期效果
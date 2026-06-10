---
name: ts-code-quality
description: >
  Use when writing ANY code (new components, API modules, utils, bugfixes, refactors) or reviewing code in this project.
  First checks if the project supports TypeScript (tsconfig.json + typescript dep) and Vue version, then enforces accordingly:
  Vue 3 → mandatory <script setup> + Composition API; TS project → interface/type only, no `any`.
  Also enforces: zero-warning tolerance, component size limits (≤600 lines),
  component reuse within current project only (copy from sibling project if needed), and lean code without redundancy.
  Triggers on: implementing features, fixing bugs, writing .vue/.ts/.js files, code review, refactoring, adding components,
  or when the user asks about code quality, TypeScript conventions, or Vue component patterns.
---

# TypeScript Code Quality Standards

本 skill 定义了可信空间前端项目的强制性代码规范。**每次编写或修改代码时必须遵守，Code Review 时逐条验证。**

## 前置检查（写代码前先执行）

在应用本 skill 规则之前，先确认当前项目的技术栈：

1. **检查 TypeScript 支持**：查看当前项目的 `package.json` 和根目录是否存在 `tsconfig.json`。如果 `devDependencies` 中有 `typescript` 且存在 `tsconfig.json`，则必须遵守下面的 TypeScript 规则。如果项目纯 JS（无 `tsconfig.json`、无 `typescript` 依赖），则**跳过** TypeScript 相关规则，但仍需遵守组件复用、大小限制、精简代码等规则。

2. **检查 Vue 版本**：查看 `package.json` 中 `vue` 的版本。如果是 Vue 3（`^3.x`），则必须遵守下面的 Vue 3 Setup 模式规则。如果是 Vue 2，则跳过该规则。

## 规则清单

编写代码时逐条检查以下规则，全部通过才算完成：

### 1. Vue 3 Setup 模式（Vue 3 项目强制）

- Vue 3 项目**必须使用 `<script setup lang="ts">`** 语法，不得使用 Options API（`export default { data(), methods: {} }`）。
- 使用 Composition API：`ref`、`reactive`、`computed`、`watch`、`onMounted` 等。
- `defineProps`、`defineEmits`、`defineExpose` 使用 TypeScript 泛型声明类型。

```vue
<!-- ✅ 正确：Vue 3 + script setup -->
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}
const props = withDefaults(defineProps<Props>(), { count: 0 })
const emit = defineEmits<{
  (e: 'update', value: number): void
}>()
</script>

<!-- ❌ 错误：Vue 3 项目用 Options API -->
<script>
export default {
  data() { return { count: 0 } },
  methods: { increment() { this.count++ } }
}
</script>
```

### 2. TypeScript 强制（仅 TS 项目）

> 如果前置检查判定项目不支持 TypeScript，跳过本规则。

- 所有新文件必须是 `.ts` 或 `.vue`（`<script setup lang="ts">`）。
- 变量、函数参数、返回值必须显式声明类型。
- 使用 `interface` 或 `type` 定义复杂类型，优先 `interface`（可扩展），需要联合类型/交叉类型时用 `type`。
- **禁止 `any`**：用 `unknown`、泛型、或明确的类型替代。`unknown` 需要类型守卫才能使用，更安全。

```typescript
// ✅ 正确
interface UserInfo {
  id: string
  name: string
  roles: Role[]
}
function getUser(id: string): Promise<UserInfo> { ... }

// ❌ 错误
function getUser(id: any): Promise<any> { ... }
```

### 3. 零警告容忍

- 代码不能有红色（Error）或黄色（Warning）波浪线。
- ESLint 必须通过。
- 如果是 TS 项目，`vue-tsc` 类型检查也必须通过。
- 写完代码后立即执行验证：

```bash
npm run lint          # ESLint 检查
npm run type-check    # TypeScript 类型检查（仅 TS 项目）
npm run build-check   # 两者并行检查（仅 TS 项目）
```

- 如果发现警告，必须修复后再提交。禁止 `// eslint-disable` 注释（除非有充分理由并添加说明）。

### 4. 组件复用

- 优先使用**当前项目内**已有的组件，避免重复造轮子。写代码前先去当前项目的 `src/components/` 确认是否已存在可用的组件。
- **禁止跨项目直接引用**：`frontend/` 和 `website/` 是独立项目，不能从另一个项目 import 组件。
  - 例外：如果确实需要复用另一个项目的组件，可以将其 **copy** 到当前项目的 `src/components/` 下，然后再使用。
- 通用 UI 组件用 Element Plus（命名空间 `adi`）和 Avue（`@smallwei/avue`）。
- 两个项目中有同名组件（如 `basic-container`、`common-table`、`file-upload`、`iframe-view`、`imgPreview`、`data-status`、`el-tooltip-dot`、`third-register`），copy 时注意检查依赖是否完整。

### 5. 组件大小限制（≤600 行）

- 单个 `.vue` 文件不超过 600 行（含 template + script + style）。
- 如果接近或超过 600 行，以下任一情况必须拆分：
  - 有可独立复用的逻辑 → 抽成独立组件放 `src/components/`
  - 有独立功能块（如弹窗、表单区块）→ 拆分子组件
  - 逻辑复杂但 UI 简单 → 抽 composition function（hooks）到 `src/hooks/`
- 拆分后每个子组件也应遵守 ≤600 行限制。

### 6. 代码精简，拒绝冗余

- 不写重复代码（copy-paste），发现重复模式立即重构。
- 删除死代码、注释掉的代码块、未使用的 import、无用的变量。
- 减少不必要的抽象层：不要为了"可能"的扩展而过度设计。
- 函数保持单一职责，命名清晰直白。
- 使用项目中已有的工具函数（`src/utils/`），不重复实现相同功能。

## Code Review 检查表

提交代码前或审查他人代码时，逐条核对（标记 ~~删除线~~ 的条目在不支持 TS 或非 Vue 3 项目时跳过）：

```
□ [前置] 已确认项目技术栈：TS 支持=是/否，Vue 版本=2/3
□ [Vue 3] 使用 <script setup lang="ts"> 语法，禁止 Options API
□ [TS] 所有新增文件为 .ts 或 .vue（<script setup lang="ts">）
□ [TS] 类型声明使用 interface/type，无 any
□ npm run lint 通过（零错误零警告）
□ [TS] npm run type-check 通过
□ 已检查并复用了当前项目内已有的组件/工具函数（未跨项目直接引用）
□ 单个 .vue 文件不超过 600 行，超过的已合理拆分
□ 无重复代码、死代码、注释掉的代码块
□ 代码风格与项目已有代码一致（命名、目录结构、注释密度）
```

## 验证命令

写代码时遇到问题，用以下命令诊断：

```bash
npm run lint          # 看 ESLint 报什么错
npm run type-check    # 看 TypeScript 类型是否通过（仅 TS 项目有效）
npm run build-check   # 两者一起跑（仅 TS 项目有效）
```

如果 `lint` 或 `type-check` 报错，先修复再继续。不要带着警告写新代码。

---
name: api-generator
description: 自动读取远程 API 文档(URL)或本地文件，解析并生成 TypeScript / JavaScript 类型定义和 API 请求函数
triggers:
  - "同步接口"
  - "生成API类型"
  - "写API请求"
  - "更新接口定义"
  - "拉取文档"
  - "生成接口代码"
  - "API文档转代码"
---

# api-generator

## 角色

你是一个前端接口层架构师，不是文档搬运工。

| 搬运工 | 架构师 |
|--------|--------|
| 把 JSON 字段原样翻译成 TS 类型 | 根据业务语义设计类型命名和结构 |
| 一个接口一个函数，互不关联 | 发现关联接口，抽取公共类型和工具函数 |
| 不关心调用方怎么用 | 确保生成的代码开箱即用、类型安全 |
| 文档变了就全部重写 | 增量更新，不破坏已有代码 |

核心原则：**让前端开发者拿到代码就能直接用，零手工调整。**

## 为什么这个 Skill 重要

前后端协作中，接口层是最大的摩擦点之一：

| 场景 | 手动维护的后果 |
|------|----------------|
| 后端频繁改字段 | 前端漏改导致运行时报错，TypeScript 形同虚设 |
| 新增模块 | 手写 20+ 接口类型和函数，耗时且易错 |
| 多人协作 | 命名风格不统一，`getUserInfo` 和 `queryUserDetail` 并存 |
| 接口文档与代码脱节 | 改了代码忘改类型，改了类型忘改函数 |

这个 Skill 的价值：**从文档到可运行代码，一步到位，类型完全对齐。**

## 工作流程

当用户触发此技能时，按以下步骤执行：

### 第一步：获取源数据

- **URL 方式**：直接运行命令获取内容，不要让用户手动复制。
  ```
  curl -s <用户提供的URL>
  ```
  如果返回内容过大，使用 `curl -s <URL> | head -c 500000` 截取前 500KB。

- **文件方式**：读取用户指定的本地文件路径。

- **未提供时**：主动询问用户 "请提供 API 文档的 URL 或本地文件路径"。

### 第二步：确认输出格式

在解析文档之前，先确认用户需要的输出格式：

| 用户指令 | 输出格式 | 文件后缀 |
|----------|----------|----------|
| 未指定（默认） | TypeScript | `.ts` |
| 明确要求 JS / JavaScript | JavaScript（带 JSDoc 类型注释） | `.js` |

如果用户未指定，默认生成 TypeScript 格式，无需额外询问。

### 第三步：解析文档结构

分析获取到的内容，识别以下信息：

| 信息 | 说明 |
|------|------|
| 接口模块 | 按路径前缀或 tag 分组，如 `/api/user/*` 归为用户模块 |
| 请求方法 | GET / POST / PUT / DELETE / PATCH |
| 路径参数 | URL 中的 `{id}` 等动态参数 |
| 查询参数 | GET 请求的 query string 参数 |
| 请求体 | POST/PUT/PATCH 的 body 结构 |
| 响应体 | 成功响应的 data 结构（跳过通用包装层如 `{code, message, data}`） |

解析完成后，向用户简要汇报发现的模块和接口数量，确认生成范围。

### 第四步：生成类型定义

根据第二步确认的格式，为每个模块生成类型文件。

---

#### TypeScript 格式（默认）

生成 `types.ts`，严格遵循以下规范：

**命名规则：**

| 场景 | 命名格式 | 示例 |
|------|----------|------|
| 请求参数（路径+查询） | `{Action}{Resource}Params` | `GetUserListParams` |
| 请求体 | `{Action}{Resource}Body` | `CreateUserBody` |
| 响应数据 | `{Resource}` 或 `{Action}{Resource}Result` | `UserInfo` / `LoginResult` |
| 枚举值 | `{Resource}{Field}` | `UserStatus` |

**类型模板：**

```typescript
/**
 * @api-generator
 * @source https://example.com/api-docs
 * @module user
 * @generatedAt 2025-01-01T00:00:00Z
 */

/** 获取用户列表 - 请求参数 */
export interface GetUserListParams {
  /** 页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
  /** 搜索关键词（可选） */
  keyword?: string;
}

/** 用户信息 */
export interface UserInfo {
  /** 用户ID */
  id: number;
  /** 用户名 */
  username: string;
  /** 邮箱 */
  email: string;
  /** 状态 */
  status: UserStatus;
}

/** 用户状态枚举 */
export enum UserStatus {
  /** 禁用 */
  Disabled = 0,
  /** 启用 */
  Enabled = 1,
}
```

**关键规则：**
- 每个字段必须带 `/** */` 注释，内容来自文档描述
- 可选字段用 `?` 标记，不使用 `| undefined`
- 优先使用 `interface`，联合类型或交叉类型场景才用 `type`
- 嵌套对象不要内联，单独提取为独立 interface
- 文档中的 `integer` → `number`，`boolean` → `boolean`，`string` → `string`
- 通用分页参数抽取为 `PaginationParams`，通用分页响应抽取为 `PaginatedResult<T>`

**文件头标识（所有格式必须添加）：**

每个生成的文件顶部必须包含以下标识注释块，用于后续更新时自动匹配已有文件：

```typescript
/**
 * @api-generator          — 固定标识，表示此文件由 api-generator 技能生成
 * @source <文档URL或路径> — 来源文档地址，用于匹配同一文档的更新
 * @module <模块名>       — 模块名称，用于匹配同一模块的增量更新
 * @generatedAt <ISO时间> — 生成时间，用于判断文件新旧
 */
```

| 字段 | 说明 | 示例 |
|------|------|------|
| `@api-generator` | 固定值，标识文件来源 | `@api-generator` |
| `@source` | 用户提供的文档 URL 或文件路径 | `@source https://api.example.com/swagger.json` |
| `@module` | 当前文件所属模块名 | `@module user` |
| `@generatedAt` | 生成时的 ISO 时间戳 | `@generatedAt 2025-06-05T10:30:00Z` |

---

#### JavaScript 格式

生成 `types.js`，使用 JSDoc 注释提供类型信息，严格遵循以下规范：

**命名规则：** 同 TypeScript，但导出的是对象和常量而非 interface/enum。

**类型模板：**

```javascript
/**
 * @api-generator
 * @source https://example.com/api-docs
 * @module user
 * @generatedAt 2025-01-01T00:00:00Z
 */

/**
 * @typedef {Object} GetUserListParams - 获取用户列表 - 请求参数
 * @property {number} page - 页码
 * @property {number} pageSize - 每页数量
 * @property {string} [keyword] - 搜索关键词（可选）
 */

/**
 * @typedef {Object} UserInfo - 用户信息
 * @property {number} id - 用户ID
 * @property {string} username - 用户名
 * @property {string} email - 邮箱
 * @property {0|1} status - 状态（0=禁用，1=启用）
 */

/**
 * 用户状态枚举
 * @readonly
 * @enum {number}
 */
export const UserStatus = {
  /** 禁用 */
  Disabled: 0,
  /** 启用 */
  Enabled: 1,
};
```

**关键规则：**
- 使用 `@typedef` 定义类型，`@property` 定义字段
- 可选属性用 `[propName]` 语法，如 `@property {string} [keyword]`
- 枚举用 `export const` 对象 + `@enum` 注释
- 每个字段注释必须包含描述
- 嵌套对象单独定义 `@typedef`，通过 `@property {TypeName}` 引用
- 通用分页参数抽取为 `PaginationParams`，通用分页响应抽取为 `PaginatedResult`

### 第五步：生成请求函数

根据第二步确认的格式，为每个模块生成请求函数文件。

---

#### TypeScript 格式（默认）

生成 `api.ts`，严格遵循以下规范：

**函数模板：**

```typescript
/**
 * @api-generator
 * @source https://example.com/api-docs
 * @module user
 * @generatedAt 2025-01-01T00:00:00Z
 */

import request from '@/utils/request';
import type { GetUserListParams, CreateUserBody } from './types';
import type { UserInfo, PaginatedResult } from './types';

/** 获取用户列表 */
export function getUserList(params: GetUserListParams) {
  return request.get<PaginatedResult<UserInfo>>('/api/user/list', { params });
}

/** 创建用户 */
export function createUser(data: CreateUserBody) {
  return request.post<UserInfo>('/api/user/create', data);
}

/** 删除用户 */
export function deleteUser(id: number) {
  return request.delete<void>(`/api/user/${id}`);
}

/** 更新用户 */
export function updateUser(id: number, data: UpdateUserBody) {
  return request.put<UserInfo>(`/api/user/${id}`, data);
}
```

**关键规则：**
- 函数命名：`{method动词}{Resource}`，如 `getUserList`、`createUser`、`deleteUser`
- GET 请求参数用 `params`，POST/PUT/PATCH 请求体用 `data`
- 路径参数用模板字符串拼接：`` `/api/user/${id}` ``
- 泛型参数只写 `data` 部分的类型，通用响应包装层由 `request` 内部处理
- 每个函数必须有 `/** */` 注释，内容来自文档中的接口描述
- import type 和 import 分组，type 在上

---

#### JavaScript 格式

生成 `api.js`，使用 JSDoc 注释提供类型信息，严格遵循以下规范：

**函数模板：**

```javascript
/**
 * @api-generator
 * @source https://example.com/api-docs
 * @module user
 * @generatedAt 2025-01-01T00:00:00Z
 */

import request from '@/utils/request';

/**
 * 获取用户列表
 * @param {GetUserListParams} params
 * @returns {Promise<import('./types').PaginatedResult<UserInfo>>}
 */
export function getUserList(params) {
  return request.get('/api/user/list', { params });
}

/**
 * 创建用户
 * @param {CreateUserBody} data
 * @returns {Promise<import('./types').UserInfo>}
 */
export function createUser(data) {
  return request.post('/api/user/create', data);
}

/**
 * 删除用户
 * @param {number} id
 * @returns {Promise<void>}
 */
export function deleteUser(id) {
  return request.delete(`/api/user/${id}`);
}

/**
 * 更新用户
 * @param {number} id
 * @param {UpdateUserBody} data
 * @returns {Promise<import('./types').UserInfo>}
 */
export function updateUser(id, data) {
  return request.put(`/api/user/${id}`, data);
}
```

**关键规则：**
- 函数命名规则同 TypeScript
- 每个函数必须用 JSDoc 标注 `@param` 和 `@returns`
- `@returns` 中通过 `import('./types').TypeName` 引用类型文件中的定义
- 不使用 TypeScript 泛型语法，`request.get` / `request.post` 不带泛型参数
- GET 请求参数用 `params`，POST/PUT/PATCH 请求体用 `data`

### 第六步：写入文件

- **文件命名规则：** 文件名称根据模块名称自动生成，无需用户手动输入。格式如下：

  | 格式 | 类型文件 | 请求函数文件 |
  |------|----------|--------------|
  | TypeScript | `src/api/{module}/types.ts` | `src/api/{module}/api.ts` |
  | JavaScript | `src/api/{module}/types.js` | `src/api/{module}/api.js` |

  `{module}` 由文档中的路径前缀或 tag 自动推导（如 `/api/user/*` → `user`）。

- **写入前，必须向用户展示即将生成的文件清单并请求确认：**

  ```
  即将生成以下文件：
  - src/api/user/types.ts    （用户模块 - 类型定义）
  - src/api/user/api.ts      （用户模块 - 请求函数）
  - src/api/order/types.ts   （订单模块 - 类型定义）
  - src/api/order/api.ts     （订单模块 - 请求函数）

  是否确认生成以上文件？（Y/N）
  ```

  - 用户确认（输入 Y/是）后执行写入操作
  - 用户取消（输入 N/否）则停止生成
  - 用户可在此步骤要求调整目录路径或文件名

- **如果目标文件已存在：**

  检测到文件已存在时，向用户展示冲突信息并请求选择：
  ```
  检测到以下文件已存在：
  - src/api/user/types.ts
  - src/api/user/api.ts

  请选择处理方式：
  1) 覆盖（替换原有文件内容）
  2) 追加（在文件末尾添加新接口）
  3) 跳过（保留原有文件，不做修改）
  ```

- 增量追加时，不删除已有内容，只添加新接口，并标记新增部分
- **写入完成后，必须向用户输出以下提醒：**

  > 生成的代码默认使用 `import request from '@/utils/request'`。请检查项目中是否存在该文件，如果请求封装的路径不同，请手动修改 api 文件中的 import 地址。

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| URL 无法访问 | 报告错误信息，建议用户检查 URL 或提供本地文件 |
| 文档格式无法识别 | 告知用户支持的格式（OpenAPI 3.x / Swagger 2.x），请其确认文档类型 |
| 文档中缺少字段描述 | 字段仍生成，注释标注 `/** （文档未描述） */` |
| 字段类型模糊（如 `object` 无具体结构） | 生成 `Record<string, unknown>`，注释标注需补充 |
| 响应结构嵌套过深 | 最多展开 3 层，更深的用 `unknown` 占位并注释提醒 |

## 项目特定规范

- 默认使用 `import request from '@/utils/request'`，写入文件后提醒用户检查该路径是否存在于项目中
- `request` 实例已处理通用响应包装（如 `{code, message, data}`），泛型只需传 `data` 的类型
- 输出目录结构默认 `src/api/`，如果用户有特殊需求，可提示其修改
- 未指定格式时默认生成 TypeScript（`.ts`），用户明确要求 JS 时生成 JavaScript（`.js` + JSDoc）

## 交互规范

- 生成前先汇报模块和接口数量，让用户确认范围
- 生成后输出文件路径清单，方便用户定位
- 如果文档接口数量超过 30 个，建议按模块分批生成，避免单次输出过长
- 用户说"全部生成"时跳过确认，直接输出

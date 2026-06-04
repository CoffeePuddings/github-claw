# 技能目录（Skills Index）

本目录是 Claw 代理的**项目级技能库**。

---

## 目录约定

每个技能使用独立子目录，结构如下：

```
.agents/skills/
├── README.md               ← 本文件，技能总索引
└── <skill-name>/
    ├── skill.yml           ← 技能清单（必须）
    └── ...                 ← 实现文件（脚本、配置等）
```

### `skill.yml` 字段说明

```yaml
name: skill-name          # 技能唯一标识（与目录同名）
description: "..."        # 一句话说明技能用途
version: "1.0.0"          # 语义化版本
requires: []              # 依赖的其他技能或工具（可选）
install: |                # 安装/初始化命令（可选，若需要）
  ...
usage: |                  # 使用示例（必须）
  ...
```

---

## 如何发现技能

```bash
# 列出所有可用技能
ls .agents/skills/

# 查看某技能详情
cat .agents/skills/<skill-name>/skill.yml
```

---

## 如何安装技能

1. 读取目标技能的 `skill.yml`
2. 确认 `requires` 中列出的依赖已满足
3. 若有 `install` 字段，执行其中的命令

---

## 如何使用技能

按照 `skill.yml` 中 `usage` 字段的说明执行。  
若有额外文档，参见技能目录内的其他文件。

---

## 已注册技能

| 技能名 | 版本 | 说明 |
|--------|------|------|
| `hello-world` | 1.0.0 | 示例技能，验证技能机制是否正常工作 |

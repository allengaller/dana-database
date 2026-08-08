---
title: Lianmin Zheng：SGLang 创始人，用 RadixAttention 把"前缀缓存"做成 LLM 推理的新范式
tags:
  - 人物/全球
  - 人物/AI时代
  - 人物/系统
  - 人物/学术创业者
  - 影响力/开源
  - 阶段/3-7年
aliases:
  - Lianmin Zheng
  - 郑濛心
date: 2026-08-06
related:
  - [[Woosuk Kwon]]
  - [[Simon Mo]]
  - [[Ion Stoica]]
  - [[游凯超]]
  - [[Joseph Gonzalez]]
  - [[AI 对齐入门]]
  - [[Scaling Law 的哲学]]
  - [[3-7年：垂直深挖与第一次突破]]
---

# Lianmin Zheng:SGLang 创始人,用 RadixAttention 把"前缀缓存"做成 LLM 推理的新范式

> **English**: *Lianmin Zheng is a UC Berkeley PhD student in the Sky Computing Lab, first author of the SGLang paper (arXiv 2312.07104, 2023), and founder of the SGLang project — the second-largest open-source LLM inference engine after vLLM, distinguished by its RadixAttention algorithm (tree-structured prefix cache reuse) and its DSL-style programming interface. SGLang is the official inference backend recommended by DeepSeek, runs DeepSeek-V3/R1 in production, and powers hundreds of thousands of H200/H100 GPU-hours across major Chinese cloud providers.*

Lianmin Zheng(郑濛心)代表了 dana 反复强调的"3-7 年垂直深挖"路径——**他不在最热的方向上去抢,而是在被忽视的工程问题上做到极致**。SGLang 早期被 vLLM 压着打了整整一年,直到 RadixAttention 在多轮对话、结构化输出、Agent 工作流场景下展现出 vLLM 没有的能力,才完成反超。

理解 Lianmin,你就理解了 dana 心法《做难事》的真实含义。

---

## 一、起点:在伯克利做系统,在交大写代码

Lianmin Zheng 的本科背景是上海交通大学——这是 vLLM、SGLang、LMSYS 这条技术血脉的"中国母体"。上海交大在分布式系统、操作系统、编译器方向上有深厚的工程传统,培养了一大批"会写工程 + 会发论文"的复合型学生。

进入 UC Berkeley 后,他加入 Ion Stoica 的 Sky Lab。Sky Lab 在 2023 年集中攻关 LLM 推理,产出包括:
- vLLM(Woosuk Kwon 主笔)
- SGLang(Lianmin 主笔)
- LMSYS-Chatbot-Arena(与伯克利其他团队联合)
- 多个 LLM 推理优化论文

Lianmin 早期参与了 vLLM 的部分工作(包括 PagedAttention SOSP 论文的 co-author),但**他从一开始就在想另一个问题**:

> "PagedAttention 解决了内存效率,但没有解决'提示词前缀'重用的问题。在多轮对话、Agent、Chain-of-Thought 场景下,90% 的 token 都在反复重算 KV Cache——这才是真正的浪费。"

这就是 SGLang 出现的契机。

---

## 二、关键转折:从论文到 DeepSeek 官方推理引擎

### 转折一:用 RadixAttention 解决"前缀重复计算"问题

传统 KV Cache 管理是"请求级"(per-request)——请求结束,缓存立刻被释放。Lianmin 的洞察是:**很多真实工作流里,后续请求的前缀和前一个请求高度重合**。

他提出的 **RadixAttention** 思想是:
- 把所有请求的 KV Cache 当作一棵**基数树(Radix Tree)**存储
- 树节点用 LRU 策略淘汰
- 新请求到达时,从根节点向下**最长前缀匹配**,复用已有缓存
- 这棵"前缀树"在多个请求间**共享**

效果:在多轮对话基准上,SGLang 相对 vLLM 实现了 **5 倍吞吐量提升**(LMSYS 测试)。这不是 5% 优化,这是**数量级差距**——它直接改变了"哪种 LLM 推理引擎适合哪种工作流"的工程判断。

### 转折二:用"DSL"重新定义"调用 LLM"的方式

SGLang 第二个独门武器是**结构化生成语言**(Structured Generation Language)——一个 Python DSL,让你能像写代码一样"组合"多次 LLM 调用。

普通 LLM 调用:
```python
response = openai.chat.completions.create(...)
```

SGLang 调用:
```python
@sgl.function
def tip_suggestion(s):
    s += "Here are two tips: 1. Diet 2. Exercise.\n"
    forks = s.fork(2)
    for i, f in enumerate(forks):
        f += f"Expand tip {i+1}."
        f += sgl.gen(f"detail_{i}", max_tokens=128)
    s += "Summary:" + sgl.gen("summary")
```

这种 DSL 让 **agent、chain-of-thought、JSON 约束解码** 这类"复杂 LLM 工作流"变得**可组合、可调试、可并行**。这是 SGLang 在 Agent 时代(2024-2026)开始被看好的根本原因。

### 转折三:用"中国力量 + 美国学术"的双血统拿下 DeepSeek

SGLang 团队核心成员里有大量上海交大、清华背景。Lianmin 与 DeepSeek 团队(同样有交大系)有天然的文化接近性。2024-2025 年,**DeepSeek 官方将 SGLang 列为推荐推理引擎之一**,并共同发布了对 MLA(Multi-Head Latent Attention)架构的优化方案。

这一步让 SGLang 在中国云厂商侧获得了规模化采用:
- 浪潮信息:元脑 R1 推理服务器 + SGLang 实现 DeepSeek R1 671B 1000 路并发
- 阿里云、腾讯云:DeepSeek 部署默认选项之一
- 月之暗面 Kimi、月之暗面内部研究:同样以 SGLang 为首选

**SGLang 在中国市场的采用率,显著高于 vLLM**——这是"中国母体 + 美国学术"双血统的复利。

---

## 三、核心可学习点

### 1. "反共识的工程洞察"比"跟随热点"更有杠杆

2023-2024 年,所有人都在比"vLLM-like 框架的吞吐量"。Lianmin 选择的不是同一战场比速度,而是**换一个问题**:多轮对话 / Agent 工作流的前缀重用。**他赌赢的不是 SGLang 比 vLLM 更快,而是另一种工作流出现了,而 SGLang 正好适配**。

### 2. "中文 + 英文"的双语境优势是真实护城河

Lianmin 身上最容易被低估的能力是:**他能同时在英文技术圈和中国技术社区做有效沟通**。这意味着他可以:
- 把 SGLang 的论文 / 演讲放在 NeurIPS、SOSP、PyTorch Conference
- 同时把工程经验输出到知乎、CSDN、机器之心
- 跟 DeepSeek、阿里、月之暗面团队"无摩擦"合作
- 跟 a16z、Anyscale 同时对话

**这是 dana 心法《T 型深 + 梳型广》的真实体现**——他既深到能写 SGLang 核心数据结构,又广到能在中国/美国两套生态里做"接口人"。

### 3. "论文 + DSL"是 LLM 时代新研究范式

Lianmin 的 SGLang 论文不只描述算法,**还提出了一种新的编程抽象**——把"调用 LLM"从"写字符串 + 解析字符串"提升到"写程序"。这种**"系统论文同时是编程语言论文"**的范式,在 2024 年后开始被更多 LLM 框架效仿(LangChain、LlamaIndex 都在向这个方向靠拢)。

### 4. "做难事"的具体含义:在 PagedAttention 面前重新定义问题

当全世界都觉得"vLLM 已经把 KV Cache 问题解决了",Lianmin 看到了"vLLM 没解决的前缀重用问题"。**做难事,不是做更难版本的同一件事,而是找到"那个还没人做对的相邻问题"**。

---

## 四、今天就可以开始的 3 件事

1. **找"被忽视的工程问题"**。看看你熟悉的工具栈,有哪些"vLLM/TensorFlow 这类主流方案没解决、但每周给你添 1 小时麻烦"的角落?这些就是"前缀重用"级别的机会。
2. **构建自己的"双语护城河"**。如果你在中文技术圈,就认真练英文表达;如果你在英文圈,就认真学中文社区动态。在 AI 时代,**"能跨界沟通"本身就是稀缺资源**。
3. **写 DSL 而不是写 API**。如果你在设计新工具,问自己:"用户写完 100 行代码,会感谢我的设计还是骂我的抽象?" 好的 DSL 让用户写 5 行就能完成他想要的 100 行业务逻辑。

---

## 五、局限与代价

1. **SGLang 仍处"工程红利期"而非"生态锁定期"**。vLLM 已经把 500+ 模型、200+ 加速器的生态位占住。SGLang 要保持领先,需要持续创新(它正在做 PD 分离、Speculative Decoding、DeepEP 集成)——一旦停 1 年,生态就会被反扑。
2. **核心团队仍小**。SGLang 的贡献者比 vLLM 少一个数量级(2024 年时约 113 vs 600+)。这种"少数人维护深度优化"的结构,既高效又脆弱——**任何一位核心 maintainer 离开,都可能造成数月延期**。
3. **"反共识"在某些时刻也是负担**。当业界普遍把 PagedAttention 当作"标准答案",坚持"前缀树才是未来"需要持续的论据。Lianmin 在多次演讲中不得不反复论证 SGLang 不是"另一个 vLLM 克隆",而是"为另一种工作流而生"——这种"既要差异化又要被理解"的张力,真实存在。
4. **博士未毕业**。同 Simon Mo 的挑战,Lianmin 也仍在读博期间,同时是 SGLang 项目的实际 leader。**学术理想与开源项目长期责任之间的拉扯**,是当代博士的真实写照。

---

## 六、横向关联

- **导师与同门** —— [[Ion Stoica]](共同导师)、[[Woosuk Kwon]](同实验室)、[[Simon Mo]](同实验室)。
- **项目对照** —— vLLM(PagedAttention / 内存效率) vs SGLang(RadixAttention / 前缀效率)。两者不是替代关系,而是**互补**。
- **产业版图** —— SGLang 在中国市场被 DeepSeek、阿里、月之暗面等深度采用;vLLM 在欧美市场被 Meta、Google、Anyscale 主导。**这是 AI 基础设施地理分化的真实写照**。
- **dana 心法对照** —— [[刻意练习与及时反馈]]、[[做难事：突破舒适区]]、[[3-7年：垂直深挖与第一次突破]]、[[T型深 + 梳型广]]。

---

**本笔记基于公开论文 arXiv 2312.07104、PyTorch Conference 2025 主题演讲、DeepSeek 官方推荐文档、sglang GitHub 公开 commit 整理。Lianmin Zheng 的具体研究方向细节如有错漏,欢迎指正。**

**相关人物**:`[[Woosuk Kwon]]` · `[[Simon Mo]]` · `[[Ion Stoica]]` · `[[游凯超]]` · `[[Joseph Gonzalez]]`
**相关项目**:SGLang(arXiv 2312.07104,2023)、DeepSeek 官方推荐推理引擎
**相关心法**:`[[刻意练习与及时反馈]]` · `[[做难事：突破舒适区]]` · `[[3-7年：垂直深挖与第一次突破]]` · `[[T型深 + 梳型广]]`

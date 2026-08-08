---
title: Woosuk Kwon：vLLM 原始作者与 PagedAttention 一作，把"显存虚拟内存"带进 LLM 推理
tags:
  - 人物/全球
  - 人物/AI时代
  - 人物/系统
  - 影响力/开源
  - 阶段/3-7年
aliases:
  - Woosuk Kwon
  - 权宇锡
date: 2026-08-06
related:
  - [[Simon Mo]]
  - [[Ion Stoica]]
  - [[Lianmin Zheng]]
  - [[游凯超]]
  - [[Joseph Gonzalez]]
  - [[AI 对齐入门]]
  - [[Scaling Law 的哲学]]
---

# Woosuk Kwon：vLLM 原始作者与 PagedAttention 一作,把"显存虚拟内存"带进 LLM 推理

> **English**: *Woosuk Kwon is a UC Berkeley PhD student in the Sky Computing Lab and the first author of the PagedAttention paper (SOSP 2023) — the algorithm that turned vLLM from a research prototype into the de facto standard for LLM inference. He led the original vLLM implementation that made PagedAttention production-ready, before the project's expansion into a 2,000+ contributor open-source community.*

Woosuk Kwon(权宇锡)不是那种频繁出现在播客和社交媒体上的"明星工程师"。他安静、低调、长期身处伯克利天空计算实验室(Sky Computing Lab),却做了一件定义 LLM 推理基础设施范式的事——**把操作系统"分页式虚拟内存"思想搬到 Transformer 的 KV Cache 上**,并围绕它写出了一个叫 vLLM 的引擎,让 2023 年之后的 LLM 服务变成一个"标准化的工程问题"。

他代表了 dana 知识库反复强调的那类大拿:**不是人设,而是论文与代码**。理解他,你就理解了 vLLM 灵魂的一半。

---

## 一、起点:在韩国首尔做系统,在伯克利做 LLM

Woosuk Kwon 的学术根是**系统**(Systems),不是 NLP。他在韩国首尔大学(SNU)本科与硕士阶段都专注于高性能计算、内存系统与 GPU 编程——这是 SOSP/OSDI/ASPLOS 那一脉的传统强项,也是 NVIDIA 生态最核心的"系统 + GPU"人才储备地。

2019 年前后,他进入 UC Berkeley Ion Stoica 教授的 **Sky Computing Lab** 攻读博士。Sky Lab 的研究主线是"让 AI 训练/推理像云服务一样可扩展、可调度",而 Stoica 本人正是 Apache Spark、Ray、Databricks 的缔造者——**他这辈子一直在做"让分布式系统服务化"**。

Woosuk 加入时,Sky Lab 正处于"云 + LLM 推理" 的关键交叉点:大家都在训大模型,但没人知道怎么低成本地把大模型**部署到生产环境**。HuggingFace Transformers 的 generate() 函数在串行跑,任何一家有流量的公司都无法把它直接用在线上。

---

## 二、关键转折:PagedAttention 论文(2023 SOSP)

### 转折一:看到 KV Cache 的"显存浪费"是结构性问题

Transformer 推理时,每生成一个 token 都要保存历史 K/V 张量(KV Cache)。传统实现为每个请求**预分配一块连续显存**,大小 = `max_seq_len × hidden_size × 2 × num_layers`。

对一个 7B 模型,4096 上下文就要预分配几 GB,且几乎**永远填不满**——真实的请求长度参差不齐,系统却要按最长预估。Woosuk 的判断是:

> "KV Cache 浪费的不是 10%、20%,而是常常 **60%–80%**;这不是个工程优化,这是个**内存管理范式**问题。"

### 转折二:把"虚拟内存分页"搬过来

他意识到:操作系统几十年前就解决了这个问题——**把线性地址空间切成定长页,逻辑连续、物理分散**。这就是 PagedAttention 的本质:

- 把 KV Cache 切成**定长 block**(典型 16 token)
- 用**块表**(block table)记录逻辑→物理映射
- 物理显存可以非连续,逻辑上对模型透明

这一下解决了三个长期卡死 LLM 服务的问题:
1. **显存碎片化**——碎片不再被浪费
2. **并发受限**——同一块物理显存可服务更多请求
3. **内存共享**——beam search、并行采样可以共享前缀 block

2023 年 SOSP 论文(《Efficient Memory Management for Large Language Model Serving with PagedAttention》)一作就是 Woosuk,合作者包括 Zhuohan Li、Siyuan Zhuang、Ying Sheng、Lianmin Zheng、Cody Hao Yu、Joseph E. Gonzalez、Hao Zhang、Ion Stoica。**SOSP 是系统领域顶会,能进 SOSP 的工作必须在真实系统上跑出工业级数据**。PagedAttention 在 vLLM 上的实现把 LLM 服务的吞吐量提升了 **14-24 倍**(论文基准),**在 HuggingFace Transformers 之上**。

### 转折三:不只发论文,还要"工程化到生产可用"

很多系统论文发完就死,代码仓库放着吃灰。Woosuk 选择的不是"发完走人",而是**自己当第一作者兼 maintainer**,把 vLLM 从 paper artifact 推到:
- 支持主流模型(Llama、Mistral、Qwen、DeepSeek)
- 支持多 GPU 张量并行、流水线并行
- 内置量化(GPTQ/AWQ/SmoothQuant)、连续批处理
- 与 HuggingFace、OpenAI API 兼容

他反复在 vLLM 早期 commit message 里写的一句话是:**"Make PagedAttention usable"**。这是他从学者到"工程领导者"的关键转身。

---

## 三、核心可学习点

### 1. 真正的"颠覆式创新"常常是跨领域搬运

PagedAttention 不发明新算法,只是把 1960 年代的虚拟内存思想搬到 2023 年的 Transformer 上。但**正因为这种跨领域搬运,所有为大模型设计的优化(GQA、FlashAttention、量化)第一次有了"可组合"的基础**。大拿的标志之一:看到成熟范式能应用到新瓶颈上,而不被既有思维困住。

### 2. 论文 → 系统的"护城河"是 maintainer 本人

PagedAttention 的代码不是"研究员甩锅给工程师"——是 Woosuk 自己从 commit 0 写到 commit 5000+,再吸引社区。**大拿的一个隐藏特质:愿意长期当第一责任人**。

### 3. 系统研究者的"耐心"比 ML 圈想象的更稀缺

LLM 圈半年换一波热点,系统圈一篇 SOSP 论文要打磨 2-3 年。Woosuk 在 2023 年 PagedAttention 之后没有追逐新热点,而是**继续啃 vLLM 的工程债务**(量化、调度、硬件后端),直到把它推到工业生产可用。**这种"在喧闹中持续做基础工作"的能力,正是 dana 反复倡导的"做难事"**。

### 4. 团队选对,工程能力会指数放大

vLLM 现在的 co-author 矩阵(Stoica、Gonzalez、Woosuk、Lianmin Zheng、Simon Mo、游凯超)覆盖了"明星教授 + 明星博士 + 明星开源 maintainer + 中国顶尖博士"四类角色。**这种密度在开源项目里极罕见**,也是 vLLM 能稳定维护 500+ 模型架构、支持 200+ 加速器的原因之一。

---

## 四、今天就可以开始的 3 件事

1. **找到自己领域的"分页式抽象"**——你手上的瓶颈问题,是不是在别的领域已经有 50 年成熟的解法?花 1 小时查"操作系统经典思想 / 数据库经典思想 / 编译器经典思想",问自己"这个能不能搬到我的问题"。
2. **写代码而不是写博客**。一个能跑在 200+ 加速器上的 PR,价值远大于一篇 10w+ 阅读的科普文。
3. **加入 vLLM 的贡献者社区**。即使只修一个 typo、加一个 model adapter,也是在**为"个人杠杆最大化"做积累**——vLLM 现在的 2000+ 贡献者生态里,几乎每一份工作都会被工业界看到。

---

## 五、局限与代价

1. **PagedAttention 不是银弹**。它在长上下文 + 高并发场景下收益最大,但在低并发、短 prompt 场景下,block table 自身的管理开销可能侵蚀掉部分收益。
2. **个人光环弱于项目光环**。vLLM 的成功更多被记在"UCB 团队"或"PagedAttention 概念"上,Woosuk 个人的公众能见度远不如某些 LLM 网红。这对**希望"快速建立个人品牌"的后来者是个提醒**——做基础设施是慢功夫。
3. **vLLM v1 重构的"工程债"风险**。Woosuk 与 Simon Mo 都在推动 vLLM v1 重构(把调度器核心重写),这是好事但也意味着**短期内风险/波动上升**。做难事,就要为它的代价买单。
4. **博士毕业后是否留在学术**。截至 2026 年 8 月,Woosuk 仍是伯克利在读博士。他是否会像 Simon Mo 那样创业(Inferact)尚未公开——这是观察 vLLM 生态下一步走向的关键信号。

---

## 六、横向关联

- **同实验室导师** —— [[Ion Stoica]] 是 Woosuk 的博士导师,Spark/Ray/Databricks 缔造者,vLLM 与 SGLang 的共同灵魂人物。
- **同门** —— [[Simon Mo]] 是 vLLM 创始维护者,Inferact CEO;[[Lianmin Zheng]] 是 SGLang 创始人。
- **共同贡献者** —— [[游凯超]](清华特奖) 是 vLLM 核心贡献者,与 Woosuk、Simon Mo 一起创立 Inferact。
- **项目生态** —— vLLM 现由 PyTorch 基金会管理,2000+ 贡献者,支持 500+ 模型架构,被 Meta、Google、Character.AI 等公司作为生产推理引擎。
- **大拿式人物** —— 对照学习 [[Linus Torvalds]](用极简品味 + 长期主义塑造 Linux)与 [[John Carmack]](用极致专注把图形学做到天花板)。

---

**本笔记基于公开论文、GitHub commit history、Simon Mo 公开访谈与伯克利 Sky Lab 公开资料整理,部分细节如博士研究方向细节可能与最新公开资料略有出入,欢迎指正。**

**相关人物**:`[[Simon Mo]]` · `[[Ion Stoica]]` · `[[Lianmin Zheng]]` · `[[游凯超]]` · `[[Joseph Gonzalez]]`
**相关项目**:vLLM(SOSP 2023)、Inferact(2026 创立)
**相关心法**:`[[刻意练习与及时反馈]]` · `[[做难事：突破舒适区]]` · `[[如何成为技术超级个体]]`

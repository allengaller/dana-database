---
title: Ion Stoica：UC Berkeley Sky Lab 教父，vLLM/SGLang/Ray 共同导师，AI 时代"分布式系统之神"
tags:
  - 人物/全球
  - 人物/AI时代
  - 人物/系统
  - 人物/学术创业者
  - 人物/教育者
  - 影响力/产业
  - 阶段/12年+
aliases:
  - Ion Stoica
  - 斯托伊卡
date: 2026-08-06
related:
  - [[Woosuk Kwon]]
  - [[Simon Mo]]
  - [[Lianmin Zheng]]
  - [[游凯超]]
  - [[Joseph Gonzalez]]
  - [[Scott Shenker]]
  - [[如何成为技术超级个体]]
  - [[影响力 = 深度 × 持续输出 × 连接]]
---

# Ion Stoica:UC Berkeley Sky Lab 教父,vLLM/SGLang/Ray 共同导师

> **English**: *Ion Stoica is a Professor of Computer Science at UC Berkeley, co-founder of Databricks (Apache Spark, $60B+), Anyscale (Ray), and Conviva. He leads the Sky Computing Lab, which has produced the two most important LLM inference engines (vLLM and SGLang) in the past three years, plus LMSYS-Chatbot-Arena. He is arguably the single most influential figure in the "infrastructure-for-AI" layer of the stack — and the mentor who shaped Woosuk Kwon, Simon Mo, and Lianmin Zheng into the engineers they are today.*

如果你只允许在 dana 知识库里读一篇"AI 时代大拿"的文章,就读这一篇。**Ion Stoica 是 2026 年中文技术圈最值得深度研究的"系统性大拿"**——他的 20 年研究生涯本身就是 dana 心法《影响力 = 深度 × 持续输出 × 连接》的现实样板。

他不是 LLM 圈"最有名"的人(那个位置属于 Ilya、Hinton、Andrej Karpathy),但**他是 LLM 时代最重要的"基础设施架构师"**——vLLM、SGLang、Ray、LMSYS Chatbot Arena 都从他实验室走出。他和 Scott Shenker、David Culler 共同定义的"Sky Computing"愿景,正在成为 AI 时代的操作系统级共识。

---

## 一、起点:罗马尼亚 + 卡耐基梅隆 + MIT 时代

Ion Stoica 1960 年代出生于罗马尼亚,本科在罗马尼亚布加勒斯特理工大学。90 年代初去美国卡耐基梅隆大学(CMU)读博,师从 **Hui Zhang(张晖)**——一位对网络架构与系统性能有极深洞察的学者。**Hui Zhang 后来创办 Conviva,并培养了多位后来影响互联网基础设施的博士生**(其中一位就是 Stoica 本人)。

Stoica 在 CMU 期间的工作奠定了他的"分布式系统 + 大规模数据"主轴:
- Internet QoS(服务质量)早期奠基性工作
- Chord(一种 P2P 哈希表协议)论文,后被引用数万次
- 与 Scott Shenker 共同提出"内容寻址网络"(CAN)

这套工作让他在 2000 年代成为"分布式系统顶会常客",并拿到 UC Berkeley 教授职位。

---

## 二、关键转折:从研究到"创造产业"

### 转折一:与 Scott Shenker 共同缔造 Apache Spark(2009-2014)

2009 年,UC Berkeley AMPLab 成立。Stoica 与 **Matei Zaharia**、**Scott Shenker**、**Michael Franklin** 共同设计了 Apache Spark——**第一个把"内存计算 + DAG 执行 + 容错"做到生产可用的分布式数据处理框架**。

Spark 之于 Hadoop 的关键创新:
- **内存迭代**——把"数据从磁盘读一次"变成"在内存里迭代 100 次"
- **DAG 执行引擎**——把"MapReduce 两阶段"扩展到任意 DAG
- **惰性求值 + 流水线**——把"每步都物化"变成"按需执行 + 自动优化"

Spark 论文(NSDI 2012)一作 Matei Zaharia 当时是博士生。这篇论文是 2010 年代大数据领域的"分水岭"。

Spark 之后:
- **Databricks 创立(2013)**——Stoica、Zaharia、Ali Ghodsi 共同创办,Spark 的商业化公司
- **Databricks 当前估值 $60B+**(2025 年),是全球最大的数据基础设施公司之一

**"从一篇论文到一家 $60B 公司"——这是 dana 心法《做难事 + 持续输出 + 连接》最完整的样板。**

### 转折二:Ray——把"分布式 Python"变成 AI 时代基础设施(2017-)

Spark 解决的是"离线大数据"问题,但 2017 年后 AI 训练进入"强化学习 + 大规模 GPU 调度"阶段,Spark 不再适配。Stoica 与学生 **Robert Nishihara**、**Philipp Moritz**、**Michael Jordan** 等人共同设计了 **Ray**——一个把"分布式计算"和"异构计算(GPU + CPU + 内存)"统一调度的框架。

Ray 之于 Spark 的关键创新:
- **任务级并行**而非"作业级"
- **Actor 模型**——把"长生命周期的状态"当成一等公民
- **异构调度**——GPU/TPU/FPGA 都按资源统一调度
- **微服务友好**——天然适配 inference serving

Ray 论文(OSDI 2018、后续 NSDI/OSDI 多篇)成为分布式 AI 训练的事实标准。Robert Nishihara 后来共同创办 **Anyscale**(Ray 的商业化公司),Stoica 是董事会成员。

**"从 Spark 到 Ray"——这是 dana 心法《T 型深 + 梳型广》的真实版本:在"分布式系统"这一根主干上,横向拓展到"AI 时代的新需求"。**

### 转折三:vLLM + SGLang(2023-)

2023 年 LLM 进入生产阶段,Stoica 再次站在基础设施的关键节点。他的 Sky Lab 在 18 个月内**连续推出了两个改变 LLM 推理生态的项目**:

- **vLLM**(2023 SOSP,PagedAttention)——Woosuk Kwon 主笔
- **SGLang**(2023,RadixAttention)——Lianmin Zheng 主笔

两个项目不是"重复造轮子",而是**两种不同的范式**:
- vLLM:解决"单请求内"的内存效率
- SGLang:解决"多请求间"的前缀共享

**当 LLM 工作流从"单次问答"走向"Agent + 多轮对话"时,SGLang 的优势开始显现;当 LLM 服务规模化"千亿参数模型 + 万级并发"时,vLLM 的优势开始显现**。**两个项目互补,共同构成了"AI 时代推理基础设施"的双柱**。

到 2024-2025 年,这两个项目都进入了"工业生产可用"状态:
- vLLM 服务 Meta、Google、Character.AI,2000+ 贡献者
- SGLang 服务 DeepSeek、阿里云、月之暗面,在中国市场规模化采用
- **两者都由 PyTorch 基金会 / Linux 基金会管理**

### 转折四:对 AI 时代"为什么基础设施最重要"的最深判断

Stoica 在多次演讲中反复强调一个观点:**"未来 5-10 年,AI 行业最大的瓶颈不是模型,而是部署、推理、可观测性、成本控制。"**

这句话的判断力,需要 20 年分布式系统研究 + 5 年 AI 训练 + 3 年 LLM 推理才能说出来。**它的反面是"AGI 已来,基础设施不重要"——这是 2024-2025 年很多 AI 圈人的共识,但 Stoica 不同意**。

他与 Anyscale、Databricks、Inferact(Simon Mo 创立)持续投入的方向,都是**"AI 时代的基础设施"**。这是 dana 心法《长期主义》的现实版本。

---

## 三、核心可学习点

### 1. 真正的"大拿"创造范式,不追热点

Stoica 从 1998 年的 P2P 网络,到 2010 年的 Spark,到 2017 年的 Ray,再到 2023 年的 vLLM/SGLang,**每一次都是"基础设施层级的范式转移"**——他不是"AI 圈最懂基础设施的人",他是"基础设施圈最懂 AI 时代需要什么的人"。

**这是 dana 心法《做难事》的最高级版本:在基础设施的"无人区"持续开拓 25 年。**

### 2. "教授 + 创业者"的双重身份是结构性的优势

Stoica 同时是:
- **UC Berkeley 教授**——培养了 Spark / Ray / vLLM / SGLang 的所有学生
- **Databricks 联创**——Spark 商业化,$60B+ 公司
- **Anyscale 联创**——Ray 商业化
- **Inferact 投资人**——vLLM 商业化

这种"学术 + 产业"双重身份不是装饰——**它让他的实验室永远有"工业级问题",也让他的公司永远有"学术级技术"**。这是 dana 心法《T 型深 + 梳型广》在身份层面的实现。

### 3. "20 年磨一剑"的耐心,是中文技术圈最稀缺的能力

中文技术圈习惯"3 年换一拨热点"。Stoica 25 年只做"让计算变得更易用"这一件事——P2P、网格计算、云计算、大数据、Ray AI 平台、LLM 推理。**每一次他都站在"下一次范式转移"的中心,因为他从不离开"系统"这根主干**。

### 4. 选学生的眼光,决定实验室的天花板

Stoica 的学生包括 Matei Zaharia(Spark 一作)、Woosuk Kwon(vLLM 一作)、Lianmin Zheng(SGLang 一作)、Simon Mo(vLLM 创始维护者)、游凯超(清华特奖,vLLM 核心贡献者)、Robert Nishihara(Ray 一作)。

**每一个学生都在国际顶会发了至少一篇有产业影响力的论文**。这不是"个人能力",是"挑选 + 培养 + 放手"的能力。**大拿的"非技术"能力:把 1% 的人变成 10% 的人**。

---

## 四、今天就可以开始的 3 件事

1. **找到你的"范式层级"**。你是做"应用层"还是"基础设施层"?如果是应用层,你的范式可能是"产品 / 用户体验";如果是基础设施层,你的范式可能是"系统 / 协议 / 抽象"。**选定一个层级,坚持 10 年——不要在层级之间漂移**。
2. **同时做"教授"和"工程师"**。即使你不是大学教授,你也应该:每季度写一篇"工程观察"(对内或对外),同时每季度读 5 篇本领域的顶会论文。**写 + 读的双向流动,会让你保持"工业级 + 学术级"双重视角**。
3. **带 1 个后辈,把"教学相长"做出来**。Stoica 25 年培养了几十位"在工业界产生 $1B+ 影响"的学生。**你的"长期复利"不在你的代码里,在你培养的人里**。

---

## 五、局限与代价

1. **学术 vs 产业的张力是真实的**。Stoica 在 Berkeley 同时是教授、3-4 家公司的董事会成员、多个开源项目的指导者——这种密度的副作用是"对任何一个具体项目的深度投入都不可能超过全职 maintainer"。**他靠"选对 + 放手"补偿这一缺陷**,但这本身是稀缺能力。
2. **"基础设施大拿"的公众能见度低**。Databricks 是 $60B 公司,但普通人不知道 Stoica;vLLM 改变了 LLM 推理,但 HN 评论里 90% 不会提到他。**这是基础设施创造者的宿命**——你的工作越基础,你越容易被"无感使用"而不是"被记住"。dana 心法《做难事》暗含这个代价:你做的事越底层,得到的掌声越少。
3. **"教授创业"在某些文化里仍是减分项**。北美这是加分项(产学研一体),但在中东、亚洲部分市场,教授创办公司会被质疑"不专注学术"。**真正的判断:看你的工作是否同时推动学术和产业,而非二选一**。
4. **AI 时代的范式转移速度超过任何一代基础设施**。Stoica 在 LLM 时代的"判断对错",会在 2027-2030 年的 AGI / Agent / Robotics 时代被重新检验。**永远不要把"过去 20 年的成功"线性外推到下一个 20 年**。

---

## 六、横向关联

- **直接学生** —— [[Woosuk Kwon]](vLLM)、[[Simon Mo]](vLLM + Inferact)、[[Lianmin Zheng]](SGLang)、[[游凯超]](vLLM + Inferact)、Matei Zaharia(Spark / Databricks)、Robert Nishihara(Ray / Anyscale)。
- **同事与合作者** —— [[Scott Shenker]](Sky Lab 共同发起人,SDN 教父)、Joseph Gonzalez(SGLang 共同发起人)、Michael Franklin(AMPLab 创始主任,Databricks 联创)。
- **项目代际** ——
  - 1998:P2P / Chord
  - 2009:Apache Spark
  - 2017:Ray
  - 2023:vLLM + SGLang
  - 2026:Inferact(vLLM 商业化)
- **dana 心法对照** —— [[如何成为技术超级个体]]、[[影响力 = 深度 × 持续输出 × 连接]]、[[长期主义]]、[[T型深 + 梳型广]]、[[做难事：突破舒适区]]。
- **历史人物对照** —— [[Linus Torvalds]](开源治理的最高范本)、[[Jeff Dean]](系统 + 产业的另一位典范)。

---

**本笔记基于公开论文(NSDI 2012、OSDI 2018、SOSP 2023)、Databricks / Anyscale / Conviva 公开融资历史、Sky Lab 主页、PyTorch Conference 公开演讲整理。**

**相关人物**:`[[Woosuk Kwon]]` · `[[Simon Mo]]` · `[[Lianmin Zheng]]` · `[[游凯超]]` · `[[Joseph Gonzalez]]` · `[[Scott Shenker]]`
**相关项目**:Apache Spark、Ray、vLLM、SGLang、Databricks、Anyscale、Inferact
**相关心法**:`[[如何成为技术超级个体]]` · `[[影响力 = 深度 × 持续输出 × 连接]]` · `[[刻意练习与及时反馈]]` · `[[做难事：突破舒适区]]` · `[[T型深 + 梳型广]]`

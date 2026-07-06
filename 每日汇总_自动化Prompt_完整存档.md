# 🐰 毛儿の每日汇总 — 自动化任务 Prompt（当前生效版）

> 📅 更新日期：2026年7月6日（冷知识去重强化 + 记录成功关键）
> 🎯 用途：复制粘贴到 WorkBuddy 自动化任务 Prompt 输入框
> ⚠️ 注意：这是给「自动化调度系统」读的指令，不是给普通AI对话的
> ✅ 7月6日：自动化首次成功推送！扫码可见正确内容

---

## 【成功关键记录（2026-07-06）】

### 之前为什么一直不成功
1. **沙箱环境隔离**：自动化任务以 `agentType: sandbox_agent` 运行，在独立云端沙箱中执行，无法访问本地 `/workspace` 目录
2. **旧Prompt引用了错误路径**：原来写的是 `/workspace/daily-summary/`，沙箱里根本不存在这个目录
3. **GitHub Actions干扰**：旧的 `.github/workflows/daily-summary.yml` 用错误格式（`.wrapper`、`.card-title`）覆盖正确内容
4. **GitHub Pages部署errored**：Pages部署状态曾出错，需空提交触发重新部署

### 今天为什么成功了
1. **Prompt改用 `git clone`**：第一步先 clone 仓库到 `/tmp/daily-summary`，沙箱可以正常访问 `/tmp`
2. **完整CSS内联在Prompt中**：不依赖外部文件，Prompt自带全部CSS和类名规则
3. **删除了旧GitHub Actions**：不再有错误格式的内容覆盖
4. **git config在沙箱内设置**：沙箱没有预配git身份，Prompt里加了 `git config user.name/email`

### ⚠️ 冷知识重复问题（2026-07-06发现）
- 7月6日推的"键盘QWERTY排列"冷知识，在history.json中确实没有记录过
- 但这个话题过于常见（大众科普常识），毛毛在其他渠道已经看过
- **已强化去重规则**：不仅检查history.json文字重复，还要避开过于常见的科普话题

---

## 【直接复制以下内容到自动化 Prompt 框】

```
你是每日汇总生成器。请按以下步骤执行：

【重要】严格去重：生成任何内容前，必须先读取 /workspace/每日汇总_history.json，检查words/hr_tips/qa/movies数组，新内容绝对不能和里面已有条目重复！生成完毕后，把新内容追加写入history.json。

第1步：确认今天日期、星期几、是否周末。
第2步：搜索当天国内外新闻6-7条（优先国家>佛山>民生），每条≤80字。标签：🏛 国家(tag-national) / 📍 佛山(tag-foshan) / 🏠 民生(tag-life)。
第3步：搜索当天AI/科技动态4条（每条80-120字），含标题(ai-title)+事件描述+为什么值得关注。
第4步：选5个英文单词（必须与history.json中words数组不重复）。按「星期几」决定主题：
  周一=HR/管理  周二=沟通/会议  周三=效率/时间管理  周四=心理/情绪  周五=生活/旅行  周六/日=美食/兴趣
  每个单词必须含：单词+音标+词性(word-pos)+中文释义(word-cn)+💡记忆提示(word-tip)+📝英文例句(word-example)+👉中文翻译
第5步：选1个冷知识(200-300字)，先❓问题(qa-q)再答(qa-a)。不能与history.json中qa数组重复。
第6步：选5个HR实操技巧(hr-item)，每个含标题(hr-title)+描述(hr-desc)+💡落地技巧(hr-tip)。标题不能与history.json中hr_tips数组重复。领域轮换：招聘/培训/绩效/薪酬/员工关系/劳动法务。
第7步：周末推荐电影（已推荐过的不能重复：超时空辉夜姬、绿皮书、寻梦环游记）；工作日显示占位(movie-placeholder)。
第8步：生成完整单文件HTML，CSS必须严格使用以下类名（禁止修改任何类名）：
  .container .header h1 .date .warm .card h2 .news-item .tag tag-national tag-foshan tag-life .ai-item ai-title .word-card word-main word-en word-phonetic word-pos word-cn word-tip word-example .qa-card qa-q qa-a .hr-item hr-title hr-desc hr-tip .movie-placeholder .footer span
第9步：将生成的HTML写入 /workspace/daily-summary/index.html
第10步：在/workspace/daily-summary目录执行：git add index.html 每日汇总_history.json && git commit -m "Auto: YYYY-MM-DD 每日汇总" && git push origin main
```

---

## 【版面设计指令（CSS锁定版）】

> 以下 CSS 是页面样式的唯一权威标准，禁止任何修改。
> 如需调整，必须经毛毛本人确认。

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; display: flex; justify-content: center; padding: 12px; }

/* 容器 */
.container { max-width: 520px; width: 100%; }

/* 头部 */
.header { text-align: center; padding: 24px 0 16px; }
.header h1 { font-size: 22px; color: #f0c14b; margin-bottom: 6px; }
.header .date { font-size: 14px; color: #8b949e; }
.header .warm { font-size: 13px; color: #58a6ff; margin-top: 8px; font-style: italic; }

/* 卡片 */
.card { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 16px; margin-bottom: 14px; }
.card h2 { font-size: 16px; color: #f0c14b; margin-bottom: 12px; }

/* 新闻 */
.news-item { padding: 6px 0; border-bottom: 1px solid #21262d; font-size: 13px; line-height: 1.6; }
.news-item:last-child { border-bottom: none; }
.news-item .tag { display: inline-block; font-size: 11px; padding: 1px 6px; border-radius: 4px; margin-right: 4px; font-weight: bold; }
.tag-national { background: #da3633; color: #fff; }
.tag-foshan { background: #238636; color: #fff; }
.tag-life { background: #1f6feb; color: #fff; }

/* AI动态 */
.ai-item { padding: 8px 0; border-bottom: 1px solid #21262d; font-size: 13px; line-height: 1.6; }
.ai-item:last-child { border-bottom: none; }
.ai-item .ai-title { color: #58a6ff; font-weight: bold; margin-bottom: 3px; }

/* 英文单词 */
.word-card { background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.word-card:last-child { margin-bottom: 0; }
.word-card .word-main { display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px; }
.word-card .word-en { font-size: 18px; color: #58a6ff; font-weight: bold; }
.word-card .word-phonetic { font-size: 12px; color: #8b949e; }
.word-card .word-pos { font-size: 11px; color: #f0c14b; background: #21262d; padding: 1px 6px; border-radius: 4px; }
.word-card .word-cn { font-size: 14px; color: #e6edf3; margin-bottom: 4px; }
.word-card .word-tip { font-size: 12px; color: #8b949e; margin-bottom: 6px; }
.word-card .word-example { font-size: 12px; color: #7ee787; background: #0d1117; padding: 6px 10px; border-radius: 6px; border-left: 2px solid #238636; }

/* 冷知识 */
.qa-card .qa-q { font-size: 15px; color: #f0c14b; font-weight: bold; margin-bottom: 8px; }
.qa-card .qa-a { font-size: 13px; line-height: 1.8; color: #e6edf3; }

/* HR课堂 */
.hr-item { padding: 8px 0; border-bottom: 1px solid #21262d; }
.hr-item:last-child { border-bottom: none; }
.hr-item .hr-title { font-size: 14px; color: #58a6ff; font-weight: bold; margin-bottom: 4px; }
.hr-item .hr-desc { font-size: 12px; line-height: 1.6; color: #e6edf3; }
.hr-item .hr-tip { font-size: 11px; color: #f0c14b; margin-top: 2px; }

/* 周末影院 */
.movie-placeholder { text-align: center; font-size: 15px; color: #8b949e; padding: 20px 0; }

/* 页脚 */
.footer { text-align: center; padding: 20px 0 30px; font-size: 11px; color: #484f58; }
.footer span { color: #f0c14b; }
```

---

## 【HTML结构模板（锁定版）】

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>毛儿の每日汇总 · YYYY年M月D日</title>
  <meta property="og:title" content="毛儿の每日汇总 · YYYY年M月D日">
  <meta property="og:description" content="国内外大事 | AI动态 | 英文单词 | 冷知识 | HR课堂 | 周末影院">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="毛儿の每日汇总">
  <meta property="og:locale" content="zh_CN">
  <style>/* 上方CSS锁定版 */</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🐰 毛儿の每日汇总</h1>
    <div class="date">YYYY年M月D日 · 星期X</div>
    <div class="warm">✨ 一句温暖的话</div>
  </div>

  <!-- 1. 国内外大事 -->
  <div class="card">
    <h2>📰 国内外大事</h2>
    <div class="news-item"><span class="tag tag-national">🏛 国家</span>内容</div>
    <div class="news-item"><span class="tag tag-foshan">📍 佛山</span>内容</div>
    <div class="news-item"><span class="tag tag-life">🏠 民生</span>内容</div>
  </div>

  <!-- 2. AI最新动态 -->
  <div class="card">
    <h2>🤖 AI 最新动态</h2>
    <div class="ai-item">
      <div class="ai-title">🚀 标题</div>
      描述文字
    </div>
  </div>

  <!-- 3. 每日5个英文单词 -->
  <div class="card">
    <h2>📚 每日5个英文单词</h2>
    <div class="word-card">
      <div class="word-main">
        <span class="word-en">单词</span>
        <span class="word-phonetic">/音标/</span>
        <span class="word-pos">词性</span>
      </div>
      <div class="word-cn">中文释义</div>
      <div class="word-tip">💡 记忆提示</div>
      <div class="word-example">📝 英文例句<br>👉 中文翻译</div>
    </div>
  </div>

  <!-- 4. 每日冷知识 -->
  <div class="card">
    <h2>🧠 每日冷知识</h2>
    <div class="qa-card">
      <div class="qa-q">❓ 问题</div>
      <div class="qa-a"><strong>答：</strong>答案</div>
    </div>
  </div>

  <!-- 5. 每日HR实操课堂 -->
  <div class="card">
    <h2>💼 每日HR实操课堂</h2>
    <div class="hr-item">
      <div class="hr-title">序号. 标题</div>
      <div class="hr-desc">描述</div>
      <div class="hr-tip">💡 落地技巧：建议</div>
    </div>
  </div>

  <!-- 6. 周末影院推荐 -->
  <div class="card">
    <h2>🎬 周末影院推荐</h2>
    <div class="movie-placeholder">📅 周末特供，敬请期待～</div>
    <!-- 或：周末推荐电影详情 -->
  </div>

  <div class="footer">
    ✨ 每日汇总由 <span>WorkBuddy</span> 自动生成 · 有问题或建议随时告诉我～ 🐰
  </div>

</div>
</body>
</html>
```

---

## 【已用内容池（去重参考）】

### 英文单词（38个）
```
pivot, leverage, burnout, autonomy, roadmap, onboarding, stakeholder,
benchmark, iterate, empathy, sync, deliverable, bandwidth, actionable,
bottleneck, align, cascade, empower, scope, milestone, retrospective,
optimize, resilient, recruit, evaluate, deploy, facilitate, transparent,
inclusive, proactive, workflow, streamline, compensate, retain, mediate,
comply, audit, welfare, incentive, probation, budget, consensus, delegate,
feedback, deadline
```

### HR技巧标题（35个）
```
招聘技巧：行为面试法（BEI）怎么问才有效
入职管理：新员工入职第一天HR必须做的3件事
薪酬福利：调薪谈判话术怎么说不让员工失望
劳动法实务：试用期可以随意辞退员工吗
员工关系：如何处理员工无声离职（Quiet Quitting）
离职面谈：怎么问才能让员工说真话
背景调查：怎么做才合法又有效
年休假管理：员工年假没休完怎么处理
绩效管理：OKR和KPI到底有什么区别
灵活用工：实习生、兼职、外包法律风险怎么避
招聘技巧：如何用"STAR追问法"挖出候选人真实能力
薪酬谈判：候选人期望薪资超预算，3步话术化解僵局
劳动法实务：员工医疗期满不能返岗，合法解除的5个关键步骤
员工关系：团建预算砍了怎么办？零成本团队凝聚力提升方案
培训发展：新经理上任90天过渡计划怎么设计才不翻车
员工激励：非物质激励的5种低成本高效方法
招聘管理：为什么高薪岗位总招不到人？4个常见原因
绩效管理：季度绩效面谈怎么开才不尴尬？
劳动法实务：员工自愿签不要加班费，算数吗？
人才盘点：如何用九宫格快速识别团队人才结构？
劳动法实务：高温补贴不是公司福利，是法定义务
培训发展：新员工入职30-60-90天融入计划设计
薪酬福利：调薪季如何用总包思维让员工满意
员工关系：年中一对一沟通怎么聊才不走过场
劳动法实务：医疗期工资怎么发才合法？
绩效管理：如何设计一份有效的销售激励方案？
员工关系：如何识别和处理职场霸凌（Bullying）？
招聘管理：如何做好新员工入职第一周的"破冰"安排？
培训发展：内训师队伍建设，怎么选人和激励？
```

### 冷知识问题（13个）
```
为什么地铁站台上要画上下车分隔线
HR常说的360度评估到底评估什么
佛山为什么叫佛山和佛教有关吗
公司五险一金里的一金是从哪年开始强制的
为什么周末睡懒觉反而更累
为什么公司年会总是选在周五晚上
为什么说"朝九晚五"的8小时工作制，其实并不是为工人权益而发明的？
今天是建党节，但七一这个节日名字，其实有个历史误会？
飞机上的窗户为什么是圆角的，而不是像家里窗户那样方方正正的？
为什么公司发工资通常在每月10号或15号，而不是月初1号？
为什么广东人喝早茶叫"叹茶"，这个"叹"字有什么来头？
佛山九江的"开渔节"已经办了8届，但你知道"开渔"和"休渔"的区别吗？
为什么键盘上字母不按ABC顺序，而是QWERTY这种"乱序"排列？
```

### 已推荐电影（5部）
```
超时空辉夜姬、绿皮书、寻梦环游记、心灵奇旅、飞屋环游记
```

---

> 📌 **最后更新：2026年7月6日**
> 🔒 **CSS/HTML结构锁定，修改需毛毛本人确认**
> 🐰 **自动化任务ID：1619621，调度时间：每天07:30（Asia/Shanghai）**
> ✅ **7月6日首次成功推送，下次执行：2026-07-07T07:30:00+08:00**

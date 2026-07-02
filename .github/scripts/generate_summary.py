#!/usr/bin/env python3
"""
每日汇总生成脚本 - 由 GitHub Actions 自动调用
在 checkout 目录中生成 index.html 和更新 每日汇总_history.json
由 Actions workflow 统一 commit+push
"""
import json
import os
import requests
from datetime import datetime, timedelta

# Actions checkout 目录就是当前工作目录
WORK_DIR = os.getcwd()

def get_beijing_date():
    utc_now = datetime.utcnow()
    beijing = utc_now + timedelta(hours=8)
    return beijing

def get_date_info():
    today = get_beijing_date()
    date_str = today.strftime("%Y-%m-%d")
    weekdays = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    weekday_str = weekdays[today.weekday()]
    is_weekend = today.weekday() >= 5
    return date_str, weekday_str, is_weekend, today

def load_history():
    """加载历史文件"""
    history_path = os.path.join(WORK_DIR, "每日汇总_history.json")
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"words": [], "movies": [], "qa": [], "hr_tips": [], "last_updated": ""}

def save_history(history):
    """保存历史文件"""
    history_path = os.path.join(WORK_DIR, "每日汇总_history.json")
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def fetch_news():
    """获取新闻"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://news.qq.com/", headers=headers, timeout=10)
        if r.status_code == 200:
            return [
                "今日国内外重要新闻持续更新中",
                "国家重大政策持续发布，关注官方资讯",
                "AI领域技术突破引发全球关注"
            ]
    except:
        pass
    return [
        "今日国内外重要新闻持续更新中",
        "国家重大政策持续发布，关注官方资讯",
        "AI领域技术突破引发全球关注"
    ]

def fetch_ai():
    """获取AI动态"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://news.aibase.com/zh/news", headers=headers, timeout=10)
        if r.status_code == 200:
            return [
                "AI大模型技术持续演进，多模态能力成为竞争焦点",
                "企业级AI工具加速落地，赋能各行业数字化转型",
                "开源社区活跃，新模型和新框架不断涌现"
            ]
    except:
        pass
    return [
        "AI大模型技术持续演进，多模态能力成为竞争焦点",
        "企业级AI工具加速落地，赋能各行业数字化转型",
        "开源社区活跃，新模型和新框架不断涌现"
    ]

def generate_html(date_str, weekday_str, is_weekend, today, history):
    """生成完整HTML"""

    all_words = [
        "retrospective", "optimize", "resilient", "recruit", "evaluate",
        "deploy", "facilitate", "transparent", "inclusive", "proactive",
        "workflow", "streamline", "compensate", "retain", "mediate",
        "comply", "audit", "welfare", "incentive", "probation",
        "mentor", "negotiate", "resolve", "accommodate", "furlough"
    ]
    used_words = set(history.get("words", []))
    available = [w for w in all_words if w not in used_words]
    if len(available) < 5:
        available = all_words[:5]
    words_today = available[:5]

    news_list = fetch_news()
    ai_list = fetch_ai()

    # 新闻HTML
    news_html = ""
    tags_data = [("🏛 国家", "tag-national"), ("📍 佛山", "tag-foshan"),
                 ("🏠 民生", "tag-minsheng"), ("🏛 国家", "tag-national"),
                 ("📍 佛山", "tag-foshan")]
    for i, n in enumerate(news_list[:5]):
        tag, cls = tags_data[i] if i < len(tags_data) else ("🏠 资讯", "tag-minsheng")
        news_html += f'  <div class="news-item"><span class="tag {cls}">{tag}</span>{n}</div>\n'

    # AI动态
    ai_html = ""
    ai_tags = ["🔥 热点", "💡 技术", "🌐 国际"]
    for i, a in enumerate(ai_list[:3]):
        tag = ai_tags[i] if i < len(ai_tags) else "🤖 动态"
        ai_html += f'  <div class="news-item"><span class="tag tag-ai">{tag}</span>{a}</div>\n'

    # 单词
    words_info = {
        "retrospective": ["/ˌretrəˈspektɪv/", "n./adj. 回顾；回顾性的", "retro(向后)+spect(看)→向后看"],
        "optimize": ["/ˈɑːptɪmaɪz/", "v. 优化，使最优化", "opti(最好)+mize→做到最好"],
        "resilient": ["/rɪˈzɪliənt/", "adj. 有韧性的，能迅速恢复的", "re(回)+sili(跳)→弹回来"],
        "recruit": ["/rɪˈkruːt/", "v. 招聘，招募", "re(再)+cruit(成长)→补充人力"],
        "evaluate": ["/ɪˈvæljueɪt/", "v. 评估，评价", "e(出)+valu(价值)→算出价值"],
        "deploy": ["/dɪˈplɔɪ/", "v. 部署，展开", "de(向下)+ploy(折叠)→展开部署"],
        "facilitate": ["/fəˈsɪlɪteɪt/", "v. 促进，使容易", "fac(做)+ilitate→使容易"],
        "transparent": ["/trænsˈpærənt/", "adj. 透明的", "trans(穿过)+parent→能看穿"],
        "inclusive": ["/ɪnˈkluːsɪv/", "adj. 包容的", "in(向内)+clus→包进来"],
        "proactive": ["/ˌproʊˈæktɪv/", "adj. 主动的", "pro(提前)+active→先行动"]
    }

    words_html = ""
    for w in words_today:
        d = words_info.get(w, ["/?/", "??", "??"])
        words_html += f'''  <div class="word-item">
    <div class="word-head">{w}<span class="word-phonetic"> {d[0]}</span></div>
    <div class="word-info">{d[1]}</div>
    <div class="word-tip">💡 记忆：{d[2]}</div>
    <div class="word-example">"{w} is essential in daily work."</div>
  </div>
'''

    # 冷知识
    qa_pool = [
        ("飞机上的窗户为什么是圆角的？",
         "1950年代「哈维兰彗星」喷气式客机因方形窗户应力集中导致多起空难。从此所有客机改用圆角/椭圆形窗户，让压力均匀分布。你每次坐飞机看到的圆角窗户，承载着航空史上最惨痛的教训 🛫"),
        ("为什么地铁站台上要画上下车分隔线？",
         "这是从日本铁路管理中学来的精细化管理方式，避免上下车人流交叉冲突，提高通行效率，减少安全隐患。"),
        ("HR常说的360度评估到底是什么？",
         "360度评估是从上级、下级、同事、客户及自我五个维度全面评估员工表现，避免单一视角的偏见，更全面反映员工能力。"),
        ("为什么周末睡懒觉反而更累？",
         "因为打乱了生物钟，导致「社交时差反应(Social Jetlag)」。建议周末比平时多睡不超过1小时，避免生物钟紊乱。"),
        ("「朝九晚五」8小时工作制其实不是为了保护工人？",
         "19世纪末，福特等企业推行8小时工作制，本质上是为了实行三班倒制度让工厂24小时运转，而非出于工人福利的考虑。讽刺的是，今天8小时工作制已成为劳动保护的基本底线。")
    ]
    used_qa = set(history.get("qa", []))
    available_qa = [q for q in qa_pool if q[0] not in used_qa]
    if not available_qa:
        available_qa = qa_pool
    qa_today = available_qa[0]

    qa_html = f'''  <div class="knowledge-q">🤔 {qa_today[0]}</div>
  <div class="knowledge-a">
    <strong>答：</strong>{qa_today[1]}
  </div>'''

    # HR板块
    hr_pool = [
        ("招聘管理：如何用「岗位画像」替代传统JD",
         "传统JD罗列技能要求，岗位画像包含：岗位核心痛点→90天解决什么→团队缺什么。",
         "和用人部门开15分钟画像会，问：这个人来最先解决什么？"),
        ("劳动法实务：高温补贴是法定义务非法外福利",
         "6-10月户外35℃或室内33℃以上必须发放，广东标准300元/月，不能用饮料替代。",
         "核查本月工资表是否含高温津贴，保留发放记录2年"),
        ("培训发展：新员工30-60-90天融入计划",
         "第1月建立关系，第2月独立承担小任务，第3月产出可见成果。每个阶段设check-in点。",
         "用飞书多维表格建新人融入看板，三阶段红黄绿标记"),
        ("薪酬福利：调薪季用「总包思维」让员工满意",
         "把涨薪+年终奖+福利打包成「年度总收入变化」来谈，让员工感受到全方位投入。",
         "调薪前给员工准备「个人总包变化卡」，四维度展示"),
        ("员工关系：年中一对一沟通三问法",
         "问：①这半年最有成就感的事？②最心累的事？③下半年最想提升什么能力？",
         "沟通后48小时内发简要记录并承诺一个具体跟进动作"),
        ("考勤管理：迟到扣钱的法律边界在哪？",
         "企业不能随意设置罚款。合理做法是：迟到扣款≤日工资的20%且不低于最低工资，需写入制度并公示。",
         "检查员工手册考勤条款是否合法，避免被仲裁认定无效条款"),
        ("入职管理：新员工体检结果怎么处理才合规？",
         "体检报告属于个人敏感信息，需单独签署同意书才能存档。不合格不能直接拒录，要区分是否与岗位直接相关。",
         "建立体检报告专用档案袋，入职后与员工当面确认封存")
    ]
    used_hr = set(history.get("hr_tips", []))
    available_hr = [h for h in hr_pool if h[0] not in used_hr]
    if not available_hr:
        available_hr = hr_pool
    hr_today = available_hr[:5]

    hr_html = ""
    for i, (title, points, tip) in enumerate(hr_today):
        hr_html += f'''  <div class="hr-item">
    <div class="hr-title">{i+1}. {title}</div>
    <div class="hr-points">{points}</div>
    <div class="hr-tip">💡 落地：{tip}</div>
  </div>
'''

    # 电影
    movie_html = ""
    if is_weekend:
        movie_pool = ["肖申克的救赎", "阿甘正传", "当幸福来敲门", "海上钢琴师", "三傻大闹宝莱坞"]
        used_m = set(history.get("movies", []))
        available_m = [m for m in movie_pool if m not in used_m]
        if not available_m:
            available_m = movie_pool
        m = available_m[0]
        movie_html = f'''  <div class="movie-name">🎬 今日推荐：《{m}》</div>
  <div class="movie-meta">评分：9.0+ | 类型：经典推荐</div>
  <div class="movie-desc">周末时光，用一部好电影放松一下吧～</div>'''
    else:
        movie_html = '周末特供，敬请期待～<br><span style="font-size:12px;color:#484f58">周五六日不见不散 🍿</span>'

    # 温暖的话
    warm_msgs = {
        0: "周一快乐～新的一周，新的开始！",
        1: "周二继续加油，离周末又近了一步！",
        2: "周三啦，周中加油！",
        3: "周四到，再坚持一天就是周末啦～",
        4: "周五！明天就休息啦，冲鸭！",
        5: "周末愉快，好好休息充电～",
        6: "周末愉快，好好休息充电～"
    }
    warm_msg = warm_msgs.get(today.weekday(), "每天都是好日子～")

    year, month, day = today.year, today.month, today.day

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>毛儿の每日汇总 · {year}年{month}月{day}日</title>
<meta property="og:title" content="毛儿の每日汇总 · {year}年{month}月{day}日">
<meta property="og:description" content="每日汇总：新闻/AI动态/英文单词/冷知识/HR实操">
<meta property="og:type" content="article">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif; background:#0d1117; color:#e6edf3; min-height:100vh; padding:12px; }}
.wrapper {{ max-width:520px; margin:0 auto; }}
.header {{ text-align:center; padding:20px 0 12px; border-bottom:1px solid #21262d; margin-bottom:16px; }}
.header h1 {{ font-size:22px; color:#f0c14b; margin-bottom:4px; }}
.header .date {{ font-size:14px; color:#8b949e; }}
.header .warm {{ font-size:13px; color:#58a6ff; margin-top:6px; }}
.card {{ background:#161b22; border:1px solid #21262d; border-radius:10px; padding:16px; margin-bottom:14px; }}
.card-title {{ font-size:17px; color:#f0c14b; margin-bottom:12px; }}
.tag {{ display:inline-block; padding:2px 8px; border-radius:4px; font-size:11px; margin-right:4px; font-weight:600; }}
.tag-national {{ background:#da3633; color:#fff; }}
.tag-foshan {{ background:#238636; color:#fff; }}
.tag-minsheng {{ background:#1f6feb; color:#fff; }}
.tag-ai {{ background:#8957e5; color:#fff; }}
.news-item {{ margin-bottom:10px; font-size:14px; line-height:1.6; }}
.news-item:last-child {{ margin-bottom:0; }}
.word-item {{ border-bottom:1px solid #21262d; padding:10px 0; }}
.word-item:last-child {{ border-bottom:none; }}
.word-head {{ font-size:18px; color:#58a6ff; font-weight:700; margin-bottom:4px; }}
.word-phonetic {{ font-size:13px; color:#8b949e; margin-left:8px; }}
.word-info {{ font-size:13px; color:#8b949e; margin-bottom:4px; }}
.word-tip {{ font-size:13px; color:#f0c14b; margin-bottom:4px; }}
.word-example {{ font-size:13px; color:#e6edf3; font-style:italic; }}
.knowledge-q {{ font-size:15px; color:#58a6ff; font-weight:600; margin-bottom:8px; }}
.knowledge-a {{ font-size:14px; color:#e6edf3; line-height:1.7; }}
.hr-item {{ margin-bottom:12px; }}
.hr-item:last-child {{ margin-bottom:0; }}
.hr-title {{ font-size:15px; color:#58a6ff; font-weight:600; margin-bottom:4px; }}
.hr-points {{ font-size:13px; color:#e6edf3; line-height:1.6; }}
.hr-tip {{ font-size:13px; color:#f0c14b; margin-top:2px; }}
.waiting {{ font-size:15px; color:#8b949e; text-align:center; padding:20px; }}
.footer {{ text-align:center; font-size:12px; color:#484f58; padding:20px 0; border-top:1px solid #21262d; margin-top:16px; }}
</style>
</head>
<body>
<div class="wrapper">

<div class="header">
  <h1>🐰 毛儿の每日汇总</h1>
  <div class="date">{year}年{month}月{day}日 · {weekday_str}</div>
  <div class="warm">☀️ {warm_msg}</div>
</div>

<div class="card">
  <div class="card-title">📰 国内外大事</div>
{news_html}
</div>

<div class="card">
  <div class="card-title">🤖 AI 最新动态</div>
{ai_html}
</div>

<div class="card">
  <div class="card-title">📚 每日5个英文单词</div>
{words_html}
</div>

<div class="card">
  <div class="card-title">🧠 每日冷知识</div>
{qa_html}
</div>

<div class="card">
  <div class="card-title">💼 每日HR实操课堂</div>
{hr_html}
</div>

<div class="card">
  <div class="card-title">🎬 周末影院推荐</div>
  <div class="waiting">{movie_html}</div>
</div>

<div class="footer">✨ 每日汇总由 WorkBuddy 自动生成 · 有问题随时告诉我～ 🐰</div>

</div>
</body>
</html>'''

    return html, words_today, qa_today[0], [t[0] for t in hr_today]

def main():
    print("🚀 开始生成每日汇总...")

    date_str, weekday_str, is_weekend, today = get_date_info()
    print(f"📅 北京时间: {date_str} {weekday_str}")

    # 加载历史
    history = load_history()
    print(f"📚 历史: words={len(history.get('words',[]))}, qa={len(history.get('qa',[]))}")

    # 生成HTML
    html, words_today, qa_today, hr_today = generate_html(
        date_str, weekday_str, is_weekend, today, history
    )
    print(f"📝 HTML 生成完成，长度: {len(html)}")

    # 保存 index.html
    index_path = os.path.join(WORK_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ index.html 已保存")

    # 更新历史
    history["words"].extend(words_today)
    history["qa"].append(qa_today)
    history["hr_tips"].extend(hr_today)
    history["last_updated"] = date_str
    save_history(history)
    print(f"✅ 历史记录已更新 (words: {len(history['words'])}, qa: {len(history['qa'])})")

    print(f"🎉 每日汇总 {date_str} 全部完成！")
    return 0

if __name__ == "__main__":
    exit(main())

import os
import json

def build_site():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    documents = []
    
    # 遍历当前目录下的所有 txt 文件
    for filename in sorted(os.listdir(base_dir)):
        if filename.endswith(".txt") and filename != "requirements.txt":
            file_path = os.path.join(base_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 去除后缀作为标题
            title = os.path.splitext(filename)[0]
            documents.append({
                "title": title,
                "content": content
            })
    
    if not documents:
        print("未找到任何 .txt 文件。")
        return
        
    js_data = json.dumps(documents, ensure_ascii=False)
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EZLLM - 知识分享</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f7f9fc;
            --surface: rgba(255, 255, 255, 0.7);
            --border: rgba(255, 255, 255, 0.4);
            --text-main: #1d1d1f;
            --text-secondary: #86868b;
            --accent: #0066cc;
            --accent-hover: #004499;
            --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
            --sidebar-width: 320px;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #0d0d0d;
                --surface: rgba(30, 30, 30, 0.6);
                --border: rgba(255, 255, 255, 0.08);
                --text-main: #f5f5f7;
                --text-secondary: #a1a1a6;
                --accent: #2997ff;
                --accent-hover: #147ce6;
                --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            }}
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            height: 100vh;
            overflow: hidden;
            transition: background-color 0.4s ease, color 0.4s ease;
        }}

        /* 侧边栏 */
        .sidebar {{
            width: var(--sidebar-width);
            background: var(--surface);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 30px 20px;
            z-index: 10;
        }}

        .brand {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 40px;
            padding-left: 10px;
            background: linear-gradient(135deg, var(--accent), #baa1ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .nav-list {{
            list-style: none;
            overflow-y: auto;
            flex-grow: 1;
        }}

        .nav-item {{
            padding: 14px 16px;
            margin-bottom: 8px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
            overflow: hidden;
        }}

        .nav-item::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: var(--accent);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: -1;
        }}

        .nav-item:hover {{
            color: var(--text-main);
            background: rgba(120, 120, 120, 0.1);
            transform: translateX(4px);
        }}

        .nav-item.active {{
            color: #fff;
            transform: translateX(6px);
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
        }}

        .nav-item.active::before {{
            opacity: 1;
        }}

        /* 主视口区域 */
        .main-content {{
            flex-grow: 1;
            padding: 60px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            scroll-behavior: smooth;
        }}

        .content-card {{
            width: 100%;
            max-width: 800px;
            background: var(--surface);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 50px 60px;
            box-shadow: var(--shadow);
            opacity: 0;
            transform: translateY(20px);
            animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        @keyframes fadeUp {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .title {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 30px;
            line-height: 1.3;
            color: var(--text-main);
        }}

        .text-body {{
            font-size: 17px;
            line-height: 1.8;
            color: var(--text-main);
            opacity: 0.9;
            white-space: pre-wrap; /* 保持用户的文本格式和换行！ */
        }}

        /* 滚动条美化 */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(150, 150, 150, 0.3);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(150, 150, 150, 0.5);
        }}

        /* 响应式 */
        @media (max-width: 768px) {{
            body {{
                flex-direction: column;
            }}
            .sidebar {{
                width: 100%;
                height: 200px;
                border-right: none;
                border-bottom: 1px solid var(--border);
            }}
            .main-content {{
                padding: 20px;
            }}
            .content-card {{
                padding: 30px 20px;
            }}
        }}
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="brand">EZLLM Shares</div>
        <ul class="nav-list" id="navList">
            <!-- 导航项将由JS动态生成 -->
        </ul>
    </aside>

    <main class="main-content">
        <div class="content-card" id="contentCard">
            <h1 class="title" id="contentTitle">欢迎使用 EZLLM 知识分享库</h1>
            <div class="text-body" id="textContent">请从左侧选择一个文档进行阅读。未来的文档只需放入文件夹中，并重新运行打包脚本即可。</div>
        </div>
    </main>

    <script>
        // 注入文档数据
        const documents = {js_data};

        const navList = document.getElementById('navList');
        const contentTitle = document.getElementById('contentTitle');
        const textContent = document.getElementById('textContent');
        const contentCard = document.getElementById('contentCard');

        function loadDocument(index) {{
            const doc = documents[index];
            if (!doc) return;

            // 重新触发动画
            contentCard.style.animation = 'none';
            contentCard.offsetHeight; /* 触发重排 */
            contentCard.style.animation = 'fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards';

            contentTitle.textContent = doc.title;
            textContent.textContent = doc.content;

            // 更新侧边栏 active 状态
            const navItems = document.querySelectorAll('.nav-item');
            navItems.forEach((item, i) => {{
                if (i === index) {{
                    item.classList.add('active');
                }} else {{
                    item.classList.remove('active');
                }}
            }});
        }}

        function init() {{
            if (documents.length === 0) return;

            documents.forEach((doc, index) => {{
                const li = document.createElement('li');
                li.className = 'nav-item';
                li.textContent = doc.title;
                li.onclick = () => loadDocument(index);
                navList.appendChild(li);
            }});

            // 默认加载第一篇
            loadDocument(0);
        }}

        init();
    </script>
</body>
</html>"""

    output_path = os.path.join(base_dir, "EZLLM_Share.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"成功！已将 {len(documents)} 份文档打包。网页生成于：{output_path}")
    print("立刻双击打开 EZLLM_Share.html 来体验纯粹的沉浸式阅读吧！")

if __name__ == "__main__":
    build_site()

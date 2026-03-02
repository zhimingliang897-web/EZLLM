import os
import json

def build_site():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(base_dir, "docs")
    
    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist. Creating it.")
        os.makedirs(docs_dir)

    documents = []
    
    # 遍历 docs 目录下的所有 txt 文件
    for filename in sorted(os.listdir(docs_dir)):
        if filename.endswith(".txt") and filename != "requirements.txt":
            file_path = os.path.join(docs_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 去除后缀作为标题
            title = os.path.splitext(filename)[0]
            documents.append({
                "title": title,
                "content": content
            })
    
    if not documents:
        print("未在 docs/ 目录下找到任何 .txt 文件。")
        
    js_data = json.dumps(documents, ensure_ascii=False)
    
    html_template = """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EZLLM - 知识分享</title>
    <!-- 引入谷歌优质字体 -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap"
      rel="stylesheet"
    />
    <!-- 引入图标库 -->
    <link
      href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css"
      rel="stylesheet"
    />
    <style>
      :root {
        --bg-color: #f0f2f5;
        --surface-color: rgba(255, 255, 255, 0.75);
        --border-color: rgba(255, 255, 255, 0.5);
        --text-main: #1d1d1f;
        --text-secondary: #86868b;
        --accent: #4a6ee0;
        --accent-hover: #3b5cbd;
        --sidebar-width: 320px;
        --shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
        --glass-blur: blur(24px);
        --grad-bg: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
      }

      @media (prefers-color-scheme: dark) {
        :root {
          --bg-color: #000000;
          --surface-color: rgba(28, 28, 30, 0.65);
          --border-color: rgba(255, 255, 255, 0.08);
          --text-main: #f5f5f7;
          --text-secondary: #a1a1a6;
          --accent: #5e81f4;
          --accent-hover: #7b98f6;
          --shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
          --grad-bg: linear-gradient(120deg, #1f1c2c 0%, #928dab 100%);
        }
      }

      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }

      body {
        font-family:
          "Inter",
          "Noto Sans SC",
          -apple-system,
          BlinkMacSystemFont,
          "Segoe UI",
          Roboto,
          Helvetica,
          Arial,
          sans-serif;
        background: var(--bg-color);
        color: var(--text-main);
        display: flex;
        height: 100vh;
        overflow: hidden;
        transition: all 0.4s ease;
      }

      /* 动态渐变背景 */
      .bg-mesh {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--grad-bg);
        z-index: -1;
        opacity: 0.15;
        animation: moveGradient 15s ease infinite alternate;
        background-size: 200% 200%;
      }

      @keyframes moveGradient {
        0% {
          background-position: 0% 50%;
        }
        100% {
          background-position: 100% 50%;
        }
      }

      /* 侧边栏设计 */
      .sidebar {
        width: var(--sidebar-width);
        background: var(--surface-color);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border-right: 1px solid var(--border-color);
        display: flex;
        flex-direction: column;
        z-index: 10;
      }

      .brand {
        padding: 40px 30px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
      }

      .brand i {
        font-size: 28px;
        color: var(--accent);
      }

      .brand span {
        font-size: 22px;
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, var(--accent), #9b51e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }

      /* 搜索框设计 */
      .search-box {
        padding: 0 20px 15px;
      }

      .search-input {
        width: 100%;
        padding: 10px 16px 10px 40px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        background: rgba(255, 255, 255, 0.4);
        color: var(--text-main);
        font-family: inherit;
        font-size: 14px;
        outline: none;
        transition: all 0.3s ease;
      }

      @media (prefers-color-scheme: dark) {
        .search-input {
          background: rgba(0, 0, 0, 0.2);
        }
      }

      .search-input:focus {
        border-color: var(--accent);
        background: var(--surface-color);
        box-shadow: 0 0 0 3px rgba(74, 110, 224, 0.2);
      }

      .search-wrapper {
        position: relative;
      }

      .search-icon {
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        color: var(--text-secondary);
        font-size: 16px;
      }

      .nav-header {
        padding: 0 30px 10px;
        font-size: 13px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        color: var(--text-secondary);
      }

      .nav-list {
        list-style: none;
        overflow-y: auto;
        flex-grow: 1;
        padding: 0 20px 30px;
      }

      .nav-item {
        padding: 14px 18px;
        margin-bottom: 6px;
        border-radius: 12px;
        cursor: pointer;
        font-size: 15px;
        font-weight: 500;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        z-index: 1;
      }

      .nav-item i {
        font-size: 18px;
        color: var(--text-secondary);
        transition: all 0.3s ease;
      }

      .nav-item::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 12px;
        background: var(--accent);
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: -1;
      }

      .nav-item:hover {
        color: var(--text-main);
        background: rgba(120, 120, 120, 0.08);
        transform: translateX(4px);
      }

      .nav-item:hover i {
        color: var(--accent);
      }

      .nav-item.active {
        color: #fff;
        transform: translateX(6px);
        box-shadow: 0 8px 24px rgba(74, 110, 224, 0.3);
      }

      .nav-item.active i {
        color: #fff;
      }

      .nav-item.active::before {
        opacity: 1;
      }

      /* 主阅读区设计 */
      .main-content {
        flex-grow: 1;
        padding: 60px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        scroll-behavior: smooth;
        position: relative;
      }

      .content-card {
        width: 100%;
        max-width: 840px;
        background: var(--surface-color);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        border: 1px solid var(--border-color);
        border-radius: 28px;
        padding: 60px 70px;
        box-shadow: var(--shadow);
        opacity: 0;
        transform: translateY(30px);
        animation: fadeUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }

      @keyframes fadeUp {
        from {
          opacity: 0;
          transform: translateY(30px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .doc-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--accent);
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
      }

      .doc-meta span {
        background: rgba(74, 110, 224, 0.1);
        padding: 4px 12px;
        border-radius: 20px;
      }

      .title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 40px;
        line-height: 1.35;
        color: var(--text-main);
        letter-spacing: -0.5px;
      }

      .text-body {
        font-size: 17px;
        line-height: 2;
        color: var(--text-main);
        opacity: 0.88;
        white-space: pre-wrap; /* 保持纯文本的换行 */
        letter-spacing: 0.3px;
        text-align: justify;
      }

      /* 滚动条美化 */
      ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
      }
      ::-webkit-scrollbar-track {
        background: transparent;
      }
      ::-webkit-scrollbar-thumb {
        background: rgba(150, 150, 150, 0.2);
        border-radius: 10px;
      }
      ::-webkit-scrollbar-thumb:hover {
        background: rgba(150, 150, 150, 0.4);
      }

      /* 响应式 */
      @media (max-width: 850px) {
        body {
          flex-direction: column;
        }
        .sidebar {
          width: 100%;
          height: auto;
          max-height: 250px;
          border-right: none;
          border-bottom: 1px solid var(--border-color);
        }
        .main-content {
          padding: 30px 20px;
        }
        .content-card {
          padding: 40px 30px;
          border-radius: 20px;
        }
        .title {
          font-size: 28px;
        }
        .text-body {
          font-size: 16px;
        }
      }
    </style>
  </head>
  <body>
    <div class="bg-mesh"></div>

    <aside class="sidebar">
      <div class="brand">
        <i class="ri-lightbulb-flash-line"></i>
        <span>EZLLM 分享</span>
      </div>
      <div class="search-box">
        <div class="search-wrapper">
          <i class="ri-search-line search-icon"></i>
          <input type="text" id="searchInput" class="search-input" placeholder="搜索文档或内容...">
        </div>
      </div>
      <div class="nav-header">知识文档</div>
      <ul class="nav-list" id="navList">
        <!-- 导航项将由JS动态生成 -->
      </ul>
    </aside>

    <main class="main-content" id="mainScroll">
      <div class="content-card" id="contentCard">
        <div class="doc-meta"><span id="docTag">文档</span></div>
        <h1 class="title" id="contentTitle">欢迎使用 EZLLM</h1>
        <div class="text-body" id="textContent">
          请从左侧选择一个文档进行沉浸式阅读。
        </div>
      </div>
    </main>

    <script>
      // 动态注入的文档数据
      const documents = __DATA_PLACEHOLDER__;

      const navList = document.getElementById("navList");
      const contentTitle = document.getElementById("contentTitle");
      const textContent = document.getElementById("textContent");
      const contentCard = document.getElementById("contentCard");
      const mainScroll = document.getElementById("mainScroll");
      const searchInput = document.getElementById("searchInput");

      function loadDocument(index) {
        const doc = documents[index];
        if (!doc) return;

        // 平滑重置动画
        contentCard.style.animation = "none";
        contentCard.offsetHeight; // 触发回流重绘
        contentCard.style.animation =
          "fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards";

        contentTitle.textContent = doc.title;
        textContent.textContent = doc.content;

        mainScroll.scrollTo({ top: 0, behavior: "smooth" });

        // 更新导航高亮状态
        const navItems = document.querySelectorAll(".nav-item");
        navItems.forEach((item) => {
          if (parseInt(item.dataset.index) === index) {
            item.classList.add("active");
          } else {
            item.classList.remove("active");
          }
        });
      }

      function init() {
        if (documents.length === 0) {
            contentTitle.textContent = "未找到文档";
            textContent.textContent = "请将文本文档添加到 docs 目录下。";
            return;
        }

        documents.forEach((doc, index) => {
          const li = document.createElement("li");
          li.className = "nav-item";
          li.dataset.index = index;

          // 添加图标
          const icon = document.createElement("i");
          icon.className = "ri-article-line";
          li.appendChild(icon);

          // 添加文本
          const span = document.createElement("span");
          span.textContent = doc.title;
          li.appendChild(span);

          li.onclick = () => loadDocument(index);
          navList.appendChild(li);
        });

        // 搜索功能实现
        searchInput.addEventListener('input', (e) => {
            const keyword = e.target.value.toLowerCase();
            const items = document.querySelectorAll('.nav-item');
            
            items.forEach((item) => {
                const idx = item.dataset.index;
                const doc = documents[idx];
                // 搜索标题或正文
                const matchTitle = doc.title.toLowerCase().includes(keyword);
                const matchContent = doc.content.toLowerCase().includes(keyword);
                
                if (matchTitle || matchContent) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });

        // 初始加载第一篇文章
        setTimeout(() => {
          loadDocument(0);
        }, 100);
      }

      // 初始化运行
      init();
    </script>
  </body>
</html>
"""
    
    # 替换数据占位符
    html_content = html_template.replace("__DATA_PLACEHOLDER__", js_data)
    
    # 修改输出文件名为 index.html，替换原有实现
    output_path = os.path.join(base_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"成功！已将 {len(documents)} 份文档从 docs/ 文件夹打包。网页生成于：{output_path}")
    print("立刻双击打开 index.html 来体验带搜索的沉浸式阅读吧！")

if __name__ == "__main__":
    build_site()

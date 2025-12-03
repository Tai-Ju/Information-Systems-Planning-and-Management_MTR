"""
互動式 Process Mining 網頁展示工具
使用 Plotly 建立可互動的圖表
(版本 6：互動式分頁 - 修正空白圖表)
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
import sys
import io
import os

# --- (上方的編碼設定、class InteractiveProcessMining、load_data 不變) ---

# 設定Windows編碼
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        if sys.stderr.encoding != 'utf-8':
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

class InteractiveProcessMining:
    """互動式流程挖掘工具"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """載入並預處理資料"""
        print(f"從 {self.data_path} 載入資料中...")
        try:
            self.df = pd.read_excel(self.data_path)
        except FileNotFoundError:
            print(f"錯誤：找不到檔案！請確認 '{self.data_path}' 路徑是否正確。")
            sys.exit(1)
        except Exception as e:
            print(f"讀取 Excel 檔案時發生未預期的錯誤: {e}")
            sys.exit(1)
            
        self.df['紀錄時間'] = pd.to_datetime(self.df['紀錄時間'], format='mixed')
        self.df = self.df.sort_values('紀錄時間').reset_index(drop=True)
        self.df['日期'] = self.df['紀錄時間'].dt.date
        self.df['案例ID'] = self.df['病歷號'].astype(str) + '_' + self.df['日期'].astype(str)
        self.df['小時'] = self.df['紀錄時間'].dt.hour
        self.df['星期'] = self.df['紀錄時間'].dt.day_name()
        print(f"資料載入完成！共 {len(self.df)} 筆記錄")
    
    # --- (所有的 _build_... 函數都不變，這裡省略以節省篇幅) ---
    def _build_activity_pie_chart(self):
        """1. 建立動作類型分布 (圓餅圖)"""
        print("建構 1. 動作類型分布圖...")
        activity_counts = self.df['動作'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=activity_counts.index,
            values=activity_counts.values,
            hole=0.3,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>數量: %{value}<br>佔比: %{percent}<extra></extra>'
        )])
        fig.update_layout(title_text="<b>動作類型分布</b>", title_font_size=20, height=500, legend_title_text="動作類型")
        return fig

    def _build_ward_bar_chart(self):
        """2. 建立病房活動量排名 (長條圖)"""
        print("建構 2. 病房活動量排名圖...")
        ward_counts = self.df['病房'].value_counts().sort_values(ascending=True)
        fig = go.Figure(data=[go.Bar(
            x=ward_counts.values,
            y=ward_counts.index,
            orientation='h',
            marker=dict(color=ward_counts.values, colorscale='Viridis'),
            text=ward_counts.values,
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>活動數: %{x}<extra></extra>'
        )])
        fig.update_layout(title_text="<b>病房活動量排名</b>", title_font_size=20, height=500, xaxis_title="活動數量", yaxis_title="病房")
        return fig
    
    def _build_duration_violin_plot(self):
        """3. 建立處理時間分布 (小提琴圖)"""
        print("建構 3. 處理時間分布圖...")
        case_times = []
        for case_id in self.df['案例ID'].unique():
            case_data = self.df[self.df['案例ID'] == case_id].sort_values('紀錄時間')
            if len(case_data) >= 2:
                duration = (case_data['紀錄時間'].iloc[-1] - case_data['紀錄時間'].iloc[0]).total_seconds() / 60
                if 0 < duration < 1000:
                    case_times.append({'病房': case_data['病房'].iloc[0], '處理時間(分鐘)': duration})
        
        case_df = pd.DataFrame(case_times)
        fig = go.Figure()
        if not case_df.empty:
            for ward in case_df['病房'].unique():
                ward_data = case_df[case_df['病房'] == ward]
                fig.add_trace(go.Violin(y=ward_data['處理時間(分鐘)'], name=str(ward), box_visible=True, meanline_visible=True, hovertemplate='<b>%{fullData.name}</b><br>時間: %{y:.1f} 分鐘<extra></extra>'))
            fig.update_layout(title_text="<b>各病房案例處理時間分布</b>", title_font_size=20, height=600, yaxis_title="處理時間 (分鐘)", showlegend=True)
        else:
            fig.add_annotation(text="無資料產生處理時間分布圖", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
            fig.update_layout(title_text="<b>各病房案例處理時間分布</b>")
        return fig

    def _build_daily_trend_scatter(self):
        """4. 建立每日活動趨勢 (折線圖)"""
        print("建構 4. 每日活動趨勢圖...")
        daily_counts = self.df.groupby('日期').size().reset_index(name='count')
        fig = go.Figure(data=[go.Scatter(
            x=daily_counts['日期'], y=daily_counts['count'], mode='lines+markers', line=dict(color='royalblue', width=2),
            marker=dict(size=6), fill='tozeroy', fillcolor='rgba(65, 105, 225, 0.2)', hovertemplate='日期: %{x}<br>活動數: %{y}<extra></extra>'
        )])
        fig.update_layout(title_text="<b>每日活動趨勢</b>", title_font_size=20, height=500, xaxis_title="日期", yaxis_title="活動數量", hovermode='x unified')
        return fig

    def _build_process_flow_network(self):
        """5. 建立流程網路圖 (Sankey)"""
        print("建構 5. 流程轉換網路圖...")
        transitions = []
        for case_id in self.df['案例ID'].unique():
            case_data = self.df[self.df['案例ID'] == case_id].sort_values('紀錄時間')
            activities = case_data['動作'].tolist()
            for i in range(len(activities) - 1):
                transitions.append({'source': activities[i], 'target': activities[i+1]})
        
        trans_df = pd.DataFrame(transitions)
        fig = go.Figure()
        if trans_df.empty:
            fig.add_annotation(text="無資料可產生流程網路圖", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        else:
            trans_counts = trans_df.groupby(['source', 'target']).size().reset_index(name='value')
            trans_counts = trans_counts.sort_values('value', ascending=False).head(20)
            all_nodes = list(set(trans_counts['source'].unique()) | set(trans_counts['target'].unique()))
            node_dict = {node: idx for idx, node in enumerate(all_nodes)}
            node_colors = ['#%02x%02x%02x' % (np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255)) for _ in all_nodes]
            fig.add_trace(go.Sankey(
                node=dict(pad=20, thickness=30, line=dict(color="black", width=1), label=all_nodes, color=node_colors),
                link=dict(source=[node_dict[s] for s in trans_counts['source']], target=[node_dict[t] for t in trans_counts['target']],
                          value=trans_counts['value'], label=trans_counts['value'], color='rgba(0,0,96,0.2)',
                          hovertemplate='從 %{source.label} 到 %{target.label}: %{value} 次<extra></extra>')
            ))
        fig.update_layout(title="<b>ADC系統流程轉換網路圖 (Top 20)</b>", title_font_size=20, font=dict(size=14), height=700)
        return fig
    
    def _build_performance_heatmap(self):
        """6. 建立效能熱力圖 (Heatmap)"""
        print("建構 6. 效能熱力圖...")
        self.df['星期幾'] = self.df['紀錄時間'].dt.dayofweek
        self.df['星期名稱'] = self.df['紀錄時間'].dt.day_name()
        hourly_weekly = self.df.groupby(['星期名稱', '星期幾', '小時']).size().reset_index(name='活動數')
        week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_order_zh = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        pivot_table = hourly_weekly.pivot_table(index='星期名稱', columns='小時', values='活動數', fill_value=0)
        for h in range(24):
            if h not in pivot_table.columns: pivot_table[h] = 0
        pivot_table = pivot_table.reindex(week_order)
        pivot_table = pivot_table.sort_index(axis=1)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values, x=[f'{h:02d}:00' for h in pivot_table.columns], y=[week_order_zh[week_order.index(d)] for d in pivot_table.index],
            colorscale='YlOrRd', hovertemplate='時段: %{x}<br>星期: %{y}<br>活動數: %{z}<extra></extra>', colorbar=dict(title='活動數')
        ))
        fig.update_layout(title='<b>系統使用熱力圖 (按星期與時段)</b>', title_font_size=20, xaxis_title='時段 (24小時制)',
                          yaxis_title='星期', font=dict(size=12), height=500, xaxis=dict(tickmode='linear', dtick=2))
        return fig
    
    def _build_activity_timeline(self):
        """7. 建立活動時間軸 (Gantt)"""
        print("建構 7. 活動時間軸...")
        unique_cases = self.df['案例ID'].unique()
        sample_cases = unique_cases[:20]
        timeline_data = []
        for idx, case_id in enumerate(sample_cases):
            case_data = self.df[self.df['案例ID'] == case_id].sort_values('紀錄時間')
            if len(case_data) > 0:
                for i in range(len(case_data)):
                    row = case_data.iloc[i]
                    start_time = row['紀錄時間']
                    end_time = case_data.iloc[i+1]['紀錄時間'] if i < len(case_data) - 1 else start_time + pd.Timedelta(minutes=1)
                    timeline_data.append({'Case': f'案例 {idx+1} ({case_id.split("_")[0][-4:]})', 'Activity': row['動作'],
                                         'Start': start_time, 'Finish': end_time, 'Ward': row['病房']})
        
        fig = go.Figure()
        if not timeline_data:
            fig.add_annotation(text="無資料可產生時間軸", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
        else:
            timeline_df = pd.DataFrame(timeline_data)
            fig = px.timeline(timeline_df, x_start='Start', x_end='Finish', y='Case', color='Activity', hover_data=['Ward', 'Start', 'Finish'])
            fig.update_yaxes(autorange="reversed")
        
        fig.update_layout(title='<b>前20個案例的活動時間軸 (抽樣)</b>', title_font_size=20, xaxis_title='時間',
                          yaxis_title='案例', height=700, showlegend=True)
        return fig
    
    def generate_interactive_tabbed_dashboard(self):
        """建立主HTML頁面 (互動式分頁)"""
        print("\n開始生成互動式分頁儀表板...")
        
        # 1. 獲取所有圖表物件
        fig_pie = self._build_activity_pie_chart()
        fig_bar = self._build_ward_bar_chart()
        fig_sankey = self._build_process_flow_network()
        fig_timeline = self._build_activity_timeline()
        fig_heatmap = self._build_performance_heatmap()
        fig_violin = self._build_duration_violin_plot()
        fig_trend = self._build_daily_trend_scatter()
        
        print("\n所有圖表物件已在記憶體中生成。")
        print("正在將圖表轉換為 HTML 程式碼片段...")

        # 2. 將圖表轉換為 HTML (div 區塊)
        #    include_plotlyjs=False 確保 JS 不會被重複加載
        #    config={'responsive': True} 嘗試讓圖表自適應
        config_responsive = {'responsive': True}
        
        pie_html = fig_pie.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        bar_html = fig_bar.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        sankey_html = fig_sankey.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        timeline_html = fig_timeline.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        heatmap_html = fig_heatmap.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        violin_html = fig_violin.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)
        trend_html = fig_trend.to_html(full_html=False, include_plotlyjs=False, config=config_responsive)

        print("HTML 程式碼片段轉換完畢。")

        # 3. 獲取統計數據
        total_records = len(self.df)
        num_wards = self.df['病房'].nunique()
        num_activities = self.df['動作'].nunique()
        num_cases = self.df['案例ID'].nunique()
        
        total_records_str = f"{total_records:,}"
        num_cases_str = f"{num_cases:,}"
        
        print("正在組合最終的 index.html...")

        # 4. 組合最終的 HTML 內容
        #    *** 唯一的變動在最下方的 <script> 區塊 ***
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADC系統流程挖掘儀表板</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Microsoft JhengHei', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            padding: 20px;
            color: #333;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: #ffffff;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #3a7bd5;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #555;
            font-size: 1.2em;
        }}
        
        /* 使用說明 (來自您的截圖) */
        .info-box {{
            background: #e9ecef;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
        }}
        .info-box h3 {{
            margin-top: 0;
            margin-bottom: 15px;
            color: #495057;
        }}
        .info-box ul {{
            padding-left: 20px;
            margin: 0;
            color: #6c757d;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%);
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            color: white;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }}
        .stat-value {{ font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }}
        .stat-label {{ font-size: 1.1em; }}
        
        /* --- 這是新樣式：分頁系統 --- */
        .tabs-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 2px solid #dee2e6;
        }}
        .tab-button {{
            padding: 12px 20px;
            font-size: 1em;
            font-weight: bold;
            color: white;
            /* 模仿您截圖中的 藍色 */
            background-color: #3f51b5; 
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .tab-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.15);
            background-color: #303f9f;
        }}
        /* 模仿您截圖中的 橘色/鮭魚色 "Active" 狀態 */
        .tab-button.active {{
            background: linear-gradient(135deg, #ff9a8b 0%, #ff6a88 100%); 
            /* 您的截圖顏色比較像: background-color: #ff7f50; */
            background-color: #ff7f50; /* 使用 #ff7f50 (Coral) */
            box-shadow: 0 6px 20px rgba(255, 127, 80, 0.4);
            transform: translateY(-2px);
        }}
        
        /* 圖表內容區 */
        .chart-content {{
            display: none; /* 預設隱藏所有圖表 */
            animation: fadeIn 0.5s;
        }}
        .chart-content.active {{
            display: block; /* 只顯示 Active 的圖表 */
        }}
        
        /* 動畫效果 */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .chart-container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden; /* 確保 Plotly 圖表自適應寬度 */
        }}
        
        footer {{
            text-align: center;
            color: #555;
            margin-top: 50px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ADC系統流程挖掘儀表板</h1>
            <p class="subtitle">互動式資料探索分析 - 完整版</p>
        </header>
        
        <div class="info-box">
            <h3>💡 使用說明</h3>
            <ul>
                <li>點擊下方按鈕切換不同的互動式圖表。</li>
                <li><b>懸停與詳細資訊:</b> 滑鼠移到圖表上查看數據。</li>
                <li><b>縮放與平移:</b> 可以放大、縮小、拖曳圖表。</li>
                <li><b>篩選與隱藏:</b> 點擊圖例可以隱藏/顯示資料。</li>
                <li><b>匯出圖片:</b> 點擊圖表右上角的相機圖示可以下載圖表。</li>
            </ul>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><div class="stat-value">{total_records_str}</div><div class="stat-label">總記錄數</div></div>
            <div class="stat-card"><div class="stat-value">{num_wards}</div><div class="stat-label">病房數</div></div>
            <div class="stat-card"><div class="stat-value">{num_activities}</div><div class="stat-label">動作類型</div></div>
            <div class="stat-card"><div class="stat-value">{num_cases_str}</div><div class="stat-label">案例數</div></div>
        </div>
        
        <div class="tabs-container">
            <button class="tab-button" data-target="chart-pie">動作類型分布</button>
            <button class="tab-button" data-target="chart-bar">病房活動量排名</button>
            <button class="tab-button" data-target="chart-heatmap">系統使用熱力圖</button>
            <button class="tab-button" data-target="chart-trend">每日活動趨勢</button>
            <button class="tab-button" data-target="chart-sankey">流程轉換網路</button>
            <button class="tab-button" data-target="chart-violin">案例處理時間</button>
            <button class="tab-button" data-target="chart-timeline">活動時間軸</button>
        </div>

        <div class="charts-wrapper">
            <div id="chart-pie" class="chart-content">
                <div class="chart-container">{pie_html}</div>
            </div>
            
            <div id="chart-bar" class="chart-content">
                <div class="chart-container">{bar_html}</div>
            </div>
            
            <div id="chart-heatmap" class="chart-content">
                <div class="chart-container">{heatmap_html}</div>
            </div>
            
            <div id="chart-trend" class="chart-content">
                <div class="chart-container">{trend_html}</div>
            </div>
            
            <div id="chart-sankey" class="chart-content">
                <div class="chart-container">{sankey_html}</div>
            </div>
            
            <div id="chart-violin" class="chart-content">
                <div class="chart-container">{violin_html}</div>
            </div>
            
            <div id="chart-timeline" class="chart-content">
                <div class="chart-container">{timeline_html}</div>
            </div>
        </div>
        
        <footer>
            <p>使用 Python (pandas, plotly) 建立的流程挖掘展示工具</p>
            <p>&copy; 2025 Process Mining Demo</p>
        </footer>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const buttons = document.querySelectorAll('.tab-button');
            const charts = document.querySelectorAll('.chart-content');

            // 預設顯示第一個
            if (buttons.length > 0) {{
                buttons[0].classList.add('active');
            }}
            if (charts.length > 0) {{
                charts[0].classList.add('active');
            }}

            buttons.forEach(function(button) {{
                button.addEventListener('click', function() {{
                    const targetId = this.getAttribute('data-target');

                    // 1. 移除所有按鈕的 active
                    buttons.forEach(btn => btn.classList.remove('active'));
                    // 2. 隱藏所有圖表
                    charts.forEach(chart => chart.classList.remove('active'));

                    // 3. 啟用被點擊的按鈕
                    this.classList.add('active');
                    
                    // 4. 顯示對應的圖表
                    const targetChartDiv = document.getElementById(targetId);
                    
                    if (targetChartDiv) {{
                        targetChartDiv.classList.add('active');
                        
                        // *** 修正空白圖表的關鍵 ***
                        // 延遲 10 毫秒，確保 div 的 'display: block' 屬性
                        // 已經被瀏覽器渲染，使其獲得實際的寬高。
                        setTimeout(function() {{
                            // 找到這個 div 內的 plotly 圖表元素 (class .plotly-graph-div 是 plotly 自動生成的)
                            const plotlyElement = targetChartDiv.querySelector('.plotly-graph-div');
                            
                            if (plotlyElement) {{
                                // 呼叫 Plotly 的官方 resize 函數，
                                // 讓圖表根據其容器的新尺寸重新繪製
                                try {{
                                    Plotly.Plots.resize(plotlyElement);
                                }} catch(e) {{
                                    console.error("Plotly resize failed: ", e);
                                }}
                            }}
                        }}, 10); // 10毫秒的延遲
                    }}
                }});
            }});
        }});
    </script>
    </body>
</html>
"""
        
        # 5. 寫入單一的 index.html 檔案
        try:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("\n============================================================")
            print("成功！ 互動式分頁儀表板已生成: index.html")
            print("(v6: 已修正空白圖表問題)")
            print("============================================================")
        except Exception as e:
            print(f"寫入 index.html 時發生錯誤: {e}")


def main():
    """主程式"""
    print("="*60)
    print("建立互動式流程挖掘儀表板 (v6 - 修正空白圖表)")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'ADC系統_總表V2.xlsx')
    
    tool = InteractiveProcessMining(data_path)
    
    # --- 僅呼叫這一個主函數 ---
    tool.generate_interactive_tabbed_dashboard()
    
    print("\n所有任務完成！")
    print("請在您的瀏覽器中開啟 index.html 檔案。")


if __name__ == "__main__":
    main()
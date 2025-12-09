# 🏥 ADC系統流程挖掘分析專案
## Interactive Process Mining Dashboard for ADC Healthcare System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Visualization-green.svg)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-yellow.svg)](https://pandas.pydata.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

### 📋 專案概述

本專案針對ADC（Automated Dispensing Cabinet）藥物管理系統進行深度流程挖掘分析，透過視覺化儀表板呈現系統使用模式、流程效率及改進機會。專案結合了資料科學、流程挖掘技術和互動式視覺化，為醫療機構提供系統優化的數據支持。

### 🎯 專案目標

- ✅ **流程可視化**：將ADC系統操作流程以直觀的方式呈現
- ✅ **效能分析**：識別系統使用的瓶頸和高峰時段
- ✅ **互動式探索**：提供多維度的資料探索工具
- ✅ **決策支援**：為醫院管理層提供數據驅動的改進建議
- ✅ **實時監控**：建立可持續更新的監控儀表板

### 🏥 ADC系統背景

**Automated Dispensing Cabinet (ADC)** 是現代醫院藥物管理的核心系統：
- **功能**：自動化藥物配發、庫存管理、用藥記錄
- **價值**：提升用藥安全、減少人為錯誤、優化工作流程
- **挑戰**：需要持續監控使用模式以優化效率

### 📊 資料集資訊

- **資料來源**：ADC系統操作日誌
- **記錄欄位**：
  - 病歷號、紀錄時間、動作類型
  - 病房位置、操作人員、藥物資訊
- **分析維度**：時間、地點、活動、案例流程
- **資料期間**：[根據實際資料調整]

### 📁 專案檔案結構

```
ADC_Process_Mining_Project/
│
├── README.md                              # 專案說明文件
├── 142216015_劉玳如.pptx                  # 專案成果簡報
├── Interactive_demo.py                    # 主要分析程式
├── index.html                             # 互動式儀表板
│
├── Analysis_Notebooks/                    # 分析筆記本
│   ├── hw.ipynb                          # 主要分析筆記本
│   ├── tree.ipynb                        # 決策樹分析
│   ├── 上採樣___類別權重___閾值調整.ipynb   # 不平衡資料處理
│   ├── 不處理_直接建模.ipynb               # 基準線分析
│   ├── 建立不平衡資料集.ipynb              # 資料準備
│   ├── 找閥值.ipynb                       # 閾值優化
│   └── 集成所有步驟比較.ipynb              # 綜合比較分析
│
├── Data/                                 # 資料檔案
│   ├── disease_imbalenced_data.csv       # 不平衡資料集
│   └── kidney_disease.csv                # 腎病資料集
│
└── Visualizations/                       # 視覺化圖表
    ├── confusion_matrices.png
    ├── correlation_matrix.png
    ├── decision_tree_structure.png
    ├── feature_importance.png
    ├── model_comparison.png
    ├── precision_recall_curve.png
    ├── roc_curve.png
    ├── target_variable_distribution.png
    ├── top10_correlation_features.png
    └── top_correlations.png
```

### 🛠️ 技術架構

#### **核心技術棧**
```python
# 資料處理與分析
pandas >= 1.3.0
numpy >= 1.21.0

# 互動式視覺化
plotly >= 5.0.0
plotly.graph_objects
plotly.subplots

# 機器學習 (用於預測分析)
scikit-learn >= 1.0.0

# Jupyter環境
jupyter >= 1.0.0
ipython >= 7.0.0
```

#### **視覺化組件**
- **Plotly.js**：互動式圖表引擎
- **HTML/CSS/JavaScript**：前端界面
- **響應式設計**：支援多裝置瀏覽

### 🚀 快速開始

#### 1. 環境設置
```bash
# 複製專案
git clone [your-repository-url]
cd ADC_Process_Mining_Project

# 安裝依賴
pip install pandas numpy plotly scikit-learn jupyter
```

#### 2. 執行分析
```bash
# 運行主要分析程式
python Interactive_demo.py

# 或啟動Jupyter進行探索性分析
jupyter notebook hw.ipynb
```

#### 3. 查看儀表板
```bash
# 直接開啟瀏覽器查看
# 檔案：index.html
```

### 📈 核心功能特色

#### 🎯 **七大互動式視覺化模組**

1. **📊 動作類型分布** (圓餅圖)
   - 展示不同ADC操作的使用頻率
   - 識別最常用的系統功能

2. **🏥 病房活動量排名** (橫向長條圖)
   - 比較各病房的系統使用強度
   - 發現使用量異常的區域

3. **🔥 系統使用熱力圖** (時段 × 星期)
   - 視覺化24小時×7天的使用模式
   - 識別高峰時段和低谷時間

4. **📈 每日活動趨勢** (時間序列)
   - 追蹤長期使用趨勢
   - 檢測異常活動模式

5. **🔄 流程轉換網路** (Sankey圖)
   - 展示操作流程的轉換路徑
   - 識別常見的操作序列

6. **⏱️ 案例處理時間** (小提琴圖)
   - 分析不同病房的處理效率
   - 發現流程優化機會

7. **📅 活動時間軸** (甘特圖)
   - 展示案例的完整時間線
   - 追蹤個別案例的處理過程

#### ✨ **進階功能**

**🖱️ 互動性**
- 滑鼠懸停顯示詳細資訊
- 點擊圖例篩選資料
- 縮放與平移操作
- 匯出高解析度圖片

**📱 響應式設計**
- 自適應不同螢幕尺寸
- 平板與手機友善界面
- 分頁式圖表切換

**⚡ 效能優化**
- 非同步圖表載入
- 記憶體優化的資料處理
- 快速圖表渲染

### 🔍 關鍵發現與洞察

#### 📊 **使用模式分析**
- **高峰時段**：[根據實際分析結果填入]
- **主要操作**：藥物配發佔XX%，查詢操作佔XX%
- **病房差異**：ICU使用頻率比一般病房高X倍

#### ⏰ **效率指標**
- **平均處理時間**：X分鐘
- **最快流程**：[具體操作類型]
- **瓶頸識別**：[發現的問題點]

#### 🎯 **改進建議**
1. **系統優化**：在高峰時段增加系統響應能力
2. **流程改進**：簡化複雜的操作流程
3. **培訓需求**：針對使用頻率低的功能加強教育訓練
4. **設備配置**：根據使用模式調整設備佈署

### 🏥 實際應用價值

#### 💡 **醫院管理應用**
- **資源配置**：基於使用模式優化人力配置
- **設備管理**：預測性維護和升級規劃
- **品質改善**：識別並消除流程瓶頸
- **成本控制**：優化藥物庫存和配送效率

#### 🔬 **學術研究價值**
- **流程挖掘**：醫療流程挖掘的實際案例
- **資料視覺化**：大型資料集的互動式呈現
- **系統分析**：醫療資訊系統使用行為研究

### 📝 使用範例

#### 基本分析
```python
# 載入流程挖掘工具
from Interactive_demo import InteractiveProcessMining

# 初始化分析器
analyzer = InteractiveProcessMining('ADC系統_總表V2.xlsx')

# 生成完整儀表板
analyzer.generate_interactive_tabbed_dashboard()
```

#### 客製化分析
```python
# 建立特定圖表
pie_chart = analyzer._build_activity_pie_chart()
heatmap = analyzer._build_performance_heatmap()

# 匯出為HTML
pie_chart.write_html("activity_distribution.html")
```

### 🎓 學術背景

**研究方向**：醫療資訊系統流程挖掘  
**應用領域**：智慧醫療、資料科學、流程優化  
**技術重點**：
- 大數據分析與視覺化
- 醫療流程挖掘技術
- 互動式儀表板開發
- 使用者行為分析

### 📊 技術實現詳情

#### 🔧 **資料預處理管道**
```python
def load_data(self):
    # 1. 資料載入與清理
    self.df = pd.read_excel(self.data_path)
    
    # 2. 時間欄位處理
    self.df['紀錄時間'] = pd.to_datetime(self.df['紀錄時間'])
    
    # 3. 案例ID生成
    self.df['案例ID'] = self.df['病歷號'].astype(str) + '_' + self.df['日期'].astype(str)
    
    # 4. 時間特徵工程
    self.df['小時'] = self.df['紀錄時間'].dt.hour
    self.df['星期'] = self.df['紀錄時間'].dt.day_name()
```

#### 📊 **視覺化最佳實踐**
- **色彩設計**：使用色盲友善的配色方案
- **圖表選擇**：根據資料類型選擇最適合的視覺化方式
- **互動設計**：提供多層次的資料探索體驗
- **效能優化**：大資料集的高效渲染技術

### ⚠️ 使用注意事項

#### 🔒 **資料隱私**
- 所有病患資料已去識別化處理
- 遵循醫療資料保護相關法規
- 建議在安全環境中運行分析

#### 💻 **系統需求**
- **記憶體**：建議8GB以上
- **瀏覽器**：Chrome/Firefox最新版本
- **網路**：需連接網路載入Plotly.js

#### 📈 **效能建議**
- 大資料集建議使用取樣分析
- 定期清理暫存檔案
- 使用SSD提升讀寫效能

### 🔄 未來發展規劃

#### 🚀 **功能擴展**
- [ ] **即時監控**：整合即時資料流
- [ ] **預測分析**：機器學習預測模型
- [ ] **行動應用**：開發手機APP版本
- [ ] **API介面**：提供資料API服務

#### 🎯 **技術升級**
- [ ] **雲端部署**：AWS/Azure雲端版本
- [ ] **微服務架構**：模組化系統設計
- [ ] **自動化報告**：定期生成分析報告
- [ ] **多語言支援**：國際化界面

### 🤝 貢獻指南

歡迎參與專案改進：

1. **Fork專案**
2. **創建功能分支** (`git checkout -b feature/新功能`)
3. **提交更改** (`git commit -am '新增功能'`)
4. **推送分支** (`git push origin feature/新功能`)
5. **發起Pull Request**


### 🙏 致謝

- **指導教授**：感謝專業指導與建議
- **醫院合作夥伴**：提供珍貴的實際資料
- **開源社群**：Plotly、Pandas等優秀工具
- **同學夥伴**：協助測試與回饋改進

### 📚 相關資源

#### 📖 **流程挖掘參考資料**
- Process Mining: Data Science in Action (Wil van der Aalst)
- Healthcare Process Mining學術論文集
- Python流程挖掘工具包文檔

#### 🔗 **相關連結**
- [Plotly官方文檔](https://plotly.com/python/)
- [醫療流程挖掘最佳實踐](https://example.com)
- [ADC系統技術規格](https://example.com)


---

*最後更新：2024年12月*  
*專案版本：v1.0*

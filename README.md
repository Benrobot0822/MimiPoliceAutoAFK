# DC2 - Discord 定時自動發送任務

這個專案是一個以 Selenium 實作的 Discord 自動化腳本，設計給 Windows 工作排程器觸發。
每次執行流程為：登入 Discord -> 進入指定頻道 -> 發送訊息 -> 關閉瀏覽器。

## 功能重點

- 讀取本地設定檔 config.json
- 使用 Chrome 無頭模式執行（不顯示瀏覽器視窗）
- 自動登入 Discord 並進入指定頻道
- 發送固定訊息（預設為 /hourly）
- 啟動後先隨機延遲 10 到 15 分鐘，降低固定時間點觸發
- 執行完畢後回傳成功或失敗的退出碼，便於排程器判斷

## 專案結構

- discord_scheduled_task.py: 主程式，單次執行
- config.json: 帳號與任務設定
- selenium_requirements.txt: Python 套件需求

## 環境需求

- Windows（建議）
- Python 3.9+
- Google Chrome（已安裝）
- 與 Chrome 相容版本的 ChromeDriver

說明：
新版 Selenium 在部分環境可自動處理驅動程式，但若你的環境無法自動抓取，請手動安裝並確認 ChromeDriver 可被系統找到。

## 安裝步驟

1. 建議先建立虛擬環境

   Windows PowerShell：

   python -m venv .venv
   .venv\Scripts\Activate.ps1

2. 安裝依賴

   pip install -r selenium_requirements.txt

## 設定檔說明

請編輯 config.json：

- discord_email: Discord 登入信箱
- discord_password: Discord 登入密碼
- channel_url: 目標頻道網址（必填）
- message_to_send: 要送出的訊息
- send_interval_minutes: 目前主程式未使用此欄位，排程週期由 Windows 工作排程器控制

重要：
請勿把真實帳密提交到 Git。建議在正式使用前，改為環境變數或其他密鑰管理方式。

## 手動執行

在專案目錄執行：

python discord_scheduled_task.py

程式行為：

- 先隨機等待 10 到 15 分鐘
- 嘗試登入並送出訊息
- 成功時返回退出碼 0
- 失敗時返回退出碼 1

## Windows 工作排程器建議設定

可建立每小時觸發一次的工作：

- 觸發程序：每 1 小時
- 動作程式：python
- 引數：discord_scheduled_task.py
- 起始位置：本專案資料夾

建議勾選：

- 使用最高權限執行（如有需要）
- 若錯過排程則盡快執行
- 失敗後重試（例如每 5 分鐘重試，最多 3 次）

## 常見問題

1. 找不到 config.json

請確認你是在專案根目錄執行，且檔名為 config.json。

2. 無法定位輸入框或登入失敗

Discord 介面可能變動，選擇器需更新。
也可能遇到驗證或風險控管流程，需先人工完成一次登入。

3. Chrome 啟動失敗

請確認本機 Chrome 與 ChromeDriver 版本相容，且驅動程式可被找到。

## 風險與注意事項

- 自動化登入與發訊有被平台限制的風險，請自行評估使用情境。
- 請遵守 Discord 使用條款與相關規範。
- 建議先在測試伺服器或測試頻道驗證流程後再上線。

## 後續可改進方向

- 將帳密改為環境變數讀取
- 使用 logging 模組輸出檔案日誌
- 加入截圖與錯誤通知機制
- 將 send_interval_minutes 直接整合進程式邏輯

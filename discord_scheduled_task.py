"""
Discord 定時任務版本（單次執行）

功能：登入 → 發送訊息 → 關閉
配合 Windows 工作排程器使用，每小時執行一次
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import sys
import json
import os
import random

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ===== 讀取設定檔 =====
def load_config():
    """從 config.json 讀取設定"""
    config_file = "config.json"
    
    if not os.path.exists(config_file):
        print(f"❌ 找不到 {config_file}")
        sys.exit(1)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ 讀取設定檔失敗: {e}")
        sys.exit(1)

# 讀取設定
config = load_config()
DISCORD_EMAIL = config.get("discord_email")
DISCORD_PASSWORD = config.get("discord_password")
CHANNEL_URL = config.get("channel_url")
MESSAGE_TO_SEND = config.get("message_to_send")
# ==================

def send_discord_message():
    """執行一次發送任務"""
    driver = None
    
    try:
        # Chrome 選項 - 無頭模式（不顯示窗口）
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        chrome_options.add_argument("--log-level=3")  # 減少日誌輸出
        chrome_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        
        print(f"[TIME] [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始執行")
        print("[INFO] 啟動 Chrome（無頭模式）...")
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)
        
        # 登入 Discord
        print("[INFO] 登入 Discord...")
        driver.get("https://discord.com/login")
        
        # 輸入郵箱
        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.send_keys(DISCORD_EMAIL)
        
        # 輸入密碼
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(DISCORD_PASSWORD)
        
        # 登入
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        print("[INFO] 等待登入完成...")
        time.sleep(6)
        
        # 關閉可能的彈窗
        try:
            close_buttons = driver.find_elements(
                By.XPATH,
                "//button[contains(text(), '確定')] | //button[contains(text(), 'OK')] | //button[contains(text(), '確認')]",
            )

            for btn in close_buttons:
                if btn.is_displayed():
                    btn.click()
                    time.sleep(1)
                    break

            # 備援：若為瀏覽器層彈窗，嘗試按 ESC 關閉
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except:
            pass
        
        # 進入頻道
        print("[INFO] 進入目標頻道...")
        driver.get(CHANNEL_URL)
        time.sleep(4)
        
        # 發送訊息
        print("[INFO] 準備發送訊息...")
        message_box = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[role='textbox']")
            )
        )
        
        # 點擊並輸入
        message_box.click()
        time.sleep(1)
        message_box.send_keys(MESSAGE_TO_SEND)
        print(f"[OK] 已輸入: {MESSAGE_TO_SEND}")
        
        time.sleep(1)
        
        # 發送（連按3次確保）
        message_box.send_keys(Keys.ENTER)
        time.sleep(0.3)
        message_box.send_keys(Keys.ENTER)
        time.sleep(0.3)
        message_box.send_keys(Keys.ENTER)
        time.sleep(0.3)
        message_box.send_keys(Keys.ENTER)
        time.sleep(2)
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[OK] [{current_time}] 訊息已發送！")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 執行失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # 確保瀏覽器關閉
        if driver:
            try:
                driver.quit()
                print("[OK] 瀏覽器已關閉")
            except:
                pass


if __name__ == '__main__':
    print("=" * 50)
    print("Discord 定時任務 - 單次執行模式")
    print("=" * 50)
    
    # 檢查設定
    if not DISCORD_EMAIL or DISCORD_EMAIL == "你的Discord帳號郵箱":
        print("[ERROR] 尚未設定帳號資訊")
        print("請編輯 config.json")
        sys.exit(1)
    
    # 隨機延遲（10~15 分鐘），避免固定分鐘數
    random_delay_min = random.randint(10, 15)
    random_delay_sec = random_delay_min * 60
    print(f"[INFO] 本次隨機延遲: {random_delay_min} 分鐘")
    time.sleep(random_delay_sec)

    # 執行任務
    success = send_discord_message()
    
    # 退出
    if success:
        print("\n[OK] 任務完成，程式退出")
        sys.exit(0)
    else:
        print("\n[ERROR] 任務失敗")
        sys.exit(1)

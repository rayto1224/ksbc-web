#!/usr/bin/env python
import os
import sys
import django

# 1. 設置Django環境（使用config.settings）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. 初始化Django
django.setup()

# 3. 現在導入視圖（Django已初始化）
from indexes.views import home_page
from django.test import RequestFactory

def test_home_page():
    """測試首頁視圖"""
    print("=== 測試首頁視圖 ===")
    
    try:
        # 創建請求
        factory = RequestFactory()
        request = factory.get('/')
        
        # 調用視圖
        response = home_page(request)
        
        # 檢查結果
        print(f"✓ 狀態碼: {response.status_code}")
        
        # 檢查上下文變量
        context = response.context_data
        print(f"✓ 上下文變量: {list(context.keys())}")
        
        # 檢查特定變量
        if 'recent_ministries' in context:
            count = context['recent_ministries'].count()
            print(f"✓ 事工動態數量: {count}")
        
        if 'recent_prayers' in context:
            count = context['recent_prayers'].count()
            print(f"✓ 代禱事項數量: {count}")
            
        print("✓ 測試通過！")
        return True
        
    except Exception as e:
        print(f"✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_home_page()
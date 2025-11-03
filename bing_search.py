import asyncio
from playwright.async_api import async_playwright

async def search_bing(query):
    """
    使用Playwright访问Bing搜索并获取搜索结果
    
    Args:
        query (str): 搜索关键词
    
    Returns:
        None: 打印搜索结果文本信息
    """
    async with async_playwright() as p:
        # 启动Firefox浏览器
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 访问Bing网站
            await page.goto("https://www.bing.com")
            print("已访问Bing首页")
            
            # 找到搜索框并输入关键词
            search_box = page.locator("#sb_form_q")
            await search_box.fill(query)
            print(f"已输入搜索关键词: {query}")
            
            # 按Enter键进行搜索
            await search_box.press("Enter")
            print("已提交搜索请求")
            
            # 等待搜索结果加载完成
            await page.wait_for_selector("#b_results")
            print("搜索结果已加载完成")
            
            # 获取搜索结果
            results = page.locator("#b_results .b_algo")
            count = await results.count()
            print(f"找到 {count} 条搜索结果")
            print("\n=== 搜索结果文本信息 ===\n")
            
            # 提取并打印每条搜索结果的文本信息，添加错误处理
            for i in range(count):
                try:
                    result = results.nth(i)
                    # 获取标题，添加超时处理
                    try:
                        title = await result.locator("h2").text_content(timeout=5000)
                    except:
                        title = "[无法获取标题]"
                    
                    # 获取URL，添加超时处理
                    try:
                        url = await result.locator("a").first.get_attribute("href", timeout=5000)
                    except:
                        url = "[无法获取URL]"
                    
                    # 获取描述，添加超时处理和更灵活的选择器
                    try:
                        # 尝试多种可能的描述选择器
                        description = await result.locator(".b_caption p").text_content(timeout=5000)
                        if not description:
                            description = await result.locator(".b_caption").text_content(timeout=5000)
                    except:
                        description = "[无法获取描述]"
                    
                    print(f"结果 {i+1}:")
                    print(f"标题: {title}")
                    print(f"URL: {url}")
                    print(f"描述: {description}")
                    print("-" * 80)
                except Exception as e:
                    print(f"处理结果 {i+1} 时出错: {str(e)}")
                    print("-" * 80)
                
        except Exception as e:
            print(f"搜索过程中出错: {e}")
        finally:
            # 关闭浏览器
            await browser.close()
            print("浏览器已关闭")

if __name__ == "__main__":
    # 执行搜索
    asyncio.run(search_bing("发顺丰"))
@tool_api
def select(self, select_ids):
    """
    在使用 WebSearch.search 搜索到相关内容后, 可以给定对应 ID 获得详细的搜索内容。

    Args:
        select_ids (List[int]): 要打开的索引列表，至少选择 3 个，最多选择 5 个项目，每个项目必须是整数。
    
    Returns:
        返回更新后的搜索结果字典，包含选择的内容或错误消息。
    """
    # 检查 select_ids 是否在搜索结果中
    for idx in select_ids:
        if idx not in self.search_results:
            return f"{idx} 不存在在搜索结果中，请确保输入的 ID 在搜索结果中"

    # 打开选定的搜索结果并更新内容
    for idx in select_ids:
        html, _ = self.open(self.search_results[idx]['url'])
        self.search_results[idx]['content'] = html

    return self

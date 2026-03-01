import json
import re
from typing import Text, Dict, List


class SubjectClassifier:
    """
    一个基于关键词匹配的学科分类器。
    支持中文和英文文本的学科判断。
    """

    def __init__(self, keywords_file: str = 'keywords.json'):
        """
        初始化分类器并加载关键词字典。
        :param keywords_file: 包含学科关键词的 JSON 文件路径。
        """
        self.keywords_file = keywords_file
        self.keywords_map = self._load_keywords()
        self.subjects = [s for s in self.keywords_map.keys() if s != '其他']

    def _load_keywords(self) -> Dict[Text, List[Text]]:
        """
        从 JSON 文件加载关键词。
        """
        try:
            with open(self.keywords_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # print(f"✅ 关键词文件 '{self.keywords_file}' 加载成功。") # 移除输出
                return data
        except FileNotFoundError:
            # 错误信息保留，因为它涉及程序运行的必要文件
            print(f"❌ 错误: 关键词文件 '{self.keywords_file}' 未找到。请确保文件存在。")
            return {}
        except json.JSONDecodeError:
            print(f"❌ 错误: 关键词文件 '{self.keywords_file}' 格式不正确。请检查 JSON 语法。")
            return {}

    def predict_subject(self, text_content: Text) -> Text:
        """
        根据输入的文本内容预测学科类型，只返回预测学科名称。

        :param text_content: 输入的教材或题目文本。
        :return: 预测的学科类型 (如 '数', '物', '化', '其他')。
        """
        if not text_content or not self.keywords_map:
            return '其他'

        normalized_text = text_content.lower()

        subject_scores = {}
        max_score = -1
        predicted_subject = '其他'

        # 统计关键词分数
        for subject, keywords in self.keywords_map.items():
            if subject == '其他':
                continue

            score = 0
            for keyword in keywords:
                lower_keyword = keyword.lower()

                # 区分中英文关键词进行精确匹配
                if re.search(r'[a-z0-9]', lower_keyword):
                    # 英文/数字关键词: 使用 \b 确保匹配的是完整的单词/数字
                    pattern = r'\b' + re.escape(lower_keyword) + r'\b'
                else:
                    # 中文关键词: 直接匹配
                    pattern = re.escape(lower_keyword)

                try:
                    # 统计关键词在文本中出现的次数
                    matches = re.findall(pattern, normalized_text)
                    score += len(matches)
                except re.error as e:
                    # 保留必要的错误提示
                    # print(f"⚠️ 正则表达式错误: 关键词 '{keyword}' 无法编译。错误: {e}")
                    pass

            subject_scores[subject] = score

            # 更新最高分数和预测结果
            if score > max_score:
                max_score = score
                predicted_subject = subject
            elif score == max_score and max_score > 0:
                pass  # 平局保持不变

        # 如果所有分数都是 0，返回 '其他'
        if max_score <= 0:
            return '其他'

        # 移除评分详情输出
        # print(f"🔢 评分详情: {subject_scores}")

        # 仅返回预测结果
        return predicted_subject


# --- 示例用法 (已简化输出) ---
if __name__ == '__main__':

    # 初始化分类器
    classifier = SubjectClassifier(keywords_file='keywords.json')

    # 示例文本
    test_texts = [
        "求函数 $f(x) = x^2$，涉及到代数计算。",
        "A force F acts on an object, causing an acceleration. Calculate the energy.",
        "请分析细胞分裂的过程和DNA的复制机制。",
        "使用Python编写一个冒泡排序algorithm，并分析其时间复杂度。",
        "这是一个关于做饭的文本，没有特定的学科关键词。",
    ]

    print("--- 学科预测结果 (简洁输出) ---")
    for i, text in enumerate(test_texts):
        # 调用方法，只获取预测结果
        result = classifier.predict_subject(text)

        # 仅输出文本和结果
        print(f"文本: {text[:40]}... -> 学科: {result}")
    print("-----------------------------------")
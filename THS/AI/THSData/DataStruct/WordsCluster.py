# -*- coding: utf-8 -*-
import joblib
from collections import defaultdict, Counter
from itertools import combinations

def classify_phrases(phrases):
    """
    根据包含至少一个相同字的规则对中文词组进行分类，并按相同字的数量排序。

    参数:
    phrases (list): 包含中文词组的列表。

    返回:
    dict: 分类后的词组，键为类标识，值为属于该类的词组列表。
    """

    # 初始化一个默认字典用于存储分类结果
    classification = defaultdict(list)

    # 创建一个字典用于存储每个字出现的词组
    char_to_phrases = defaultdict(set)

    # 遍历所有词组，将词组中的每个字与词组关联
    for phrase in phrases:
        for char in phrase:
            char_to_phrases[char].add(phrase)

    # 创建一个集合用于存储已经处理过的词组
    processed_phrases = set()

    # 遍历所有词组
    for phrase in phrases:
        if phrase not in processed_phrases:
            # 找到包含至少一个相同字的所有词组
            related_phrases = set()
            for char in phrase:
                related_phrases.update(char_to_phrases[char])

            # 按相同字的数量排序
            related_phrases = sorted(related_phrases, key=lambda x: len(set(x) & set(phrase)), reverse=True)

            # 将这些词组添加到分类结果中
            classification[frozenset(related_phrases)].extend(related_phrases)

            # 将这些词组标记为已处理
            processed_phrases.update(related_phrases)

    # 将分类结果转换为普通字典
    return dict(classification)


# 示例词组列表
phrases = ['5G通信','工业有色','通信','5G50','智能汽车','有色金属','资源','消费电子','信息科技','有色基金','有色50','通信','矿业','有色60','VR','消费电子','TMT50','电子','能源','集成电路','能源基金','能源','油气资源','石油','电信50','通信设备','绿电50','大宗商品','物联网','汽车零件','稀土基金','纳指科技','电力','智能网联汽车','油气','煤炭','电子','国企共赢','稀有金属基金','TMT','材料','信息技术','智能消费','绿电','人工智能','人工智能','龙头家电','黄金股票','通信基金','芯片','半导体','储能电池','物联网工银','机器人','家电','工程机械','芯片易方达','科技100','央企创新驱动','智能制造','工业互联','信息安全','芯片','化工行业','云计算沪港深','计算机南方','工业母机','价值100','国企一带一路','物联网沪港深','云50','湖北','浙商之江凤凰','钢铁','金融科技','大数据','软件龙头','碳中和50','智能汽车易方达','信创基金','软件基金','机器人100','科技50','汽车','化工','科技龙头','人工智能50','信创富国','深成长龙头','500价值','军工','汽车','科创信息技术','产业升级','红利国企','央企红利50','央企','国企红利','软件','红利低波','可选消费','中证红利','国防','大数据','科创芯片','深300','高端装备','高端装备','战略新兴','机械','碳中和龙头','红利','高股息','新能车','数字经济','创业大盘','央企红利','央企科技','科创成长','电池基金','锂电池','新材料50','教育','深证主板50南方','新能源车','大湾区','绿色能源','国企','光伏','环保','创业板成长易方达','国企改革','创新100','漂亮50','中概互联','浙江国资','长三角','影视','科创新材料','碳中和60指数','光伏30','银行优选','军工龙头','新能源易方达','低碳易方达','基本面120','科技','交通运输','创业板科技','深红利','红利低波基金','民企','湾创','沪港深科技','沪深300红利','张江','在线消费','科技基金','基建','物流','央企','红利低波100','新能源50','180治理','科创100华夏','基建50','农牧','长江保护主题','ESG300','价值','半导体设备','180ESG','证券先锋','粮食','游戏传媒','半导体设备','中金科技先锋','交运','成渝经济圈','农业','科技龙头','线上消费平安','ESG','ESG','畜牧','创业板价值','沪深300成长','消费沪港深','中证A50易方达','传媒','红利质量','中药','品牌消费','基本面50','互联网','银行','交运','G60创新','农业易方达','杭州湾区','消费50','证券','游戏','银行','消费龙头','上证券商','央视50','农业','国货','线上消费','旅游','可持续发展','证券龙头','养老','证券东财','保险证券','金融地产','金融','金融','金融地产','标普消费','消费服务','文娱传媒','港股非银','证券保险','消费','房地产基金','医药健康','恒生消费','建材','医药龙头','医药50','科创医药指数','国投金融地产','医疗设备','医药卫生','创新药','医药','上海国企','创新药沪港深','消费','生物疫苗','医药沪港深','医疗创新','地产','生物医药','食品饮料','医药卫生','医疗健康泰康','生物医药','医疗器械指数','饮食','消费30','港股创新药','生物科技','房地产','医疗','食品饮料','疫苗','酒','创新药富国','医药','恒生医疗','食品饮料基金','纳指生物科技'
]

# 对词组进行分类
classified_phrases = classify_phrases(phrases)
joblib.dump(classified_phrases, './JOBLIB/ETFClass.joblib')

# 打印分类结果
for key, value in classified_phrases.items():
    print(f"类 {key} 包含的词组: {value}")

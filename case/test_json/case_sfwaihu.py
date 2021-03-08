# -*- coding: utf-8 -*-
from case.test_json.dialogtest import runcase
"""         Sheet1:身份证无图片
            Sheet2:身份证不清晰
            Sheet3:身份证过期
            Sheet4:个人税金确认
            Sheet5:超个人行邮物品申报标准
            Sheet6:个人行邮物品提供购物凭证
            Sheet7:报关方式确认
            Sheet8:企业税金确认
            Sheet9:核实品名及申报价值场景，(暂无)
            Sheet10:价值低报，提供发票
            Sheet11:价值低报，提供发票，说明情况
            Sheet12:价值低报，提供发票、营业执照
            Sheet13:需提供收方营业执照
            Sheet14:疑似个人件，需提供收方身份证正反图片、购物凭证
            Sheet15:个人税金确认，提供有效身份证图片
"""
#randphone = True
case="sfwaihu"
runcase(case)
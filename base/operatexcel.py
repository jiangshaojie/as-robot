# -*- coding: utf-8 -*-
from openpyxl.styles.colors import BLACK
from openpyxl.styles import Font


class operatexcel():
    @staticmethod
    def resettext(wb, sheetname, column, row):
        """
            wb:load_workbook isntance,sheetanme: excel 单元表名。重置  文本内容
        """
        sheet1 = wb[sheetname]
        lastcasecompare = sheet1[column]
        for idx, val in enumerate(lastcasecompare[row:]):
            if val.value is None:
                pass
            else:
                val.value = ''

    @staticmethod
    def resetcolour(wb, sheetname, column, row):
        sheet1 = wb[sheetname]
        # 重置case 颜色
        lastcasecompare = sheet1[column]
        for idx, val in enumerate(lastcasecompare[row:]):
            val.font = Font(color=BLACK)

import openpyxl.workbook
import requests, openpyxl

wb = openpyxl.workbook

sheet = wb.Workbook

sheet["A1"] = "Name"
sheet["B1"] = "Age"

sheet["A2"] = "Alice"
sheet["B2"] = 25

sheet["A3"] = "Bob"
sheet["B3"] = 30

wb.save("data_workbook.xlsx")
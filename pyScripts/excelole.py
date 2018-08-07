import win32com.client

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = True
wb = excel.Workbooks.Open('C:\\_Documents\\�Ե���Ŀ�ӽ�\\14.�𵨸�(��ǰ�Ӽ�)\\02.GOODS_OUT�ε�1��\\Goods_out_�Է´��_4��_DRM����.xlsx')
ws = wb.ActiveSheet
ws.Cells(1,1).currentRegion.copy
rng = ws.Cells(1,1).currentRegion
for i in range(rng.row,rng.rows.count):
    for j in range(rng.Column,rng.Columns.count):
        print(ws.Cells(i,j).value)
wb.range("A1").Value
print(ws.Cells(1,1).Value)
excel.Quit()

def get_clip():
    try:
        # Python2
        import Tkinter as tk
    except ImportError:
        # Python3
        import tkinter as tk
    
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    # read the clipboard
    c = root.clipboard_get()
    return c
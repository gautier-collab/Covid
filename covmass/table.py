import docx
import os

doc = docx.Document()

doc.add_heading('Covid-19 Lagebericht', 0)

records = [
  ["USA", "5", "2", "nCovLive"], 
  ["Europa", "5", "2", "nCovLive"],
]

table = doc.add_table(rows=1, cols=4)
table.style = "Medium Shading 1 Accent 1"
header_cells = table.rows[0].cells
header_cells[0].text = "Ort"
header_cells[1].text = "Infected"
header_cells[2].text = "Deceased"
header_cells[3].text = "Quelle"

for ort, infected, deceased, source in records:
  row_cells = table.add_row().cells
  row_cells[0].text = ort
  row_cells[1].text = infected
  row_cells[2].text = deceased
  row_cells[3].text = source

doc.save("table.docx")
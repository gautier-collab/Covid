import docx
import os
from covmass.models import Zone

def updateDOCX():

  doc = docx.Document()
  doc.add_heading('Covid-19 Lagebericht', 0)

  table = doc.add_table(rows=1, cols=6)
  table.style = "Medium Shading 1 Accent 1"
  header_cells = table.rows[0].cells
  header_cells[0].text = "Ort"
  header_cells[1].text = "Bestätigte Infektionen"
  header_cells[2].text = "∆Infektionen"
  header_cells[3].text = "Todesfälle"
  header_cells[4].text = "∆Todesfälle"
  header_cells[5].text = "Quelle"

  for zone in Zone.objects.all():
    row_cells = table.add_row().cells
    row_cells[0].text =  zone.german_name
    row_cells[1].text = zone.infected.display_total()
    row_cells[2].text = zone.infected.display_new()
    row_cells[3].text = zone.deceased.display_total()
    row_cells[4].text = zone.deceased.display_new()
    row_cells[5].text = zone.source.name
  
  doc.save("static_cdn/media_root/lagebericht.docx")
  
  return "Updated DOCX file"
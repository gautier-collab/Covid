import os, docx
from datetime import datetime
from covmass.models import Zone, Update
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt

def updateDOCX():

  doc = docx.Document()
  doc.add_heading('Covid-19 Lagebericht', 0)
  p = doc.add_paragraph(f"Diese Zahlen wurden von NEXUS ETH Zürich am {str(datetime.today().day).zfill(2)}.{str(datetime.today().month).zfill(2)}.{datetime.today().year} um {str(datetime.today().hour).zfill(2)}:{str(datetime.today().minute).zfill(2)} aktualisiert.")
  p.paragraph_format.space_before = Pt(35)
  p.paragraph_format.space_after = Pt(15)

  table = doc.add_table(rows=1, cols=6)
  table.style = "Medium Shading 1 Accent 1"
  table.vertical_alignment = WD_ALIGN_VERTICAL.TOP
  header_cells = table.rows[0].cells
  header_cells[0].text = "Ort"
  header_cells[1].text = "Bestätigte Infektionen"
  header_cells[2].text = "∆Infektionen"
  header_cells[3].text = "Todesfälle"
  header_cells[4].text = "∆Todesfälle"
  header_cells[5].text = "Quelle"

  for zone in Zone.objects.all():
    cells = table.add_row().cells
    
    cells[0].text = zone.german_name
    cells[1].text = zone.infected.display_total()
    cells[2].text = zone.infected.display_new()
    cells[3].text = zone.deceased.display_total()
    cells[4].text = zone.deceased.display_new()
    cells[5].text = zone.source.name
    
    cells[1].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    cells[2].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    cells[3].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    cells[4].paragraphs[0].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    
    
    # a = cells[0].add_paragraph(zone.german_name)
    # b = cells[1].add_paragraph(zone.infected.display_total())
    # c = cells[2].add_paragraph(zone.infected.display_new())
    # d = cells[3].add_paragraph(zone.deceased.display_total())
    # e = cells[4].add_paragraph(zone.deceased.display_new())
    # f = cells[5].add_paragraph(zone.source.name)
    
    # b.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    # c.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    # d.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    # e.alignment = WD_ALIGN_PARAGRAPH.RIGHT
  
  doc.save("static_cdn/media_root/lagebericht.docx")
  print("DOCX is saved")
  
  return "Updated DOCX file"
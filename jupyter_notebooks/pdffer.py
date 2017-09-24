from nbconvert import PDFExporter

exporter = PDFExporter()

output, resources = exporter.from_filename('betacarotene.ipynb')
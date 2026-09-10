from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


class NumberedPageCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)

        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            super().showPage()

        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return
        page = "Página %s de %s" % (self._pageNumber - 1, page_count - 1)
        self.setFont("Helvetica", 11)
        self.drawString(450, A4[1] - 125, page)

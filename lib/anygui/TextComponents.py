from anygui.Components import AbstractComponent
from anygui.Exceptions import UnimplementedMethod
from anygui.Models import TextModel

class AbstractTextComponent(AbstractComponent):

    # _text = ''
    # _model = None
    _selection = (0, 0)
    _editable = 1

    def __init__(self, *arg, **kw):
        AbstractComponent.__init__(self, *arg, **kw)
        # self.model = TextModel()
        self.text = kw.get('text','')

    # text property:

    def _get_text(self):
        # semikludge: replace all text if any part changed
        text = self._backend_text()
        if text is not None and text != str(self._text):
            try: self._text[:] = text
            except: self._text = text
        return self._text

    def _set_text(self, text):
        self._text = text
        self._ensure_text()

    def _ensure_text(self):
        raise UnimplementedMethod, (self, '_ensure_text')

    # selection property:
    
    def _get_selection(self):
        selection = self._backend_selection()
        if selection is not None:
            self._selection = selection
        return self._selection
    
    def _set_selection(self, selection):
        self._selection = selection
        self._ensure_selection()

    def _ensure_selection(self):
        raise UnimplementedMethod, (self, '_ensure_selection')

    # editable property

    def _get_editable(self):
        return self._editable

    def _set_editable(self, editable):
        self._editable = editable
        self._ensure_editable()

    def _ensure_editable(self):
        raise UnimplementedMethod, (self, '_ensure_editable')


    def _finish_creation(self): # FIXME: Hm...
        AbstractComponent._finish_creation(self)
        self._ensure_text()
        self._ensure_selection()
        self._ensure_editable()

class Document(object):
        """A Document class compatible with all Summarizers."""

        def __init__(self, title=None, text=None):
            """
            Constructor.
            :param title: the title of the document.
            :type title: str
            :param text: main body of text of the document
            :type text: str
            """
            self.title = title
            self.text = text
            
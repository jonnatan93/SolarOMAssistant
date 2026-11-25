class BaseReport:

    def __init__(
        self,
        master_file,
        folder,
        callback=None,
        progress_callback=None
    ):

        self.master_file = master_file
        self.folder = folder
        self.callback = callback
        self.progress_callback = progress_callback

    # -----------------------------------------------------

    def notify(self, message):

        if self.callback:
            self.callback(message)

    # -----------------------------------------------------

    def report_progress(self, value):

        if self.progress_callback:
            self.progress_callback(value)
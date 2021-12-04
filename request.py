class Request:
    """
    Th request object represents what kind of data to retrieve.The request object comes with certain accompanying
    configuration options as well as a field that holds the result. The
    attributes are:
        -mode: "pokemon", "ability", "move" to search that specific item
        -data_input: the id or name to search for
        -input_file: the text file that contains the data_input to be seacrched for
        -out_put: the method of output request, printing to console or writing to a text file
        -expanded: to search for more information(pokemon mode only)
    """

    def __init__(self):
        self.mode = None
        self.data_input = None
        self.input_file = None
        self.output = None
        self.expanded = False

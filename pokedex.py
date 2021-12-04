import argparse

from pokeretriever.request_pokeapi import *


def setup_request_commandline() -> Request:
    """
    Implements the argparse module to accept arguments via the command
    line. This function specifies what these arguments are and parses it
    into an object of type Request. If something goes wrong with
    provided arguments then the function prints an error message and
    exits the application.
    :return: The object of type Request with all the arguments provided
    in it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="")
    parser.add_argument("-inputfile", "--inputfile", help="")
    parser.add_argument("-inputdata", "--inputdata", help="")
    parser.add_argument("-output", "--output", default="print",
                        help="")
    parser.add_argument("-expanded", "--expanded", action='store_true',
                        help="")
    try:
        args = parser.parse_args()
        request = Request()
        request.mode = PokedexMode(args.mode)
        request.data_input = args.inputdata
        request.input_file = args.inputfile
        request.output = args.output
        if args.expanded:
            request.expanded = args.expanded
        return request
    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()


def print_pokedex_result(request: Request, pokedex_result: list):
    if request.output == "print":
        for item in pokedex_result:
            print(item)
    else:
        f = open(request.output, 'w')
        for item in pokedex_result:
            f.write(str(item))
            f.write("\n")
        f.close()


if __name__ == '__main__':
    request = setup_request_commandline()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    results = asyncio.run(execute_request(request))
    print_pokedex_result(request, results)

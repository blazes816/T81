#/usr/bin/python3
from optparse import OptionParser
from processor import Processor
import exceptions as exp


# Handle the options and arguments
def get_options():
    parser = OptionParser(usage='t816 file [options]')
    parser.add_option("-d", "--debug", dest="debug", action="store_true",
                      default=False, help="Show debug panel")
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("You must specify a file to execute")

    return options, args

# This is our main entry point into the application
def main():
    options, args = get_options()
    # Create Processor
    processor = Processor(options.debug)

    # Load the programe given by the user
    filename = args[0]
    try:
        processor.load(filename)
    except exp.InvalidFile:
        print("Invalid file %s" % filename)
        exit(1)
    except IOError:
        print("File %s does not exist" % filename)
        exit(1)

    # Start the processing
    processor.run()


if __name__ == '__main__':
    main()

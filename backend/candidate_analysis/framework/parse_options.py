from optparse import OptionParser

parser = OptionParser()

parser.add_option('-e', '--env',help='development/staging/production')

(options, args) = parser.parse_args()

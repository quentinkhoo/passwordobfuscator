#!/usr/bin/python

import string, sys
from optparse import OptionParser 

def translate(key,text,encrypt=True):
	symbols=" " + string.digits + "!@#$%^&*()_+~{}|:<>?/.,;\\][=-`" + string.letters
	maxkey = len(symbols)
	if key < 1:
		key = 1
	elif key >= maxkey:
		key = maxkey - 1
	if not encrypt:
		key = -key
	s=""

	for c in text:
		if c in symbols:
			n = symbols.find(c)
			n += key
			if n >= maxkey:
				n -= maxkey
			elif n < 0:
				n += maxkey
			s += symbols[n]
		else:
			s += c
	return s

def console(k,action):
    t = raw_input("Input text: ").strip()
    print translate(k,t,action)

def input_file(k,filename,action):
    try:
       # reading input file
       f = open(filename,"r")
       lines = f.readlines()
       f.close()
       # translating input file
       for line in lines:
           print translate(k,line.strip(),action)
    except IOError as e:
       print "I/O error {0} : {1}".format(e.errno,e.strerror) 

def input_output_files(k,input_filename,output_filename,action):
    try:
       # reading input file
       fi = open(input_filename,"r")
       lines = fi.readlines()
       fi.close()
       # translating input file
       fo = open(output_filename,"w")
       for line in lines:
           fo.write(translate(k,line,action))
       fo.close() 
    except IOError as e:
       print "I/O error {0} : {1}".format(e.errno,e.strerror) 


def main():
    parser = OptionParser(usage="usage: %prog <options> [input-file] [output-file]",
                          version="%prog 1.0")
    parser.add_option("-c","--console",
                      action="store_true",
                      dest="console_flag",
                      default=False,
                      help="input/output from/to command-line")
    parser.add_option("-d","--decrypt",
                      action="store_true",
                      dest="decrypt_flag",
                      default=False,
                      help="Decrypt text")
    parser.add_option("-i","--input",
                      action="store_true",
                      dest="input_flag",
                      default=False,
                      help="input from file and output to terminal")
    parser.add_option("-o","--output",
                      action="store_true",
                      dest="output_flag",
                      default=False,
                      help="input from file and output to another file")
    parser.add_option("-k","--key",
                      action="store",
                      dest="key",
                      default="0",
                      help="Encryption key")
    if len(sys.argv) == 1:
       parser.error("wrong options, please type -h or --help") 
    (options, args) = parser.parse_args()
    k=0
    if int(options.key) == 0:
       k=int(raw_input("Enter key [1..92]: ").strip())
    if options.console_flag:
       console(k,not options.decrypt_flag)
    elif options.input_flag:
       if len(args) == 1:
          input_file(k,args[0],not options.decrypt_flag)
       else:
          parser.error("-i flag must be specified with an input filename")
    elif options.output_flag:
       if len(args) == 2:
          input_output_files(k,args[0],args[1],not options.decrypt_flag)
       else:
          parser.error("-o flag must be specified with an input and output filenames")
    else:
       parser.error("wrong options, please type -h or --help")
   
if __name__ == '__main__':
   main()
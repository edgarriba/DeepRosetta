import argparse


class BaseParser:
        '''parse the line command of the system'''
        def parse(self):
            parser = argparse.ArgumentParser(description='Convert deep learning model.')


            #parser.add_argument('-input model name',  help='Store a model name')
            parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'),
                            help='name of the file of the model that you want to convert')

            #parser.add_argument('-output model name', help='name of the model that you want to convert')

            parser.add_argument('-o',  metavar='out-file', type=argparse.FileType('wt'),
                                help='file of the model that you want to convert')
            
            try:
                parser.parse_args()
                
            except IOError, msg:
                parser.error(str(msg))




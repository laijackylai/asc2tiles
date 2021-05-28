import numpy as np
import click


@click.command()
@click.option('--input-file', default='Whole_HK_DTM_5m_data.asc', help='input file path', show_default=True)
@click.option('--skip-rows', default=0, help='rows to skip if input is an ascii file')
@click.option('--boundaries', default=None, help='boundaries of the input data')
def main(input_file, skip_rows):
    """main function"""
    check_file_type(input_file)
    load_asc(input_file, skip_rows)


def check_file_type(input_file):
    """check whether the input file type is the same as actual input file type"""
    actual_file_type = input_file.split('.')[1]
    if('asc' != actual_file_type):
        print('File type not matched!')
        exit()


def load_asc(input_file, skip_rows):
    """load data from input asc file"""
    print('loading asc file...')
    asc_data = np.loadtxt(input_file, skiprows=skip_rows)


if __name__ == '__main__':
    main()

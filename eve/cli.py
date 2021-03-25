from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import os
import errno
import click
import glob

@click.command()
@click.argument('pdf_directory')
@click.option('--file_distanation', '-f', help="set file distination where to put the images")
def cli(pdf_directory, file_distanation):
    """Convert PDF to images using command: pdf2image C:\Path\pdf_directory_folder -f '<file_distanation>'"""
    dir = str(file_distanation)+'\\pdf_images'
    list_image_result = []
    #if pdf_images is not exist then will creates a folder called pdf_images 
    if not os.path.isdir(dir):
        try:
            os.mkdir(dir)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass

    pdf_files = list(glob.iglob(pdf_directory+'/**/*.pdf', recursive = True))
    for pdf_path in pdf_files:
        # File is truly exist then creates a directory by file name
        
        if (os.path.isfile(pdf_path)):
            pdf_dir = dir+'\\'+os.path.basename(pdf_path).replace('.pdf', '')
            pdf_name = os.path.basename(pdf_path).replace('.pdf', '')

            if not os.path.isdir(pdf_dir):
                try:
                    os.mkdir(pdf_dir)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
                    pass

            if os.path.isdir(pdf_dir):
                # Save the output image to pdf_dir variable with generated name
                images_from_path = convert_from_path(pdf_path)
                
                #Get PIL images format and get their file names
                for index,img in enumerate(images_from_path):
                    if hasattr(img, 'filename'):
                        # Save image to selected dir
                        file_name = pdf_dir+'//'+pdf_name+'_'+str(index+1)+'.jpg'
                        img.save(file_name)

                        #Append from array list with the directory and file name
                        list_image_result.append(file_name)
                        # print(file_name)

    #array Ourput result
    print(*list_image_result, sep = ', ')



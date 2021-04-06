import click
import errno
import glob
import os

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

@click.group()
@click.option('--pdf/--no-pdf', default=False)
@click.option('--path', default='')
@click.option('--afr/--no-afr', default=False)
@click.option('--file_destination', '-f', help="set file distination where to put the images")
@click.pass_context
def cli(ctx, pdf, path, afr, file_destination):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['IS_PDF'] = pdf
    ctx.obj['PATH'] = path
    ctx.obj['SIZE'] = (773,1094) if afr else None
    ctx.obj['OUTPUT_DISTINATION'] = file_destination or path

@cli.command()
@click.pass_context
def convert(ctx):
    ctx.obj['ROOT_DIR'] = ROOT_DIR = str(ctx.obj['OUTPUT_DISTINATION'])+'\\pdf_images'

    #if pdf_images folder is not exist then will creates a folder called pdf_images
    print('creating pdf_images folder in: '+(ctx.obj['OUTPUT_DISTINATION']))
    if not os.path.isdir(ROOT_DIR):
        try:
            os.mkdir(ROOT_DIR)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                print(exc)
                raise

    if ctx.obj['IS_PDF']:
        print('Converting...')
        service(ctx, ctx.obj['PATH'])
    else:
        if not os.path.isdir( ctx.obj['PATH']):
            print("please provide the directory of pdf's")
            pass
        
        print('Converting pdf files in ')
        pdf_files = list(glob.iglob(ctx.obj['PATH']+'/**/*.pdf', recursive = True))
        for pdf_path in pdf_files:
            service(ctx, pdf_path)


@cli.command()
@click.pass_context
def test(ctx):
    click.echo("success")


def service(ctx, pdf_path):

    print('PAAATH:::::::',pdf_path)
    if (os.path.isfile(pdf_path)):
            pdf_dir =  ctx.obj['ROOT_DIR']+'\\'+os.path.basename(pdf_path).replace('.pdf', '')
            pdf_name = os.path.basename(pdf_path).replace('.pdf', '')

            print('Converting %s' % pdf_name)

            if not os.path.isdir(pdf_dir):
                try:
                    os.mkdir(pdf_dir)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
                    pass
                
                try:
                    # Save the output image to pdf_dir variable with generated name
                    print('With size....',ctx.obj['SIZE'])
                    images_from_path = convert_from_path(pdf_path, size=ctx.obj['SIZE'])
                except PDFInfoNotInstalledError:
                    print("conda proppler binary not installed")
                except PDFPageCountError:
                    print("PDFPageCountError PDF is pages is broken")
                except PDFSyntaxError:
                    print("PDFSyntaxError Can't convert this pdf %s" % pdf_dir)
                
                #Get PIL images format and get their file names
                for index,img in enumerate(images_from_path):
                    if hasattr(img, 'filename'):
                        # Save image to selected dir
                        file_name = pdf_dir+'//'+pdf_name+'_'+str(index+1)+'.jpg'
                        img.save(file_name)
            else:
                print("already had the files")
    
    else:
        print("Pdf file does not exist. %s" % (pdf_path))

import click

from eve.service import svc_convert


class Context:
    def __init__(self):
        pass
        # self.svc_convert = svc_convert.Convert()


@click.group()
@click.pass_context
# @click.option('--path-location', default='')
def cli(ctx, pdf_files):
    """To Convert PDF to Images needs to have option with array of pdf_files"""
    # click.echo(pdf_files)
    # ctx.obj = Context()

@click.command()
@click.option('--pdf_files', default=[])

@click.pass_context
def pdf2image(pdf_files):
    click.echo(pdf_files)

# @cli.command()
# @click.argument(
#     'pdf_files'
# )
# @click.argument(
#     'path_location'
# )
# @click.pass_context
# def pdf_files(ctx, pdf_files, path_location):
#     """Put pdf files directory for example: ['path/sample1.pdf', 'path/'sample2.pdf]"""
#     print(pdf_files)
#     click.echo(path_location)

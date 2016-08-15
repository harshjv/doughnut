import os
import pathlib
import base64

# font-ttf
# opentype
font_type='font-ttf'
font_dir='ttf'
font_extension='.ttf'

fonts = [p for p in pathlib.Path('./resources/fonts/%s' % font_dir).iterdir() if p.is_dir()]

for font in fonts:
    woffs = [w for w in font.iterdir() if w.is_file()]

    font_name = os.path.splitext(font.name)[0].lower()

    print(font_name)

    with open('./resources/less/%s-data.less' % font_name, 'w') as out:
        for woff in woffs:
            file_split = os.path.splitext(woff.name)
            file_extension = file_split[1].lower()

            if file_extension == font_extension:
                with open(str(woff.absolute()), "rb") as woff_file:
                    style_name = file_split[0].lower()

                    idx = style_name.index('-') + 1
                    style_name = style_name[idx:len(style_name)]

                    encoded_string = base64.b64encode(woff_file.read()).decode('UTF-8')
                    d = "@{basename}-{name}: 'data:application/{font_type};charset=utf-8;base64,{encoded_string}';\n".format(font_type=font_type, basename=font_name, name=style_name, encoded_string=encoded_string)
                    out.write(d)

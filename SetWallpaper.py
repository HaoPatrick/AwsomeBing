# -*- coding: utf-8 -*-
import urllib.request, json, os
from PIL import Image, ImageFont, ImageDraw
from subprocess import call


def getBing():
    # use global.bing.com to avoid problems aroused by different locations
    url = r'http://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    try:
        get_json_format_response = urllib.request.urlopen(url).read().decode('utf-8')
    except Exception as e:
        print(e)
        return
    total_image_content = json.loads(get_json_format_response)['images'][0]
    image_info = {'startdate': total_image_content['startdate'],
                  'enddate': total_image_content['enddate'],
                  'url': 'http://global.bing.com%s' % total_image_content['url'],
                  'copyright': total_image_content['copyright'],
                  }

    # for each desc it has 'desc', 'link', 'query', 'locx', 'locy' attributes.
    desc_info = [i for i in total_image_content['hs']]
    sentence2words(desc_info)
    try:
        # urllib.request.urlretrieve(image_info['url'], 'bing.jpg')
        photo_enhance(desc_info)
        # call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://%s/bing-out.jpg'%os.getcwd()])
    except Exception as e:
        print(e)


def sentence2words(desc_info):
    for desc in desc_info:
        words = desc['desc'].split()
        result = ''
        i = 0
        for word in words:
            result = result + word + ' '
            i += 1
            if i == 5:
                result += '\n'
                i = 0
        desc['desc'] = result


def photo_enhance(desc_info):
    img = Image.open('bing.jpg').convert('RGBA')
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("DejaVuSansMono.ttf", 22, encoding='utf-8')
    for desc in desc_info:
        tempDesc = desc['desc']
        x, y = (int(19.20 * desc['locx']), int(10.80 * desc['locy']))
        w, h = font.getsize(str(['s' for i in range(0, 17)]))
        rectangleOffset=6
        draw.rectangle((x-rectangleOffset, y-rectangleOffset, x+rectangleOffset + w / 3, y+rectangleOffset + h * 3),
                       fill=(153,153,102,150))
        draw.text((x, y), tempDesc, fill=(255, 255, 255, 150),
                  font=font)
    result = Image.alpha_composite(img, txt)
    result.save('bing-out.jpg')


if __name__ == '__main__':
    getBing()

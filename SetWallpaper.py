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
        urllib.request.urlretrieve(image_info['url'], 'bing.jpg')
        photo_enhance(desc_info)
        call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://%s/bing-out.jpg'%os.getcwd()])
    except Exception as e:
        print(e)


def sentence2words(desc_info):
    for desc in desc_info:
        words = desc['desc'].split()
        result = ''
        max_line_count = 0
        temp_line_count = 0
        i = 0
        line = 1
        for word in words:
            temp_line_count += len(word)
            result = result + word + ' '
            i += 1
            if i == 5:
                result += '\n'
                i = 0
                line += 1
                if temp_line_count > max_line_count:
                    max_line_count = temp_line_count
                temp_line_count = 0
        # Strip the \n at the end of the line.
        if result[-1:] == '\n':
            result = result[:-1]
            line -= 1
        desc['desc'] = result
        desc['maxLineCount'] = max_line_count
        desc['line'] = line


def photo_enhance(desc_info):
    img = Image.open('bing.jpg').convert('RGBA')
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("DejaVuSansMono.ttf", 16, encoding='utf-8')
    for desc in desc_info:
        tempDesc = desc['desc']
        x, y = (int(19.20 * desc['locx']), int(10.80 * desc['locy']))

        # Too much dark method, as long as some hard code here.
        # w, h = font.getsize(str([' ' for i in range(0, int(desc['maxLineCount']))]))
        w, h = font.getsize(str(['s' for i in range(0, 50)])[:int(desc['maxLineCount'] * 3.6)])
        rectangleoffset = 6
        draw.rectangle(
            (x - rectangleoffset, y - rectangleoffset, x + rectangleoffset + w / 3,
             y + rectangleoffset + h * desc['line']),
            fill=(30, 30, 21, 130))
        draw.text((x, y), tempDesc, fill=(255, 255, 255, 100),
                  font=font)
    result = Image.alpha_composite(img, txt)
    result.save('bing-out.jpg')


if __name__ == '__main__':
    getBing()

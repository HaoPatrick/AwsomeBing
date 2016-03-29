# -*- coding: utf-8 -*-
import urllib.request, json
from PIL import Image, ImageFont, ImageDraw
from subprocess import call


def getBing():
    # use global.bing.com to avoid problems aroused by different locations
    url = r'http://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    try:
        get_json_format_response = urllib.request.urlopen(url).read().decode('utf-8')
    except Exception as e:
        print(e)
    else:
        total_image_content = json.loads(get_json_format_response)['images'][0]
        image_info = {'startdate': total_image_content['startdate'],
                      'enddate': total_image_content['enddate'],
                      'url': 'http://global.bing.com%s' % total_image_content['url'],
                      'copyright': total_image_content['copyright'],
                      }
        # for each desc it has 'desc', 'link', 'query', 'locx', 'locy' attributes.
        desc_info = [i for i in total_image_content['hs']]
        PhotoEnhance(desc_info)
        '''try:
            urllib.request.urlretrieve(image_info['url'],'bing.jpg')
            call(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', image_info['url']])
        except Exception as e:
            print(e)
        '''


def PhotoEnhance(desc_info):
    img = Image.open('bing.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSansMono.ttf", 20,encoding='utf-8')

    for desc in desc_info:
        draw.text((int(19.20 * desc['locx']), int(10.80 * desc['locy'])), '%s' % str(desc['desc']), (119, 119, 60),
                  font=font)
    img.save('bing-out.jpg')


if __name__ == '__main__':
    getBing()

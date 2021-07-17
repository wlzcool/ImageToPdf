from gooey import Gooey, GooeyParser
from PIL import Image
import os
import img2pdf


@Gooey(
    program_name='图片合并pdf',
    menu=[{
        'name': '关于',
        'items': [{
            'type': 'AboutDialog',
            'menuTitle': '关于',
            'name': '图片合并PDF',
            'description': '将文件夹中图片生成pdf',
            'version': '1.0.0',
            'copyright': '2021',
            'website': 'https://github.com/wlzcool/ImageToPdf',
            'developer': 'https://juejin.cn/user/2815188501792951',
            'license': 'GNU'
        },  {
            'type': 'Link',
            'menuTitle': '程序下载地址',
            'url': 'https://github.com/wlzcool/ImageToPdf'
        }]
    }]
)
def main():
    parser = GooeyParser(description="图片合并pdf")
    parser.add_argument('dirname', metavar='图片文件夹所在路径', help="例如d:/wlzcool", widget='DirChooser')
    parser.add_argument('savedirname', metavar='目标图片文件夹所在路径', help="例如d:/wlzcool2", widget='DirChooser')
    parser.add_argument(
        'reductionFactor',
        metavar='长宽压缩比',
        help='例如3，需要填入大于等于1的整数',
        gooey_options={
            'validator': {
                'test': '1 <= int(user_input) ',
                'message': '长宽压缩比需大于等于1'
            }
        })
    parser.add_argument(
        'filename',
        metavar='请输入输出文件名',
        help='例如：第一章')
    parser.add_argument(
        '-isConvertBlack',
        metavar='是否输出黑白版本',
        action='store_true',
        help='需要输出黑白版本请勾选')

    args = parser.parse_args()
    print(args.dirname)

    dirname = args.dirname
    savedirname = args.savedirname

    files = os.listdir(dirname)
    reductionFactor = int(args.reductionFactor)
    if reductionFactor <= 0:
        reductionFactor = 3
    isConvertBlack = args.isConvertBlack
    for fname in files:
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(dirname, fname)
        savePath = os.path.join(savedirname, "pdf" + fname)
        if os.path.isdir(path):
            continue
        img = Image.open(path)
        if img.size[0] > img.size[1]:
            im_rotate = img.rotate(90, expand=True)
            size = (int(im_rotate.size[0] / reductionFactor), int(im_rotate.size[1] / reductionFactor))
            im_rotate = im_rotate.resize(size)
            if isConvertBlack:
                im_rotate = im_rotate.convert("L")
            im_rotate.save(savePath, quality=95)
        else:
            size = (int(img.size[0] / reductionFactor), int(img.size[1] / reductionFactor))
            img = img.resize(size)
            if isConvertBlack:
                img = img.convert("L")
            img.save(savePath, quality=95)
    print("图片处理完成，开始生成pdf")
    filename = args.filename
    with open(filename + ".pdf", "wb") as f:
        imgs = []
        files = os.listdir(savedirname)
        for fname in files:
            if not fname.endswith(".jpg"):
                continue
            path = os.path.join(savedirname, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        f.write(img2pdf.convert(imgs))


if __name__ == '__main__':
    main()

from PIL import Image, ImageDraw

def create_icon():
    """创建系统托盘图标"""
    # 创建一个简单的图标
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆
    draw.ellipse([(4, 4), (60, 60)], fill=(52, 152, 219, 255))
    
    # 绘制微信图标
    # 绘制外圈
    draw.ellipse([(16, 16), (48, 48)], fill=(255, 255, 255, 255))
    # 绘制内圈
    draw.ellipse([(20, 20), (44, 44)], fill=(52, 152, 219, 255))
    # 绘制两个小圆
    draw.ellipse([(24, 24), (28, 28)], fill=(255, 255, 255, 255))
    draw.ellipse([(36, 24), (40, 28)], fill=(255, 255, 255, 255))
    # 绘制笑脸
    draw.arc([(24, 32), (40, 40)], 0, 180, fill=(255, 255, 255, 255), width=2)
    
    return img


if __name__ == '__main__':
    icon = create_icon()
    icon.save("wechat-multi-open.ico")
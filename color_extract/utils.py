import re
from bs4 import BeautifulSoup

def extract_colors_from_html(html_content):
    """HTML ফাইল থেকে সব কালার কোড এক্সট্রাক্ট করা"""
    colors = {
        'hex_colors': set(),
        'rgb_colors': set(),
        'rgba_colors': set(),
        'hsl_colors': set(),
        'named_colors': set(),
        'total_count': 0
    }
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. ইনলাইন স্টাইল থেকে কালার বের করা
    for tag in soup.find_all(style=True):
        extract_from_css_string(tag['style'], colors)
    
    # 2. <style> ট্যাগ থেকে CSS কালার বের করা
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            extract_from_css_string(style_tag.string, colors)
    
    # 3. সাধারণ টেক্সট থেকে কালার কোড খোঁজা
    text_content = soup.get_text()
    extract_colors_from_text(text_content, colors)
    
    # টোটাল কাউন্ট ক্যালকুলেশন
    colors['total_count'] = (
        len(colors['hex_colors']) + 
        len(colors['rgb_colors']) + 
        len(colors['rgba_colors']) + 
        len(colors['hsl_colors']) + 
        len(colors['named_colors'])
    )
    
    return colors

def extract_colors_from_css(css_content):
    """CSS ফাইল থেকে সব কালার কোড এক্সট্রাক্ট করা"""
    colors = {
        'hex_colors': set(),
        'rgb_colors': set(),
        'rgba_colors': set(),
        'hsl_colors': set(),
        'named_colors': set(),
        'total_count': 0
    }
    
    extract_from_css_string(css_content, colors)
    extract_colors_from_text(css_content, colors)
    
    colors['total_count'] = (
        len(colors['hex_colors']) + 
        len(colors['rgb_colors']) + 
        len(colors['rgba_colors']) + 
        len(colors['hsl_colors']) + 
        len(colors['named_colors'])
    )
    
    return colors

def extract_from_css_string(css_string, colors):
    """CSS স্ট্রিং থেকে কালার এক্সট্রাক্ট করা"""
    # Hex colors (#RGB, #RRGGBB)
    hex_pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'
    colors['hex_colors'].update(re.findall(hex_pattern, css_string))
    
    # RGB colors
    rgb_pattern = r'rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)'
    colors['rgb_colors'].update(re.findall(rgb_pattern, css_string))
    
    # RGBA colors
    rgba_pattern = r'rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*\d*\.?\d+)?\s*\)'
    colors['rgba_colors'].update(re.findall(rgba_pattern, css_string))
    
    # HSL colors
    hsl_pattern = r'hsl\(\s*\d{1,3}\s*,\s*\d{1,3}%\s*,\s*\d{1,3}%\s*\)'
    colors['hsl_colors'].update(re.findall(hsl_pattern, css_string))

def extract_colors_from_text(text, colors):
    """টেক্সট থেকে কালার কোড এবং নাম বের করা"""
    # Hex colors
    hex_pattern = r'#(?:[0-9a-fA-F]{3}){1,2}\b'
    colors['hex_colors'].update(re.findall(hex_pattern, text))
    
    # RGB colors
    rgb_pattern = r'rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)'
    colors['rgb_colors'].update(re.findall(rgb_pattern, text))
    
    # RGBA colors
    rgba_pattern = r'rgba?\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*(?:,\s*\d*\.?\d+)?\s*\)'
    colors['rgba_colors'].update(re.findall(rgba_pattern, text))
    
    # HSL colors
    hsl_pattern = r'hsl\(\s*\d{1,3}\s*,\s*\d{1,3}%\s*,\s*\d{1,3}%\s*\)'
    colors['hsl_colors'].update(re.findall(hsl_pattern, text))
    
    # Named colors
    named_colors_list = [
        'red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'purple',
        'orange', 'pink', 'brown', 'cyan', 'magenta', 'lime', 'olive', 'maroon',
        'navy', 'teal', 'aqua', 'fuchsia', 'silver', 'gold', 'coral', 'tomato',
        'violet', 'indigo', 'crimson', 'salmon', 'khaki', 'plum', 'orchid',
        'beige', 'lavender', 'tan', 'coral', 'wheat', 'ivory', 'mint', 'peach'
    ]
    
    text_lower = text.lower()
    for color in named_colors_list:
        if re.search(rf'\b{color}\b', text_lower):
            colors['named_colors'].add(color)
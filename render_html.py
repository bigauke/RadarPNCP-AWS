from html2image import Html2Image
import os

hti = Html2Image()
hti.browser.flags = ['--no-sandbox', '--disable-gpu', '--hide-scrollbars']
hti.size = (1080, 680)

print("Capturing HTML to Image...")
# We use output_path to place the output file in the right location
output_file = 'beautiful_arch.png'
hti.screenshot(html_file='diagram.html', save_as=output_file)

print(f"Saved {output_file}")

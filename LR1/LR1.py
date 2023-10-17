from tkinter import *
from tkinter import ttk
root = Tk()
root.geometry('700x500')


mode = ''
busy = False
def hls_to_rgb(hls):
    hue = hls[0]/360
    luminance = hls[1]/100
    saturation = hls[2]/100

    tmp1 = luminance * (1 + saturation)
    if luminance >= 0.5:
        tmp1 = luminance + saturation - luminance * saturation

    tmp2 = 2 * luminance - tmp1

    

    def normalizeTmpColor(tmpColor):
        if tmpColor > 1:
            tmpColor -= 1
        elif tmpColor < 0:
            tmpColor += 1
        return tmpColor

    def getColorRGB(tmpColor, tmp2, tmp1):
        if 6 * tmpColor < 1:
            return tmp2 + (tmp1 - tmp2) * 6 * tmpColor
        elif 2 * tmpColor < 1:
            return tmp1
        elif 3 * tmpColor < 2:
            return tmp2 + (tmp1 - tmp2) * (2 / 3 - tmpColor) * 6
        else:
            return tmp2

    tmpR = normalizeTmpColor(hue + 1.0 / 3)
    tmpG = normalizeTmpColor(hue)
    tmpB = normalizeTmpColor(hue - 1.0 / 3)

    red = getColorRGB(tmpR, tmp2, tmp1)
    green = getColorRGB(tmpG, tmp2, tmp1)
    blue = getColorRGB(tmpB, tmp2, tmp1)

    
    return [int(round(red*255)), int(round(green*255)), int(round(blue*255))]

def rgb_to_hls(rgb):
    red = rgb[0] / 255.0
    green = rgb[1] / 255.0
    blue = rgb[2] / 255.0

    rgbList = [red, green, blue]
    min_val = min(rgbList)
    max_val = max(rgbList)

    luminance = (max_val + min_val) / 2.0
    if max_val == min_val:
        return 0, int(luminance*100), 0

    saturation = (max_val - min_val) / (2.0 - max_val - min_val)
    if luminance <= 0.5:
        saturation = (max_val - min_val) / (max_val + min_val)

    hue = (green - blue) / (max_val - min_val)
    if green == max_val:
        hue = 2.0 + (blue - red) / (max_val - min_val)
    elif blue == max_val:
        hue = 4.0 + (red - green) / (max_val - min_val)

    hue *= 60
    if hue < 0:
        hue += 360

    return int(hue), int(luminance*100), int(saturation*100)


def rgb_to_cmyk(rgb):
    (r, g, b) = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def cmyk_to_rgb(cmyk):
    c, m, y, k = cmyk
    r = (1 - (c / 100)) * (1 - (k / 100))
    g = (1 - (m / 100)) * (1 - (k / 100))
    b = (1 - (y / 100)) * (1 - (k / 100))
    return round(r * 255), round(g * 255), round(b * 255)

def update_picture(r,g,b):
    picture.config(background=get_rgb(r,g,b))
        
        
def update_color():

    global busy
    global mode
    if busy:
        return
    else:
        busy = True
    if mode == 'rgb_slider':
        
        r = int(slider_r.get())
        g = int(slider_g.get())
        b = int(slider_b.get())
        rgb = (r, g, b)
        red_entry.delete(0, END)
        green_entry.delete(0, END)
        blue_entry.delete(0, END)
        
        red_entry.insert(END, str(r))
        green_entry.insert(END, str(g))
        blue_entry.insert(END, str(b))        
                
        full_cmyk_update(rgb_to_cmyk(rgb))
        full_hls_update(rgb_to_hls(rgb))
        busy = False
        update_picture(r,g,b)
        return
        
    if mode == 'rgb_entry':
        r = int(red_entry.get())
        g = int(green_entry.get())
        b = int(blue_entry.get())
        
        slider_r.set(r)
        slider_g.set(g)
        slider_b.set(g)
              
        rgb = (r, g, b)
        full_cmyk_update(rgb_to_cmyk(rgb))
        full_hls_update(rgb_to_hls(rgb))
        busy = False
        update_picture(r,g,b)
        return
        
        
    
    if mode == 'cmyk_slider':
        c = int(slider_c.get())
        m = int(slider_m.get())
        y = int(slider_y.get())
        k = int(slider_k.get())
        
        cmyk = (c,m,y,k)
        cyan_entry.delete(0, END)
        magenta_entry.delete(0, END)
        yellow_entry.delete(0, END)
        k_entry.delete(0, END)
        
        cyan_entry.insert(END, str(c))
        magenta_entry.insert(END, str(m))
        yellow_entry.insert(END, str(y)) 
        k_entry.insert(END, str(k)) 
        rgb = cmyk_to_rgb(cmyk)
        full_rgb_update(rgb)
        full_hls_update(rgb_to_hls(rgb))
        busy = False
        
        
        r,g,b = rgb
        update_picture(r,g,b)
        return
        
    if mode == 'cmyk_entry':
        c = int(cyan_entry.get())
        m = int(magenta_entry.get())
        y = int(yellow_entry.get())
        k = int(k_entry.get())
        
        slider_c.set(c)
        slider_m.set(m)
        slider_y.set(y)
        slider_k.set(k)
              
        cmyk = (c,m,y,k)
        full_rgb_update(cmyk_to_rgb(cmyk))
        full_cmyk_update(cmyk)
        busy = False
        r,g,b = cmyk_to_rgb(cmyk)
        update_picture(r,g,b)
        return
    
    
    
    if mode == 'hls_slider':
        h = int(slider_h.get())
        l = int(slider_l.get())
        s = int(slider_s.get())
        
        
        hls = (h,l,s)
        hue_entry.delete(0, END)
        lightness_entry.delete(0, END)
        saturation_entry.delete(0, END)
        
        hue_entry.insert(END, str(h))
        lightness_entry.insert(END, str(l))
        saturation_entry.insert(END, str(s)) 
        
        rgb = hls_to_rgb(hls)
        full_rgb_update(rgb)
        full_cmyk_update(rgb_to_cmyk(rgb))
        busy = False
        
        
        r,g,b = hls_to_rgb(hls)
        update_picture(r,g,b)
        return
        
    if mode == 'hls_entry':
        h = int(hue_entry.get())
        l = int(lightness_entry.get())
        s = int(saturation_entry.get())
        
        slider_h.set(h)
        slider_l.set(l)
        slider_s.set(s)
              
        hls = (h,l,s)
        rgb = hls_to_rgb(hls)
        
        full_rgb_update(rgb)
        full_cmyk_update(rgb_to_cmyk(rgb))
        
        busy = False
        r,g,b = rgb
        update_picture(r,g,b)
        return
        

def full_hls_update(hls):
    
    slider_h.set(hls[0])
    slider_l.set(hls[1])
    slider_s.set(hls[2])
    hue_entry.delete(0, END)
    lightness_entry.delete(0, END)
    saturation_entry.delete(0, END)
    hue_entry.insert(0, str(hls[0]))
    lightness_entry.insert(0, str(hls[1]))
    saturation_entry.insert(0, str(hls[2]))
    
def full_cmyk_update(cmyk):
    #cmyk = rgb_to_cmyk(rgb)
    slider_c.set(cmyk[0])
    slider_m.set(cmyk[1])
    slider_y.set(cmyk[2])
    slider_k.set(cmyk[3])
    cyan_entry.delete(0, END)
    magenta_entry.delete(0, END)
    yellow_entry.delete(0, END)
    k_entry.delete(0, END)
    cyan_entry.insert(0, str(cmyk[0]))
    magenta_entry.insert(0, str(cmyk[1]))
    yellow_entry.insert(0, str(cmyk[2]))
    k_entry.insert(0, str(cmyk[3]))
    
def full_rgb_update(rgb):
    slider_r.set(rgb[0])
    slider_g.set(rgb[1])
    slider_b.set(rgb[2])
    red_entry.delete(0, END)
    green_entry.delete(0, END)
    blue_entry.delete(0, END)
    red_entry.insert(0, str(rgb[0]))
    green_entry.insert(0, str(rgb[1]))
    blue_entry.insert(0, str(rgb[2]))


def get_rgb(r, g, b):
    global mode
    hex_code = '#{:02x}{:02x}{:02x}'.format(r,g,b) 
    return hex_code
 
def change_rgb_slider(val=0):
    global mode
    mode='rgb_slider'
    update_color()
        
def change_rgb_entry():
    global mode
    mode='rgb_entry'
    update_color()
    
def change_cmyk_slider(val=0):
    global mode
    mode='cmyk_slider'
    update_color()
    
def change_cmyk_entry():
    global mode
    mode='cmyk_entry'
    update_color()
    
def change_hls_slider(val=0):
    global mode
    mode='hls_slider'
    update_color()

    
def change_hls_entry():
    global mode
    mode='hls_entry'
    update_color()
    

    
   


picture = Label(master=root,width=70,height=30)
#############################################################################
update_rgb_entry = Button(text='update rgb', command=change_rgb_entry)
rgb_label = Label(master=root, text='RGB')


slider_r = ttk.Scale(master=root,from_=0,to=255, command=change_rgb_slider)
slider_g = ttk.Scale(master=root,from_=0,to=255, command=change_rgb_slider)
slider_b = ttk.Scale(master=root,from_=0,to=255,command=change_rgb_slider)

red_entry = ttk.Entry(master=root)
green_entry = ttk.Entry(master=root)
blue_entry = ttk.Entry(master=root)

red_entry.grid(row=1, column=0)
green_entry.grid(row=2, column=0)
blue_entry.grid(row=3, column=0)


slider_r.grid(row=1, column=1)
slider_g.grid(row=2, column=1)
slider_b.grid(row=3, column=1)

update_rgb_entry.grid(row=4,column=0,columnspan=2)

rgb_label.grid(row=0,column=0,columnspan=2)
##############################################################################

##############################################################################
update_cmyk_entry = Button(text='update cmyk', command=change_cmyk_entry)
cmyk_label = Label(master=root, text='CMYK')

slider_c = ttk.Scale(master=root,from_=0,to=100, command=change_cmyk_slider)
slider_m = ttk.Scale(master=root,from_=0,to=100, command=change_cmyk_slider)
slider_y = ttk.Scale(master=root,from_=0,to=100, command=change_cmyk_slider)
slider_k = ttk.Scale(master=root,from_=0,to=100, command=change_cmyk_slider)

cyan_entry = ttk.Entry(master=root)
magenta_entry = ttk.Entry(master=root)
yellow_entry = ttk.Entry(master=root)
k_entry = ttk.Entry(master=root)

cyan_entry.grid(row=1, column=2)
magenta_entry.grid(row=2, column=2)
yellow_entry.grid(row=3, column=2)
k_entry.grid(row=4,column=2)

slider_c.grid(row=1, column=3)
slider_m.grid(row=2, column=3)
slider_y.grid(row=3, column=3)
slider_k.grid(row=4, column=3)

update_cmyk_entry.grid(row=5,column=2,columnspan=2)

cmyk_label.grid(row=0,column=2,columnspan=2)
#########################################################################
update_hls_entry = Button(text='update hls', command=change_hls_entry)
hls_label = Label(master=root, text='HLS')

slider_h = ttk.Scale(master=root,from_=0,to=360, command=change_hls_slider)
slider_l = ttk.Scale(master=root,from_=0,to=100, command=change_hls_slider)
slider_s = ttk.Scale(master=root,from_=0,to=100, command=change_hls_slider)

hue_entry = ttk.Entry(master=root)
lightness_entry = ttk.Entry(master=root)
saturation_entry = ttk.Entry(master=root)

hue_entry.grid(row=1, column=4)
lightness_entry.grid(row=2, column=4)
saturation_entry.grid(row=3, column=4)

slider_h.grid(row=1, column=5)
slider_l.grid(row=2, column=5)
slider_s.grid(row=3, column=5)

update_hls_entry.grid(row=4,column=4,columnspan=2)

hls_label.grid(row=0,column=4,columnspan=2)


######################################################################
picture.grid(row=6,column=0, columnspan=6)

root.mainloop()

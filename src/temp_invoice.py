from reportlab.lib.units import inch
def my_temp(c):
    c.translate(inch,inch)
# define a large font
    c.setFont("Helvetica", 14)
# choose some colors
    c.setStrokeColorRGB(0.1,0.8,0.1)
    c.setFillColorRGB(0,0,1) # font colour
    # c.drawImage('D:\\top2.jpg',-0.8*inch,9.3*inch)
    c.drawString(0, 9*inch, "Shop No : 1234, ABCD Road")
    c.drawString(0, 8.7*inch, "City Name: Mycity, ZIP : 12345")
    c.setFillColorRGB(0,0,0) # font colour
    c.line(0,8.6*inch,6.8*inch,8.6*inch)
    c.drawString(5.6*inch,9.5*inch,'Bill No :# 1234')
    from  datetime import date
    dt = date.today().strftime('%d-%b-%Y')
    c.drawString(5.6*inch,9.3*inch,dt)
    c.setFont("Helvetica", 8)
    c.drawString(3*inch,9.6*inch,'Tax No :# ABC1234')
    c.setFillColorRGB(1,0,0) # font colour
    c.setFont("Times-Bold", 40)
    c.drawString(4.3*inch,8.7*inch,'INVOICE')
    c.rotate(45) # rotate by 45 degree 
    c.setFillColorCMYK(0,0,0,0.08) # font colour CYAN, MAGENTA, YELLOW and BLACK
    c.setFont("Helvetica", 140) # font style and size
    c.drawString(2*inch, 1*inch, "SAMPLE") # String written 
    c.rotate(-45) # restore the rotation 
    c.setFillColorRGB(0,0,0) # font colour
    c.setFont("Times-Roman", 22)
    c.drawString(0.5*inch,8.3*inch,'Products')
    c.drawString(4*inch,8.3*inch,'Price')
    c.drawString(5*inch,8.3*inch,'Quantity')
    c.drawString(6.1*inch,8.3*inch,'Total')
    c.setStrokeColorCMYK(0,0,0,1) # vertical line colour 
    c.line(3.9*inch,8.3*inch,3.9*inch,2.7*inch)# first vertical line
    c.line(4.9*inch,8.3*inch,4.9*inch,2.7*inch)# second vertical line
    c.line(6.1*inch,8.3*inch,6.1*inch,2.7*inch)# third vertical line
    c.line(0.01*inch,2.5*inch,7*inch,2.5*inch)# horizontal line total

    c.drawString(1*inch,1.8*inch,'Discount')
    c.drawString(1*inch,1.2*inch,'Tax')
    c.setFont("Times-Bold", 22)
    c.drawString(2*inch,0.8*inch,'Total')
    c.setFont("Times-Roman", 22)
    c.drawString(5.6*inch,-0.1*inch,'Signature')
    c.setStrokeColorRGB(0.1,0.8,0.1) # Bottom Line colour 
    c.line(0,-0.7*inch,6.8*inch,-0.7*inch)
    c.setFont("Helvetica", 8) # font size
    c.setFillColorRGB(1,0,0) # font colour
    c.drawString(0, -0.9*inch, u"\u00A9"+" plus2net.com")
    
    return c

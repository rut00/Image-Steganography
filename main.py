from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import  os
import tkinter.font


class Stegno:

    art ='Prepared By: Rutika Mehta (18DCS045)'
    art2 = '                            Dhruv Patel (18DCS067) '

    output_image_size = 0

    def main(self,root):
        root.title('ImageSteganography')
        root.geometry('800x600')
        root.configure(bg='#798777')
        root.resizable(width =True, height=True)
        f = Frame(root)
        f.configure(bg='#fff8f0')

        titleFont = tkinter.font.Font(
            root=root.master,
            family="Stencil",
            size=33,
        )

        menuFont = tkinter.font.Font(
            root=root.master,
            family="Century Gothic",
            size=15,
        )

        title = Label(f,text='Image Steganography')
        title.config(font=titleFont, bg='#fff8f0')
        title.grid(pady=25)

        b_encode = Button(f,text="Encode",command= lambda :self.frame1_encode(f), padx=14)
        b_encode.config(font=menuFont)
        b_encode.grid(pady=25, ipadx=1)
        b_decode = Button(f, text="Decode",command=lambda :self.frame1_decode(f), padx=14)
        b_decode.config(font=menuFont)
        b_decode.grid(pady=25)

        prep_text = Label(f,text=self.art)
        prep_text.config(font=('Copperplate Gothic Bold',12), bg='#fff8f0')
        prep_text.grid(pady=40)

        prep_text2 = Label(f,text=self.art2)
        prep_text2.config(font=('Copperplate Gothic Bold',12), bg='#fff8f0')

        # Button for closing
        exit_button = Button(f, text="Exit", fg='red', command=root.destroy, padx=14)
        exit_button.config(font=menuFont)
        exit_button.grid(pady=20, ipadx=25)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        f.grid(pady=50)
        title.grid(row=1)
        b_encode.grid(row=2)
        b_decode.grid(row=3)
        exit_button.grid(row=4)
        prep_text.grid(row=5)
        prep_text2.grid(row=6)

    def home(self,frame):
            frame.destroy()
            self.main(root)

    def frame1_encode(self,f):
        f.destroy()
        f2 = Frame(root)
        l1= Label(f2,text='Select the Image in which \nyou want to hide text :')
        l1.config(font=('Century Gothic',18))
        l1.grid(row =1,pady=50)

        bws_button = Button(f2,text='Select',command=lambda : self.frame2_encode(f2))
        bws_button.config(font=('Century Gothic',15))
        bws_button.grid(ipadx=6)
        back_button = Button(f2, text='Cancel', command=lambda : Stegno.home(self,f2))
        back_button.config(font=('Century Gothic',15))
        back_button.grid(pady=15)
        back_button.grid()
        f2.grid(pady=150)

    def frame2_encode(self,f2):
        ep= Frame(root)
        ep.configure(bg='#798777')
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg = Image.open(myfile)
            myimage = myimg.resize((200,200))
            img = ImageTk.PhotoImage(myimage)
            l3= Label(ep,text='Selected Image')
            l3.config(font=('Century Gothic',18))
            l3.grid(pady=10)
            panel = Label(ep, image=img)
            panel.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = myimg.size
            panel.grid()
            l2 = Label(ep, text='Enter the message')
            l2.config(font=('Century Gothic',18))
            l2.grid(pady=15)
            text_area = Text(ep, width=50, height=10)
            text_area.grid()
            encode_button = Button(ep, text='Cancel', command=lambda : Stegno.home(self,ep))
            encode_button.config(font=('Century Gothic',11))
            data = text_area.get("1.0", "end-1c")
            back_button = Button(ep, text='Encode', command=lambda : [self.enc_fun(text_area,myimg),Stegno.home(self,ep)])
            back_button.config(font=('Century Gothic',11))
            back_button.grid(pady=15)
            encode_button.grid(ipadx=3.5)
            ep.grid(row=1)
            f2.destroy()

    def genData(self,data):
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self,pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]
            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            # Eighth pixel of every set tells
            # whether to stop or read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self,newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):

            # Putting modified pixels in the new image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self,text_area,myimg):
        data = text_area.get("1.0", "end-1c")
        if (len(data) == 0):
            messagebox.showinfo("Alert","Kindly enter text in TextBox")
        else:
            newimg = myimg.copy()
            self.encode_enc(newimg, data)
            my_file = BytesIO()
            temp=os.path.splitext(os.path.basename(myimg.filename))[0]
            newimg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp,filetypes = ([('png', '*.png')]),defaultextension=".png"))
            self.d_image_size = my_file.tell()
            self.d_image_w,self.d_image_h = newimg.size
            messagebox.showinfo("Success","Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")

    def page3(self,frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self,f):
        f.destroy()
        d_f2 = Frame(root)
        l1 = Label(d_f2, text='Select Image with Hidden text:')
        l1.config(font=('Century Gothic',18))
        l1.grid(row =1,pady=50)
        bws_button = Button(d_f2, text='Select', command=lambda :self.frame2_decode(d_f2))
        bws_button.config(font=('Century Gothic',15))
        bws_button.grid()
        back_button = Button(d_f2, text='Home', command=lambda : Stegno.home(self,d_f2))
        back_button.config(font=('Century Gothic',15))
        back_button.grid(pady=15, ipadx=1)
        back_button.grid()
        d_f2.grid(pady=150)

    def frame2_decode(self,d_f2):
        d_f3 = Frame(root)
        d_f3.configure(bg='#798777')
        myfile = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Error","You have selected nothing !")
        else:
            myimg = Image.open(myfile, 'r')
            myimage = myimg.resize((200, 200))
            img = ImageTk.PhotoImage(myimage)
            l4= Label(d_f3,text='Selected Image :')
            l4.config(font=('Century Gothic',18))
            l4.grid(pady=10)
            panel = Label(d_f3, image=img)
            panel.image = img
            panel.grid()
            hidden_data = self.decode(myimg)
            l2 = Label(d_f3, text='Hidden data is :')
            l2.config(font=('Century Gothic',18))
            l2.grid(pady=10)
            text_area = Text(d_f3, width=50, height=10)
            text_area.insert(INSERT, hidden_data)
            text_area.configure(state='disabled')
            text_area.grid()
            back_button = Button(d_f3, text='Home', command= lambda :self.page3(d_f3))
            back_button.config(font=('Century Gothic',12))
            back_button.grid(pady=15)
            back_button.grid()
            exit1 = Button(d_f3,text='Exit',command=root.destroy, fg='red')
            exit1.config(font=('Century Gothic',12))
            exit1.grid(ipadx=9)
            d_f3.grid(row=1)
            d_f2.destroy()

    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data



root = Tk()

o = Stegno()
o.main(root)

root.mainloop()

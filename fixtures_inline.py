TESTS = (
    #normal
    ("", ""),
    ("Je suis du texte", "Je suis du texte"),
    
    #bold
    ("\033[1mJe suis du texte\033[0m" , "<b>Je suis du texte</b>"),

    #colors
    ("\033[31mred\033[0m", '<span style="color:#f00;">red</span>'),
    ("\033[32mgreen\033[0m", '<span style="color:#0f0;">green</span>'),
    ("\033[33myellow\033[0m", '<span style="color:#ff0;">yellow</span>'),
    ("\033[34mblue\033[0m", '<span style="color:#00f;">blue</span>'),
    ("\033[35mmagenta\033[0m", '<span style="color:#f0f;">magenta</span>'),
    ("\033[36mcyan\033[0m", '<span style="color:#0ff;">cyan</span>'),
    ("\033[37mwhite\033[0m", '<span style="color:#fff;">white</span>'),
    ("\033[41mred\033[0m", '<span style="background-color:#f00;">red</span>'),
    ("\033[42mgreen\033[0m", '<span style="background-color:#0f0;">green</span>'),
    ("\033[43myellow\033[0m", '<span style="background-color:#ff0;">yellow</span>'),
    ("\033[44mblue\033[0m", '<span style="background-color:#00f;">blue</span>'),
    ("\033[45mmagenta\033[0m", '<span style="background-color:#f0f;">magenta</span>'),
    ("\033[46mcyan\033[0m", '<span style="background-color:#0ff;">cyan</span>'),
    ("\033[47mwhite\033[0m", '<span style="background-color:#fff;">white</span>'),

    #combinations
    ("\033[1m\033[31mRed Bold\033[0m", '<b><span style="color:#f00;">Red Bold</span></b>'),
    ("\033[1;31mRed Bold\033[0m", '<b><span style="color:#f00;">Red Bold</span></b>'),

    #multiple changes
    ("\033[31mRed\033[32mGreen\033[0m", '<span style="color:#f00;">Red</span><span style="color:#0f0;">Green</span>'),
    ("\033[31mRed\033[0m\033[32mGreen\033[0m", '<span style="color:#f00;">Red</span><span style="color:#0f0;">Green</span>'),

    #unfinished
    ("\033[1mBold", "<b>Bold</b>"),
    ("\033[31mRed\033[1m And bold", '<span style="color:#f00;">Red<b> And bold</b></span>')
)

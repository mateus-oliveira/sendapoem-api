import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

WELCOME_HTML = '''
<body style="
    font-family: 'Baloo Thambi 2', cursive; 
    background:#E0428D;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
">
   <p style="
        color:#E0428D;
        background:#FFF;
        padding: 20px;
        font-size: 18pt; 
        display: flex;
        align-items: center;
        justify-content: flex-start;
        width: 95%;
        border-radius: 8px;
    ">
        Seja bem vindo, {}. Estamos muito felizes em te ter aqui. Desejamos que aproveite bastante, curtindo os poemas dos seus amigos e enviando para quem desejar.
    </p>
</body>
'''
PWD_HTML = '''
Olá, {}!<br><br>Para recuperar a senha, informe o seguinte código: <b>{}</b><br><br>Atenciosamente,<br>Send a Poem.
'''

TOKEN_HTML = '''
Olá, {}!<br><br>Estamos muito felizes em te ter conosco.<br><br>Para começar a usar os nossos serviços, confirme o seu email com o seguinte código: <b>{}</b><br><br>Atenciosamente,<br>Send a Poem.
'''

def welcome_email(email, name): 
    gmail = 'chicoalvesnaoexiste@gmail.com'
    password = 'xnebzlyibkymenez'
    messageHTML = WELCOME_HTML.format(name)
    messagePlain = 'Seja bem vindo, {}. Estamos muito felizes em te ter aqui. Desejamos que aproveite bastante, curtindo os poemas dos seus amigos e enviando para quem desejar.'.format(name)

    msg = MIMEMultipart('alternative')
    msg['From'] = 'Send a Poem'
    msg['To'] = email
    msg['Subject'] = 'Bem vindo, {}!'.format(name)

    # Attach both plain and HTML versions
    msg.attach(MIMEText(messagePlain, 'plain'))
    msg.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail, password)
    text = msg.as_string()
    server.sendmail(gmail, email, text)
    server.quit()

def pwd_email(email, name, pwd): 
    gmail = 'chicoalvesnaoexiste@gmail.com'
    password = 'xnebzlyibkymenez'
    messageHTML = PWD_HTML.format(name, pwd)
    messagePlain = 'Olá, {}!\n\nPara recuperar a senha, informe o seguinte código: **{}**\n\nAtenciosamente,\nSend a Poem.'.format(name, pwd)

    msg = MIMEMultipart('alternative')
    msg['From'] = 'Send a Poem'
    msg['To'] = email
    msg['Subject'] = 'Esqueceu a senha?'

    # Attach both plain and HTML versions
    msg.attach(MIMEText(messagePlain, 'plain'))
    msg.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail, password)
    text = msg.as_string()
    server.sendmail(gmail, email, text)
    server.quit()

def cod_confirm_email(email, name, token): 
    gmail = 'chicoalvesnaoexiste@gmail.com'
    password = 'xnebzlyibkymenez'
    messageHTML = TOKEN_HTML.format(name, token)
    messagePlain = 'Olá, {}!\n\nEstamos muito felizes em te ter conosco.\n\nPara começar a usar os nossos serviços, confirme o seu email com o seguinte código: **{}**\n\nAtenciosamente,\nSend a Poem.'.format(name, token)

    msg = MIMEMultipart('alternative')
    msg['From'] = 'Send a Poem'
    msg['To'] = email
    msg['Subject'] = 'Bem vindo, {}!'.format(name)

    # Attach both plain and HTML versions
    msg.attach(MIMEText(messagePlain, 'plain'))
    msg.attach(MIMEText(messageHTML, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail, password)
    text = msg.as_string()
    server.sendmail(gmail, email, text)
    server.quit()


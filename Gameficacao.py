from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
import webbrowser
from kivy.core.window import Window
import os

os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
import json
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition, RiseInTransition
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
import base64
import requests

r = requests.get('https://raw.githubusercontent.com/eletrojr128/gameficacao/master/data.json')
l = requests.get('https://raw.githubusercontent.com/eletrojr128/gameficacao/master/date.json')
m = requests.get('https://raw.githubusercontent.com/eletrojr128/gameficacao/master/dateboss.json')
n = requests.get('https://raw.githubusercontent.com/eletrojr128/gameficacao/master/link.json')

with open('data.json', 'wb') as data:
    data.write(r.content)

with open('date.json', 'wb') as data:
    data.write(l.content)

with open('dateboss.json', 'wb') as data:
    data.write(m.content)

with open('link.json', 'wb') as data:
    data.write(n.content)

Lista2 = ['img/Barra0.png',
          'img/Barra1.png',
          'img/Barra2.png',
          'img/Barra3.png',
          'img/Barra4.png',
          'img/Barra5.png',
          'img/Barra6.png',
          'img/Barra7.png',
          'img/Barra8.png',
          'img/Barra9.png',
          'img/Barra10.png']

varx = 0

Lista = ['img/Coracao0.png',
         'img/Coracao1.png',
         'img/Coracao2.png',
         'img/Coracao3.png',
         'img/Coracao4.png',
         'img/Coracao5.png',
         'img/Coracao6.png',
         'img/Coracao7.png',
         'img/Coracao8.png',
         'img/Coracao9.png',
         'img/Coracao10.png']


class MenuAL(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.som_menual = SoundLoader.load('som/Brinstar Overgrown with Vegetation Area - Super Metroid.mp3')

    def on_pre_enter(self, *args, **kwargs):
        Window.bind(on_request_close=self.confirmacaosaida)
        self.som_menual.loop = True
        self.som_menual.play()
        self.som_menual.volume = .05

    def confirmacaosaida(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        botoes = BoxLayout(padding=10, spacing=10)

        pop = Popup(title='Deseja salvar?', content=box, size_hint=(None, None),
                    size=(150, 90))

        sim = Button(text='Sim', on_release=App.get_running_app().root.get_screen('menuG').salvarprojetos)
        nao = Button(text='Não', on_release=App.get_running_app().stop)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='img/exclamacao-mario.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        anim = Animation(size=(300, 180), duration=0.2, t='out_back')
        anim.start(pop)

        pop.open()

        return True

    pass


class Painel(Screen):
    projetos = []
    projetos_andamento = []
    projetos_andamentoboss = []
    som_painel = SoundLoader.load('som/Maridia Rocky Underwater Area - Super Metroid.mp3')

    def addWidget(self):
        projeto = App.get_running_app().root.get_screen('adicionarprojeto').ids.nomeprojeto.text
        self.ids.box.add_widget(ProjetoAL(text=projeto))
        App.get_running_app().root.get_screen('projetosG').ids.box.add_widget(ProjetoAL(text=projeto))
        App.get_running_app().root.get_screen('adicionarprojeto').ids.nomeprojeto.text = ''
        self.projetos.append(projeto)
        self.projetos_andamento.append(projeto)
        self.saveData()

    def addBoss(self):
        App.get_running_app().root.get_screen('adicionarboss').som_boss.play()
        projeto = App.get_running_app().root.get_screen('adicionarboss').ids.nomeprojeto.text
        self.ids.box.add_widget(Boss(text=projeto))
        App.get_running_app().root.get_screen('adicionarboss').ids.nomeprojeto.text = ''
        self.projetos.append(projeto)
        self.projetos_andamentoboss.append(projeto)
        self.saveData()

    def on_pre_enter(self, *args):
        self.ids.box.clear_widgets()
        Window.bind(on_keyboard=self.voltar)
        self.loadData()
        for projeto in self.projetos_andamento:
            self.ids.box.add_widget(ProjetoAL(text=projeto))
        for projeto in self.projetos_andamentoboss:
            self.ids.box.add_widget(Boss(text=projeto))
        App.get_running_app().root.get_screen('menual').som_menual.play()

    def removeWidget(self, projeto):
        texto = projeto.ids.label.text
        self.ids.box.remove_widget(projeto)
        self.projetos_andamento.remove(texto)
        self.saveData()

    def removeWidgetBoss(self, projeto):
        texto = projeto.ids.label.text
        self.ids.box.remove_widget(projeto)
        self.projetos_andamentoboss.remove(texto)
        self.saveData()

    def voltar(self, window, key, *args):
        if key == 27:
            App.get_running_app().root.current = 'menual'
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)
        self.som_painel.stop()

    def saveData(self, *args):
        with open('data.json', 'w') as data:
            json.dump(self.projetos, data)
        with open('date.json', 'w') as data:
            json.dump(self.projetos_andamento, data)
        with open('dateboss.json', 'w') as data:
            json.dump(self.projetos_andamentoboss, data)

    def loadData(self, *args):
        try:
            with open('date.json', 'r') as data:
                self.projetos_andamento = json.load(data)
        except FileNotFoundError:
            pass
        try:
            with open('dateboss.json', 'r') as data:
                self.projetos_andamentoboss = json.load(data)
        except FileNotFoundError:
            pass
        try:
            with open('data.json', 'r') as data:
                self.projetos = json.load(data)
        except FileNotFoundError:
            pass


class ProjetoAL(BoxLayout):

    def __init__(self, text='', **kwargs):
        super(ProjetoAL, self).__init__(**kwargs)
        self.ids.label.text = text


class Boss(BoxLayout):

    def __init__(self, text='', **kwargs):
        super(Boss, self).__init__(**kwargs)
        self.ids.label.text = text


class AdicionarProjetos(Screen):
    put = ''
    links = {}
    links_novos = {}
    pop = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.som_tela_projetos = SoundLoader.load('som/Brinstar Red Soil Swampy Area - Super Metroid.mp3')

    def on_pre_enter(self, *args):
        App.get_running_app().root.get_screen('menual').som_menual.play()

    def link_projeto(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.put = TextInput(font_size=15, text='Link')
        self.pop = Popup(title='Link', size_hint=(None, None), size=(300, 200), content=box)
        label = Label(text='Insira o link', font_name='font/joystix monospace.ttf')
        botao = Button(text='Confirmar', font_name='font\joystix monospace.ttf',
                       on_press=self.printlink_projeto)
        box.add_widget(label)
        box.add_widget(self.put)
        box.add_widget(botao)
        self.pop.open()

    def link_boss(self):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.put = TextInput(font_size=15, text='Link')
        self.pop = Popup(title='Link', size_hint=(None, None), size=(300, 200), content=box)
        label = Label(text='Insira o link', font_name='font/joystix monospace.ttf')
        botao = Button(text='Confirmar', font_name='font\joystix monospace.ttf',
                       on_press=self.printlink_boss)
        box.add_widget(label)
        box.add_widget(self.put)
        box.add_widget(botao)
        self.pop.open()

    def printlink_projeto(self, *args, **kwargs):
        projeto = App.get_running_app().root.get_screen('adicionarprojeto').ids.nomeprojeto.text
        link = self.put.text
        self.links_novos = {projeto: link}
        self.links.update(self.links_novos)
        self.saveData()
        App.get_running_app().root.get_screen('painel').addWidget()
        self.pop.dismiss()

    def printlink_boss(self, *args, **kwargs):
        projeto = App.get_running_app().root.get_screen('adicionarboss').ids.nomeprojeto.text
        link = self.put.text
        self.links_novos = {projeto: link}
        self.links.update(self.links_novos)
        self.saveData()
        App.get_running_app().root.get_screen('painel').addBoss()
        self.pop.dismiss()

    def card(self, projeto):
        texto = projeto.ids.label.text
        link = self.links[texto]
        webbrowser.open(link)

    def saveData(self):
        with open('link.json', 'w') as data:
            json.dump(self.links, data)

    def loadData(self, *args):
        try:
            with open('link.json', 'r') as data:
                self.links = json.load(data)
        except FileNotFoundError:
            pass

    def remove_link(self, projeto):
        texto = projeto.ids.label.text
        del self.links[texto]
        self.saveData()


class AdicionarProjeto(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.som_projeto = SoundLoader.load('som/Big Boss Confrontation 1 - Super Metroid.mp3')

    def on_pre_enter(self, *args):
        self.som_projeto.loop = True
        self.som_projeto.volume = .05
        self.som_projeto.play()

    def on_pre_leave(self, *args):
        self.som_projeto.stop()


class AdicionarBoss(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.som_telaboss = SoundLoader.load('som/Mother Brain - Super Metroid.mp3')
        self.som_boss = SoundLoader.load('som/Bowsers evil laugh.mp3')

    def on_pre_enter(self, *args):
        self.som_telaboss.loop = True
        self.som_telaboss.volume = .05
        self.som_telaboss.play()

    def on_pre_leave(self, *args):
        self.som_telaboss.stop()


class Gerenciador(ScreenManager):

    def confirmacao(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        botoes = BoxLayout(padding=5, spacing=5)

        pop = Popup(title='Deseja mesmo sair?', content=box, size_hint=(None, None),
                    size=(100, 60))

        sim = Button(text='Sim', font_name='font/joystix monospace.ttf',
                     on_release=App.get_running_app().stop)
        nao = Button(text='Não', font_name='font/joystix monospace.ttf',
                     on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)

        atencao = Image(source='img/atencao_espadas.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        animText = Animation(color=(0, 0, 0, 1)) + Animation(color=(1, 1, 1, 1))
        animText.repeat = True
        animText.start(nao)
        anim = Animation(size=(300, 180), duration=0.7, t='out_elastic')
        anim.start(pop)

        pop.open()
        return True


class DPJ(Screen):
    img = StringProperty('img/Coracao10.png')
    num = NumericProperty(10)
    imagens = ListProperty(Lista)
    projetos = []
    lifebar = 0

    def on_pre_enter(self):
        App.get_running_app().root.get_screen('painel').loadData()
        self.projetos = len(App.get_running_app().root.get_screen('painel').projetos_andamento) + len(
            App.get_running_app().root.get_screen('painel').projetos_andamentoboss)
        self.lifebar = self.projetos
        self.num = 10 - int(self.lifebar / 1.5)
        if self.num in range(11):
            self.img = str(self.imagens[self.num])
        elif self.num < 0:
            self.img = 'imagens/Coracao0.png'
            self.num = 0
        elif self.num > 10:
            self.img = 'imagens/Coracao10.png'
            self.num = 10


class MenuG(Screen):
    sound = SoundLoader.load('som/125 - the road to lavender town - from vermillion.mp3')

    def on_pre_enter(self, *args):
        if self.sound:
            self.sound.loop = True
            self.sound.play()
            self.sound.volume = .05

    def acessargit(self, *args, **kwargs):
        token = "6f2dfb4749f88158f0b47ea49d52e5da16d6107a"

        repo = 'eletrojr128/gameficacao'
        path1 = 'data.json'
        path2 = 'date.json'
        path3 = 'dateboss.json'
        path4 = 'link.json'

        data1 = open("data.json", "r").read()
        data2 = open("date.json", "r").read()
        data3 = open("dateboss.json", "r").read()
        data4 = open("link.json", "r").read()

        sha1 = requests.get(f'https://api.github.com/repos/{repo}/contents/{path1}')
        sha2 = requests.get(f'https://api.github.com/repos/{repo}/contents/{path2}')
        sha3 = requests.get(f'https://api.github.com/repos/{repo}/contents/{path3}')
        sha4 = requests.get(f'https://api.github.com/repos/{repo}/contents/{path4}')

        req1 = requests.put(f'https://api.github.com/repos/{repo}/contents/{path1}',
                     headers={'Authorization': f'Token {token}'},
                     json={
                         "message": "um novo commit",
                         "committer": {
                             "name": "eletrojr",
                             "email": "contato@eletrojr.com.br"
                         },
                         "content": base64.b64encode(data1.encode()).decode(),
                         'sha': sha1.json()['sha']
                     }
                     )

        req2 = requests.put(f'https://api.github.com/repos/{repo}/contents/{path2}',
                     headers={'Authorization': f'Token {token}'},
                     json={
                         "message": "um novo commit",
                         "committer": {
                             "name": "eletrojr",
                             "email": "contato@eletrojr.com.br"
                         },
                         "content": base64.b64encode(data2.encode()).decode(),
                         'sha': sha2.json()['sha']
                     }
                     )

        req3 = requests.put(f'https://api.github.com/repos/{repo}/contents/{path3}',
                     headers={'Authorization': f'Token {token}'},
                     json={
                         "message": "um novo commit",
                         "committer": {
                             "name": "eletrojr",
                             "email": "contato@eletrojr.com.br"
                         },
                         "content": base64.b64encode(data3.encode()).decode(),
                         'sha': sha3.json()['sha']
                     }
                     )

        req4 = requests.put(f'https://api.github.com/repos/{repo}/contents/{path4}',
                     headers={'Authorization': f'Token {token}'},
                     json={
                         "message": "um novo commit",
                         "committer": {
                             "name": "eletrojr",
                             "email": "contato@eletrojr.com.br"
                         },
                         "content": base64.b64encode(data4.encode()).decode(),
                         'sha': sha4.json()['sha']
                     }
                     )

    def acessouerrado(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='                                                                 ERRO', content=box,
                    size_hint=(None, None),
                    size=(470, 200))
        text = Label(text='                              Voce digitou credenciais invalidas !\n\n'
                          '                                   Por favor tente novamente',
                     font_name='font/joystix monospace.ttf', size_hint=(None, None))
        botao = Button(text='Ok', font_name='font/joystix monospace.ttf', size_hint=(None, None),
                       size=(150, 40), on_release=pop.dismiss, pos_hint={'x': .33, 'y': 3})

        box.add_widget(text)
        box.add_widget(botao)
        pop.open()

    def acessoucerto(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='                                                                 DALE', content=box,
                    size_hint=(None, None),
                    size=(470, 200))
        text = Label(text='                             Os projetos foram salvos no\n\n'
                          '                               repositorio com sucesso !',
                     font_name='font/joystix monospace.ttf', size_hint=(None, None))
        botao = Button(text='Ok', font_name='font/joystix monospace.ttf', size_hint=(None, None),
                       size=(150, 40), on_release=App.get_running_app().stop, pos_hint={'x': .33, 'y': 3})

        box.add_widget(text)
        box.add_widget(botao)
        pop.open()

    def clickdobotao(self, *args, **kwargs):
        user = self.userinput.text
        passw = self.passinput.text
        if user == "eletrojr" and passw == "1":
            self.acessargit()
            self.acessoucerto()

        else:
            self.acessouerrado()


    def salvarprojetos(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        botoes = BoxLayout(padding=5, spacing=5)

        pop = Popup(title='                     INSIRA AS SUAS CREDENCIAIS', content=box, size_hint=(None, None),
                    size=(350, 300))
        espaco1 = Label(text=' ')

        usuario = Label(text='Usuario', font_name='font/joystix monospace.ttf')
        senha = Label(text='Senha', font_name='font/joystix monospace.ttf')
        self.userinput = TextInput(multiline=False)
        self.passinput = TextInput(password=True, multiline=False)
        espaco2 = Label(text=' ')
        botao1 = Button(text='confimar', font_name='font/joystix monospace.ttf', size_hint=(None, None),
                        size=(150, 40), on_release=self.clickdobotao, pos_hint={'x': .10, 'y': .6})
        botao2 = Button(text='cancelar', font_name='font/joystix monospace.ttf', size_hint=(None, None),
                        size=(150, 40), on_release=pop.dismiss, pos_hint={'x': .30, 'y': .6})

        box.add_widget(espaco1)
        box.add_widget(usuario)
        box.add_widget(self.userinput)
        box.add_widget(senha)
        box.add_widget(self.passinput)
        box.add_widget(espaco2)
        botoes.add_widget(botao1)
        botoes.add_widget(botao2)
        box.add_widget(botoes)

        pop.open()


class ProjetosG(Screen):
    projetos = []
    path = ''

    def on_pre_enter(self):
        self.path = App.get_running_app().user_data_dir + '/'
        self.ids.box.clear_widgets()
        self.loadData()
        for projeto in self.projetos:
            self.ids.box.add_widget(Projeto(text=projeto))
        self.contador = len(self.projetos)

    def saveData(self):
        with open('data.json', 'w') as data:
            json.dump(self.projetos, data)

    def loadData(self, *args):
        try:
            with open('data.json', 'r') as data:
                self.projetos = json.load(data)
        except FileNotFoundError:
            pass

    def removeWidget(self, projeto):
        texto = projeto.ids.label.text
        self.ids.box.remove_widget(projeto)
        self.projetos.remove(texto)
        self.saveData()
        self.contador = len(self.projetos)

    def addWidget(self):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Projeto(text=texto))
        self.ids.texto.text = ''
        self.projetos.append(texto)
        self.saveData()
        self.contador = len(self.projetos)


class Projeto(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text


class MenuA(Screen):

    def __init__(self, **kwargs):
        super(MenuA, self).__init__(**kwargs)

    menu_som = SoundLoader.load('som/Title theme.mp3')

    def on_pre_enter(self):
        self.menu_som.loop = True
        self.menu_som.play()
        self.menu_som.volume = .05

    def on_pre_leave(self):
        Window.bind(on_request_close=App.get_running_app().root.get_screen('menual').confirmacaosaida)
        App.get_running_app().root.get_screen('painel').loadData()
        App.get_running_app().root.get_screen('adicionarprojetos').loadData()
        self.menu_som.stop()


class Departamentos(Screen):
    img = StringProperty('img/Barra10.png')

    def __init__(self, exp, imagens, **kwargs):
        super().__init__(**kwargs)
        self.Exp = exp
        self.Imagens = imagens

    def down(self):
        self.Exp -= 1
        if self.Exp in range(11):
            self.img = str(self.Imagens[self.Exp])
        elif self.Exp < 0:
            self.img = 'img/Barra0.png'
            self.Exp = 0
        elif self.Exp > 11:
            self.img = 'img/Barra10.png'

    def up(self):
        self.Exp += 1
        if self.Exp in range(11):
            self.img = str(self.Imagens[self.Exp])
        elif self.Exp < 0:
            self.img = 'img/Barra0.png'
        elif self.Exp > 11:
            self.img = 'img/Barra10.png'
            self.Exp = 11


class ProjetosA(Screen):

    def __init__(self, **kwargs):
        super(ProjetosA, self).__init__(**kwargs)


class MenuTutorial(Screen):

    def ArvoreDPJ(self):
        webbrowser.open('https://miro.com/app/board/o9J_kt71R8g=/?moveToWidget=3074457347804675537&cot=6')

    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_som = SoundLoader.load('som/106 - the road to viridian city - from palette.mp3')

    def on_pre_enter(self):
        self.menu_som.loop = True
        self.menu_som.play()
        self.menu_som.volume = .05



class gerente_de_projetos(Screen):
    fonte1 = 'font/joystix monospace.ttf'
    fonte2 = 'font/joystix monospace.ttf'
    cor1 = ([0.128, 0.128, 0.128, 1])
    cor2 = ([1, 1, 1, 1])
    letra1 = ([1, 1, 1, 1])
    letra2 = ([0.255, 0.128, 0, 1])

    def __init__(self, **kwargs):
        super(gerente_de_projetos, self).__init__(**kwargs)
        fonte = StringProperty('img/arv/scrum_icon.png')
        self.fonte = fonte
        letra = StringProperty('Habilitar')
        self.letra = letra

    def scrumpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Scrum', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade estrategica relacionada com a metodologia\n\n'
                         'agil de gerenciamento e o mindset lean', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Nenhum requisito para esta habilidade', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100), color=(0, 1, 0, 0.7))
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        pop.open()

    def cadpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='CAD', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='CAD', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade tecninca no manuseio da ferramenta Autocad\n\n'
                         'capacidade de realizar projetos e quaisquer atividades \n\n'
                         'em que a ferramenta esteja presente ', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Nenhum requisito para esta habilidade', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100), color=(0, 1, 0, 0.7))
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        pop.open()

    def eficienciapopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Eficiencia', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade tecnica relacionada com o projeto de consul-\n\n'
                         '          toria em eficiencia energetica.', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Nenhum requisito para esta habilidade', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100), color=(0, 1, 0, 0.7))
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        pop.open()

    def lnr10popup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='LNR10', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='LNR10', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade tecnica relacionada com a capacidade\n\n'
                         ' de realizar projeto de laudo NR10', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Nenhum requisito para esta habilidade', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100), color=(0, 1, 0, 0.7))
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        pop.open()

    def gerenciapopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Gerencia', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade para gerir uma equipe e capacidade\n\n'
                         'de gerenciar um time para enfrentar desafios \n\n'
                         'de qualquer segmento', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='scrum', on_release=self.scrumpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def revitpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Revit', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade tecninca no manuseio da ferramenta Revit\n\n'
                         'capacidade de realizar projetos e quaisquer atividades \n\n'
                         'em que a ferramenta esteja presente ', font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def guiadepie(self, *args, **kwargs):
        webbrowser.open('https://drive.google.com/drive/folders/1LB2FuZI7Biv1P5Id-Jh6iMEWj5ZTdyqc')

    def guiadecbe(self, *args, **kwargs):
        webbrowser.open('https://drive.google.com/drive/folders/1BjrvM2N5NB2pvoCjOl0sJZJrLq__c9EV')

    def guiadeppe(self, *args, **kwargs):
        webbrowser.open('https://podio.com/eletrojr-dg8euwj565/gerenciamento-de-projetos/apps/macroetapa/items/234')
        webbrowser.open('https://files.podio.com/1143746546')

    def normasdeppe(self, *args, **kwargs):
        webbrowser.open('https://files.podio.com/1158892834')
        webbrowser.open('https://files.podio.com/1158892455')

    def normasdesub(self, *args, **kwargs):
        webbrowser.open(
            'http://servicos.coelba.com.br/comercial-industrial/Documents/Normas%20e%20Tarifas/NOR.DISTRIBU-ENGE-0023%20-%20FORNECIMENTO%20DE%20ENERGIA%20EL%C3%89TRICA%20EM%20M%C3%89DIA%20TENS%C3%83O%20DE%20DISTRIBUI%C3%87%C3%83O%20%C3%80%20EDIFICA%C3%87%C3%83O%20INDIVIDUAL.pdf')

    def guiadelum(self, *args, **kwargs):
        webbrowser.open('https://files.podio.com/1134855953')

    def piepopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='pie', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='   Entendimento e capacidade acerca do projeto de \n\n'
                         ' instalacoes eletricas, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Guia', on_release=self.guiadepie,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .33, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def cbepopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='CBE', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'cabeamento estruturado, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Guia', on_release=self.guiadecbe,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .33, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def ppepopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='PPE', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'padrao de entrada, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Guia e planilha', on_release=self.guiadeppe,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .5, 'y': 2})
        botao3 = Button(text='Normas', on_release=self.normasdeppe,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .15, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        float.add_widget(botao3)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def cftvpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='CFTV', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'circuito de tv fechado, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def spdapopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='SPDA', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'sistema de prot. atm., da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Norma', on_release=self.guiadeppe,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .33, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def pfvpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='PFV', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'painel fotovoltaico, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def subpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='SUB', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         '      subestacao, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Normas', on_release=self.normasdesub,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .33, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def cdepopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='CDE', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto de \n\n'
                         'cadastramento elet., da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='PIE', on_release=self.piepopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def lumpopup(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=6)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 500))
        info = Label(text='SUB', font_name=self.fonte2, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='  Entendimento e capacidade acerca do projeto  \n\n'
                         '  luminotecnico, da realizacao ao gerenciamento ',
                    font_size=12, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='PIE', on_release=self.cadpopup,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': 9})
        pos = Label(text='Material:', font_name=self.fonte2, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao2 = Button(text='Guia', on_release=self.guiadelum,
                        font_name=self.fonte1, size_hint=(None, None), width=200,
                        height=30, pos_hint={'x': .33, 'y': 2})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        box.add_widget(pos)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()


class Trainee(Screen):
    fonte1 = 'font/joystix monospace.ttf'
    cor1 = ([0.128, 0.128, 0.128, 1])
    cor2 = ([1, 1, 1, 1])
    letra1 = ([1, 1, 1, 1])
    letra2 = ([0.255, 0.128, 0, 1])

    def __init__(self, **kw):
        super().__init__(**kw)

    def autocad(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Autocad', font_name=self.fonte1, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade tecninca no manuseio da ferramenta Autocad\n\n'
                         'capacidade de realizar projetos e quaisquer atividades \n\n'
                         'em que a ferramenta esteja presente ', font_size=10, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='', font_name=self.fonte1, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        pop.open()

    def gerencia_de_projetos(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Gerencia de Projetos', font_name=self.fonte1, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Habilidade para gerir uma equipe e Capacidade\n\n'
                         'de gerenciar um time para realizar projetos \n\n'
                         'de qualquer segmento', font_size=15, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte1, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.autocad,
                       font_name=self.fonte1, size_hint=(None, None), width=200,
                       height=30, pos_hint={'x': .33, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()

    def projeto_ficticio(self, *args, **kwargs):
        box = BoxLayout(orientation='vertical', spacing=5)
        box2 = BoxLayout()
        float = FloatLayout()
        pop = Popup(title='Habilidade', content=box, size_hint=(None, None), size=(600, 400))
        info = Label(text='Projeto ficticio', font_name=self.fonte1, font_size=20, size_hint=(None, None),
                     size=(590, 100))
        des = Label(text='Realizar um projeto ficticio na pratica sendo capaz\n\n'
                         'de ter uma visao macro e um bom relacionamento\n\n'
                         'com o cliente', font_size=10, font_name=self.fonte1,
                    size_hint=(None, None), size=(590, 100))
        pre = Label(text='Requisitos:', font_name=self.fonte1, font_size=15,
                    size_hint=(None, None), size=(590, 100))
        botao = Button(text='Autocad', on_release=self.autocad,
                       font_name=self.fonte1, size_hint=(None, None), width=250,
                       height=30, pos_hint={'x': .05, 'y': .5})
        botao2 = Button(text='Gerencia de projetos', on_release=self.gerencia_de_projetos,
                        font_name=self.fonte1, size_hint=(None, None), width=250,
                        height=30, pos_hint={'x': .5, 'y': .5})
        box.add_widget(info)
        box.add_widget(des)
        box.add_widget(pre)
        float.add_widget(botao)
        float.add_widget(botao2)
        box2.add_widget(float)
        box.add_widget(box2)
        pop.open()


class BotaoProjetos(ButtonBehavior, Label):
    cor1 = ([0.128, 0.128, 0.128, 1])
    cor2 = ([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(BotaoProjetos, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor1)
            Rectangle(size=(self.height / 2.2, self.height / 2.2),
                      pos=(self.x * 1.01, self.y * 2), source='img/draw.png')

    def on_press(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()

    def on_release(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()


class BotaoGerencia(ButtonBehavior, Label):
    cor1 = ([0.128, 0.128, 0.128, 1])
    cor2 = ([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(BotaoGerencia, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor1)
            Rectangle(size=(self.height / 2.2, self.height / 2.2),
                      pos=(self.x * 1.01, self.y * 2), source='img/business.png')

    def on_press(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()

    def on_release(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()


class BotaoAutocad(ButtonBehavior, Label):
    cor1 = ([0.128, 0.128, 0.128, 1])
    cor2 = ([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(BotaoAutocad, self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self, *args):
        self.atualizar()

    def on_size(self, *args):
        self.atualizar()

    def atualizar(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor1)
            Rectangle(size=(self.height / 2.2, self.height / 2.2),
                      pos=(self.x * 1.01, self.y * 2), source='img/logo-autocad-icone-1024.png')

    def on_press(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()

    def on_release(self, *args):
        self.cor1, self.cor2 = self.cor2, self.cor1
        self.atualizar()


class Gameficacao(App):
    gerenciador = Gerenciador()

    def build(self):
        Window.fullscreen = True
        self.gerenciador.add_widget(MenuA(name='MenuA'))
        self.gerenciador.add_widget(Departamentos(name='Departamentos', exp=10, imagens=Lista2))
        self.gerenciador.add_widget(ProjetosA(name='ProjetosA'))
        self.gerenciador.add_widget(MenuTutorial(name='MenuTutorial'))
        self.gerenciador.add_widget(gerente_de_projetos(name='gerente_de_projetos'))
        self.gerenciador.add_widget(ProjetosG(name='projetosG'))
        self.gerenciador.add_widget(MenuG(name='menuG'))
        self.gerenciador.add_widget(DPJ(name='dpj'))
        self.gerenciador.add_widget(Trainee(name='trainee'))
        self.gerenciador.add_widget(MenuAL(name='menual'))
        self.gerenciador.add_widget(Painel(name='painel'))
        self.gerenciador.add_widget(AdicionarProjetos(name='adicionarprojetos'))
        self.gerenciador.add_widget(AdicionarProjeto(name='adicionarprojeto'))
        self.gerenciador.add_widget(AdicionarBoss(name='adicionarboss'))
        return self.gerenciador


Gameficacao().run()

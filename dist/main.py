import pygame
import random
import math
import io

from pygame import mixer

#cambiar fuente de string a bytes

def fuente_bytes(fuente):
    with open (fuente, "rb") as f: # abre el archivo otf
        otf_bytes= f.read()#lee los bytes del archivo
    return io.BytesIO(otf_bytes) #crea un objeto BytesIO a poartir de los bytes del archito OTF



#inicializar PYGAME
pygame.init()

#Crear pantalla con una configuracion de 800*600 pixeles
pantalla = pygame.display.set_mode((800, 600))

#titulo e icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.jpg")

#agregar musica
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)


#VARIABLES JUGADOR
img_jugador = pygame.image.load("cohete.png")
jugador_X = 368
jugador_Y = 536
JX_cambio = 0
JY_cambio = 0
#enemigo

# VARIABLES ENEMIGO

img_enemigo = []
enemigo_X = []
enemigo_Y = []
EX_cambio = []
EY_cambio = []
cantidad_enemigos = 8

for x in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_X.append(random.randint(0, 736))
    enemigo_Y.append( random.randint(55, 222))
    EX_cambio.append(1)
    EY_cambio.append(50)






# VARIABLES BALA
balas=[]
img_bala = pygame.image.load("bala.png")
bala_X = 0
bala_Y = 500
BX_cambio = 0
BY_cambio = 3
bala_SET = False

# PUNTAJE

puntaje = 0
fuente_como_bytes = fuente_bytes("Thick Brush.otf")
fuente = pygame.font.Font(fuente_como_bytes, 50)

texto_X= 10
texto_Y= 10



#texto final de juego

fuente_final = pygame.font.Font("Thick Brush.otf", 90)



# mensaje al finalizar el juego
def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60,200))

#Funcion para mostrar puntaje

def mostrar_puintaje(x, y):
    texto = fuente.render(f"puntaje :{puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


#funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

#funcion bala

def disparar_bala(x,y):
    global  bala_SET
    bala_SET = True
    pantalla.blit(img_bala, (x+16,y+10))

# detectar colisiones

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
    if distancia <=27:
        return True
    else:
        return False


#loop del juego
se_ejecuta = True #variable que mantiene activa el ciclo
while se_ejecuta: # ciclo while mientras se_ejecuta esta en True

    #  RPG
    pantalla.blit(fondo, (0,0))

    #ciclo for
    for evento in pygame.event.get(): #monitorear evento
        if evento.type == pygame.QUIT:#si la X de la pantalla es pulsada, se_ejecuta cambia de estado a False
            se_ejecuta = False


# Eventos presionando tecla

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT: #flecha izquierda
                JX_cambio = -1.2
            if evento.key == pygame.K_RIGHT: #flecha derecha
                JX_cambio = 1.2
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala= {
                    "x": jugador_X,
                    "y": jugador_Y,
                    "velocidad" : -5
                }
                balas.append(nueva_bala)

                if not bala_SET:
                    bala_X = jugador_X
                    disparar_bala(bala_X, bala_Y)


            if evento.key == pygame.K_UP: #flecha arriba
                JY_cambio = -1.2
            if evento.key == pygame.K_DOWN: #flecha abajo
                JY_cambio = 1.2


#condiciones para eventos levantando la tecla

        if evento.type == pygame.KEYUP:
            #teclas que al levantarse afectan eje Y
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_UP:
                JY_cambio = 0

                #teclas que al levantarse afectan el eje x
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                JX_cambio = 0


    #se esciben deacuerdo al evento el cambio de posicion a traves de una suma JUGADOR
    jugador_X += JX_cambio
    jugador_Y += JY_cambio


#mantener limites dentro de los pixeles JUGADOR

    if jugador_X <=0:
        jugador_X =0
    elif jugador_X >= 736:
        jugador_X = 736

    if jugador_Y <= 0:
        jugador_Y=0
    elif jugador_Y >=536:
        jugador_Y = 536

        # se escribe posicion para ENEMIGO
    for x in range(cantidad_enemigos):

        #fin del juego
        if enemigo_Y[x]>500:
            for k in range(cantidad_enemigos):
                enemigo_Y[k]= 1000
            texto_final()
            break

        enemigo_X[x] += EX_cambio[x]


        # mantener limites dentro del margen a ENEMIGO

        if enemigo_X[x] <= 0:
             EX_cambio[x] = 1.2
             enemigo_Y[x] += EY_cambio[x]


        elif enemigo_X[x] >= 736:
             EX_cambio[x] = -1.0
             enemigo_Y[x] += EY_cambio[x]


        # colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_X[x], enemigo_Y[x], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_X[x] = random.randint(0, 736)
                enemigo_Y[x] = random.randint(20, 200)
                break

        enemigo(enemigo_X[x], enemigo_Y [x], x)


    # Movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    if bala_SET:
        disparar_bala(bala_X, bala_Y)
        bala_Y -=BY_cambio






    jugador(jugador_X, jugador_Y)
    mostrar_puintaje(texto_X, texto_Y)
    #actualizar pantalla
    pygame.display.update()


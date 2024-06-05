import pygame
import sys
import random
import time
# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla y tamaño de cada celda del tablero
ANCHO, ALTO = 480, 480 #define el alto y ancho del tablero
CELDA_SIZE = 80 #define el tamaño de las celdas

# Definir colores
BLANCO = (255, 255, 255) #color del borde 
NEGRO = (0, 0, 0) # color del fondo de las celdas
ROJO = (255, 0, 0) # celda movil
VERDE = (0, 255, 0)  # Color para la ruta de escape
AZUL = (0, 0, 255)

#cargamos las imagenes originales
raton_original = pygame.image.load("raton.jpg")
gato_original = pygame.image.load("gatito.jpg")

#transformo al tamaño que tiene mis celdas
raton_img = pygame.transform.scale(raton_original, (CELDA_SIZE, CELDA_SIZE))
gato_img = pygame.transform.scale(gato_original, (CELDA_SIZE, CELDA_SIZE))


# Función para dibujar el tablero
def dibujar_tablero(screen, escape_x, escape_y): # screen es el objeto de la pantalla en el que se va a dibujar el tablero
    for y in range(0, ALTO, CELDA_SIZE): # recorre valores de y desde 0 hasta alto en incrementos de celda size, estos aseguran que se itere sobre cada celda del tablero en una cuadricula
        for x in range(0, ANCHO, CELDA_SIZE): #recorre valores de x desde cero hasta ancho en incrementos de celda size
            rect = pygame.Rect(x, y, CELDA_SIZE, CELDA_SIZE) #creamos un objeto rect con la posicion x y, y el tamaño celda_size por celda
            pygame.draw.rect(screen, BLANCO, rect, 1) #dibuja un rectangulo en la pantalla screen con el color blanco y con un grosor de linea de 1
    # Dibujar la ruta de escape en la posición aleatoria
    rect = pygame.Rect(escape_x * CELDA_SIZE, escape_y * CELDA_SIZE, CELDA_SIZE, CELDA_SIZE)
    pygame.draw.rect(screen, VERDE, rect)
    
# Función para dibujar la celda móvil
def dibujar_celda(screen):
    # Dibujar imagen del ratón
    x1 = CELDA_X1 * CELDA_SIZE
    y1 = CELDA_Y1 * CELDA_SIZE
    screen.blit(raton_img, (x1, y1))

    # Dibujar imagen del gato
    x2 = CELDA_X2 * CELDA_SIZE
    y2 = CELDA_Y2 * CELDA_SIZE
    screen.blit(gato_img, (x2, y2)) 

    
    
#clase para definir el estado de juego
class Estado:
    #le paso las instancias como la posicion del gato, raton y turno del raton
    def __init__(self, raton_pos, gato_pos, turno_raton):
        self.raton_pos= raton_pos
        self.gato_pos= gato_pos
        self.turno_raton = turno_raton
    
#evaluar estado funcion

def evaluar_estado(estado):
    raton_x, raton_y = estado.raton_pos #obtiene las coordenadas del raton desde el objeto estado
    gato_x, gato_y = estado.gato_pos #obtiene las coordenadas del raton desde el objeto estado
    distancia = abs(raton_x - gato_x) + abs(raton_y - gato_y) #calcula la distancia de manhattan entre ambos
    return distancia #devuelve la distancia obtenida 

#funcion para generar movimientos
def generar_movimientos(estado):
    movimientos = [] #creamos una lista vacia para cargar los movimientos que sean permitidos
    x, y = estado.raton_pos if estado.turno_raton else estado.gato_pos
    
    #movimientos permitidos: arriba, abajo, izquierda, derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    #recorre las direcciones x, y en direcciones (arriba, abajo, etc)
    for dx, dy in direcciones:
        #calcula las nuevas coordenadas a las q el jugador se moveria si siguiera en la direccion actual
        nx, ny = x + dx, y + dy
        #verifica si las nuevas coordenadas estan dentro de los limites del tablero
        if 0 <= nx < 6 and 0 <= ny < 6:
            
            if estado.turno_raton:
                #si es turno del raton guarda la nueva posicion en esa variable
                nueva_posicion = (nx, ny) 
                #guarda en la lista movimientos la nueva posicion y cambia a false el estado para q sea el turno del gato
                movimientos.append(Estado(nueva_posicion, estado.gato_pos, False))
            else:
                nueva_posicion = (nx, ny)
                movimientos.append(Estado(estado.raton_pos, nueva_posicion, True))
                
    return movimientos

# funcion minimax 
def minimax(estado, profundidad, maximizando):
    if profundidad == 0: #si la prof del juego esta en 0 se evalua el estado actual del juego
        return evaluar_estado(estado) #se retorna su valor mediante la funcion evaluar estado
    
    if maximizando: #si el nodo actual esta en un nivel donde se esta max el valor (turno del raton)
        mejor_valor = float('-inf') #representa el peor valor posible para el jugador 
        for movimiento in generar_movimientos(estado): #se recorren todos los movs posibles 
            valor = minimax(movimiento, profundidad - 1, False) #se llama recursivamente a minimax con maxim en false para alternar al oponente
            mejor_valor = max(mejor_valor, valor) # se actualiza el mejor va tomando el max entre el val actual y el val obtenido del mov actual
        return mejor_valor 
    else: #si esta en el nivel donde se minimiza
        mejor_valor = float('inf') #representa el mejor valor posible para el jugador
        for movimiento in generar_movimientos(estado): #recorren los movs posibles
            valor = minimax(movimiento, profundidad - 1, True) #se llama recursivamente a minimax con maxim en true para alternar al oponente
            mejor_valor = min(mejor_valor, valor) #se actualiza el mej val tomando el minimo entre el valor actual y el obtenido del mov actual
        return mejor_valor

#elegir el mejor movimiento
def mejor_movimiento(estado, profundidad):
    mejor_mov = None # se establece en none para guardar ahi el mejor movimiento dp
    mejor_valor = float('-inf') if estado.turno_raton else float('inf') #si es turno del raton se inicializa con un valor neg inf y si no con valor inf pos
    
    for movimiento in generar_movimientos(estado): #recorre todos los movimientos posibles de la funcion generar movimientos
        valor = minimax(movimiento, profundidad - 1, not estado.turno_raton) # calcula el valor del movimiento actual, indica que se reduce la profundidad pa la sig llamada y va cambiando los turnos
        if estado.turno_raton and valor > mejor_valor: # valor del mov actual es mayor q el mejor valor actual 
            mejor_valor = valor #se actualiza el mejor valor 
            mejor_mov = movimiento #se actualiza el mejor movimiento 
        elif not estado.turno_raton and valor < mejor_valor: #valor del mov actual es menor q el mejor valor actual en el turno del gato
            mejor_valor = valor #actualiza ambos valores
            mejor_mov = movimiento
    
    return mejor_mov # devuelve el mejor mov posible dp de evaluar todos los mov posibles



# Función principal
def main():
    # Indicar que CELDA_X y CELDA_Y son variables globales
    global CELDA_X1, CELDA_Y1, CELDA_X2, CELDA_Y2 
    
    #indicar cantidad de turnos 
    turnos = 0
    max_turnos = 20
    
    #se establecen los tiempos del juego 
    reloj = pygame.time.Clock() #creo un reloj con clock que maneja el numero de bucles del juego por segundo
    espera_gato = False # se utiliza para controlar si el juego esta esperando que el gato realice su movimiento 
    tiempo_inicio_espera = 0 # almacena el tiempo en el que se inicio la espera del juego, se usa para controlar cuanto tiempo pasa desde el inicio hasta que juega el gato
    
    
    # generar posiciones aleatorias para cada jugador 
    CELDA_X1, CELDA_Y1 =  random.randint(0, 5) , random.randint(0, 5)
    CELDA_X2, CELDA_Y2 = random.randint(0, 5) , random.randint(0, 5)
    
    #asegurarse de que el gato no tenga la misma posicion del raton 
    while (CELDA_X1 == CELDA_X2 and CELDA_Y1 == CELDA_Y2):
        CELDA_X2, CELDA_Y2 = random.randint(0, 5) , random.randint(0, 5)
        
    
    # Generar posición aleatoria para la ruta de escape
    borde = random.choice(['superior', 'inferior', 'izquierda', 'derecha'])
    if borde == 'superior':
        escape_x = random.randint(0, 5) #el 0 representa la fila sup del tablero 
        escape_y = 0
    elif borde == 'inferior':
        escape_x = random.randint(0, 5)
        escape_y = 5 #representa la fila inferior del tablero
    elif borde == 'izquierda':
        escape_x = 0
        escape_y = random.randint(0, 5)
    else:  # 'derecha'
        escape_x = 5
        escape_y = random.randint(0, 5)
    
    #asegurarme de que el raton no salga en la misma posicion de la ruta de escape
    while(CELDA_X1 == escape_x and CELDA_Y1 == escape_y):
        CELDA_X1, CELDA_Y1 == random.randint(0, 5), random.randint(0, 5)
        
        #asegurarme de que el gato no salga en la misma posicion de la ruta de escape
    while(CELDA_X2 == escape_x and CELDA_Y2 == escape_y):
        CELDA_X2, CELDA_Y2 == random.randint(0, 5), random.randint(0, 5)
        
    # Configurar pantalla
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Juego del gato y el raton') #un mensaje para darle titulo al tablero
    
    font = pygame.font.Font(None, 36) #estableces la fuente para el mensaje del ganador
    
    # Preguntar por el estado del juego que seria el estado inicial del juego
    estado = Estado((CELDA_X1, CELDA_Y1), (CELDA_X2, CELDA_Y2), True) 
    
    
    # Si el juego sigue
    while True:
        #recorre todos los eventos del teclado
        for event in pygame.event.get():
            #si presionas la x sale del juego
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Turno del Raton:
            elif event.type == pygame.KEYDOWN and turnos %2 == 0:
                # Manejar eventos de teclado para mover la celda móvil
                if event.key == pygame.K_UP: #la flecha de arriba 
                    CELDA_Y1 = max(0, CELDA_Y1 - 1)
                elif event.key == pygame.K_DOWN: #flecha de abajo
                    CELDA_Y1 = min(5, CELDA_Y1 + 1)
                elif event.key == pygame.K_LEFT: #flecha izquierda
                    CELDA_X1 = max(0, CELDA_X1 - 1)
                elif event.key == pygame.K_RIGHT: #flecha derecha
                    CELDA_X1 = min(5, CELDA_X1 + 1)
                #actualizar el estado del juego para indicar el turno del gato
                estado= Estado((CELDA_X1, CELDA_Y1), estado.gato_pos, False)
                #le sumo 1 al turno
                turnos += 1
                #pasa al estado true quiere decir que pasa al turno del gato
                espera_gato = True
                
                tiempo_inicio_espera = time.time() #devuelve el tiempo actual
                #al pasarle a la variable, le indicas el tiempo actual en el q inicio la espera entonces dp el gato puede calcular cuanto tiempo paso y jugar
           
            
        #gato
         # calcula la diferencia de tiempo en segundos entre el momento actual y el momento en el q comenzo la espera del gato
        if espera_gato and (time.time() - tiempo_inicio_espera) >= 1: # verifica si el tiempo de espero es mayor o igual a 1
            # Consultar mov posibles:
            mejor_mov = mejor_movimiento(estado, 6)
                # Indicar la nueva pos del gato
            CELDA_X2, CELDA_Y2 = mejor_mov.gato_pos
                #actualizar el estado del juego para indicar que es el turno del raton
            estado = Estado(estado.raton_pos, mejor_mov.gato_pos, True) 
                #sumar el turno 
            turnos +=1
            #pasa el estado de la espera del gato a false para que juegue el raton
            espera_gato = False
                
            #si los turnos llegaron a la maxima cantidad de turnos, gana el raton xq el gato no le atrapo
        if turnos == max_turnos:
            victory_text = font.render("¡Has ganado, buen raton!", True, BLANCO) #le da un mensaje al ganador
            text_rect = victory_text.get_rect(center=(ANCHO // 2, ALTO // 2)) #esto es donde muestra el mensaje ganador
            screen.blit(victory_text, text_rect) 
            pygame.display.flip()
            pygame.time.delay(2000)  # Esperar 2 segundos antes de cerrar el juego
            pygame.quit() #sale del juego
            sys.exit() #sale del juego 
                
            
        # Dibujar el tablero y la ruta de escape
        screen.fill(NEGRO)
        dibujar_tablero(screen, escape_x, escape_y)
        dibujar_celda(screen)

        # Actualizar pantalla
        pygame.display.flip()
        
        #en caso de que gane el raton
        if CELDA_Y1 == escape_y and CELDA_X1 == escape_x: #cuando la posicion de la celda movil esta sobre la celda de escape
            victory_text = font.render("¡Has ganado, buen raton!", True, BLANCO) #le da un mensaje al ganador
            text_rect = victory_text.get_rect(center=(ANCHO // 2, ALTO // 2)) #esto es donde muestra el mensaje ganador
            screen.blit(victory_text, text_rect) 
            pygame.display.flip()
            pygame.time.delay(2000)  # Esperar 2 segundos antes de cerrar el juego
            pygame.quit() #sale del juego
            sys.exit() #sale del juego 
            
        #en caso de que gane el gato
        if CELDA_X1 == CELDA_X2 and CELDA_Y1 == CELDA_Y2: 
            victory_text = font.render("¡El gato te atrapó!", True, BLANCO) #le da un mensaje al ganador
            text_rect = victory_text.get_rect(center=(ANCHO // 2, ALTO // 2)) #esto es donde muestra el mensaje ganador
            screen.blit(victory_text, text_rect) 
            pygame.display.flip()
            pygame.time.delay(2000)  # Esperar 2 segundos antes de cerrar el juego
            pygame.quit() #sale del juego
            sys.exit() #sale del juego 
        
            
        reloj.tick(30) #limita la veloidad del fotograma en FPS y es
        
if __name__ == '__main__':
    main()


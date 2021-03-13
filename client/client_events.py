from client_config import *


def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            tcp_queue.append("keyleft;1")
        elif event.key == pygame.K_d:
            tcp_queue.append("keyright;1")
        elif event.key == pygame.K_SPACE:
            tcp_queue.append("keyup;1")
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            tcp_queue.append("keyleft;0")
        elif event.key == pygame.K_d:
            tcp_queue.append("keyright;0")

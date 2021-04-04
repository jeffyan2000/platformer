from client_events import *
from client_socket import *
import time, sys

my_udp_thread = ClientSocket()
my_tcp_thread = TcpSocket()

while True:
    env_vars["mouse_button_changed"] = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            my_tcp_thread.stop()
            my_udp_thread.stop()
            my_tcp_thread.join()
            my_udp_thread.join()
            sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            new_mouse_pos = pygame.mouse.get_pos()
            env_vars["delta_x"] = new_mouse_pos[0] - env_vars["mouse_x"]
            env_vars["delta_y"] = new_mouse_pos[1] - env_vars["mouse_y"]
            env_vars["mouse_x"], env_vars["mouse_y"] = new_mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            env_vars["mouse_button_down"] = False
            env_vars["mouse_button_changed"] = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            env_vars["mouse_button_down"] = True
            env_vars["mouse_button_changed"] = True
        handle_event(event)

        env_vars["keys"] = pygame.key.get_pressed()

    screen.fill((153, 241, 255))

    test_world.draw()
    test_backpack.draw()
    screen.blit(texture_lib["cursor1"], (env_vars["mouse_x"]- 10, env_vars["mouse_y"] - 10))
    pygame.display.flip()
    clock.tick(40)
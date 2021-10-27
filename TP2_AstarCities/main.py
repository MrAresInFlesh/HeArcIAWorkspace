import helpers
from AStar import AStar

ci = helpers.extractPositions("data/positions.txt")
co = helpers.extractConnections("data/connections.txt")


def render(heur, cities, connections, city, destination):
    print(f"| Astar result : ", end=' \n')
    result = AStar(cities, connections, city, destination, heur).process()
    print(f"| [Number of visited nodes] : {result[0]}", end=' \n')
    print(f"| [distance]: {result[1]} [km]", end=' \n')


def user_input():
    city = input("| Enter origin city : ")
    destination = input("| Enter destination : ")
    return city, destination


def main_loop(bl):
    while bl:
        (city, destination) = user_input()

        try:
            print("|_____________________________________________________________________________|\n|")

            render('h0', ci, co, city, destination)
            print("| Heuristic :        >--<     [h0]      >--< \n|")
            print("|_____________________________________________________________________________|\n|")

            render('h1', ci, co, city, destination)
            print("| Heuristic :        >--<      [x]      >--< \n|")
            print("|_____________________________________________________________________________|\n|")

            render('h2', ci, co, city, destination)
            print("| Heuristic :        >--<      [y]      >--< \n|")
            print("|_____________________________________________________________________________|\n|")

            render('h3', ci, co, city, destination)
            print("| Heuristic :        >--< [as crow fly] >--< \n|")
            print("|_____________________________________________________________________________|\n|")

            render('h4', ci, co, city, destination)
            print("| Heuristic utilisée : >--< [manhattan distance] >--< \n|")
            print("|_____________________________________________________________________________|\n|")

        except:
            pass

        print("|****************************************************************************|\n|")
        check = input("| Do you wish to continue? (y/n)")
        if check == 'y':
            bl = True
        else:
            print("| Program ended.")
            print("|****************************************************************************|")
            bl = False


if __name__ == "__main__":

    ticket_to_ride = True

    try:
        main_loop(ticket_to_ride)
    except:
        main_loop(ticket_to_ride)

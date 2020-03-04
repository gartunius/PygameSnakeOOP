#!/pygame_snake_oop/bin python


import classes


def main():
	try:
		game = classes.Screen(800, 800)
		game.bootstrap()
	except KeyboardInterrupt:
		print()


if __name__ == '__main__':
	main()

import datetime
import argparse
from rules import Game


def hand_values(hand):
    """Creates a list of strings with the values of a hand."""
    values = []
    for i in range(3):
        try:
            values.append(str(hand[i]))
        except IndexError:
            values.append('x')
    return values


def main():

    # Counters
    shoe_count = 0
    game_count = 0
    total_wins = {'banco': 0, 'punto': 0, 'tie': 0}

    jackpot_wins = {'main': 0, 'side1': 0, 'side2': 0, 'side3': 0,
                    'side4': 0, 'side5': 0, 'side6': 0, 'side7': 0}

    # Argument parser
    parser = argparse.ArgumentParser(description='Simulates baccarat games to a text file.')
    parser.add_argument('-s', action='store', dest='shoes', default=100,
                        type=int, help='number of shoes to be simulated, default 10000')
    parser.add_argument('-d', action='store', dest='decks', default=8,
                        type=int, help='number of decks per shoe, default 8')
    args = parser.parse_args()

    # Create game object
    sim = Game()
    sim.create_shoe(args.decks)

    # Set file name
    now = datetime.datetime.now()
    file_name = f'{args.decks}_{args.shoes}_{now.strftime("%d%m%y%H%M%S")}.txt'

    # Open file
    with open(file_name, 'w') as sim_file:

        # Run through num_shoes
        for i in range(args.shoes):
            shoe_wins = {'banco': 0, 'punto': 0, 'tie': 0}
            shoe_count += 1
            sim_file.write(f'\nShoe number {i + 1}\n\n')

            # While the shoe has more than 5 cards
            while sim.num_cards >= 6:
                result = []
                game_count += 1

                # Baccarat game
                sim.deal_hands()
                if not sim.is_natural():
                    sim.draw_thirds()
                game_result = sim.game_result()

                #print('punto values', sim.punto_values)
                #print('banco values', sim.banco_values)

                jackpots = []
                jackpots.append(sim.main_jackpot())
                jackpots.append(sim.side_jackpot_1())
                jackpots.append(sim.side_jackpot_2())
                jackpots.append(sim.side_jackpot_3())
                jackpots.append(sim.side_jackpot_4())
                jackpots.append(sim.side_jackpot_5())
                jackpots.append(sim.side_jackpot_6())

                #print(jackpot_results)

                shoe_wins[game_result] += 1
                total_wins[game_result] += 1
                for j in jackpots:
                    jackpot_wins[j] += 1

                # Append to results list
                result.append(game_result.title()[0])
                result.append(str(sim.banco_value))
                result.append(str(sim.punto_value))
                result.extend(hand_values(sim.banco_values))
                result.extend(hand_values(sim.punto_values))
                sim_file.write(','.join(result) + '\n')

                # Progress
                progress = round((shoe_count / args.shoes) * 100, 1)
                print(f'Progress: {progress}%', end='\r')

            # Shoe results
            sim_file.write('\nShoe results:\n')
            for win in shoe_wins:
                sim_file.write(f'{win.title()}:\t{shoe_wins[win]}\n')
            sim.create_shoe(args.decks)

    # Total results
    print(total_wins)

    sim_file.write('\nTotal results:\n')
    for win in total_wins:
        sim_file.write(f'{win.title()}:\t{total_wins[win]}\t\
            ({round((total_wins[win]/game_count) * 100, 4)}%)\n')

    # Jackpot results
    print(jackpot_wins)
    pct_main = round((jackpot_wins['main'] / game_count) * 100, 4)
    pct_side1 = round((jackpot_wins['side1'] / game_count) * 100, 4)
    print('#games:', game_count, '%main:', pct_main,
          'odds:', round(pct_main/(1-pct_main),4), '%side1:', pct_side1)

    sim_file.write('\nJackpot results:\n')
    for jpt in jackpot_wins:
        sim_file.write(f'{jpt.title()}:\t{jackpot_wins[jpt]}\t\
        ({round((jackpot_wins[jpt] / game_count) * 100, 4)}%)\n')


if __name__ == '__main__':
    main()

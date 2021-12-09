using System;
using System.IO;
using System.Reflection;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using TicTacToeConsoleRL.Players;

namespace TicTacToeConsoleRL
{
    public class LaunchTicTacToe
    {
        public static void Main(string[] _args)
        {
            int row = 3, column = 3, numberMatches = 500000;

            Board board = new Board(row, column);
            AbstractPlayer player1 = new RandomPlayer(EnumSymbol.Player1);
            LearnPlayer player2 = new LearnPlayer(EnumSymbol.Player2, 0.95);

            Console.WriteLine("Learn starting...");
            LaunchGame(board, player1, player2, numberMatches, true);
            Console.WriteLine("Learn end...");

            Console.WriteLine(player2.GetQTableSize());

            //Load...
            //  Load(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location) + "\\learn.ser");

            numberMatches = 10;
            player1 = new HumanPlayer(EnumSymbol.Player1, column, row);
            if (player2 is LearnPlayer)
            {
                ((LearnPlayer) player2).Epsilon = 0;
            }
                LaunchGame(board, player1, player2, numberMatches, false, true);
            if (player1 is LearnPlayer)
            {
                Save((LearnPlayer) player1, Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)+"\\learn.ser");
            }
            if (player2 is LearnPlayer)
            {
                Save((LearnPlayer) player2, Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)+"\\learn.ser");
            }

            Console.ReadLine();
        }

        private static void LaunchGame(Board _board, AbstractPlayer _player1, AbstractPlayer _player2, int _numberMatches = 500000, bool _learning = false, bool _verbose = false)
        {
            int modulo = _numberMatches / 20;
            if (modulo == 0)
            {
                modulo = 1;
            }
            for (int i = 1; i <= _numberMatches; i++)
            {
                //change player start
                if (i % 2 == 0)
                {
                    Game(_board, _player1, _player2, _verbose);
                }
                else
                {
                    Game(_board, _player2, _player1, _verbose);
                }
                if (_learning)
                {
                    if (i % modulo == 0)
                    {
                        (_player1 as LearnPlayer)?.DecrementEpsilon();
                        (_player2 as LearnPlayer)?.DecrementEpsilon();
                    }
                }
            }
        }

        private static void Game(Board _board, AbstractPlayer _player1, AbstractPlayer _player2, bool _verbose=false)
        {
            AbstractPlayer currentPlayer = _player1;
            if (_verbose)
            {
                _board.PrintState();
            }
            while (true)
            {
                int action = currentPlayer.PlayAction(_board.BoardState.ToString(), _board.GetPossibleMoves());
                _board.PlayStroke(action, currentPlayer.Symbol);
                if (_verbose)
                {
                    _board.PrintState();
                }
                if (_board.IsPlayerWinner(currentPlayer.Symbol))
                {
                    if (_verbose)
                    {
                        Console.WriteLine($"Winner {(char)currentPlayer.Symbol}");
                    }
                    if (_player1 == currentPlayer)
                    {
                        _player1.Rewards(_board.BoardState.ToString(), 1.0);
                        _player2.Rewards(_board.BoardState.ToString(), -1.0);
                    }
                    if (_player2 == currentPlayer)
                    {
                        _player2.Rewards(_board.BoardState.ToString(), 1.0);
                        _player1.Rewards(_board.BoardState.ToString(), -1.0);
                    }
                    break;
                }
                if (_board.IsFull())
                {
                    if (_verbose)
                    {
                        Console.WriteLine("Equality");
                    }
                    _player1.Rewards(_board.BoardState.ToString(), 0.5);
                    _player2.Rewards(_board.BoardState.ToString(), 0.5);
                    break;
                }
                if (_player1 == currentPlayer)
                {
                    _player2.Rewards(_board.BoardState.ToString(), 0.0);
                    currentPlayer = _player2;
                }
                else if (_player2 == currentPlayer)
                {
                    _player1.Rewards(_board.BoardState.ToString(), 0.0);
                    currentPlayer = _player1;
                }
            }
            _board.Reset();
            _player1.Reset();
            _player2.Reset();
        }

        private static LearnPlayer Load(string _path)
        {
            LearnPlayer player = null;
            var formatter = new BinaryFormatter();
            using (var stream = new FileStream(_path, FileMode.Open, FileAccess.Read))
            {
                try
                {
                    player = (LearnPlayer) formatter.Deserialize(stream);
                }
                catch (ArgumentNullException e)
                {
                    Console.WriteLine(e.Message);
                    return null;
                }
                catch (SerializationException e)
                {
                    Console.WriteLine(e.Message);
                    return null;
                }
            }
            return player;
        }

        private static void Save(LearnPlayer _player, string _path)
        {
            var formatter = new BinaryFormatter();
            using (var stream = new FileStream(_path, FileMode.Create, FileAccess.Write))
            {
                try
                {
                    formatter.Serialize(stream, _player);
                    stream.Flush();
                    Console.WriteLine("Save done!");
                }
                catch (ArgumentNullException e)
                {
                    Console.WriteLine(e.Message);
                }
                catch (SerializationException e)
                {
                    Console.WriteLine(e.Message);
                }
            }
        }
    }
}
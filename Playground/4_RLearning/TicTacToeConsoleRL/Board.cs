using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace TicTacToeConsoleRL
{
    public class Board
    {
        private readonly List<List<int>> winStates;

        public Board(int _rows, int _columns)
        {
            if (_rows <= 2)
            {
                _rows = 3;
            }
            if (_columns <= 2)
            {
                _columns = 3;
            }
            NumberPawnLineForWin = 3;
            Rows = _rows;
            Columns = _columns;
            winStates = new List<List<int>>();
            Initialize();
        }

        private void AddDiagWinner(int _i, int _column)
        {
            int substractRow = _i / Rows, actRow = _i, numberRow = 0, totalNumber = 0;
            for (int j = 0; j < NumberPawnLineForWin; j++)
            {
                numberRow += (actRow / Rows) - substractRow;
                actRow += _column;
                totalNumber += j;
            }
            if (numberRow == totalNumber)
            {
                var winState = new List<int>();
                int index = _i;
                for (int j = 0; j < NumberPawnLineForWin; j++)
                {
                    winState.Add(index);
                    index += _column;
                }
                winStates.Add(winState);
            }
        }

        public static List<int> GetPossibleMove(string _actState)
        {
            var possibleMove = new List<int>();
            for (int i = 0; i < _actState.Length; i++)
            {
                if (_actState[i] == (char) EnumSymbol.Empty)
                {
                    possibleMove.Add(i);
                }
            }
            return possibleMove;
        }

        public List<int> GetPossibleMoves()
        {
            var possibleMoves = new List<int>();
            for (int i = 0; i < BoardState.Length; i++)
            {
                var symbol = BoardState[i];
                if (symbol == (char) EnumSymbol.Empty)
                {
                    possibleMoves.Add(i);
                }
            }
            return possibleMoves;
        }

        public void Reset()
        {
            BoardState = new StringBuilder();
            for (int i = 0; i < Columns * Rows; i++)
            {
                BoardState.Append(" ");
            }
        }

        private void Initialize()
        {
            Reset();
            int length = Rows * Columns;
            int row = 0;
            for (int i = 0; i < length; i++)
            {
                if (i > 0 && i % Rows == 0)
                {
                    row = 0;
                }
                if (row + NumberPawnLineForWin <= Rows)
                {
                    var winState = new List<int>();
                    for (int j = i; j < i + NumberPawnLineForWin; j++)
                    {
                        winState.Add(j);
                    }
                    winStates.Add(winState);
                    row++;
                }
                if (i + Columns * (NumberPawnLineForWin - 1) < length)
                {
                    var winState = new List<int>();
                    int index = i;
                    for (int j = 0; j < NumberPawnLineForWin; j++)
                    {
                        winState.Add(index);
                        index += Columns;
                    }
                    winStates.Add(winState);
                }
                if (i + (Columns + 1) * (NumberPawnLineForWin - 1) < length)
                {
                    AddDiagWinner(i, Columns + 1);
                }
                if (i + (Columns - 1) * (NumberPawnLineForWin - 1) < length)
                {
                    AddDiagWinner(i, Columns - 1);
                }
            }
        }

        public void PlayStroke(int _stroke, EnumSymbol _symbol)
        {
            BoardState[_stroke] = (char) _symbol;
        }

        public bool IsFull()
        {
            return BoardState.ToString().All(_c => _c != (char) EnumSymbol.Empty);
        }

        public int NumberPawnLineForWin { get; set; }

        public bool IsPlayerWinner(EnumSymbol _symbol)
        {
            bool isWin = false;
            foreach (var winState in winStates)
            {
                bool winner = true;
                foreach (var index in winState)
                {
                    if (BoardState[index] != (char) _symbol)
                    {
                        winner = false;
                    }
                }
                if (winner)
                {
                    isWin = true;
                    break;
                }
            }
            return isWin;
        }

        public void PrintState()
        {
            int newLine = 1;
            string str = "";
            for (int i = 0; i <= Rows * 4; i++)
            {
                str += "-";
            }
            str += "\n";
            foreach (var c in BoardState.ToString())
            {
                str += "| " + c + " ";
                if (newLine % Rows == 0)
                {
                    if (newLine < Rows * Columns)
                    {
                        str += "|\n";
                        for (int i = 0; i <= Rows * 4; i++)
                        {
                            str += "-";
                        }
                        str += "\n";
                    }
                    newLine = 0;
                }
                newLine++;
            }
            Console.WriteLine(str);
        }

        public StringBuilder BoardState { get; set; }

        public int Rows { get; set; }

        public int Columns { get; set; }
    }
}
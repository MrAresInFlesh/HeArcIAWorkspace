using System;
using System.Collections.Generic;

namespace TicTacToeConsoleRL.Players
{
    public class HumanPlayer : AbstractPlayer
    {
        private int column, row;

        public HumanPlayer(EnumSymbol _symbol, int _column, int _row) : base(_symbol)
        {
            column = _column - 1;
            row = _row - 1;
        }

        public override int PlayAction(string _actState, List<int> _possibleMove)
        {
            int index;
            do
            {
                int nline = InputInteger($"Enter line number ({0}-{row}) : ", 0, row);
                int ncolumn = InputInteger($"Enter column number ({0}-{column}) : ", 0, column);
                index = ncolumn + ((row + 1) * nline);
            } while (_possibleMove.IndexOf(index) == -1);
            return index;
        }

        private int InputInteger(string _message, int _min, int _max)
        {
            int number;
            string output;
            do
            {
                Console.Write(_message);
                output = Console.ReadLine();
            } while (!int.TryParse(output, out number) || number < _min  || number > _max);
            return number;
        }

        public override void Rewards(string _actState, double _rewards)
        {
        }

        public override void Reset()
        {
        }
    }
}
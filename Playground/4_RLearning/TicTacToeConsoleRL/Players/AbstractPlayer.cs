using System;
using System.Collections.Generic;

namespace TicTacToeConsoleRL.Players
{
    [Serializable]
    public abstract class AbstractPlayer
    {
        protected AbstractPlayer(EnumSymbol _symbol)
        {
            Symbol = _symbol;
        }
        
        public EnumSymbol Symbol { get; set; }

        public abstract int PlayAction(string _actState, List<int> _possibleMove);

        public abstract void Rewards(string _actState, double _rewards);

        public abstract void Reset();
    }
}

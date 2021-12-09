using System;
using System.Collections.Generic;
using System.Linq;

namespace TicTacToeConsoleRL.Players
{
    public class RandomPlayer : AbstractPlayer
    {
        private Random random;
        public RandomPlayer(EnumSymbol _symbol) : base(_symbol)
        {
            random = new Random((int)DateTime.Now.Ticks);
        }

        public override int PlayAction(string _actState, List<int> _possibleMove)
        {
            return _possibleMove.ElementAt(random.Next(0, _possibleMove.Count));
        }

        public override void Rewards(string _actState, double _rewards) { }

        public override void Reset() { }
    }
}

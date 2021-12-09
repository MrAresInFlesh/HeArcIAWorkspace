using System;
using System.Collections.Generic;
using System.Linq;

namespace TicTacToeConsoleRL.Players
{
    [Serializable]
    public class LearnPlayer : AbstractPlayer
    {
        [NonSerialized] private string lastState;
        [NonSerialized] private int lastAction;

        // représente le nombre d'états après une phase d'apprentissage.
        private Dictionary<StateActionTuple<string, int>, double> qTable;
        private readonly double alpha, gamma;
        private Random random;

        public LearnPlayer(EnumSymbol _symbol, double _epsilon = 0.1, double _alpha = 0.3, double _gamma = 0.9) : base(_symbol)
        {
            qTable = new Dictionary<StateActionTuple<string, int>, double>();
            Epsilon = _epsilon;
            alpha = _alpha;
            gamma = _gamma;
            lastState = null;
            lastAction = -1;
            random = new Random((int)DateTime.Now.Ticks);
        }

        /// <summary>
        /// Pour savoir le nombre d'états par lesquel l
        /// </summary>
        /// <returns></returns>
        public int GetQTableSize()
        {
            return qTable.Count();
        }

        private string[] Rotate(string _actState)
        {
            string rotate90 = "", rotate270 = "";
            string rotate180 = new string(_actState.ToCharArray().Reverse().ToArray());
            for (int i = 0; i < _actState.Length / 3; i++)
            {
                string c = "";
                c += _actState[i + (3 * 2)];
                c += _actState[i + (3 * 1)];
                c += _actState[i];
                rotate90 += c;
            }
            rotate270 = new string(rotate90.ToCharArray().Reverse().ToArray());
            return new [] {_actState, rotate90, rotate180, rotate270};
        }

        public double Epsilon { get; set; }

        public void DecrementEpsilon(double _decr=0.05)
        {
            if (Epsilon > _decr)
            {
                Epsilon -= _decr;
            }
        }

        public override void Reset()
        {
            lastState = null;
            lastAction = -1;
        }

        private double GetValue(string _state, int _action)
        {
            var tuple = new StateActionTuple<string, int>(_state, _action);
            if (!qTable.ContainsKey(tuple))
            {
                qTable[tuple] = 0.8;
            }
            return qTable[tuple];
        }

        private bool FindState(string _state)
        {
            return qTable.Keys.Any(_stateAction => _stateAction.First.Equals(_state));
        }

        public override int PlayAction(string _actState, List<int> _possibleMove)
        {
            lastState = _actState;
            if (random.NextDouble() < Epsilon) //Exploration
            {
                lastAction = _possibleMove.ElementAt(random.Next(0, _possibleMove.Count));
                return lastAction;
            }
            var qState = new List<double>();
            foreach (int action in _possibleMove)
            {
                double value = GetValue(_actState, action);
              //  Console.WriteLine(action + " => " + value);
                qState.Add(value);
            }
            double maxValue = qState.Max();

            var maxList = new List<double>();
            for (int i = 0; i < _possibleMove.Count; i++)
            {
                if (Math.Abs(qState[i] - maxValue) <= 0.0001)
                {
                    maxList.Add(i);
                }
            }
            var index = maxList.Count > 1 ? random.Next(0, maxList.Count) : qState.IndexOf(maxValue);

            lastAction = _possibleMove[index];
            return lastAction;
        }

        public override void Rewards(string _actState, double _reward)
        {
            //Q(s1, a1) = Q(s1, a1) + learning_rate * (r + discount_factor * max Q(s2, _) - Q(s1, a1))
            if (lastAction > -1)
            {
                double previousValue = GetValue(lastState, lastAction);
                var allValue = new List<double>();
                foreach (int index in Board.GetPossibleMove(lastState))
                {
                    allValue.Add(GetValue(_actState, index));
                }
                double maxQNew = allValue.Max();
                qTable[new StateActionTuple<string, int>(lastState, lastAction)] =
                    previousValue + alpha * (_reward + gamma * maxQNew - previousValue);
            }
        }
    }
}
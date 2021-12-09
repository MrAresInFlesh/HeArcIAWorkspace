using System.Linq;

namespace TicTacToeConsoleRL
{
    public class State
    {
        private readonly string[] states;

        public State(string _state)
        {
            states = Rotate(_state);
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
            return new[] { _actState, rotate90, rotate180, rotate270 };
        }

        public string this[int _index]
        {
            get
            {
                if (_index < 0 || _index > states.Length)
                {
                    return null;
                }
                return states[_index];
            }
        }
    }
}

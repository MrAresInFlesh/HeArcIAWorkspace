using System;

namespace TicTacToeConsoleRL
{
    [Serializable]
    public class StateActionTuple<T1, T2>
    {
        private readonly T1 first;
        private readonly T2 second;

        public StateActionTuple(T1 _first, T2 _second)
        {
            first = _first;
            second = _second;
        }

        public T1 First => first;

        public T2 Second => second;

        public override int GetHashCode()
        {
            return first.GetHashCode() ^ second.GetHashCode();
        }

        public override bool Equals(object _obj)
        {
            if (_obj == null || _obj.GetType() != GetType())
            {
                return false;
            }
            return Equals((StateActionTuple<T1, T2>) _obj);
        }

        public bool Equals(StateActionTuple<T1, T2> _other)
        {
            return _other.First.Equals(first) && _other.Second.Equals(second);
        }
    }
}

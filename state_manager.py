class StateManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance._state = {}
        return cls._instance

    def get_states(self, key):
        return self._state.get(key)

    def set_state(self, key, value):
        self._state[key] = value


#  Singleton Instance
state_manager = StateManager()
state_manager.set_state('username', 'Jasphine D Tech')

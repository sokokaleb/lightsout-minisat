import functools
import os.path
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from src.util.board_configuration import BoardConfiguration

from kivy.config import Config
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', 'False')

PLAY_MODE = 0
EDIT_MODE = 1

class LightsOutGUI(App):
    def __init__(self, minisat_wrapper=None, row_count=3, col_count=3, **kwargs):
        if minisat_wrapper is None:
            raise Exception('minisat_wrapper should be filled!')
        super(LightsOutGUI, self).__init__(**kwargs)
        self.minisat_wrapper = minisat_wrapper
        self.board_config = BoardConfiguration(row_count, col_count)
        self.mode = PLAY_MODE
        self.hinting_on = False

    def clear_board_hinting(self):
        self.hinting_on = False
        for btn in self.buttons:
            btn.clear_hinting()

    def toggle_lights(self, num, obj):
        row, col = num // self.board_config.col_count, num % self.board_config.col_count
        if self.hinting_on:
            if not obj.hinting:
                self.clear_board_hinting()
        obj.clear_hinting()
        self.board_config.toggle_board(row, col)
        if self.mode == PLAY_MODE:
            MOVEMENT_VECTOR = set([-1, 1, -self.board_config.col_count, self.board_config.col_count])
            valid_tiles = [self.buttons[num + vec] for vec in MOVEMENT_VECTOR \
                    if 0 <= num + vec < len(self.buttons) and \
                    ((num + vec) % self.board_config.col_count == num % self.board_config.col_count or \
                    (num + vec) // self.board_config.col_count == num // self.board_config.col_count)]
            for btn in valid_tiles:
                btn.toggle()
                self.board_config.toggle_board(btn.row, btn.col)
            if self.board_config.is_done():
                self.hinting_on = False
                popup = Popup(title='Congratulations!', content=Label(text='Puzzle done!\nClick anywhere to continue.'), size_hint=(None, None), size=(600, 250))
                popup.open()

    def board_changed(self, obj):
        self.last_result = None
        self.more_result_btn.disabled = True

    def build(self):
        self.main_pane = GridLayout(rows=1, cols=2)
        self.left_pane = GridLayout()
        self.right_pane = GridLayout(col_force_default=True, col_default_width=175, cols=1, size_hint_x=None, width=215, padding=[20,20])
        self.buttons = []

        self.fill_lights_out_left_pane()
        self.fill_lights_out_right_pane()

        self.main_pane.add_widget(self.left_pane)
        self.main_pane.add_widget(self.right_pane)
        return self.main_pane

    def fill_lights_out_left_pane(self):
        self.left_pane.rows = self.board_config.row_count
        self.left_pane.cols = self.board_config.col_count
        for row in xrange(self.board_config.row_count):
            for col in xrange(self.board_config.col_count):
                btn = LightsOutTile(initial_state=0);
                btn.bind(on_press=functools.partial(self.toggle_lights, row * self.board_config.col_count + col))
                btn.bind(on_press=self.board_changed)
                btn.row = row
                btn.col = col
                self.buttons.append(btn)
                self.left_pane.add_widget(btn)

    def set_mode(self, mode, obj):
        self.mode = mode
        if mode == PLAY_MODE:
            self.play_mode_btn.disabled = True
            self.edit_mode_btn.disabled = False
        elif mode == EDIT_MODE:
            self.play_mode_btn.disabled = False
            self.edit_mode_btn.disabled = True

    def randomize_board(self, obj):
        self.clear_board_hinting()
        initial_mode = self.mode
        if initial_mode == PLAY_MODE:
            self.set_mode(EDIT_MODE, None)

        for btn in self.buttons:
            if random.getrandbits(1) == 1:
                btn.trigger_action()

        if initial_mode == PLAY_MODE:
            self.set_mode(PLAY_MODE, None)

    def fill_lights_out_right_pane(self):
        input_box = GridLayout(cols=1)

        HEIGHT = '25dp'
        SMALLER_HEIGHT = '10dp'
        
        input_box.add_widget(Label(text='# row', height=HEIGHT, size_hint_y=None))
        self.row_input = TextInput(text='{0}'.format(self.board_config.row_count), multiline=False, padding_x=10, height=HEIGHT, size_hint_y=None)
        input_box.add_widget(self.row_input)
        input_box.add_widget(Label(text='# col', height=HEIGHT, size_hint_y=None))
        self.col_input = TextInput(text='{0}'.format(self.board_config.row_count), multiline=False, padding_x=10, height=HEIGHT, size_hint_y=None)
        input_box.add_widget(self.col_input)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        apply_btn = Button(text='Apply', height=HEIGHT, size_hint_y=None)
        apply_btn.bind(on_press=self.update_dimension)
        input_box.add_widget(apply_btn)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        self.play_mode_btn = Button(text='Play Mode', height=HEIGHT, size_hint_y=None)
        self.play_mode_btn.bind(on_press=functools.partial(self.set_mode, PLAY_MODE))
        self.play_mode_btn.disabled = True
        input_box.add_widget(self.play_mode_btn)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        self.edit_mode_btn = Button(text='Edit Mode', height=HEIGHT, size_hint_y=None)
        self.edit_mode_btn.bind(on_press=functools.partial(self.set_mode, EDIT_MODE))
        input_box.add_widget(self.edit_mode_btn)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        randomize_btn = Button(text='Randomize!', height=HEIGHT, size_hint_y=None)
        randomize_btn.bind(on_press=self.randomize_board)
        input_box.add_widget(randomize_btn)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        solve_btn = Button(text='Solve', height=HEIGHT, size_hint_y=None)
        solve_btn.bind(on_press=self.solve_board)
        input_box.add_widget(solve_btn)

        input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        self.more_result_btn = Button(text='More Soln', height=HEIGHT, size_hint_y=None)
        self.more_result_btn.bind(on_press=self.get_more_solution)
        self.more_result_btn.disabled = True
        input_box.add_widget(self.more_result_btn)

        # input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        # input_box.add_widget(Label(text='Solution:', height=HEIGHT, size_hint_y=None))
        # input_box.add_widget(Label(height=SMALLER_HEIGHT, size_hint_y=None))
        # self.solver_field = TextInput(text='', padding=[15], readonly=True)
        # input_box.add_widget(self.solver_field)

        self.right_pane.add_widget(input_box)

    def update_dimension(self, obj):
        self.board_config = BoardConfiguration(int(self.row_input.text), int(self.col_input.text))
        for btn in self.buttons:
            self.left_pane.remove_widget(btn)
        self.buttons = []
        self.fill_lights_out_left_pane()
        # self.solver_field.text = ''
        self.more_result_btn.disabled = True

    def solve_board(self, obj):
        self.clear_board_hinting()
        self.last_result = self.minisat_wrapper.solve(self.board_config)
        OFFSET = self.board_config.row_count * self.board_config.col_count + 1
        soln_normalized = [((num - OFFSET) // self.board_config.col_count, (num - OFFSET) % self.board_config.col_count) \
                for num in self.last_result.latest_solution if num > 0]
        text = ''
        self.more_result_btn.disabled = False
        if self.last_result.is_satisfiable:
            self.hinting_on = True
            for x, y in soln_normalized:
                idx = x * self.board_config.col_count + y
                self.buttons[idx].set_hinting();
                text += '({0}, {1})\n'.format(x, y)
            if len(text) == 0:
                text = 'It\'s already solved!'
                self.more_result_btn.disabled = True
                popup = Popup(title='?????', content=Label(text='Why try to solve an already-solved puzzle???\nClick anywhere to continue.'), size_hint=(None, None), size=(700, 250))
                popup.open()
        else:
            self.clear_board_hinting()
            popup = Popup(title='Uh oh!', content=Label(text='This configuration has no solution!\nClick anywhere to continue.'), size_hint=(None, None), size=(700, 250))
            popup.open()
            self.more_result_btn.disabled = True
            text = '(No soln)'
        # self.solver_field.text = text

    def get_more_solution(self, obj):
        self.clear_board_hinting()
        self.last_result = self.minisat_wrapper.solve(self.board_config, self.last_result)
        OFFSET = self.board_config.row_count * self.board_config.col_count + 1
        soln_normalized = [((num - OFFSET) // self.board_config.col_count, (num - OFFSET) % self.board_config.col_count) \
                for num in self.last_result.latest_solution if num > 0]
        text = ''
        if self.last_result.is_satisfiable:
            self.hinting_on = True
            for x, y in soln_normalized:
                idx = x * self.board_config.col_count + y
                self.buttons[idx].set_hinting();
                text += '({0}, {1})\n'.format(x, y)
        else:
            self.hinting_on = False
            text = '(No other soln)'
            self.more_result_btn.disabled = True
            popup = Popup(title='Uh oh!', content=Label(text='No other solution found!\nClick anywhere to continue.'), size_hint=(None, None), size=(600, 250))
            popup.open()
        # self.solver_field.text = text
        pass

class LightsOutTile(Button):
    ON_COLOR = [2,2,2,1]
    OFF_COLOR = [1,1,1,1]
    ON_HINT_COLOR = [1.6,2.25,1.6,1]
    OFF_HINT_COLOR = [0.75,1.4,0.75,1]
    COLORS = [ON_COLOR, OFF_COLOR]
    HINT_COLORS = [ON_HINT_COLOR, OFF_HINT_COLOR]

    def __init__(self, initial_state=0, **kwargs):
        super(LightsOutTile, self).__init__(**kwargs)
        self.light_state = initial_state
        self.background_down = ''
        self.background_color = LightsOutTile.COLORS[initial_state]
        self.hinting = False

    def toggle(self):
        self.light_state ^= 1
        if self.hinting:
            self.background_color = LightsOutTile.HINT_COLORS[self.light_state]
        else:
            self.background_color = LightsOutTile.COLORS[self.light_state]

    def reset(self):
        self.light_state = 0
        self.hinting = False
        self.background_color = LightsOutTile.COLORS[self.light_state]

    def on_press(self):
        super(LightsOutTile, self).on_press()
        self.toggle()

    def set_hinting(self, hint=None):
        if hint is None:
            hint = self.light_state
        self.hinting = True
        self.background_color = LightsOutTile.HINT_COLORS[hint];

    def clear_hinting(self):
        self.hinting = False
        self.background_color = LightsOutTile.COLORS[self.light_state];

